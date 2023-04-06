from spydrnet.ir import FirstClassElement
from spydrnet.ir import OuterPin
from spydrnet.ir.views.outerpinsview import OuterPinsView
from spydrnet.global_state import global_callback
from spydrnet.global_state.global_callback import _call_create_instance
from copy import deepcopy
from collections import OrderedDict


class Instance(FirstClassElement):
    """Netlist instance of a netlist definition.

    Instances are literally instances of definitions and they reside inside other definitions.
    Function names have been set to prevent potential confusion that could arise because instances have both a parent definition and definitions which they reference.


    :ivar parent: the parent of the object. Parent is the definition that instances another definition.
    :ivar child: the instance itself is the child of the parent.
    :ivar reference: the item of the object. Reference is the definition of the instance.

    For example, when writing definition 1, we instance definition 2. Definition 1 is the parent, the instance is the child, and definition 2 is the instance's reference.

    """
    __slots__ = ['_parent', '_reference', '_pins','_is_top_instance']

    def __init__(self, name=None, properties=None):
        """Creates an empty object of type instance.

        parameters
        ----------

        name - (str) the name of this instance
        properties - (dict) the dictionary which holds the properties
        """
        super().__init__()
        self._parent = None
        self._reference = None
        self._pins = OrderedDict()
        self._is_top_instance = False
        _call_create_instance(self)
        if name != None:
            self.name = name
        if properties != None:
            assert isinstance(
                properties, dict), "properties must be a dictionary"
            for key in properties:
                self[key] = properties[key]

    @property
    def parent(self):
        """Get the definition that contains this instance"""
        return self._parent

    def test(self):

        return True

    @property
    def reference(self):
        """Get the definition that this instance is instantiating"""
        return self._reference

    @reference.setter
    def reference(self, value):
        """Change the definition that represents this instance.
        Port positioning and size must be taken into account when a new definition is being used.
        if they are different the connections cannot be done automatically with this function.

        parameters
        ----------

        value - (Definition) the definition that this instance should be an instance of"""
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
                        self._pins[pin] = OuterPin(self, pin)
            value._references.add(self)
        self._reference = value

    @reference.deleter
    def reference(self):
        self.reference = None

    def get_ports(self, *args, **kwargs):
        from spydrnet.util.get_ports import get_ports
        return get_ports(self, *args, **kwargs)

    @property
    def pins(self):
        """Get the pins on this instance.
        Can do instance.pins[<inner_pin>] to get the inner pin's associated outer pins."""
        return OuterPinsView(self._pins)

    def _clone_rip_and_replace_in_definition(self, memo):
        """Slide the outerpins references into a new context.

        The instance still references something outside of what has been cloned.
        """
        for op in self._pins.values():
            op._clone_rip_and_replace(memo)

    def _clone_rip_and_replace_in_library(self, memo):
        """Move the instance into a new library/netlist.

        This will replace the reference if affected and replace the inner pins that will be affected as well.
        The instance should not be in the references list of the reference definition
        """
        new_pins = OrderedDict()
        for ip, op in self._pins.items():
            new_pins[memo[ip]] = op
        self._pins = new_pins

    def _clone_rip(self):
        """Remove the instance from its current environmnet.

        This will remove the instance from any wires but it will add it in to the references set on the definition which it instantiates.
        """
        for op in self._pins.values():
            op._wire = None
        self._reference._references.add(self)

    def _clone(self, memo):
        """Not api safe clone function
        clone the instance leaving all references in tact.
        The instance can then either be ripped or ripped and replaced
        """
        assert self not in memo, "the object should not have been copied twice in this pass"
        from spydrnet.ir import Instance as InstanceExtended
        c = InstanceExtended()
        memo[self] = c
        c._parent = None
        for inner_pin, outer_pin in self._pins.items():
            new_outer_pin = outer_pin._clone(memo)
            new_outer_pin._instance = c
            c._pins[inner_pin] = new_outer_pin
        c._reference = self._reference
        c._data = deepcopy(self._data)
        return c

    def clone(self):
        """

        Clone the instance in an api safe way.
        This call will return a cloned instance that has the following properties:

         * the pins in the instance will all be disconnected from wires but they will maintain their references to inner pins
         * the instance references is the same as the cloned object
         * the reference's references list contains this instance
         * the instance is orphaned (no longer a child of the definition to which the cloned definition belonged

        """
        c = self._clone(OrderedDict())
        c._clone_rip()
        return c

    def is_leaf(self):
        """Check to see if the definition that this instance contains represents a leaf cell.

        Leaf cells are cells with no children instances or no children cables.
        Blackbox cells are considered leaf cells as well as direct pass through cells with cables only
        """
        if self._reference is None:
            return False
        elif len(self._reference._children) > 0 or len(self._reference._cables) > 0:
            return False
        return True

    def is_unique(self):
        """
        Check to see if the instance is unique
        """
        if len(self.reference.references) == 1 or self.reference.is_leaf():
            return True
        else:
            return False

    def __str__(self):
        """Re-define the print function so it is easier to read"""
        rep = super().__str__()
        rep = rep[:-1] + '; '
        if self.parent is None:
            rep += 'parent definition undefined'
        elif self.parent.name is None:
            rep += 'parent definition.name undefined'
        else:
            rep += 'parent definition.name \'' + self.parent.name + '\''

        rep += '; '

        if self.reference is None:
            rep += 'reference definition undefined'
        elif self.reference.name is None:
            rep += 'reference definition.name undefined'
        else:
            rep += 'reference definition.name \'' + self.reference.name + '\''
        rep += '>'
        return rep

    @property
    def is_top_instance(self):
        return self._is_top_instance

    @is_top_instance.setter
    def is_top_instance(self,value):
        self._is_top_instance = value