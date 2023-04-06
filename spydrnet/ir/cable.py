from spydrnet.ir import Bundle
from spydrnet.ir import Wire
from spydrnet.ir.views.listview import ListView
from spydrnet.global_state import global_callback
from spydrnet.global_state.global_callback import _call_create_cable
from copy import deepcopy, copy, error


class Cable(Bundle):
    """Representation of several wires in a collection.

    Much like ports, cables extend the bundle class, giving them indexing ability. They represent several wires in a collection or bus that are generally related.
    This could be thought of much like vector types in VHDL ie std_logic_vector (7 downto 0)"""
    __slots__ = ['_wires']

    def __init__(self, name=None, properties=None, is_downto=None, is_scalar=None, lower_index=None):
        """Create a cable with no wires and default values for a bundle.

        parameters
        ----------

        name - (str) the name of this instance
        properties - (dict) the dictionary which holds the properties
        id_downto - (bool) set the downto status. Downto is False if the right index is higher than the left one, True otherwise
        is_scalar - (bool) set the scalar status. Return True if the item is a scalar False otherwise.
        lower_index - (int) get the value of the lower index of the array.

        """
        super().__init__()
        self._wires = list()
        _call_create_cable(self)
        if name != None:
            self.name = name

        if is_downto is not None:
            self.is_downto = is_downto

        if is_scalar is not None:
            self.is_scalar = is_scalar

        if lower_index is not None:
            self.lower_index = lower_index

        if properties != None:
            assert isinstance(
                properties, dict), "properties must be a dictionary"
            for key in properties:
                self[key] = properties[key]

    def _items(self):
        """Overrides the bundle _items function to return wires"""
        return self._wires

    @property
    def wires(self):
        """Gets a list of wires that are in this cable"""
        return ListView(self._wires)

    @wires.setter
    def wires(self, value):
        """Sets the wires to a reordered list of wires.

        This function is to be used for reordering of wires
        """
        value_list = list(value)
        value_set = set(value_list)
        # try:
        assert len(value_list) == len(value_set) and set(self._wires) == value_set, \
            "Set of values does not match, assigment can only be used for reordering, values must be unique"
        # except:
        #     import pdb; pdb.set_trace()
        self._wires = value_list

    def create_wires(self, wire_count):
        """Creates wire_count wires for this cable and adds them to it.

        parameters
        ----------

        wire_count - (int) the number of wires to be added to the cable.
        """
        for _ in range(wire_count):
            self.create_wire()
        return self.wires[-wire_count:]

    def create_wire(self):
        """Creates a wire and adds it to the cable. Returns the wire that was created"""
        wire = Wire()
        self.add_wire(wire)
        return wire

    def add_wire(self, wire, position=None):
        """Adds a wire to the cable at the given position. This wire must not belong to a cable already

        parameters
        ----------

        wire - (Wire) the wire to be added to the cable. This wire must not belong to any other cable.

        position - (int, default None) the index in the wires list at which to add the wire.
        """
        assert wire.cable is not self, "Wire already belongs to this cable"
        assert wire.cable is None, "Wire already belongs to a different cable"
        global_callback._call_cable_add_wire(self, wire)
        if position is not None:
            self._wires.insert(position, wire)
        else:
            self._wires.append(wire)
        wire._cable = self

    def remove_wire(self, wire):
        """removes the given wire from the cable and return it. The wire must belong to this cable

        parameters
        ----------

        wire - (Wire) the wire to be removed from the cable.
        """
        assert wire.cable == self, "Wire does not belong to this cable"
        self._remove_wire(wire)
        self._wires.remove(wire)

    def remove_wires_from(self, wires):
        """Remove all wires given from the cable. Each must be a member of this cable.

        parameters
        ----------

        wires - (List of Wire objects) wires to be removed from the cable.
        """
        if isinstance(wires, set):
            excluded_wires = wires
        else:
            excluded_wires = set(wires)
        assert all(
            x.cable == self for x in excluded_wires), "Some wires do not belong to this cable"
        for wire in excluded_wires:
            self._remove_wire(wire)
        self._wires = list(x for x in self._wires if x not in excluded_wires)

    def _remove_wire(self, wire):
        """Internal wire removal call. dissociates the wire from the cable"""
        global_callback._call_cable_remove_wire(self, wire)
        wire._cable = None

    def _clone_rip_and_replace(self, memo):
        """Remove from its current environment and place it into the new cloned environment with references held in the memo dictionary"""
        for w in self._wires:
            w._clone_rip_and_replace(memo)

    def _clone_rip(self):
        """Remove from its current environmnet. This will remove all pin pointers and create a floating stand alone instance."""
        for w in self._wires:
            w._clone_rip()
            w._cable = self

    def _clone(self, memo):
        """Not api safe clone function
        clone leaving all references in tact.
        the element can then either be ripped or ripped and replaced"""
        assert self not in memo, "the object should not have been copied twice in this pass"
        from spydrnet.ir import Cable as CableExtended
        c = CableExtended()
        memo[self] = c
        new_wires = list()
        for w in self._wires:
            new_wires.append(w._clone(memo))
        c._wires = new_wires
        for w in c._wires:
            w._cable = c
        c._definition = None
        c._is_downto = deepcopy(self._is_downto)
        c._is_scalar = deepcopy(self._is_scalar)
        c._lower_index = deepcopy(self._lower_index)
        c._data = deepcopy(self._data)
        return c

    def clone(self):
        """
        Clone the Cable and all of its wires in an api safe way
        the following will be true of the returned cable

         * The cable will be orphaned from any definitions
         * the wires in the cable will not be connected to any pins
         * is_downto, is_scalar, lower_index will be maintained
         * the wires in the cable will all have the cable set as the parent
        """
        c = self._clone(dict())
        c._clone_rip()
        return c

    def __str__(self):
        """Re-define the print function so it is easier to read"""
        rep = str(type(self))
        rep = rep[:-1] + '; '
        if self.is_downto is not None and self.is_downto is True:
            rep += 'is_downto: True; '
        else:
            rep += 'is_downto: False; '
        if self.is_scalar is True:
            rep += 'is_scalar: True; '
        else:
            rep += 'is_scalar: False; '
        rep += 'lower index: ' + str(self.lower_index)
        rep += '>'
        return rep
