from spydrnet.ir.netlist import Netlist
import spydrnet.ir as ir
import weakref

flyweight = weakref.WeakKeyDictionary()


class HRef(ir.Element):
    @staticmethod
    def get_all_hrefs_of_item(item):
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
        if isinstance(netlist, Netlist) is False:
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
        parent = None
        for item in sequence:
            href = HRef.from_parent_and_item(parent, item)
            parent = href
        return href

    @staticmethod
    def from_parent_and_item(parent, item):
        href = HRef(item, parent)
        if href in flyweight:
            return flyweight[href]()
        else:
            flyweight[href] = weakref.ref(href)
            return href

    __slots__ = ['_hashcode', 'parent', 'item', '__weakref__']

    def __init__(self, item, parent=None):
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
        :return:
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
                    search_stack += (x for x in parent.references if x != href.parent.item)
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
