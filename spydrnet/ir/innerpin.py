from spydrnet.ir import Pin
from copy import deepcopy, copy, error


class InnerPin(Pin):
    """Pins that correspond to definitions.

    These pins can be thought of as on the inside of a definition. There can be
    many outer pins for each inner pin
    """
    __slots__ = ['_port']

    def __init__(self):
        super().__init__()
        self._port = None

    @property
    def port(self):
        """Return the port that the inner pin is a part of.

        This object cannot be modified directly by the end user."""
        return self._port

    def _clone_rip_and_replace(self, memo):
        """Remove from its current environment and place it into the new cloned environment with references held in the memo dictionary"""
        if self._wire != None:
            assert self._wire in memo, "wire must have been cloned in order to rip and replace innerpin"
            self._wire = memo[self._wire]

    def _clone_rip(self):
        """Remove from its current environmnet. This will remove all pin pointers and create a floating stand alone instance."""
        self._wire = None

    def _clone(self, memo):
        """Not api safe clone function.

        Clone leaving all references in tact.
        the element can then either be ripped or ripped and replaced"""
        assert self not in memo, "the object should not have been copied twice in this pass"
        from spydrnet.ir import InnerPin as InnerPinExtended
        c = InnerPinExtended()
        memo[self] = c
        c._wire = self._wire
        c._port = None
        return c

    def clone(self):
        """Clone the inner pin in an api safe way.

        The following conditions will be met:

         * The inner pin will be orphaned from any ports
         * The pin will not be connected to any wires
         * The pin will not be referenced to by any wires or outer pins

        """
        c = self._clone(dict())
        c._clone_rip()
        return c
