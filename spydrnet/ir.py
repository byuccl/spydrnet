import sys
from enum import Enum

class Element:
    """Base class of all intermediate representation objects"""
    _nextUID_ = 0
    def __init__(self):
        """set up the members and generate a unique identifier (uid) that is one greater than the last uid"""
        self.data = dict()
        self.name = None
        self.uid  = Element._nextUID_
        Element._nextUID_ = Element._nextUID_ + 1

        self._metadata = dict()
    
    def __setitem__(self, key, value):
        self._metadata.__setitem__(sys.intern(key), value)

    def __delitem__(self, key):
        self._metadata.__delitem__(key)

    def __getitem__(self, key):
        return self._metadata.__getitem__(key)

    def __contains__(self, item):
        return self._metadata.__contains__(item)

    def pop(self, item):
        return self._metadata.pop(item)

class Environment(Element):
    def __init__(self):
        super().__init__()
        self.libraries = list()
        self.top_instance = None

    def create_library(self):
        library = Library()
        self.add_library(library)
        return library
    
    def add_library(self, library):
        self.libraries.append(library)
        library.environment = self

    def get_library(self, identifier):
        for library in self.libraries:
            if 'EDIF.identifier' in library:
                if library['EDIF.identifier'].lower() == identifier.lower():
                    return library
        raise KeyError()

class Library(Element):
    def __init__(self):
        super().__init__()
        self.environment = None
        self.definitions = list()

    def create_definition(self):
        definition = Definition()
        self.add_definition(definition)
        return definition

    def add_definition(self, definition):
        self.definitions.append(definition)
        definition.library = self

    def get_definition(self, identifier):
        for definition in self.definitions:
            if 'EDIF.identifier' in definition:
                if definition['EDIF.identifier'].lower() == identifier.lower():
                    return definition
        raise KeyError()

class Definition(Element):
    def __init__(self):
        super().__init__()
        self.library = None
        self.ports = list()
        self.cables = list()
        self.instances = list()

    def create_port(self):
        port = Port()
        self.add_port(port)
        return port

    def add_port(self, port):
        self.ports.append(port)
        port.definition = self

    def get_port(self, identifier):
        for port in self.ports:
            if 'EDIF.identifier' in port:
                if port['EDIF.identifier'].lower() == identifier.lower():
                    return port
        raise KeyError()
 
    def create_instance(self):
        instance = Instance()
        self.add_instance(instance)
        return instance
    
    def add_instance(self, instance):
        self.instances.append(instance)
        instance.parent_definition = self

    def get_instance(self, identifier):
        for instance in self.instances:
            if 'EDIF.identifier' in instance:
                if instance['EDIF.identifier'].lower() == identifier.lower():
                    return instance
        raise KeyError()

    def create_cable(self):
        cable = Cable()
        self.add_cable(cable)
        return cable

    def add_cable(self, cable):
        self.cables.append(cable)
        cable.definition = self

    def get_cable(self, identifier):
        for cable in self.cables:
            if 'EDIF.identifier' in cable:
                if cable['EDIF.identifier'].lower() == identifier.lower():
                    return cable
        raise KeyError()

    def get_pin(self, port_identifier, index = 0):
        port = self.get_port(port_identifier)
        return port.get_pin(index)


class Bundle(Element):
    def __init__(self):
        super().__init__()
        self.is_downto = True
        self.is_scalar = False
        self.lower_index = 0

class Port(Bundle):
    class Direction(Enum):
        UNDEFINED = 0
        INOUT = 1
        IN = 2
        OUT = 3
    
    def __init__(self):
        super().__init__()
        self.definition = None
        self.direction = self.Direction.UNDEFINED
        self.inner_pins = list()

    def initialize_pins(self, pin_count):
        for _ in range(pin_count):
            self.create_pin()
    
    def create_pin(self):
        inner_pin = InnerPin()
        self.add_pin(inner_pin)
        return inner_pin

    def add_pin(self, inner_pin):
        self.inner_pins.append(inner_pin)
        inner_pin.port = self

    def get_pin(self, index = 0):
        return self.inner_pins[index]

class Pin:
    def __init__(self):
        self.wire = None

class InnerPin(Pin):
    def __init__(self):
        super().__init__()
        self.port = None

class OuterPin(Pin):
    def __init__(self):
        super().__init__()
        self.instance = None
        self.inner_pin = None

class Cable(Bundle):
    def __init__(self):
        super().__init__()
        self.definition = None
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


class Wire(Element):
    def __init__(self):
        self.cable = None
        self.pins = list()

    def connect_pin(self, pin):
        self.pins.append(pin)
        pin.wire = self

class Instance(Element):
    def __init__(self):
        super().__init__()
        self.parent_definition = None
        self.definition = None
        self.outer_pins = dict()

    def get_pin(self, port_identifier, index = 0):
        port = self.definition.get_port(port_identifier)
        inner_pin = port.get_pin(index)
        if inner_pin not in self.outer_pins:
            outer_pin = OuterPin()
            self.outer_pins[inner_pin] = outer_pin
            outer_pin.instance = self
            outer_pin.inner_pin = inner_pin
            return outer_pin
        else:
            return self.outer_pins[inner_pin]
