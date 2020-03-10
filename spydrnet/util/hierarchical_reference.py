import spydrnet.ir as ir
import weakref

flyweight = weakref.WeakKeyDictionary()


class HRef:
    @staticmethod
    def from_parent_and_item(parent, item):
        href = HRef(item, parent)
        if href in flyweight:
            return flyweight[href]()
        else:
            flyweight[href] = weakref.ref(href)
            return href

    @staticmethod
    def from_sequence(sequence):
        parent = None
        for item in sequence:
            href = HRef.from_parent_and_item(parent, item)
            parent = href
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
