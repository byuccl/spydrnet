import spydrnet.ir as ir


class HRef:
    @staticmethod
    def from_item(item, parent=None, netlist=None):
        if parent is None and netlist is None:
            reference = item.reference
            if reference:
                library = reference.library
                if library:
                    netlist = library.netlist
        top_href = HRef(item, parent, netlist)
        HRef._populate_base_href(top_href)
        return top_href

    @staticmethod
    def from_reference_change(parent_href, reference):
        for href in HRef._gen_base_hrefs_from_parent_href_and_definition(parent_href, reference):
            HRef._populate_base_href(href)
            yield href

    @staticmethod
    def _populate_base_href(top_href):
        search_stack = [top_href]
        while search_stack:
            href = search_stack.pop()
            parent = href.parent
            item = href.item
            if parent:
                parent.children[item] = href
            if isinstance(item, ir.Instance):
                reference = item.reference
                search_stack += HRef._gen_base_hrefs_from_parent_href_and_definition(href, reference)
            elif isinstance(item, ir.Port):
                for pin in item.pins:
                    search_stack.append(HRef(pin, href))
            elif isinstance(item, ir.Cable):
                for wire in item.wires:
                    search_stack.append(HRef(wire, href))

    @staticmethod
    def _gen_base_hrefs_from_parent_href_and_definition(parent_href, definition):
        if definition:
            for port in definition.ports:
                yield HRef(port, parent_href)
            for cable in definition.cables:
                yield HRef(cable, parent_href)
            for instance in definition.children:
                yield HRef(instance, parent_href)

    __slots__ = ['_hashcode', 'netlist', 'parent', 'item', 'children']

    def __init__(self, item, parent=None, netlist=None):
        self._hashcode = ((0 if parent is None else hash(parent))*31 + hash(item) & 0xFFFF_FFFF_FFFF_FFFF)
        self.parent = parent
        if parent is not None:
            self.netlist = parent.netlist
        else:
            self.netlist = netlist
        self.item = item
        self.children = dict()

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
        elif isinstance(item, ir.Pin):
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
        hname = "{}{}".format(hseperator.join(reversed(names)), bus_index)
        return hname

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