from spydrnet.ir import Element


class Pin(Element):
    """Pin connects to a single wire.

    This class is extended by InnerPin and OuterPin"""
    __slots__ = ['_wire',]

    def __init__(self):
        self._wire = None

    @property
    def wire(self):
        """Get the wire the pin is connected to. This value cannot be modified directly by the end user."""
        return self._wire

    def __str__(self):
        """Re-define the print function so it is easier to read"""
        rep = str(type(self))
        rep = rep[:-1] + '; '
        if self.wire is None:
            rep += 'Wire connected undefined'
        else:
            rep += 'connected to\'' + str(self.wire) + '\''
        rep += '>'
        return rep
