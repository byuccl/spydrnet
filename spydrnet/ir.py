import sys
import itertools
import weakref
from enum import Enum


class Element:
    """Base class of all intermediate representation objects"""
    _nextUID_ = 0

    def __init__(self):
        """
        Set up the members with a unique id and data namespace managers
        The object has self.uid that is accessable although it should not be changed.
        All other members are private."""
        #self.data = dict()
        #self.name = None
        self.uid  = Element._nextUID_
        Element._nextUID_ = Element._nextUID_ + 1

        self._metadata = dict()
        self._managers = list()
    
    @property
    def parent(self):
        '''
        Return the parent of the element
        ?should this be overridden by the implementing objects?
        '''
        return None
    
    @property
    def children(self):
        '''
        Return a children iterator of the children of the element
        ?should this be overridden by the implementing objects?
        '''
        return iter(())

    def add_data_manager(self, manager):
        '''
        Add a datamanager to the element.
        @param manager is a datamanager that has already been created and is ready for use
        '''
        manager.set_owner_and_populate_lookup(self)
        self._managers.append(manager)

    def __setitem__(self, key, value):
        '''
        create an entry in the dictionary of the element it will be stored in the metadata.
        '''
        key = sys.intern(key)
        self._metadata.__setitem__(sys.intern(key), value)
        self.setitem_callback(self)

    def setitem_callback(self, element):
        '''
        Add an element to the data managers so that the element can be later found very quickly
        @param element is the element to be added to the data managers
        '''
        for manager in self._managers:
            manager.add_to_lookup(element)
        if self.parent:
            self.parent.setitem_callback(element)

    def __delitem__(self, key):
        self._metadata.__delitem__(key)

    def __getitem__(self, key):
        return self._metadata.__getitem__(key)

    def __contains__(self, item):
        return self._metadata.__contains__(item)

    def __iter__(self):
        return self._metadata.__iter__()

    def pop(self, item):
        return self._metadata.pop(item)

    def lookup_element(self, cls, key, identifier):
        '''
        find a sub element by identifier, key and class
        Parameters
        ----------
        cls : the class of the element to be looked up
        key : the key of the element to be looked up
        identifier : the identifier of the element to be looked up
        Returns
        -------
        element
            the element that matches the description passed in includng class
        Exceptions
        ----------
        KeyError if the element is not found in the lookup
        '''
        for manager in self._managers:
            element = manager.lookup(cls, key, identifier)
            if element:
                return element
        for child in self.children:
            if cls == type(child):
                if key in child:
                    if identifier == child[key]:
                        return child
        raise KeyError()


class Design(Element):
    '''
    TODO we might want to rename this to netlist or is that the environment
    Holds a netlist object
    '''
    def __init__(self):
        super().__init__()
        self.netlist = None

    @property
    def parent(self):
        return None

    @property
    def children(self):
        return iter((self.netlist,))


class Environment(Element):
    '''
    represents a netlist object
    contains a top level instance and libraries
    '''
    def __init__(self):
        super().__init__()
        self.design = None
        self.libraries = list()
        self._top_instance = None
        self._top_virtual_instance = None

    @property
    def top_instance(self):
        '''
        get the top instance in the environment
        Returns
        -------
        Instance
            The top level instance in the environment
        '''
        return self._top_instance

    @top_instance.setter
    def top_instance(self, instance):
        '''

        '''
        from spydrnet.virtual_ir import generate_virtual_instances_from_top_level_instance
        if isinstance(instance, Instance):
            self._top_instance = instance
            if self._top_virtual_instance:
                search_stack = [self._top_virtual_instance]
                while search_stack:
                    current_virtual_instance = search_stack.pop()
                    search_stack += current_virtual_instance.virtualChildren.values()
                    definition = current_virtual_instance.instance.definition
                    definition.virtual_instances.discard(current_virtual_instance)
            self._top_virtual_instance = generate_virtual_instances_from_top_level_instance(instance)
    
    @property
    def top_virtual_instance(self):
        return self._top_virtual_instance
            
            

    @property
    def parent(self):
        return self.design

    @property
    def children(self):
        return iter(self.libraries)

    def create_library(self):
        library = Library()
        self.add_library(library)
        return library
    
    def add_library(self, library):
        self.libraries.append(library)
        library.environment = self
        self.setitem_callback(library)

    def get_library(self, identifier):
        library = self.lookup_element(Library, 'EDIF.identifier', identifier)
        return library


