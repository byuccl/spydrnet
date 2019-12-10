import sys
import itertools
import weakref
from enum import Enum


class Element(object):
    """
    Base class of all intermediate representation objects.

    An intermediate representation object represents an item in a netlist. Items range in specificity from pins on a
    port or wires in a cable up to an item that represents the netlist as a whole.

    Each element implements a dictionary for storing key-value pairs. The key should be a case sensitive string and the
    value should be a primitive type (string, integer, float, boolean) or potentially nested collections of primitive
    types. The purpose of this dictionary is to provide a space for properties and metadata associated with the element.

    Key namespaces are separated with a *period* character. If the key is void of a *period* than the key resides in the
    root namespace. Keys in the root namespace are considered properties. Other keys are considered metadata. For
    example '<LANG_OF_ORIGIN>.<METADATA_TAG>':<metadata_value> is considered metadata associated with the netlist's
    language of origin.

    Only data pertinent to the netlist should be stored in this dictionary. Cached data (namespace management, anything
    that can be recreated from the netlist) should be excluded from this dictionary. The intent of the IR is to house
    the basis of data for the netlist.

    The only key that is reserved is 'NAME'. It is the primary name of the element. NAME may be undefined or inferred,
    for example, a pin on a port may be nameless, but infer its name for its parent port and position.
    """
    __slots__ = ['_data']

    def __init__(self):
        """
        Initialize an element with an empty data dictionary.
        """
        self._data = dict()

    def __setitem__(self, key, value):
        '''
        create an entry in the dictionary of the element it will be stored in the metadata.
        '''
        key = sys.intern(key)
        self._data.__setitem__(sys.intern(key), value)

    def __delitem__(self, key):
        self._data.__delitem__(key)

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __contains__(self, item):
        return self._data.__contains__(item)

    def __iter__(self):
        return self._data.__iter__()

    def pop(self, item):
        return self._data.pop(item)


class Netlist(Element):
    """
    Represents a netlist object.

    Contains a top level instance and libraries
    """
    __slots__ = ['_libraries', '_top_instance']

    def __init__(self):
        super().__init__()
        self._libraries = list()
        self._top_instance = None

    @property
    def libraries(self):
        return ListView(self._libraries)

    @libraries.setter
    def libraries(self, value):
        assert set(self._libraries) == set(value), "Set of values do not match, this assignment can only reorder values"
        self._libraries = list(value)

    @property
    def top_instance(self):
        """
        Get the top instance in the netlist.

        Returns
        -------
        Instance
            The top level instance in the environment
        """
        return self._top_instance

    @top_instance.setter
    def top_instance(self, instance):
        assert instance is None or isinstance(instance, Instance), "Must specify an instance"
        # TODO: Should we have a DRC that makes sure the instance is of a definition contained in netlist?
        self._top_instance = instance

    def create_library(self):
        library = Library()
        self.add_library(library)
        return library
    
    def add_library(self, library, position=None):
        assert library not in self._libraries, "Library already included in netlist"
        assert library.netlist is None, "Library already belongs to a different netlist"
        if position is not None:
            self._libraries.insert(position, library)
        else:
            self._libraries.append(library)
        library._netlist = self

    def remove_library(self, library):
        self._remove_library(library)
        self._libraries.remove(library)

    def remove_libraries_from(self, libraries):
        if isinstance(libraries, set):
            excluded_libraries = libraries
        else:
            excluded_libraries = set(libraries)
        assert all(x.netlist == self for x in excluded_libraries), "Some libraries to remove are not included in " \
                                                                   "netlist "
        included_libraries = list()
        for library in self._libraries:
            if library not in excluded_libraries:
                included_libraries.append(library)
            else:
                self._remove_library(library)
        self._libraries = included_libraries

    def _remove_library(self, library):
        assert library.netlist == self, "Library is not included in netlist"
        library._netlist = None


