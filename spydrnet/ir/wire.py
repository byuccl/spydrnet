from copy import copy

import spydrnet as sdn
from spydrnet.global_state import global_callback
from spydrnet.ir import Element, OuterPin
from spydrnet.ir.views.listview import ListView


class Wire(Element):
    """
    Represents a wire object
    """
    __slots__ = ['_cable', '_pins']

    def __init__(self):
        self._cable = None
        self._pins = list()

    @property
    def cable(self):
        """The cable that the wire contains"""
        return self._cable

    @property
    def pins(self):
        """The a list of pins that the wire is connected to"""
        return ListView(self._pins)

    @pins.setter
    def pins(self, value):
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_list) == len(value_set) and set(self._pins) == value_set, \
            "Set of values do not match, assignment can only be used to reorder, values must be unique"
        self._pins = value_list

    def connect_pin(self, pin, position=None):
        """Connects a pin to the wire

        parameters
        ----------

        value - The pin to connect to
        """
        global_callback._call_wire_connect_pin(self, pin)
        if isinstance(pin, OuterPin):
            instance = pin.instance
            inner_pin = pin.inner_pin
            assert instance is not None and inner_pin is not None, \
                "Outer pin must represent an instance and an inner_pin"
            assert inner_pin in instance.pins, "Pin not associated with instance"
            outer_pin = instance.pins[inner_pin]
            assert outer_pin.wire is not self, "Pin already connected to this wire"
            assert outer_pin.wire is None, "Pin already connected to a different wire"
            pin._wire = self
            pin = outer_pin
        else:
            assert pin.wire is None, "Pin already connected to a different wire"
        if position is not None:
            self._pins.insert(position, pin)
        else:
            self._pins.append(pin)
        pin._wire = self

    def disconnect_pin(self, pin):
        """Disconnect a pin from the wire

        parameters
        ----------

        value - The pin to disconnect
        """
        if isinstance(pin, OuterPin):
            instance = pin.instance
            inner_pin = pin.inner_pin
            assert instance is not None and inner_pin is not None, \
                "Outer pin must represent an instance and an inner_pin"
            assert inner_pin in instance.pins, "Pin not associated with instance"
            outer_pin = instance.pins[inner_pin]
            assert outer_pin.wire is self, "Pin is disconnected or connected to a different wire."
            self._disconnect_pin(pin)
            pin = outer_pin
        else:
            assert pin.wire == self, "Pin does not belong to this wire"
        self._pins.remove(pin)
        self._disconnect_pin(pin)

    def disconnect_pins_from(self, pins):
        """Disconnect a list of pins from the wire

        parameters
        ----------

        value - The list of pins to disconnect
        """
        if isinstance(pins, set):
            excluded_pins = pins
        else:
            excluded_pins = set(pins)
        all_pins_can_be_disconnected = True
        for pin in excluded_pins:
            if isinstance(pin, OuterPin):
                instance = pin.instance
                inner_pin = pin.inner_pin
                if instance is None or inner_pin is None or inner_pin not in instance.pins or \
                        instance.pins[inner_pin].wire is not self:
                    all_pins_can_be_disconnected = False
                    break
            else:
                if pin.wire != self:
                    all_pins_can_be_disconnected = False
                    break
        assert all_pins_can_be_disconnected, "Some of the pins to disconnect are not associated with an instance, " \
                                             "already disconnected, or connected to a different wire"
        for pin in excluded_pins:
            if isinstance(pin, OuterPin):
                self._disconnect_pin(pin)
                pin = pin.instance.pins[pin]
            self._disconnect_pin(pin)
        self._pins = list(x for x in self._pins if x not in excluded_pins)

    def _disconnect_pin(self, pin):
        global_callback._call_wire_disconnect_pin(self, pin)
        pin._wire = None

    def _clone_rip_and_replace(self, memo):
        """Remove from its current environment and place it into the new cloned environment with references held in the memo dictionary"""
        new_pins = list()
        for p in self._pins:
            assert p in memo, "the pin must be cloned"
            new_pins.append(memo[p])
        self._pins = new_pins
        pass

    def _clone_rip(self):
        """Remove from its current environmnet.

        This will remove all pin pointers and create a floating stand alone instance."""
        self._pins = list()
        pass

    def _clone(self, memo):
        """Not api safe clone function

        clone leaving all references in tact.
        the element can then either be ripped or ripped and replaced"""
        assert self not in memo, "the object should not have been copied twice in this pass"
        from spydrnet.ir import Wire as ExtendedWire
        c = ExtendedWire()
        memo[self] = c
        c._cable = None
        # shallow copy the list so that it retains its pin references
        c._pins = copy(self._pins)
        return c

    def clone(self):
        """clone wire in an api safe way.

        The following properties can be expected from the returned element:
         * The wire is not connected to any pins.
         * The wire is orphaned from any cable.
         * No pins are connected to the wire
         """
        c = self._clone(dict())
        c._clone_rip()
        return c

    def index(self):
        """if this wire is in a cable, returns the index number of the wire in the parent cable"""

        assert self.cable is not None, "the wire does not belong to a cable"

        return self.cable.wires.index(self)

    def __str__(self):
        """Re-define the print function so it is easier to read"""
        rep = str(type(self))
        rep = rep[:-1] + '; '
        if self.cable is None:
            rep += 'Not contained by any Cable'
        elif self.cable.name is None:
            rep += 'Contained by Cable whose name is undefined'
        else:
            rep += 'Contained by Cable.name \'' + str(self.cable.name) + '\' ' + str(self.cable)
        rep += '>'
        return rep

    def get_driver(self):
        '''
        returns the driver(s) of the wire
        '''
        drivers = []
        for pin in self._pins:
            if pin.__class__ is sdn.InnerPin:
                if pin.port.direction is sdn.IN:
                    drivers.append(pin)
            else:
                if pin.inner_pin.port.direction is sdn.OUT:
                    drivers.append(pin)
        return drivers
