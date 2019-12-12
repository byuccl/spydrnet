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
        """
        create an entry in the dictionary of the element it will be stored in the metadata.
        """
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
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_list) == len(value_set) and set(self._libraries) == value_set, \
            "Set of values do not match, this assignment can only reorder values, values must be unique"
        self._libraries = value_list

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
        assert library.netlist == self, "Library is not included in netlist"
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

    @staticmethod
    def _remove_library(library):
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
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_list) == len(value_set) and set(self._definitions) == value_set, \
            "Set of values do not match, this function can only reorder values, values must be unique"
        self._definitions = value_list

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
        assert definition.library == self, "Library is not included in netlist"
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

    @staticmethod
    def _remove_definition(definition):
        definition._library = None


class Definition(Element):
    """
    Represents a definition of a cell, module, entity/architecture, or paralleled structure object.

    Contains a pointer to parent library, ports, cables, and instances.
    """
    __slots__ = ['_library', '_ports', '_cables', '_children', '_references']

    def __init__(self):
        super().__init__()
        self._library = None
        self._ports = list()
        self._cables = list()
        self._children = list()
        self._references = set()

    @property
    def library(self):
        return self._library

    @property
    def ports(self):
        return ListView(self._ports)

    @ports.setter
    def ports(self, value):
        target = list(value)
        target_set = set(target)
        assert len(target) == len(target_set) and set(self._ports) == target_set, \
            "Set of values do not match, this function can only reorder values, values must be unique"
        self._ports = target

    @property
    def cables(self):
        return ListView(self._cables)

    @cables.setter
    def cables(self, value):
        target = list(value)
        target_set = set(target)
        assert len(target) == len(target_set) and set(self._cables) == set(target), \
            "Set of values do not match, this function can only reorder values, values must be unique"
        self._cables = target

    @property
    def children(self):
        return ListView(self._children)

    @children.setter
    def children(self, value):
        target = list(value)
        target_set = set(target)
        assert len(target) == len(target_set) and set(self._children) == target_set, \
            "Set of values do not match, this function can only reorder values, values must be unique"
        self._children = target

    @property
    def references(self):
        return SetView(self._references)

    def is_leaf(self):
        if len(self._children) > 0 or len(self._cables) > 0:
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
        assert port.definition == self, "Port is not included in definition"
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

    @staticmethod
    def _remove_port(port):
        port._definition = None

    def create_child(self):
        instance = Instance()
        self.add_child(instance)
        return instance

    def add_child(self, instance, position=None):
        assert instance.parent is not self, "Instance already included in definition"
        assert instance.parent is None, "Instance already belongs to a different definition"
        if position is not None:
            self._children.insert(position, instance)
        else:
            self._children.append(instance)
        instance._parent = self

    def remove_child(self, child):
        assert child.parent == self, "Instance is not included in definition"
        self._remove_child(child)
        self._children.remove(child)

    def remove_children_from(self, children):
        if isinstance(children, set):
            excluded_children = children
        else:
            excluded_children = set(children)
        assert all(x.parent == self for x in excluded_children), "Some children are not parented by the definition"
        included_children = list()
        for child in self._children:
            if child not in excluded_children:
                included_children.append(child)
            else:
                self._remove_child(child)
        self._children = included_children

    @staticmethod
    def _remove_child(child):
        child._parent = None

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
        self._remove_cable(cable)
        self._cables.remove(cable)

    def remove_cables_from(self, cables):
        if isinstance(cables, set):
            excluded_cables = cables
        else:
            excluded_cables = set(cables)
        assert all(x.definition == self for x in excluded_cables), "Some cables are not included in the definition"
        included_cables = list()
        for cable in self._cables:
            if cable not in excluded_cables:
                included_cables.append(cable)
            else:
                self._remove_cable(cable)
        self._cables = included_cables

    @staticmethod
    def _remove_cable(cable):
        cable._definition = None


