from spydrnet.ir.pin import Pin


class OuterPin(Pin):
    """
    Pins that correspond to instances. These pins can be thought of as on the outside of an instance. There can be many
    outer pins for each inner pin
    """
    __slots__ = ['_instance', '_inner_pin']

    @staticmethod
    def from_instance_and_inner_pin(instance, inner_pin):
        '''create an outer pin associated with a given inner_pin and instance object.

        parameters
        ----------

        instance - (Instance) the instance to associate with this pin

        inner_pin - (InnerPin) the inner pin with which to associate this outer pin'''
        return OuterPin(instance, inner_pin)

    def __init__(self, instance=None, inner_pin=None):
        '''create an OuterPin.

        parameters
        ----------

        instance - (Instance) the instance with which to associate this outper pin.

        inner_pin - (InnerPin) a definition's inner pin to be associated with this instance outer pin.'''
        super().__init__()
        self._instance = instance
        self._inner_pin = inner_pin

    @property
    def instance(self):
        '''Return the instance with which this pin is associated'''
        return self._instance

    @property
    def inner_pin(self):
        '''get the inner pin associated with this outer pin'''
        return self._inner_pin

    def __eq__(self, other):
        if isinstance(other, OuterPin):
            return self._instance == other._instance and self._inner_pin == other._inner_pin
        return False

    def __hash__(self):
        return hash((self._instance, self._inner_pin))