from abc import ABC

from spydrnet.callback.callback_listener import CallbackListener
from spydrnet.plugins.namespace_manager.default_namespace import DefaultNamespace
from spydrnet.plugins.namespace_manager.edif_namespace import EdifNamespace
from spydrnet.ir import Netlist, Library, Definition, Port, Cable, Instance
from spydrnet.global_state.global_service import register_lookup, deregister_lookup
import weakref


def _load_policies():
    NamespaceManager.policies["DEFAULT"] = DefaultNamespace
    NamespaceManager.policies["EDIF"] = EdifNamespace
    NamespaceManager.default = "DEFAULT"


class NamespaceManager(CallbackListener, ABC):
    default = None
    policies = dict()

    def __init__(self):
        super().__init__()
        self.namespaces = weakref.WeakKeyDictionary()
        self.ignore_ns_change = False

    def register_all_listeners(self):
        super().register_all_listeners()
        register_lookup(".NAME", self.lookup)
        register_lookup("EDIF.identifier", self.lookup)

    def deregister_all_listeners(self):
        super().deregister_all_listeners()
        deregister_lookup(".NAME")
        deregister_lookup("EDIF.identifier")

    def lookup(self, parent, element_type, key, value):
        if parent in self.namespaces:
            namespace = self.namespaces[parent]
            return namespace.lookup(element_type, key, value)

    def create_netlist(self, netlist):
        netlist[".NS"] = self.default

    def create_library(self, library):
        library[".NS"] = self.default

    def create_definition(self, definition):
        definition[".NS"] = self.default

    def create_port(self, port):
        port[".NS"] = self.default

    def create_cable(self, cable):
        cable[".NS"] = self.default

    def create_instance(self, instance):
        instance[".NS"] = self.default

    def definition_add_port(self, definition, port):
        self.add(definition, port)

    def definition_remove_port(self, definition, port):
        self.remove(port, parent=definition)

    def definition_add_child(self, definition, child):
        self.add(definition, child)

    def definition_remove_child(self, definition, child):
        self.remove(child, parent=definition)

    def definition_add_cable(self, definition, cable):
        self.add(definition, cable)

    def definition_remove_cable(self, definition, cable):
        self.remove(cable, parent=definition)

    def library_add_definition(self, library, definition):
        self.add(library, definition)

    def library_remove_definition(self, library, definition):
        self.remove(definition, parent=library)

    def netlist_add_library(self, netlist, library):
        self.add(netlist, library)

    def netlist_remove_library(self, netlist, library):
        self.remove(library, parent=netlist)

    def dictionary_set(self, element, key, value):
        if key == ".NS":
            if self.ignore_ns_change is False and (key not in element or element[key] != value):
                if self.get_parent(element) is not None:
                    raise ValueError("Cannot change the namespace of a object already belonging to a parent")
                if value not in self.policies:
                    raise ValueError('The namespace policy specified does not exist. Supported namespaces include: {}'.format(", ".join(self.policies)))
                target_namespace = self.policies[value]
                if self.is_compliant(target_namespace, element) is False:
                    raise ValueError("The current element is not compliant with the target namespace policy.")
                self.apply_namespace(value, target_namespace, element)
        elif key in {".NAME", "EDIF.identifier"}:
            if ".NS" in element:
                target_policy = self.policies[element[".NS"]]
                if target_policy.is_name_valid(key, value) is False:
                    raise ValueError("Target name not valid for the current namespace policy.")

            parent = self.get_parent(element)
            if parent and parent in self.namespaces:
                namespace = self.namespaces[parent]
                if namespace.no_conflict(element, key, value):
                    namespace.update(element, key, value)
                else:
                    raise ValueError("Applying name would result in a naming conflict")

    def dictionary_delete(self, element, key):
        if key == ".NS":
            if self.ignore_ns_change is False:
                if self.get_parent(element) is not None:
                    raise ValueError("Cannot change the namespace of a object already belonging to a parent")
                if ".NS" in element:
                    self.drop_namespace(element)
        elif key in {".NAME", "EDIF.identifier"}:
            parent = self.get_parent(element)
            if parent and parent in self.namespaces:
                namespace = self.namespaces[parent]
                namespace.remove(element, key)

    def dictionary_pop(self, element, key):
        if key == ".NS":
            if self.ignore_ns_change is False:
                if self.get_parent(element) is not None:
                    raise ValueError("Cannot change the namespace of a object already belonging to a parent")
                if ".NS" in element:
                    self.drop_namespace(element)
        elif key in {".NAME", "EDIF.identifier"}:
            self.remove(element, key)

    def add(self, parent, child):
        if parent:
            namespace = None
            if parent in self.namespaces:
                namespace = self.namespaces[parent]
                for key in ["EDIF.identifier", ".NAME"]:
                    if key in child:
                        no_conflict = namespace.no_conflict(child, key, child[key])
                        if no_conflict is False:
                            raise ValueError("Adding this element would result in a naming conflict. " + child[key])
            if ".NS" in parent:
                parent_namespace = parent[".NS"]
                if ".NS" not in child or child[".NS"] != parent_namespace:
                    child[".NS"] = parent_namespace
            elif ".NS" in child:
                del child[".NS"]
            if namespace is not None:
                for key in ["EDIF.identifier", ".NAME"]:
                    if key in child:
                        namespace.update(child, key, child[key])

    def remove(self, element, key=None, parent=None):
        if parent is None:
            parent = self.get_parent(element)
        if parent and parent in self.namespaces:
            namespace = self.namespaces[parent]
            if key is None:
                for key in ["EDIF.identifier", ".NAME"]:
                    if key in element:
                        namespace.remove(element, key)
            else:
                namespace.remove(element, key)

    @staticmethod
    def get_parent(element):
        parent = None
        if isinstance(element, Library):
            parent = element.netlist
        elif isinstance(element, Definition):
            parent = element.library
        elif isinstance(element, (Port, Cable)):
            parent = element.definition
        elif isinstance(element, Instance):
            parent = element.parent
        return parent

    @staticmethod
    def is_compliant(target_namespace, element):
        search_stack = [(element, False)]
        while search_stack:
            element, visited = search_stack.pop()
            if not visited:
                search_stack.append((element, True))
                if isinstance(element, Netlist):
                    search_stack += ((x, False) for x in element.libraries)
                elif isinstance(element, Library):
                    search_stack += ((x, False) for x in element.definitions)
                elif isinstance(element, Definition):
                    search_stack += ((x, True) for x in element.ports)
                    search_stack += ((x, True) for x in element.cables)
                    search_stack += ((x, True) for x in element.children)
            else:
                if target_namespace.is_compliant(element) is False:
                    return False
        return True

    def apply_namespace(self, value, target_namespace, original_element):
        self.ignore_ns_change = True
        search_stack = [original_element]
        while search_stack:
            element = search_stack.pop()
            if ".NS" in element and element in self.namespaces:
                del self.namespaces[element]
            element[".NS"] = value
            new_namespace = None
            if target_namespace.needs_namespace(element):
                new_namespace = target_namespace()
                self.namespaces[element] = new_namespace

            if isinstance(element, Netlist):
                self._update_new_namespace(element.libraries, new_namespace)
                search_stack += element.libraries
            elif isinstance(element, Library):
                self._update_new_namespace(element.definitions, new_namespace)
                search_stack += element.definitions
            elif isinstance(element, Definition):
                self._update_new_namespace(element.ports, new_namespace)
                self._update_new_namespace(element.cables, new_namespace)
                self._update_new_namespace(element.children, new_namespace)
                search_stack += element.ports
                search_stack += element.cables
                search_stack += element.children
        self.ignore_ns_change = False

    def _update_new_namespace(self, elements, namespace):
        if namespace:
            for element in elements:
                if element.name:
                    namespace.update(element, ".NAME", element.name)
                if 'EDIF.identifier' in element:
                    namespace.update(element, "EDIF.identifier", element['EDIF.identifier'])

    def drop_namespace(self, original_element):
        self.ignore_ns_change = True
        search_stack = [original_element]
        while search_stack:
            element = search_stack.pop()
            if element in self.namespaces:
                del self.namespaces[element]
            if element is not original_element and ".NS" in element:
                del element[".NS"]
            if isinstance(element, Netlist):
                search_stack += element.libraries
            elif isinstance(element, Library):
                search_stack += element.definitions
            elif isinstance(element, Definition):
                search_stack += element.ports
                search_stack += element.cables
                search_stack += element.children
        self.ignore_ns_change = False


_load_policies()