class Bundle(Element):
    __slots__ = ['_definition', '_is_downto', '_is_scalar', '_lower_index']

    def __init__(self):
        super().__init__()
        self._definition = None
        self._is_downto = True
        self._is_scalar = True
        self._lower_index = 0

    @property
    def definition(self):
        return self._definition

    @property
    def is_downto(self):
        return self._is_downto

    @is_downto.setter
    def is_downto(self, value):
        self._is_downto = value

    def _items(self):
        return None

    @property
    def is_scalar(self):
        _items = self._items()
        if _items and len(_items) > 1:
            return False
        return self._is_scalar

    @is_scalar.setter
    def is_scalar(self, value):
        _items = self._items()
        if _items and len(_items) > 0 and value is True:
            raise RuntimeError("Cannot set is_scalar to True on a multi-item bundle")
        else:
            self._is_scalar = value

    @property
    def is_array(self):
        return not self.is_scalar

    @is_array.setter
    def is_array(self, value):
        _items = self._items()
        if _items and len(_items) > 0 and value is False:
            raise RuntimeError("Cannot set is_array to False on a multi-item bundle")
        else:
            self._is_scalar = not value

    @property
    def lower_index(self):
        return self._lower_index

    @lower_index.setter
    def lower_index(self, value):
        self._lower_index = value


class Port(Bundle):
    __slots__ = ['_direction', '_pins']

    class Direction(Enum):
        """
        Define the possible directions for a given port
        """
        UNDEFINED = 0
        INOUT = 1
        IN = 2
        OUT = 3

    def __init__(self):
        """
        setup an empty port
        """
        super().__init__()
        self._direction = self.Direction.UNDEFINED
        self._pins = list()

    def _items(self):
        return self._pins

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if isinstance(value, self.Direction):
            self._direction = value
        elif isinstance(value, int):
            for direction in self.Direction:
                if direction.value == value:
                    self._direction = direction
                    break
        elif isinstance(value, str):
            value = value.lower()
            for direction in self.Direction:
                if direction.name.lower() == value:
                    self._direction = direction
                    break
        else:
            raise TypeError(f"Type {type(value)} cannot be assigned to direction")

    @property
    def pins(self):
        return ListView(self._pins)

    @pins.setter
    def pins(self, value):
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_set) == len(value_list) and set(self._pins) == value_set, \
            "Set of values do not match, assignment can only be used to reorder values, values must be unique"
        self._pins = value_list

    def initialize_pins(self, pin_count):
        """
        create pin_count pins in the given port a downto style syntax is assumed
        Parameters:
        pin_count : this is the number of pins to add to the port
        """
        for _ in range(pin_count):
            self.create_pin()
        return self.pins

    def create_pin(self):
        """
        create a pin and add it to the port.
        return:
        the inner_pin created
        """
        pin = InnerPin()
        self.add_pin(pin)
        return pin

    def add_pin(self, pin, position=None):
        """
        add a pin to the port in an unsafe fashion. The calling class must take care of the indicies.
        """
        assert isinstance(pin, InnerPin)
        assert pin.port is not self, "Pin already belongs to this port"
        assert pin.port is None, "Pin already belongs to another port"
        if position is None:
            self._pins.append(pin)
        else:
            self._pins.insert(position, pin)
        pin._port = self

    def remove_pin(self, pin):
        assert pin.port == self, "Pin does not belong to this port."
        self._remove_pin(pin)
        self._pins.remove(pin)

    def remove_pins_from(self, pins):
        if isinstance(pins, set):
            exclude_pins = pins
        else:
            exclude_pins = set(pins)
        assert all(isinstance(x, InnerPin) and x.port == self for x in exclude_pins), "All pins to remove must be " \
                                                                                      "InnerPins and belong to the port"
        for pin in exclude_pins:
            self._remove_pin(pin)
        self._pins = list(x for x in self._pins if x not in exclude_pins)

    @staticmethod
    def _remove_pin(pin):
        pin._port = None


class Pin:
    __slots__ = ['_wire']

    def __init__(self):
        self._wire = None

    @property
    def wire(self):
        return self._wire


class InnerPin(Pin):
    __slots__ = ['_port']

    def __init__(self):
        super().__init__()
        self._port = None

    @property
    def port(self):
        return self._port


class OuterPin(Pin):
    __slots__ = ['_instance', '_inner_pin']

    @staticmethod
    def from_instance_and_inner_pin(instance, inner_pin):
        return OuterPin(instance, inner_pin)

    def __init__(self, instance=None, inner_pin=None):
        super().__init__()
        self._instance = instance
        self._inner_pin = inner_pin

    @property
    def instance(self):
        return self._instance

    @property
    def inner_pin(self):
        return self._inner_pin

    def __eq__(self, other):
        if isinstance(other, OuterPin):
            return self._instance == other._instance and self._inner_pin == other._inner_pin
        return False

    def __hash__(self):
        return hash((self._instance, self._inner_pin))