class Library(Element):
    """
    Represents a library object.

    Contains a pointer to parent netlist and definitions.
    """
    __slots__ = ['_netlist', '_definitions']

    def __init__(self):
        super().__init__()
        self._netlist = None
        self._definitions = list()

    @property
    def netlist(self):
        return self._netlist

    @property
    def definitions(self):
        return ListView(self._definitions)

    @definitions.setter
    def definitions(self, value):
        assert set(self._definitions) == set(value), "Set of values do not match, this function can only reorder values"
        self._definitions = list(value)

    def create_definition(self):
        definition = Definition()
        self.add_definition(definition)
        return definition

    def add_definition(self, definition, position=None):
        assert definition.library is not self, "Definition already included in library"
        assert definition.library is None, "Definition already belongs to a different library"
        if position is not None:
            self._definitions.insert(position, definition)
        else:
            self._definitions.append(definition)
        definition._library = self

    def remove_definition(self, definition):
        self._remove_definition(definition)
        self._definitions.remove(definition)

    def remove_definitions_from(self, definitions):
        if isinstance(definitions, set):
            excluded_definitions = definitions
        else:
            excluded_definitions = set(definitions)
        assert all(x.library == self for x in excluded_definitions), "Some definitions to remove are not included in " \
                                                                     "the library "
        included_definitions = list()
        for definition in self._definitions:
            if definition not in excluded_definitions:
                included_definitions.append(definition)
            else:
                self._remove_definition(definition)
        self._definitions = included_definitions

    def _remove_definition(self, definition):
        assert definition.library == self, "Library is not included in netlist"
        definition._library = None


class Definition(Element):
    """
    Represents a definition of a cell, module, entity/architecture, or paralleled structure object.

    Contains a pointer to parent library, ports, cables, and instances.
    """
    __slots__ = ['_library', '_ports', '_cables', '_instances']

    def __init__(self):
        super().__init__()
        self._library = None
        self._ports = list()
        self._cables = list()
        self._instances = list()

    @property
    def library(self):
        return self._library

    @property
    def ports(self):
        return ListView(self._ports)

    @ports.setter
    def ports(self, value):
        target = list(value)
        assert set(self._ports) == set(target), "Set of values do not match, this function can only reorder values"
        self._ports = target

    @property
    def cables(self):
        return ListView(self._cables)

    @cables.setter
    def cables(self, value):
        target = list(value)
        assert set(self._cables) == set(target), "Set of values do not match, this function can only reorder values"
        self._cables = target

    @property
    def instances(self):
        return ListView(self._instances)

    @instances.setter
    def instances(self, value):
        target = list(value)
        assert set(self._instances) == set(target), "Set of values do not match, this function can only reorder values"
        self._instances = target

    def is_leaf(self):
        if len(self._instances) > 0 or len(self._cables) > 0:
            return False
        return True

    def create_port(self):
        port = Port()
        self.add_port(port)
        return port

    def add_port(self, port, position=None):
        assert port.definition is not self, "Port already included in definition"
        assert port.definition is None, "Port already belongs to a different definition"
        if position is not None:
            self._ports.insert(position, port)
        else:
            self._ports.append(port)
        port._definition = self

    def remove_port(self, port):
        self._remove_port(port)
        self._ports.remove(port)

    def remove_ports_from(self, ports):
        if isinstance(ports, set):
            excluded_ports = ports
        else:
            excluded_ports = set(ports)
        assert all(x.definition == self for x in excluded_ports), "Some ports to remove are not included in the " \
                                                                  "definition."
        included_ports = list()
        for port in self._ports:
            if port not in excluded_ports:
                included_ports.append(port)
            else:
                self._remove_port(port)
        self._ports = included_ports

    def _remove_port(self, port):
        assert port.definition == self, "Port is not included in definition"
        port._definition = None

    def create_instance(self):
        instance = Instance()
        self.add_instance(instance)
        return instance
    
    def add_instance(self, instance, position=None):
        assert instance.parent is not self, "Instance already included in definition"
        assert instance.parent is None, "Instance already belongs to a different definition"
        if position is not None:
            self._instances.insert(position, instance)
        else:
            self._instances.append(instance)
        instance._parent = self

    def remove_instance(self, instance):
        assert instance.parent == self, "Instance is not included in definition"
        self._instances.remove(instance)
        instance._parent = None

    def create_cable(self):
        cable = Cable()
        self.add_cable(cable)
        return cable

    def add_cable(self, cable, position=None):
        assert cable.definition is not self, "Cable already included in definition"
        assert cable.definition is None, "Cable already belongs to a different definition"
        if position is not None:
            self._cables.insert(position, cable)
        else:
            self._cables.append(cable)
        cable._definition = self

    def remove_cable(self, cable):
        assert cable.definition == self, "Cable is not included in definition"
        self._cables.remove(cable)
        cable._definition = None


