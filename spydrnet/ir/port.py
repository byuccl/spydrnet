from spydrnet.ir import Bundle
from spydrnet.ir import InnerPin
from spydrnet.ir import OuterPin
from spydrnet.ir.views.listview import ListView
from spydrnet.global_state import global_callback
from spydrnet.global_state.global_callback import _call_create_port
from copy import deepcopy, copy, error

from enum import Enum


class Port(Bundle):
    """
    Located on the inside of a definition.

    Ports contain information about the quantity and directon of pins that go into and out of the defined struture when instanced.
    """
    __slots__ = ['_direction', '_pins']

    class Direction(Enum):
        """Define the possible directions for a given port.

        Possible Directions are:

        UNDEFINED, INOUT, IN, OUT
        """
        UNDEFINED = 0
        INOUT = 1
        IN = 2
        OUT = 3

    def __init__(self, name=None, properties=None, is_downto=None, is_scalar=None, lower_index=None, direction=None):
        """Setup an empty port

        parameters
        ----------

        name - (str) the name of this instance
        properties - (dict) the dictionary which holds the properties
        id_downto - (bool) set the downto status. Downto is False if the right index is higher than the left one, True otherwise
        is_scalar - (bool) set the scalar status. Return True if the item is a scalar False otherwise.
        lower_index - (int) get the value of the lower index of the array.
        direction - (Enum) Define the possible directions for a given port. (UNDEFINED, INOUT, IN, OUT)

        """
        super().__init__()
        self._direction = self.Direction.UNDEFINED
        self._pins = list()
        _call_create_port(self)
        if name != None:
            self.name = name

        if is_downto is not None:
            self.is_downto = is_downto

        if is_scalar is not None:
            self.is_scalar = is_scalar

        if lower_index is not None:
            self.lower_index = lower_index
        if direction is not None:
            self.direction = direction

        if properties != None:
            assert isinstance(
                properties, dict), "properties must be a dictionary"
            for key in properties:
                self[key] = properties[key]

    def _items(self):
        """Overrides the _items function in the bundles class. For ports, pins are returned"""
        return self._pins

    @property
    def direction(self):
        """Gets the direction of the port.

        This will be a variable of type Port.Direction
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        """Set the direction of the port.

        parameters
        ----------

        value - (Port.Direction or int or str) when a Port.Direction is passed in it will set the port accordingly. when an int is passed in it will be 0: UNDEFINED, 1: INOUT, 2: IN, 3: OUT. if a string is passed in it is case insensitively compared with the names and assigned accordingly
        """
        if isinstance(value, self.Direction):
            self._direction = value
        elif isinstance(value, int):
            for direction in self.Direction:
                if direction.value == value:
                    self._direction = direction
                    break
        elif isinstance(value, str):
            value = value.lower()
            for direction in self.Direction:
                if direction.name.lower() == value:
                    self._direction = direction
                    break
        else:
            raise TypeError(
                "Type {} cannot be assigned to direction".format(type(value)))

    @property
    def pins(self):
        """Get a list of the pins that are in the port"""
        return ListView(self._pins)

    @pins.setter
    def pins(self, value):
        """This function can set the pins for the port, but it can only be used to reorder the pins in the port.
        It cannot be used to add or remove pins from the port. to do this use the add_pin or remove_pin functions instead

        parameters
        ----------

        value - (List of InnerPin objects) the reordered pins

        """
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_set) == len(value_list) and set(self._pins) == value_set, \
            "Set of values do not match, assignment can only be used to reorder values, values must be unique"
        self._pins = value_list

    def create_pins(self, pin_count):
        """Create pin_count pins in the given port a downto style syntax is assumed.

        Parameters
        ----------

        pin_count - (int) this is the number of pins to add to the port
        """
        for _ in range(pin_count):
            self.create_pin()
        return self.pins[-pin_count:]

    def create_pin(self):
        """Create a pin and add it to the port.

        return:
        the inner_pin created
        """
        from spydrnet.ir import InnerPin as InnerPinExtended
        pin = InnerPinExtended()
        self.add_pin(pin)
        if self.definition:
            for reference in self.definition.references:
                reference._pins[pin] = OuterPin(reference, pin)
        return pin

    def add_pin(self, pin, position=None):
        """Add a pin to the port at the given position.

        parameters
        ----------

        pin - (Pin) the pin to be added to the port.

        position - (int, default None) the index at which to add the pin
        """
        assert isinstance(pin, InnerPin)
        assert pin.port is not self, "Pin already belongs to this port"
        assert pin.port is None, "Pin already belongs to another port"
        global_callback._call_port_add_pin(self, pin)
        if position is None:
            self._pins.append(pin)
        else:
            self._pins.insert(position, pin)
        pin._port = self

    def remove_pin(self, pin):
        """Remove the given pin from the port.

        The pin must belong to the port in order to be removed. Wires are disconnected from the pin that is removed.

        parameters
        ----------

        pin - (Pin) a pin to be removed from the port.
        """
        assert pin.port == self, "Pin does not belong to this port."
        self._remove_pin(pin)
        self._pins.remove(pin)

    def remove_pins_from(self, pins):
        """Remove several pins from the port at once.

        The wires are disconnected from the pins that are removed.

        parameters
        ----------

        pins - (List of Pin objects) a list of all pins to be removed from the port.

        """
        if isinstance(pins, set):
            exclude_pins = pins
        else:
            exclude_pins = set(pins)
        assert all(isinstance(x, InnerPin) and x.port == self for x in exclude_pins), "All pins to remove must be " \
                                                                                      "InnerPins and belong to the port"
        for pin in exclude_pins:
            self._remove_pin(pin)
        self._pins = list(x for x in self._pins if x not in exclude_pins)

    def _remove_pin(self, pin):
        """Internal pin removal function.
        Disconnects the wires from the pin and remvoes all the pins reference to other pins."""
        global_callback._call_port_remove_pin(self, pin)
        if self.definition:
            for reference in self.definition.references:
                outer_pin = reference.pins[pin]
                wire = outer_pin.wire
                if wire:
                    wire.disconnect_pin(outer_pin)
                del reference._pins[pin]
                outer_pin._instance = None
                outer_pin._inner_pin = None
        pin._port = None

    def _clone_rip_and_replace(self, memo):
        """Remove from its current environment and place it into the new cloned environment with references held in the memo dictionary"""
        for p in self._pins:
            p._clone_rip_and_replace(memo)

    def _clone_rip(self):
        """Remove from its current environmnet.

        This will remove all pin pointers and create a floating stand alone instance."""
        for p in self._pins:
            p._clone_rip()

    def _clone(self, memo):
        """Not api safe clone function.

        Clone leaving all references in tact.
        The element can then either be ripped or ripped and replaced.
        """
        assert self not in memo, "the object should not have been copied twice in this pass"
        from spydrnet.ir import Port as PortExtended
        c = PortExtended()
        memo[self] = c
        c._direction = deepcopy(self._direction)
        new_pins = list()
        for p in self._pins:
            new_pins.append(p._clone(memo))
        c._pins = new_pins
        c._definition = None
        c._is_downto = deepcopy(self._is_downto)
        c._is_scalar = deepcopy(self._is_scalar)
        c._lower_index = deepcopy(self._lower_index)
        for p in c._pins:
            p._port = c
        c._data = deepcopy(self._data)
        return c

    def clone(self):
        """Clone the port in an api safe way.

        The following rules will be observed:

         * all the pins will be disconnected from wires
         * the port will be orphaned
         * all pins will belong to the returned port
         * direction, downto, is_scalar, lower_index will all be maintained

        """
        c = self._clone(dict())
        c._clone_rip()
        return c

    def __str__(self):
        """Re-define the print function so it is easier to read"""
        rep = super().__str__()
        rep = rep[:-1] + '; '
        rep += str(self.direction)
        rep += '>'
        return rep