class Cable(Bundle):
    __slots__ = ['_wires']

    def __init__(self):
        super().__init__()
        self._wires = list()

    def _items(self):
        return self._wires

    @property
    def wires(self):
        return ListView(self._wires)

    @wires.setter
    def wires(self, value):
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_list) == len(value_set) and set(self._wires) == value_set, \
            "Set of values does not match, assigment can only be used for reordering, values must be unique"
        self._wires = value_list

    def initialize_wires(self, wire_count):
        for _ in range(wire_count):
            self.create_wire()

    def create_wire(self):
        wire = Wire()
        self.add_wire(wire)
        return wire

    def add_wire(self, wire, position=None):
        assert wire.cable is not self, "Wire already belongs to this cable"
        assert wire.cable is None, "Wire already belongs to a different cable"
        if position is not None:
            self._wires.insert(position, wire)
        else:
            self._wires.append(wire)
        wire._cable = self

    def remove_wire(self, wire):
        assert wire.cable == self, "Wire does not belong to this cable"
        self._remove_wire(wire)
        self._wires.remove(wire)

    def remove_wires_from(self, wires):
        if isinstance(wires, set):
            excluded_wires = wires
        else:
            excluded_wires = set(wires)
        assert all(x.cable == self for x in excluded_wires), "Some wires do not belong to this cable"
        for wire in excluded_wires:
            self._remove_wire(wire)
        self._wires = list(x for x in self._wires if x not in excluded_wires)

    @staticmethod
    def _remove_wire(wire):
        wire._cable = None


class Wire:
    __slots__ = ['_cable', '_pins']

    def __init__(self):
        self._cable = None
        self._pins = list()

    @property
    def cable(self):
        return self._cable

    @property
    def pins(self):
        return ListView(self._pins)

    @pins.setter
    def pins(self, value):
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_list) == len(value_set) and set(self._pins) == value_set, \
            "Set of values do not match, assignment can only be used to reorder, values must be unique"
        self._pins = value_list

    def connect_pin(self, pin, position=None):
        if isinstance(pin, OuterPin):
            instance = pin.instance
            inner_pin = pin.inner_pin
            assert instance is not None and inner_pin is not None, \
                "Outer pin must represent an instance and an inner_pin"
            assert inner_pin in instance.pins, "Pin not associated with instance"
            outer_pin = instance.pins[inner_pin]
            assert outer_pin.wire is not self, "Pin already connected to this wire"
            assert outer_pin.wire is None, "Pin already connected to a different wire"
            pin._wire = self
            pin = outer_pin
        else:
            assert pin.wire is None, "Pin already connected to a different wire"
        if position is not None:
            self._pins.insert(position, pin)
        else:
            self._pins.append(pin)
        pin._wire = self

    def disconnect_pin(self, pin):
        if isinstance(pin, OuterPin):
            instance = pin.instance
            inner_pin = pin.inner_pin
            assert instance is not None and inner_pin is not None, \
                "Outer pin must represent an instance and an inner_pin"
            assert inner_pin in instance.pins, "Pin not associated with instance"
            outer_pin = instance.pins[inner_pin]
            assert outer_pin.wire is self, "Pin is disconnected or connected to a different wire."
            self._disconnect_pin(pin)
            pin = outer_pin
        else:
            assert pin.wire == self, "Pin does not belong to this wire"
        self._pins.remove(pin)
        self._disconnect_pin(pin)

    def disconnect_pins_from(self, pins):
        if isinstance(pins, set):
            excluded_pins = pins
        else:
            excluded_pins = set(pins)
        all_pins_can_be_disconnected = True
        for pin in excluded_pins:
            if isinstance(pin, OuterPin):
                instance = pin.instance
                inner_pin = pin.inner_pin
                if instance is None or inner_pin is None or inner_pin not in instance.pins or \
                        instance.pins[inner_pin].wire is not self:
                    all_pins_can_be_disconnected = False
                    break
            else:
                if pin.wire != self:
                    all_pins_can_be_disconnected = False
                    break
        assert all_pins_can_be_disconnected, "Some of the pins to disconnect are not associated with an instance, " \
                                             "already disconnected, or connected to a different wire"
        for pin in excluded_pins:
            if isinstance(pin, OuterPin):
                self._disconnect_pin(pin)
                pin = pin.instance.pins[pin]
            self._disconnect_pin(pin)
        self._pins = list(x for x in self._pins if x not in excluded_pins)

    @staticmethod
    def _disconnect_pin(pin):
        pin._wire = None