class Bundle(Element):
    __slots__ = ['_definition', 'is_downto', 'is_scalar', 'lower_index']

    def __init__(self):
        super().__init__()
        self._definition = None
        self.is_downto = True
        self.is_scalar = False
        self.lower_index = 0

    @property
    def definition(self):
        return self._definition


class Port(Bundle):
    class Direction(Enum):
        """
        Define the possible directions for a given port
        """
        UNDEFINED = 0
        INOUT = 1
        IN = 2
        OUT = 3
    
    def __init__(self):
        '''setup an empty port''' 
        super().__init__()
        self.direction = self.Direction.UNDEFINED
        self.inner_pins = list()
        self.left_index = 0
        self.right_index = 0
        self.low_index = 0


    def initialize_pins(self, pin_count):
        '''
        create pin_count pins in the given port a downto style syntax is assumed
        Parameters:
        pin_count : this is the number of pins to add to the port
        '''
        self.left_index = pin_count -1
        self.right_index = 0
        self.low_index = 0
        for _ in range(pin_count):
            self._create_pin()

    def initialize_pins_in_range(self, left_index, right_index):
        '''
        create pins in the given port. no style is assumed and right and left indicies can each be larger than the other
        This can mimic the vhdl to and downto syntax. just put the indicies in order into the call.
        paramters:
        left_index - the index on the left of the expression in the input format
        right_index - the index on the right of the expression in the input format
        '''
        self.left_index = left_index
        self.right_index = right_index
        if left_index > right_index:
            pin_count = left_index - right_index + 1
            self.low_index = right_index
        elif left_index < right_index:
            pin_count = right_index - left_index + 1
            self.low_index = left_index
        else:
            pin_count = 1
            self.low_index = right_index
        for _ in range(pin_count):
            self._create_pin()

    def set_direction(self, direction):
        '''
        sets the direction for the port
        parameters:
        direction - the direction of the port this can be a string or a Port.Direction object
        '''
        if isinstance(direction, str):
            if direction.lower() == 'in':
                direction = self.Direction.IN
            elif direction.lower() == 'out':
                direction = self.Direction.OUT
            elif direction.lower() == 'inout':
                direction = self.Direction.INOUT
            else:
                direction = self.Direction.UNDEFINED
        self.direction = direction
    
    def _create_pin(self):
        '''
        create and add a pin in an unsafe fashion without updating the indicies, the calling function must worry about indicies on the port
        '''
        inner_pin = InnerPin()
        self._add_pin(inner_pin)
        return inner_pin

    def _add_pin(self, inner_pin):
        '''
        add a pin to the port in an unsafe fashion. The calling class must take care of the indicies.
        '''
        self.inner_pins.append(inner_pin)
        inner_pin.port = self

    def create_pin(self):
        '''
        create a pin and add it to the port. Also update the indices as needed
        return:
        the inner_pin created
        '''
        inner_pin = InnerPin()
        self.add_pin(inner_pin)
        return inner_pin

    def add_pin(self, inner_pin):
        '''
        add a pin to the port and update the indices to reflect the added pin
        '''
        if self.right_index == self.low_index:
            self.left_index += 1
        else:
            self.right_index += 1
        self.inner_pins.append(inner_pin)
        inner_pin.port = self

    def get_pin(self, index = 0):
        '''
        get the pin at the given index in the original indexing system
        returns:
        the pin at the given index
        '''
        return self.inner_pins[index-self.low_index]


