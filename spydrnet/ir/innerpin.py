from spydrnet.ir.pin import Pin


class InnerPin(Pin):
    """
    Pins that correspond to definitions. These pins can be thought of as on the inside of a definition. There can be
    many outer pins for each inner pin
    """
    __slots__ = ['_port']

    def __init__(self):
        super().__init__()
        self._port = None

    @property
    def port(self):
        '''return the port that the inner pin is a part of. This object cannot be modified directly by the end user.'''
        return self._port
