import sys

class Element:
    def __init__(self):
        self.data = dict()
    
    def set_entry(self, key, value):
        self.data[sys.intern(key)] = value

    def get_value(self, key):
        return self.data.get(key)

class Environment(Element):
    def __init__(self):
        super().__init__()
        self.libraries = list()
        self.top_instance = None

    def create_library(self):
        library = library()
        self.add_library(library)
        return library
    
    def add_library(self, library):
        self.libraries.append(library)
        library.environment = self

class Library:
    def __init__(self):
        self.environment = None
        self.definitions = list()

class Definition:
    def __init__(self):
        self.library = None
        self.ports = list()
        self.cables = list()
        self.instances = list()

class Bundle:
    def __init__(self):
        self.is_downto = True
        self.is_scalar = False
        self.lower_index = 0

class Port(Bundle):
    def __init__(self):
        self.definition = None
        self.direction = None
        self.inner_pins = list()

class Pin:
    def __init__(self):
        self.wire = None

class InnerPin(Pin):
    def __init__(self):
        self.port = None

class OuterPin(Pin):
    def __init__(self):
        self.instance = None
        self.inner_pin = None

class Cable(Bundle):
    def __init__(self):
        self.definition = None
        self.wires = list()

class Wire:
    def __init__(self):
        self.cable = None
        self.pins = list()

class Instance:
    def __init__(self):
        self.definition = None
        self.outer_pins = list()
