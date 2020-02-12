from spydrnet.ir.outerpin import OuterPin
from spydrnet.ir.views.listview import ListView
from spydrnet.global_state import global_callback
from copy import copy, deepcopy, error


class Wire:
    __slots__ = ['_cable', '_pins']

    def __init__(self):
        self._cable = None
        self._pins = list()

    @property
    def cable(self):
        return self._cable

    @property
    def pins(self):
        return ListView(self._pins)

    @pins.setter
    def pins(self, value):
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_list) == len(value_set) and set(self._pins) == value_set, \
            "Set of values do not match, assignment can only be used to reorder, values must be unique"
        self._pins = value_list

    def connect_pin(self, pin, position=None):
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

    def __deepcopy__(self, memo):
        if self in memo:
            raise error("the object should not have been copied twice in this pass")
        c = Wire()
        memo[self] = c
        c._cable = None
        c._pins = copy(self._pins) #shallow copy the list so that it is a new list but it still refers to the pins.
        return c