class Pin:
    def __init__(self):
        self.wire = None


class InnerPin(Pin):
    def __init__(self):
        super().__init__()
        self.port = None

    def get_virtualPins(self):
        port = self.port
        definition = port.definition
        for vi in definition.virtual_instances:
            virtual_port = vi.virtualPorts[port]
            virtual_pin = virtual_port.virtualPins[self]
            yield virtual_pin


class OuterPin(Pin):
    def __init__(self):
        super().__init__()
        self.instance = None
        self.inner_pin = None

    def get_virtualWires(self):
        parent_definition = self.instance.parent_definition
        for vi in parent_definition.virtual_instances:
            wire = self.wire
            cable = wire.cable
            virtual_cable = vi.virtualCables[cable]
            virtual_wire = virtual_cable.virtualWires[wire]
            yield virtual_wire


class Cable(Bundle):
    def __init__(self):
        super().__init__()
        self.wires = list()

    def initialize_wires(self, wire_count):
        for _ in range(wire_count):
            self.create_wire()

    def create_wire(self):
        wire = Wire()
        self.add_wire(wire)
        return wire

    def add_wire(self, wire):
        self.wires.append(wire)
        wire.cable = self

    def get_wire(self, index):
        return self.wires[index]


class Wire:
    def __init__(self):
        self.cable = None
        self.pins = list()

    def connect_pin(self, pin):
        self.pins.append(pin)
        pin.wire = self
        
    def disconnect_pin(self, pin):
        self.pins.remove(pin)
        pin.wire = None

    def get_virtualWires(self):
        cable = self.cable
        definition = cable.definition
        for vi in definition.virtual_instances:
            virtual_cable = vi.virtualCables[cable]
            virtual_wire = virtual_cable.virtualWires[self]
            yield virtual_wire


class Instance(Element):
    '''
    netlist instance of a netlist definition
    '''
    def __init__(self):
        '''
        creates an empty object of type instance
        '''
        super().__init__()
        self._parent = None
        self._reference = None
        self.outer_pins = dict()

    @property
    def reference(self):
        return self._parent

    @reference.setter
    def reference(self, value):
        self._reference = value

    def is_leaf(self):
        """
        check to see if the netlist instance is an instance of a leaf definition
        Returns
        -------
        boolean
            True if the definition is leaf
            False if the definition is not leaf
        """
        return self._reference.is_leaf()

    def get_pin(self, port_identifier, index = 0):
        """
        get a pin by port and index
        Parameters
        ----------
        port_identifier

        index

        """
        port = self.definition.get_port(port_identifier)
        inner_pin = port.get_pin(index)
        return self.get_outer_pin(inner_pin)
            
    def get_outer_pin(self, inner_pin):
        if inner_pin not in self.outer_pins:
            outer_pin = OuterPin()
            self.outer_pins[inner_pin] = outer_pin
            outer_pin.instance = self
            outer_pin.inner_pin = inner_pin
            return outer_pin
        else:
            return self.outer_pins[inner_pin]


class ListView:
    __slots__ = ['_list', '__getitem__', '__contains__', '__eq__', '__ge__', '__gt__', '__iter__', '__le__', '__len__',
                 '__lt__', '__ne__', '__reversed__', 'copy', 'count', 'index']

    def __init__(self, list_object):
        assert(isinstance(list_object, list))
        self._list = list_object
        self.__getitem__ = self._list.__getitem__
        self.__contains__ = self._list.__contains__
        self.__eq__ = self._list.__eq__
        self.__ge__ = self._list.__ge__
        self.__gt__ = self._list.__gt__
        self.__iter__ = self._list.__iter__
        self.__le__ = self._list.__le__
        self.__len__ = self._list.__len__
        self.__lt__ = self._list.__lt__
        self.__ne__ = self._list.__ne__
        self.__reversed__ = self._list.__reversed__
        self.copy = self._list.copy
        self.count = self._list.count
        self.index = self._list.index