class Instance(Element):
    """
    netlist instance of a netlist definition
    """
    __slots__ = ['_parent', '_reference', '_pins']

    def __init__(self):
        """
        creates an empty object of type instance
        """
        super().__init__()
        self._parent = None
        self._reference = None
        self._pins = dict()

    @property
    def parent(self):
        return self._parent

    @property
    def reference(self):
        return self._reference

    @reference.setter
    def reference(self, value):
        if value is None:
            for pin in self.pins:
                wire = pin.wire
                if wire:
                    wire.disconnect_pin(pin)
                pin._instance = None
            self._pins.clear()
        else:
            assert isinstance(value, Definition)
            if self._reference is not None:
                assert len(self.reference.ports) == len(value.ports) and all(len(x.pins) == len(y.pins) for x, y in
                                                                             zip(self.reference.ports, value.ports)), \
                    "Reference reassignment only supported for definitions with matching port positions"
                for cur_port, new_port in zip(self.reference.ports, value.ports):
                    for cur_pin, new_pin in zip(cur_port.pins, new_port.pins):
                        outer_pin = self._pins.pop(cur_pin)
                        outer_pin._inner_pin = new_pin
                        self._pins[new_pin] = outer_pin
            else:
                for port in value.ports:
                    for pin in port.pins:
                        self._pins[pin] = OuterPin.from_instance_and_inner_pin(self, pin)
            value._references.add(self)
        self._reference = value

    @property
    def pins(self):
        return OuterPinsView(self._pins)


class ListView:
    __slots__ = ['_list', '__add__', '__getitem__', '__contains__', '__eq__', '__hash__', '__ge__', '__gt__',
                 '__iter__', '__le__', '__len__', '__lt__', '__ne__', '__mul__', '__rmul__', '__reversed__', '__repr__',
                 '__str__', 'copy', 'count', 'index', '__iadd__', '__imul__']

    def __init__(self, list_object):
        assert isinstance(list_object, list)
        self._list = list_object
        for attr in self.__slots__[1:-2]:
            exec(f"self.{attr} = list_object.{attr}")
        for attr in self.__slots__[-2:]:
            exec(f"self.{attr} = self.unsupported_operator")

    def __radd__(self, other):
        return other + self._list

    def unsupported_operator(self, other):
        raise TypeError("unsupported operator for type SetView")


class SetView:
    __slots__ = ['__and__', '__rand__', '__eq__', '__ge__', '__gt__', '__hash__', '__iter__', '__le__', '__len__',
                 '__lt__', '__ne__', '__or__', '__ror__', '__sub__', '__rsub__', '__xor__', '__rxor__', '__repr__',
                 '__str__', 'copy', 'difference', 'intersection', 'isdisjoint', 'issubset', 'issuperset',
                 'symmetric_difference', 'union', '__iand__', '__ior__', '__ixor__', '__isub__']

    def __init__(self, set_object):
        assert isinstance(set_object, set)
        for attr in self.__slots__[:-4]:
            exec(f"self.{attr} = set_object.{attr}")
        for attr in self.__slots__[-4:]:
            exec(f"self.{attr} = self.unsupported_operator")

    def unsupported_operator(self, other):
        raise TypeError("unsupported operator for type SetView")


class OuterPinsView:
    __slots__ = ['_dict', '__eq__', '__ge__', '__gt__', '__hash__', '__le__', '__len__', '__lt__', '__ne__',
                 '__repr__', '__str__', 'copy', 'fromkeys', 'items', 'keys', 'values']

    def __init__(self, dict_object):
        assert isinstance(dict_object, dict)
        self._dict = dict_object
        for attr in self.__slots__[1:]:
            exec(f"self.{attr} = dict_object.{attr}")

    def __contains__(self, item):
        if item not in self._dict:
            if isinstance(item, OuterPin):
                return item.inner_pin in self._dict
        return True

    def __getitem__(self, item):
        if isinstance(item, OuterPin):
            return self._dict[item.inner_pin]
        return self._dict[item]

    def __iter__(self):
        return iter(self._dict.values())

    def get(self, key, default=None):
        if isinstance(key, OuterPin):
            return self._dict.get(key.inner_pin, default)
        return self._dict.get(key, default)