class Library(Element):
    def __init__(self):
        super().__init__()
        self.environment = None
        self.definitions = list()

    @property
    def parent(self):
        return self.environment

    @property
    def children(self):
        return iter(self.definitions)

    def create_definition(self):
        definition = Definition()
        self.add_definition(definition)
        return definition

    def add_definition(self, definition, position=None):
        if position is not None:
            self.definitions.insert(position, definition)
        else:
            self.definitions.append(definition)
        definition.library = self
        self.setitem_callback(definition)

    def get_definition(self, identifier):
        definition = self.lookup_element(Definition, 'EDIF.identifier', identifier)
        return definition


class Definition(Element):
    def __init__(self):
        super().__init__()
        self.library = None
        self.ports = list()
        self.cables = list()
        self.instances = list()
        self.virtual_instances = set()

    def is_leaf(self):
        if len(self.instances) > 0 or len(self.cables) > 0:
            return False
        return True

    @property
    def parent(self):
        return self.library

    @property
    def children(self):
        return itertools.chain(self.ports, self.cables, self.instances)

    def create_port(self):
        port = Port()
        self.add_port(port)
        return port

    def add_port(self, port):
        self.ports.append(port)
        port.definition = self
        self.setitem_callback(port)

    def get_port(self, identifier):
        port = self.lookup_element(Port, 'EDIF.identifier', identifier)
        return port
 
    def create_instance(self):
        instance = Instance()
        self.add_instance(instance)
        return instance
    
    def add_instance(self, instance):
        self.instances.append(instance)
        instance.parent_definition = self
        self.setitem_callback(instance)

    def get_instance(self, identifier):
        instance = self.lookup_element(Instance, 'EDIF.identifier', identifier)
        return instance

    def create_cable(self):
        cable = Cable()
        self.add_cable(cable)
        return cable

    def add_cable(self, cable):
        self.cables.append(cable)
        cable.definition = self
        self.setitem_callback(cable)

    def get_cable(self, identifier):
        cable = self.lookup_element(Cable, 'EDIF.identifier', identifier)
        return cable

    def get_pin(self, port_identifier, index = 0):
        """
        Deprecated: 0.1.0
        """
        port = self.get_port(port_identifier)
        return port.get_pin(index)


class Bundle(Element):
    def __init__(self):
        super().__init__()
        self.definition = None
        self.is_downto = True
        self.is_scalar = False
        self.lower_index = 0

    @property
    def parent(self):
        return self.definition


class Port(Bundle):
    class Direction(Enum):
        '''Define the possible directions for a given port'''
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
    TODO are we going to rename this?
    netlist instance of a netlist definition
    '''
    def __init__(self):
        '''
        creates an empty object of type instance
        '''
        super().__init__()
        self._parent_definition = None
        self._definition = None
        self.outer_pins = dict()

    @property
    def parent_definition(self):
        return self._parent_definition

    @parent_definition.setter
    def parent_definition(self, value):
        self._parent_definition = value
        #definition = self.definition
        #for virtual_parent in value.virtual_instances:
        #    virtual_parent.create_virtual_child(self)

    @property
    def definition(self):
        return self._definition

    @definition.setter
    def definition(self, value):
        self._definition = value
        #parent_definition = self.parent_definition
        #if parent_definition:
        #    for virtual_parent in parent_definition.virtual_instances:
        #        virtual_parent.create_virtual_child

    def is_leaf(self):
        '''
        check to see if the netlist instance is an instance of a leaf definition
        Returns
        -------
        boolean
            True if the definition is leaf
            False if the definition is not leaf
        '''
        return self.definition.is_leaf()

    def get_pin(self, port_identifier, index = 0):
        '''
        get a pin by port and index
        Parameters
        ----------
        port_identifier

        index
            
        '''
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
