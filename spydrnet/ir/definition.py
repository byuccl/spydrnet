from spydrnet.ir.first_class_element import FirstClassElement
from spydrnet.ir.port import Port
from spydrnet.ir.cable import Cable
from spydrnet.ir.instance import Instance
from spydrnet.ir.outerpin import OuterPin
from spydrnet.ir.views.listview import ListView
from spydrnet.ir.views.setview import SetView
from spydrnet.global_state import global_callback
from spydrnet.global_state.global_callback import _call_create_definition
from copy import deepcopy, copy, error


class Definition(FirstClassElement):
    """
    Represents a definition of a cell, module, entity/architecture, or paralleled structure object.

    Contains a pointer to parent library, ports, cables, and instances.
    """
    __slots__ = ['_library', '_ports', '_cables', '_children', '_references']

    def __init__(self):
        super().__init__()
        self._library = None
        self._ports = list()
        self._cables = list()
        self._children = list()
        self._references = set()
        _call_create_definition(self)

    @property
    def library(self):
        """
        Get the library that contains this definition
        """
        return self._library

    @property
    def ports(self):
        """
        get the ports that are instanced in this definition
        """
        return ListView(self._ports)

    @ports.setter
    def ports(self, value):
        """
        Reorder ports that are instanced in this definition. Use remove_port and add_port to remove and add ports
        respectively

        parameters
        ----------

        value - (List of type Port objects) the reordered list of ports
        """
        target = list(value)
        target_set = set(target)
        assert len(target) == len(target_set) and set(self._ports) == target_set, \
            "Set of values do not match, this function can only reorder values, values must be unique"
        self._ports = target

    @property
    def cables(self):
        """
        get the cables that are instanced in this definition
        """
        return ListView(self._cables)

    @cables.setter
    def cables(self, value):
        """
        Reorder the cables in this definition. Use add_cable and remove_cable to add or remove cables.


        parameters
        ----------

        value - (List of type Cable objects) the reordered list of cables
        """
        target = list(value)
        target_set = set(target)
        assert len(target) == len(target_set) and set(self._cables) == set(target), \
            "Set of values do not match, this function can only reorder values, values must be unique"
        self._cables = target

    @property
    def children(self):
        """
        return a list of all instances instantiated in this definition
        """
        return ListView(self._children)

    @children.setter
    def children(self, value):
        """
        reorder the list of instances instantiated in this definition use add_child and remove_child to add or remove
        instances to or from the definition

        parameters
        ----------

        value - (List of type Instance objects) the reordered list of instances
        """
        target = list(value)
        target_set = set(target)
        assert len(target) == len(target_set) and set(self._children) == target_set, \
            "Set of values do not match, this function can only reorder values, values must be unique"
        self._children = target

    @property
    def references(self):
        """
        get a list of all the instances of this definition
        """
        return SetView(self._references)

    def is_leaf(self):
        """
        Check to see if this definition represents a leaf cell.

        Leaf cells are cells with no children instances or no
        children cables. Blackbox cells are considered leaf cells as well as direct pass through cells with cables only
        """
        if len(self._children) > 0 or len(self._cables) > 0:
            return False
        return True

    def create_port(self):
        """
        create a port, add it to the definition, and return that port
        """
        port = Port()
        self.add_port(port)
        return port

    def add_port(self, port, position=None):
        """
        add a preexisting port to the definition. this port must not be a member of any definition

        parameters
        ----------

        port - (Port) the port to add to the definition

        position - (int, default None) the index in the port list at which to add the port
        """
        assert port.definition is not self, "Port already included in definition"
        assert port.definition is None, "Port already belongs to a different definition"
        global_callback._call_definition_add_port(self, port)
        if position is not None:
            self._ports.insert(position, port)
        else:
            self._ports.append(port)
        port._definition = self
        for reference in self.references:
            for pin in port.pins:
                reference._pins[pin] = OuterPin(reference, pin)

    def remove_port(self, port):
        """
        remove a port from the definition. This port must be a member of the definition in order to be removed

        parameters
        ----------

        port - (Port) the port to be removed
        """
        assert port.definition == self, "Port is not included in definition"
        self._remove_port(port)
        self._ports.remove(port)

    def remove_ports_from(self, ports):
        """
        remove a set of ports from the definition. All these ports must be included in the definition

        parameters
        ----------

        ports - (Set containing Port type objects) the ports to remove from the definition
        """
        if isinstance(ports, set):
            excluded_ports = ports
        else:
            excluded_ports = set(ports)
        assert all(x.definition == self for x in excluded_ports), "Some ports to remove are not included in the " \
                                                                  "definition."
        for port in excluded_ports:
            self._remove_port(port)
        self._ports = list(x for x in self._ports if x not in excluded_ports)

    def _remove_port(self, port):
        """
        internal function to dissociate the port from the definition

        Parameters
        ----------

        port - (Port) the port to remove from the definition
        """
        global_callback._call_definition_remove_port(self, port)
        for reference in self.references:
            for pin in port.pins:
                outer_pin = reference.pins[pin]
                wire = outer_pin.wire
                if wire:
                    wire.disconnect_pin(outer_pin)
                del reference._pins[pin]
                outer_pin._instance = None
                outer_pin._inner_pin = None
        port._definition = None

    def create_child(self):
        """
        create an instance to add to the definition, add it, and return the instance.
        """
        instance = Instance()
        self.add_child(instance)
        return instance

    def add_child(self, instance, position=None):
        """
        Add an existing instance to the definition. This instance must not already be included in a definition

        parameters
        ----------

        instance - (Instance) the instance to add as a child of the definition

        position - (int, default None) the index in the children list at which to add the instance.
        """
        assert instance.parent is not self, "Instance already included in definition"
        assert instance.parent is None, "Instance already belongs to a different definition"
        global_callback._call_definition_add_child(self, instance)
        if position is not None:
            self._children.insert(position, instance)
        else:
            self._children.append(instance)
        instance._parent = self

    def remove_child(self, child):
        """
        remove an instance from the definition. The instance must be a member of the definition already

        parameters
        ----------

        instance - (Instance) the instance to be removed from the definition
        """
        assert child.parent == self, "Instance is not included in definition"
        self._remove_child(child)
        self._children.remove(child)

    def remove_children_from(self, children):
        """
        remove a set of instances from the definition. All instances must be members of the definition

        parameters
        ----------

        children - (Set of Instance type objects) the children to be removed from the definition
        """
        if isinstance(children, set):
            excluded_children = children
        else:
            excluded_children = set(children)
        assert all(x.parent == self for x in excluded_children), "Some children are not parented by the definition"
        included_children = list()
        for child in self._children:
            if child not in excluded_children:
                included_children.append(child)
            else:
                self._remove_child(child)
        self._children = included_children

    def _remove_child(self, child):
        """
        internal function for dissociating a child instance from the definition.
        """
        global_callback._call_definition_remove_child(self, child)
        child._parent = None

    def create_cable(self):
        """
        create a cable, add it to the definition, and return the cable.
        """
        cable = Cable()
        self.add_cable(cable)
        return cable

    def add_cable(self, cable, position=None):
        """
        add a cable to the definition. The cable must not already be a member of another definition.

        parameters
        ----------

        cable - (Cable) the cable to be added

        position - (int, default None) the position in the cable list at which to add the cable
        """
        assert cable.definition is not self, "Cable already included in definition"
        assert cable.definition is None, "Cable already belongs to a different definition"
        global_callback._call_definition_add_cable(self, cable)
        if position is not None:
            self._cables.insert(position, cable)
        else:
            self._cables.append(cable)
        cable._definition = self

    def remove_cable(self, cable):
        """
        remove a cable from the definition. The cable must be a member of the definition.

        parameters
        ----------

        cable - (Cable) the cable to be removed from the definition
        """
        assert cable.definition == self, "Cable is not included in definition"
        self._remove_cable(cable)
        self._cables.remove(cable)

    def remove_cables_from(self, cables):
        """
        remove a set of cables from the definition. The cables must be members of the definition

        parameters
        ----------

        cables - (Set of Cable type objects) the cables to be remove from the definition
        """
        if isinstance(cables, set):
            excluded_cables = cables
        else:
            excluded_cables = set(cables)
        assert all(x.definition == self for x in excluded_cables), "Some cables are not included in the definition"
        included_cables = list()
        for cable in self._cables:
            if cable not in excluded_cables:
                included_cables.append(cable)
            else:
                self._remove_cable(cable)
        self._cables = included_cables

    def _remove_cable(self, cable):
        """
        dissociate the cable from this definition. This function is internal and should not be called.
        """
        global_callback._call_definition_remove_cable(self, cable)
        cable._definition = None

    def _clone_rip_and_replace(self, memo):
        '''if an instance that is a reference of this definition was cloned then update the list of references of the definition.
        for each of the children instances, we should also update the reference to refer to any cloned dictionaries
        inner pins now also need to be updated with new inner pins for each of the definitions that was cloned.'''
        new_references = set()
        for instance in self._references:
            #if the instance was cloned then replace it in our references also update its reference
            if instance in memo:
                new_instance = memo[instance]
                new_references.add(new_instance)
            else:
                new_references.add(instance)
        self._references = new_references
        
        for instance in self._children:
            if instance.reference in memo:
                instance._reference = memo[instance.reference]
                instance._clone_rip_and_replace_in_library(memo)

    def _clone_rip(self):
        '''remove from its current environmnet. add all instances to their appropriate reference lists.'''   
        for instance in self._children:
            instance._reference._references.add(instance)
        self._references = set()


    def _clone(self, memo):
        '''not api safe clone function
        clone leaving all references in tact.
        the element can then either be ripped or ripped and replaced'''
        assert self not in memo, "the object should not have been copied twice in this pass"
        c = Definition()
        memo[self] = c
        c._data = deepcopy(self._data)
        c._library = None
        
        new_ports = list()
        for p in self.ports:
            new_ports.append(p._clone(memo))
        c._ports = new_ports
        
        new_cables = list()
        for ca in self.cables:
            new_cables.append(ca._clone(memo))
        c._cables = new_cables

        new_children = list()
        for ch in self.children:
            new_children.append(ch._clone(memo))
        c._children = new_children
        
        c._references = copy(self._references)
        
        for port in c._ports:
            port._definition = c
            port._clone_rip_and_replace(memo)
        
        for cable in c._cables:
            cable._definition = c
            cable._clone_rip_and_replace(memo)

        for instance in c._children:
            instance._parent = c
            instance._clone_rip_and_replace_in_definition(memo)

        return c

    def clone(self):
        """
        Clone the definition in an api safe way.
        The cloned object will have the following properties
        
         * the definition will be orphaned and will not belong to any library
         * each of the sub elements of the definition will also be cloned and the connection structure between them will be updated.
         * the cloned instances will still point to the reference to which the pointed before. They will also be members of the references list of those definitions.
         
        """
        c = self._clone(dict())
        c._clone_rip()
        return c
