class Element:
    """Base class of all intermediate representation objects"""
    _nextUID_ = 0
    def __init__(self):
        """set up the members and generate a unique identifier (uid) that is one greater than the last uid"""
        self.data = dict()
        self.name = None
        self.uid  = Element._nextUID_
        Element._nextUID_ = Element._nextUID_ + 1

    def getName(self):
        """return the name of the object"""
        return self.name
    
    def getMetadata(self, key):
        """
        return the metadata value mapped to by key or None if no entry exists

        Arguments:
        key -- the value to dereference
        """
        return self.data[key]

class Environment(Element):
    def __init__(self):
        self.libraries = list()
        self.top_instance = None

class Library(Element):
    def __init__(self):
        self.environment = None
        self.definitions = list()

class Definition(Element):
    def __init__(self):
        self.library = None
        self.ports = list()
        self.cables = list()
        self.instances = list()

class Bundle(Element):
    def __init__(self):
        self.is_downto = True
        self.is_scalar = False
        self.lower_index = 0

class Port(Bundle):
    def __init__(self):
        self.definition = None
        self.direction = None
        self.inner_pins = list()

class Pin(Element):
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

class Wire(Element):
    def __init__(self):
        self.cable = None
        self.pins = list()

class Instance(Element):
    def __init__(self):
        self.definition = None
        self.outer_pins = list()
