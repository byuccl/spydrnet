import spydrnet.ir as ir
import weakref

from spydrnet.shortcuts.getter import GetterShortcuts

flyweight = weakref.WeakKeyDictionary()


class HRef(GetterShortcuts):
    """A hierarchical reference to a specific element in a netlist.

    Definitions can be instanced more than once (i.e., multiple instances can reference the same definition).
    When a definition is instanced more than once, it causes the contents of the definition to be shared. Therefore, any
    changes to a multi-instanced definition will be reflected in all instances of that definition. Similarly, any
    references to the contents of a multi-instanced definition refer to the contents of all of the instances and not to
    the contents of a specific instance. This sharing creates challenges for analyzing and transforming the netlist.

    Hierarchical references refer to a netlist element by hierarchical sequence. A hierarchical sequence begins with the
    the top-instance of netlist (see Netlist.top_instance). The sequence continues with children instances (parent to
    child) until the instance of interest is reached. The instance of interest is the final instance in the sequence.
    When the referenced element is an instance, the sequence terminates. When the referenced element is a port, pin,
    cable, or wire, the sequence continues with those elements until the desired element is specified (e.g., port;
    port, pin; cable; or cable, wire. In this way, hierarhical elements are uniquely referenced even though the contents
    of a definition may be shared.

    **Hierarchical Sequence Examples:**

    Here are some examples of hierarchical sequences:

    * Top Instance:
        * ``[top_instance]``
    * Top Instance Port
        * ``[top_instance, port]``
    * Top Instance Pin
        * ``[top_instance, port, pin]``
    * Shared Sub-Instance Cable)
        * ``[top_instance, sub_instance_A, sub_instance_C, cable]``
        * ``[top_instance, sub_instance_B, sub_instance_C, cable]``
        * ``sub_instance_A`` and ``sub_instance_B`` are instances (or children) with the definition referenced by
          ``top_instance``.
        * ``sub_instance_A`` and ``sub_instance_B`` reference the same definition, which contains ``sub_instance_C``.
        * Even though ``cable`` is the same element in both sequences, each sequence uniquely references the cable
          inside ``sub_instance_A`` and ``sub_instance_B`` respectively.

    **Netlist Analysis and Transformation:**

    Hierarchical references provide unique handles on hierarchical elements. A unique handle allows for such elements to
    be considered individually even though two hierarchical may point to some of the same elements. This makes it
    possible, for example, to consider pin connectivity across hierarchy even though the actual pins may be the same.

    In some netlist tranformations, it may be desirable to modify the contents of a specific instance without modifying
    the contents of another instance that refers to the same definition. Hierarchical references make it possible to
    refer to an instance that should be changed. Once the definition is made unique (see spydrnet.uniquify), then any
    alterations will only affect the originally specified instance. Hierarchical instances also allow for uniqueness
    checking (see HRef.is_unique).

    **Hierarchical Reference Representation:**

    HRefs represent hierarchy as nodes in a hierarchical tree. The root node is an HRef to the top_instance of a netlist
    with no parent node. Each HRef contains a pointer to its parent HRef (``None`` in the case of the root HRef), a
    pointer to the element in the netlist that it references, and a hashcode generated from each referenced object.

    Storing the hashcode with the object saves on re-computation and allows for quick operations in containers that
    require Hashable objects. If the hashcode were not stored with the object, it would have to be recalculated for
    each hash-dependent operation, which could consume a large amount of computational resources depending on the
    hierarchical depth of the node. Parent and item pointers are immutable. The hashcode of a referenced item is also
    immutable. Therefore, the hashcode of a HRef should not change during its existence (even if a netlist
    transformation renders it invalid).

    **Use of a Flyweight Pattern:**

    Due the the nature of hierarchical references, parent nodes can be referenced more than once. Rather than having
    multiple hierarchical nodes in memory that point to the same hierarchical parent, a flyweight can be used to save
    on memory. A flyweight pattern is used here to share hierarchical parent nodes. See `Flyweight pattern
    <https://en.wikipedia.org/wiki/Flyweight_pattern>`_.

    **Lack of Parent to Child Pointers:**

    A parent to child pointer requires a lookup diction from each child item to each child hierarchical node. This
    approach could be taken, but it recreates much of the same information that is available in the original netlist. It
    was therefore decided to leverage the flyweight pattern rather than explicitly manage all of the necessary
    child-item to child-node relationships.

    .. attribute:: item: the item of the object
    .. attribute:: parent: the parent of the object
    """
    @staticmethod
    def get_all_hrefs_of_item(item):
        """Get all the href of the itsm

        parameters
        ----------

        item - The item to get the href from.

        """
        if isinstance(item, ir.Instance):
            for href in HRef.get_all_hrefs_of_instances(item):
                yield href
        elif isinstance(item, ir.Definition):
            for href in HRef.get_all_hrefs_of_instances(item.references):
                yield href
        elif isinstance(item, ir.Port):
            definition = item.definition
            if definition:
                for href in HRef.get_all_hrefs_of_instances(definition.references):
                    yield HRef.from_parent_and_item(href, item)
        elif isinstance(item, ir.InnerPin):
            port = item.port
            if port:
                definition = port.definition
                if definition:
                    for href in HRef.get_all_hrefs_of_instances(definition.references):
                        href_port = HRef.from_parent_and_item(href, port)
                        yield HRef.from_parent_and_item(href_port, item)
        elif isinstance(item, ir.OuterPin):
            instance = item.instance
            inner_pin = item.inner_pin
            if instance and inner_pin:
                port = inner_pin.port
                if port:
                    for href in HRef.get_all_hrefs_of_instances(instance):
                        href_port = HRef.from_parent_and_item(href, port)
                        yield HRef.from_parent_and_item(href_port, inner_pin)
        elif isinstance(item, ir.Cable):
            definition = item.definition
            if definition:
                for href in HRef.get_all_hrefs_of_instances(definition.references):
                    yield HRef.from_parent_and_item(href, item)
        elif isinstance(item, ir.Wire):
            cable = item.cable
            if cable:
                definition = cable.definition
                if definition:
                    for href in HRef.get_all_hrefs_of_instances(definition.references):
                        href_cable = HRef.from_parent_and_item(href, cable)
                        yield HRef.from_parent_and_item(href_cable, item)

    @staticmethod
    def get_all_hrefs_of_instances(instances, netlist=None):
        """
        Assuming all instances are vaild (meaning their reference belongs in a proper library inside a netlist).
        :param instances:
        :param netlist:
        :return:
        """
        if isinstance(instances, ir.Instance):
            instances = {instances}
        else:
            instances = set(x for x in instances if isinstance(x, ir.Instance))

        if netlist is None:
            instance = next(iter(instances), None)
            if instance:
                reference = instance.reference
                if reference:
                    library = reference.library
                    if library:
                        netlist = library.netlist
        if isinstance(netlist, ir.Netlist) is False:
            return

        top_instance = netlist.top_instance

        bound = set()
        search_stack = list(instances)
        while search_stack:
            instance = search_stack.pop()
            parent_def = instance.parent
            if parent_def:
                for parent_inst in parent_def.references:
                    if parent_inst not in bound:
                        bound.add(parent_inst)
                        search_stack.append(parent_inst)

        href = HRef.from_parent_and_item(None, top_instance)
        search_stack = [href]
        while search_stack:
            href = search_stack.pop()
            item = href.item
            if item in instances:
                yield href
            reference = item.reference
            if reference:
                for child in reference.children:
                    if child in bound:
                        href_child = HRef.from_parent_and_item(href, child)
                        search_stack.append(href_child)
                    elif child in instances:
                        href_child = HRef.from_parent_and_item(href, child)
                        yield href_child

    @staticmethod
    def from_sequence(sequence):
        """Return the href of the sequence

        parameters
        ----------

        sequence - The sequence to get the href from

        """
        parent = None
        for item in sequence:
            href = HRef.from_parent_and_item(parent, item)
            parent = href
        return href

    @staticmethod
    def from_parent_and_item(parent, item):
        """Return the href with given parent and item

        parameters
        ----------

        parent - the parent obejct of this href
        item - the item that the href is reference to

        """
        href = HRef(item, parent)
        if href in flyweight:
            return flyweight[href]()
        else:
            flyweight[href] = weakref.ref(href)
            return href

    __slots__ = ['_hashcode', 'parent', 'item', '__weakref__']

    def __init__(self, item, parent=None):
        """Initialize the href

        parameters
        ----------

        item - the item that the href is reference to
        parent - the parent obejct of this href

        """
        self._hashcode = hash(hash(parent)*31 + hash(item))
        self.parent = parent
        self.item = item

    def __hash__(self):
        return self._hashcode

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, HRef) is False:
            return False
        this = self
        that = other
        while this is not None and that is not None:
            if this.item == that.item:
                this = this.parent
                that = that.parent
            else:
                return False
        if this is None and that is None:
            return True
        return False

    def __repr__(self):
        return "<{} {} '{}' at 0x{:016X}>".format(self.__class__.__name__, self.item.__class__.__name__, self.name,
                                                  id(self))

    def __str__(self):
        name = self.name
        return name

    @property
    def is_unique(self):
        """
        A hierarchical reference must be valid to be unique. If it is not valid, it may not be unique.
        : return:
        """
        if self.is_valid is False:
            return False
        href = self
        search_stack = list()
        instances = set()
        while href:
            item = href.item
            if isinstance(item, ir.Instance):
                instances.add(item)
                parent = item.parent
                if parent and len(parent.references) > 1 and href.parent:
                    search_stack += (x for x in parent.references if x !=
                                     href.parent.item)
            href = href.parent
        while search_stack:
            instance = search_stack.pop()
            reference = instance.parent
            if reference:
                for parent in reference.references:
                    if parent in instances:
                        return False
                    else:
                        search_stack.append(parent)
        return True

    @property
    def is_valid(self):
        """Checks if the href is valid

        """
        href = self
        while href:
            hparent = href.parent  # href
            item = href.item
            if isinstance(item, ir.Instance):
                if not hparent:
                    reference = item.reference
                    if not reference:
                        return False
                    library = reference.library
                    if not library:
                        return False
                    netlist = library.netlist
                    if not netlist:
                        return False
                    top_instance = netlist.top_instance
                    if not top_instance:
                        return False
                    if top_instance == item:
                        return True
                    return False
                else:
                    parent = item.parent  # definition
                    if not parent:
                        return False
                    hparent_item = hparent.item  # instance
                    if hparent_item not in parent.references:
                        return False
                    href = hparent
            elif isinstance(item, (ir.Cable, ir.Port)):
                if not hparent:
                    return False
                definition = item.definition
                if not definition:
                    return False
                if hparent.item not in definition.references:
                    return False
                href = hparent
            elif isinstance(item, ir.Wire):
                if not hparent:
                    return False
                cable = item.cable
                if not cable:
                    return False
                if hparent.item != cable:
                    return False
                href = hparent
            elif isinstance(item, ir.InnerPin):
                if not hparent:
                    return False
                port = item.port
                if not port:
                    return False
                if hparent.item != port:
                    return False
                href = hparent
            else:
                href = None
        return False

    @property
    def name(self):
        """Stores the name of the href

        """
        hseperator = '/'
        names = list()
        index = None
        item = self.item
        if isinstance(item, ir.Wire):
            cable = item.cable
            if cable.is_array:
                index = cable.lower_index + cable.wires.index(item)
            href = self.parent
        elif isinstance(item, ir.InnerPin):
            port = item.port
            if port.is_array:
                index = port.lower_index + port.pins.index(item)
            href = self.parent
        else:
            href = self
        while href is not None:
            item = href.item
            item_name = item.get(".NAME", "")
            names.append(item_name)
            href = href.parent
        bus_index = "" if index is None else "[{}]".format(index)
        hname = "{}{}".format(hseperator.join(reversed(names[:-1])), bus_index)
        return hname
