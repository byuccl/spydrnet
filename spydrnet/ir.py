import sys
from enum import Enum

class Element:
    def __init__(self):
        self._data = dict()
    
    def __setitem__(self, key, value):
        self._data.__setitem__(sys.intern(key), value)

    def __delitem__(self, key):
        self._data.__delitem__(key)

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __contains__(self, item):
        return self._data.__getitem__(item)

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

    def create_instance(self):
        instance = Instance()
        self.add_instance(instance)
        return instance
    
    def add_instance(self, instance):
        self.instances.append(instance)
        instance.definition = self

    def create_cable(self):
        cable = Cable()
        self.add_cable(cable)
        return cable

    def add_cable(self, cable):
        self.cables.append(cable)
        cable.definition = self

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

class Wire:
    def __init__(self):
        self.cable = None
        self.pins = list()

class Instance(Element):
    def __init__(self):
        super().__init__()
        self.definition = None
        self.outer_pins = list()
