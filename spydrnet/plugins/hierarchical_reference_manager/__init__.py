from abc import ABC

import spydrnet.callback.callback_listener as callback_listener
import spydrnet.ir as ir
import weakref

import spydrnet.plugins.hierarchical_reference_manager.hierarchical_reference as hr


class HRefMgr(callback_listener.CallbackListener, ABC):
    default_hierarchical_seperator = '/'
    hierarchical_seperator = weakref.WeakKeyDictionary()

    def __init__(self):
        super().__init__()
        self.htrees = weakref.WeakKeyDictionary()
        self.defmap = weakref.WeakKeyDictionary()
        self.instance_without_reference_map = weakref.WeakKeyDictionary()
        self.namemaps = weakref.WeakKeyDictionary()

    def cable_add_wire(self, cable, wire):
        definition = cable.definition
        if definition and definition in self.defmap:
            for href in self.defmap[definition]:
                cable_href = href.children[cable]
                wire_href = hr.HRef.from_item(wire, cable_href)
                cable_href.children[wire] = wire_href

    def cable_remove_wire(self, cable, wire):
        definition = cable.definition
        if definition and definition in self.defmap:
            for href in self.defmap[definition]:
                cable_href = href.children[cable]
                del cable_href.children[wire]

    def definition_add_port(self, definition, port):
        if definition in self.defmap:
            for href in self.defmap[definition]:
                port_href = hr.HRef.from_item(port, href)
                self._update_defmap_and_namemap(port_href)
                href.children[port] = port_href

    def definition_remove_port(self, definition, port):
        if definition in self.defmap:
            for href in self.defmap[definition]:
                port_href = href.children[port]
                self._update_defmap_and_namemap(port_href)
                del href.children[port]

    def definition_add_child(self, definition, child):
        if definition in self.defmap:
            for href in self.defmap[definition]:
                inst_href = hr.HRef.from_item(child, href)
                self._update_defmap_and_namemap(inst_href)
                href.children[child] = inst_href

    def definition_remove_child(self, definition, child):
        if definition in self.defmap:
            for href in self.defmap[definition]:
                inst_href = href.children[child]
                self._remove_from_defmap_and_namemap(inst_href)
                del href.children[child]

    def definition_add_cable(self, definition, cable):
        if definition in self.defmap:
            for href in self.defmap[definition]:
                cable_href = hr.HRef.from_item(cable, href)
                self._update_defmap_and_namemap(cable_href)
                href.children[cable] = cable_href

    def definition_remove_cable(self, definition, cable):
        if definition in self.defmap:
            for href in self.defmap[definition]:
                cable_href = href.children[cable]
                self._update_defmap_and_namemap(cable_href)
                del href.children[cable]

    def port_add_pin(self, port, pin):
        definition = port.definition
        if definition and definition in self.defmap:
            for href in self.defmap[definition]:
                cable_href = href.children[port]
                wire_href = hr.HRef.from_item(pin, cable_href)
                cable_href.children[pin] = wire_href

    def port_remove_pin(self, port, pin):
        definition = port.definition
        if definition and definition in self.defmap:
            for href in self.defmap[definition]:
                cable_href = href.children[port]
                del cable_href.children[pin]

    def dictionary_set(self, element, key, value):
        if key == ".NAME" and (".NAME" not in element or element[".NAME"] != value):
            self._rename(element, value)

    def dictionary_delete(self, element, key):
        if key == ".NAME" and element[".NAME"] != '':
            self._rename(element, '')

    def dictionary_pop(self, element, key):
        if key == ".NAME" and element[".NAME"] != '':
            self._rename(element, '')

    def _rename(self, element, name):
        if isinstance(element, ir.Cable):
            definition = element.definition
            if definition in self.defmap:
                for href in self.defmap[definition]:
                    cable_href = href.children[element]
                    self._remove_from_defmap_and_namemap(cable_href)
                    self._update_defmap_and_namemap(cable_href, new_name='')
        elif isinstance(element, ir.Port):
            definition = element.definition
            if definition in self.defmap:
                for href in self.defmap[definition]:
                    port_href = href.children[element]
                    self._remove_from_defmap_and_namemap(port_href)
                    self._update_defmap_and_namemap(port_href, new_name='')
        elif isinstance(element, ir.Instance):
            definition = element.reference
            if definition:
                if definition in self.defmap:
                    for href in self.defmap[definition]:
                        inst_href = href.children[element]
                        self._remove_from_defmap_and_namemap(inst_href)
                        self._update_defmap_and_namemap(inst_href, new_name='')
            elif element in self.instance_without_reference_map:
                inst_href = self.instance_without_reference_map[element]
                self._remove_from_defmap_and_namemap(inst_href)
                self._update_defmap_and_namemap(inst_href, new_name='')

    def instance_reference(self, instance, reference):
        current_reference = instance.reference
        if current_reference:
            if current_reference in self.defmap:
                hrefs = list(x for x in self.defmap[current_reference] if x.item == instance)
                for href in hrefs:
                    self._remove_from_defmap_and_namemap(href)
                    if reference:
                        for child in hr.HRef.from_reference_change(href, reference):
                            href.children[child.item] = child
                    self._update_defmap_and_namemap(href, reference)
        elif reference and instance in self.instance_without_reference_map:
            href = self.instance_without_reference_map[instance]
            if href:
                self._remove_from_defmap_and_namemap(href)
                for child in hr.HRef.from_reference_change(href, reference):
                    href.children[child.item] = child
                self._update_defmap_and_namemap(href, reference)

    def netlist_top_instance(self, netlist, instance):
        if netlist in self.htrees and self.htrees[netlist].item != instance:
            self._remove_from_defmap_and_namemap(self.htrees[netlist])
            del self.htrees[netlist]
        if (netlist not in self.htrees or self.htrees[netlist].item != instance) and instance is not None:
            self.hierarchical_seperator[netlist] = self.default_hierarchical_seperator
            top_ref = hr.HRef.from_item(instance, netlist=netlist)
            self.htrees[netlist] = top_ref
            self._update_defmap_and_namemap(top_ref)

    def _update_defmap_and_namemap(self, href, new_reference=None, new_name=None):
        netlist = href.netlist
        hseperator = self.hierarchical_seperator[netlist]
        if netlist not in self.namemaps:
            self.namemaps[netlist] = dict()
        namemap = self.namemaps[netlist]
        parent = href.parent
        name_stack = [] if parent is None else [parent.name]
        search_stack = [(href, False)]
        while search_stack:
            href, name_on_stack = search_stack.pop()
            if name_on_stack:
                name_stack.pop()
                continue
            item = href.item
            if isinstance(item, ir.Instance):
                if new_reference is not None:
                    reference = new_reference
                    new_reference = None
                else:
                    reference = item.reference
                if reference:
                    if reference not in self.defmap:
                        self.defmap[reference] = set()
                    self.defmap[reference].add(href)
                else:
                    self.instance_without_reference_map[item] = href
            if isinstance(item, (ir.Port, ir.Cable, ir.Instance)):
                if new_name is not None:
                    name = new_name
                    new_name = None
                elif item.name is not None:
                    name = item.name
                else:
                    name = ""
                name_stack.append(name)
                search_stack.append((href, True))

                element_type = type(item)
                if element_type not in namemap:
                    namemap[element_type] = dict()
                element_namemap = namemap[element_type]
                hierarchical_name = hseperator.join(name_stack)
                if hierarchical_name in element_namemap:
                    value = element_namemap[hierarchical_name]
                    if isinstance(value, set) is False:
                        value = {value}
                        element_namemap[hierarchical_name] = value
                    if href in value:
                        assert False
                    value.add(href)
                else:
                    element_namemap[hierarchical_name] = href
            search_stack += ((x, False) for x in href.children.values())

    def _remove_from_defmap_and_namemap(self, href):
        netlist = href.netlist
        hseperator = self.hierarchical_seperator[netlist]
        namemap = self.namemaps[netlist]
        parent = href.parent
        name_stack = [] if parent is None else [parent.name]
        search_stack = [(href, False)]
        while search_stack:
            href, name_on_stack = search_stack.pop()
            item = href.item
            if name_on_stack:
                element_type = type(item)
                element_namemap = namemap[element_type]
                hierarchical_name = hseperator.join(name_stack)
                value = element_namemap[hierarchical_name]
                if isinstance(value, set):
                    value.remove(href)
                    if len(value) == 1:
                        element_namemap[hierarchical_name] = next(iter(value))
                else:
                    del element_namemap[hierarchical_name]
                if len(element_namemap) == 0:
                    del namemap[element_type]

                name_stack.pop()
                continue

            if isinstance(item, ir.Instance):
                reference = item.reference
                if reference:
                    if reference in self.defmap:
                        defmap = self.defmap[reference]
                        defmap.remove(href)
                        if len(defmap) == 0:
                            del self.defmap[reference]
                else:
                    del self.instance_without_reference_map[item]
            if isinstance(item, (ir.Port, ir.Cable, ir.Instance)):
                name = item.name
                name_stack.append("" if name is None else name)
                search_stack.append((href, True))
            search_stack += ((x, False) for x in href.children.values())

        if len(namemap) == 0:
            del self.namemaps[netlist]
