from spydrnet.ir import Pin
from copy import deepcopy, copy, error


class OuterPin(Pin):
    """
    Pins that correspond to instances. These pins can be thought of as on the outside of an instance. There can be many
    outer pins for each inner pin
    """
    __slots__ = ['_instance', '_inner_pin']

    @staticmethod
    def from_instance_and_inner_pin(instance, inner_pin):
        """Create an outer pin associated with a given inner_pin and instance object.

        parameters
        ----------

        instance - (Instance) the instance to associate with this pin

        inner_pin - (InnerPin) the inner pin with which to associate this outer pin"""
        from spydrnet.ir import OuterPin as OuterPinExtended
        return OuterPinExtended(instance, inner_pin)

    def __init__(self, instance=None, inner_pin=None):
        """create an OuterPin.

        parameters
        ----------

        instance - (Instance) the instance with which to associate this outper pin.

        inner_pin - (InnerPin) a definition's inner pin to be associated with this instance outer pin."""
        super().__init__()
        self._instance = instance
        self._inner_pin = inner_pin

    @property
    def instance(self):
        """Return the instance with which this pin is associated"""
        return self._instance

    @property
    def inner_pin(self):
        """get the inner pin associated with this outer pin"""
        return self._inner_pin

    def __eq__(self, other):
        if isinstance(other, OuterPin):
            return self._instance == other._instance and self._inner_pin == other._inner_pin
        return False

    def __hash__(self):
        return hash((self._instance, self._inner_pin))

    def _clone_rip_and_replace(self, memo):
        """remove from its current environment and place it into the new cloned environment with references held in the memo dictionary"""
        if self._wire != None:
            assert self._wire in memo, "can't call this function when the wire has not been cloned yet"
            self._wire = memo[self._wire]

    def _clone_rip(self):
        """Remove from its current environmnet.

        This will remove all pin pointers and create a floating stand alone instance.
        """
        self._inner_pin = None
        self._wire = None

    def _clone(self, memo):
        """Not api safe clone function

        clone leaving all references in tact.
        the element can then either be ripped or ripped and replaced"""
        assert self not in memo, "the object should not have been copied twice in this pass"
        from spydrnet.ir import OuterPin as OuterPinExtended
        c = OuterPinExtended()
        memo[self] = c
        c._instance = None
        c._inner_pin = self._inner_pin
        c._wire = self._wire
        return c

    def clone(self):
        """Clone the pin in an api safe way.

        The following conditions will be met with the returned outer pin:

         * the pin will not be connected to any wires
         * the pin will be orphaned from any instance
         * the pin will not be connected to any inner pins
        """
        c = self._clone(dict())
        c._clone_rip()
        return c
