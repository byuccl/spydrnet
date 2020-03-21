from spydrnet.ir.element import Element


class Pin(Element):
    '''pin connects to a single wire. This class is extended by InnerPin and OuterPin'''
    __slots__ = ['_wire', '__weakref__']

    def __init__(self):
        self._wire = None

    @property
    def wire(self):
        '''get the wire the pin is connected to. This value cannot be modified directly by the end user.'''
        return self._wire
