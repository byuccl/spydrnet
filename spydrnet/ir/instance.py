from spydrnet.ir.element import Element
from spydrnet.ir.outerpin import OuterPin
from spydrnet.ir.views.outerpinsview import OuterPinsView
from spydrnet.global_state import global_callback


class Instance(Element):
    """
    netlist instance of a netlist definition. Instances are literally instances of definitions and they reside inside definitions.
    Function names have been set to adjust for the potential confusion that could arise because instances both have a parent definition and have definitions which they reference.
    """
    __slots__ = ['_parent', '_reference', '_pins']

    def __init__(self):
        """
        creates an empty object of type instance
        """
        super().__init__()
        self._parent = None
        self._reference = None
        self._pins = dict()

    @property
    def parent(self):
        '''Get the definition that contains this instance'''
        return self._parent

    @property
    def reference(self):
        '''get the definition that this instance is instantiating'''
        return self._reference

    @reference.setter
    def reference(self, value):
        '''change the definition that represents this instance.
        Port positioning and size must be taken into account when a new definition is being used.
        if they are different the connections cannot be done automatically with this function.

        parameters
        ----------

        value - (Definition) the definition that this instance should be an instance of'''
        global_callback._call_instance_reference(self, value)
        if value is None:
            for pin in self.pins:
                wire = pin.wire
                if wire:
                    wire.disconnect_pin(pin)
                if isinstance(pin, OuterPin):
                    pin._instance = None
                    pin._inner_pin = None
            self._pins.clear()
            if self._reference:
                self._reference._references.remove(self)
        else:
            if self._reference is not None:
                assert len(self.reference.ports) == len(value.ports) and all(len(x.pins) == len(y.pins) for x, y in
                                                                             zip(self.reference.ports, value.ports)), \
                    "Reference reassignment only supported for definitions with matching port positions"
                self._reference._references.remove(self)
                for cur_port, new_port in zip(self.reference.ports, value.ports):
                    for cur_pin, new_pin in zip(cur_port.pins, new_port.pins):
                        outer_pin = self._pins.pop(cur_pin)
                        outer_pin._inner_pin = new_pin
                        self._pins[new_pin] = outer_pin
            else:
                for port in value.ports:
                    for pin in port.pins:
                        self._pins[pin] = OuterPin.from_instance_and_inner_pin(self, pin)
            value._references.add(self)
        self._reference = value

    @reference.deleter
    def reference(self):
        self.reference = None

    @property
    def pins(self):
        '''get the pins on this instance.'''
        return OuterPinsView(self._pins)