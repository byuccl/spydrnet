#COPYRIGHT BYUCCL 2020

import weakref
from spydrnet.callback.callback_listener import CallbackListener
from spydrnet.ir import Library, Definition, Instance, Port, Cable


class EdifNamespaceManager(CallbackListener):
    '''
    this class is a plugin using the callback listener to manage a database for name management.
    
    This class implements and registers all listeners and presents to the user
    the ability to do quick lookups based on name.
    '''

    def __init__(self):
        super().__init__()
        # dictionary for each namespace
        self.net_dict = weakref.WeakKeyDictionary()
        self.lib_dict = weakref.WeakKeyDictionary()
        self.defp_dict = weakref.WeakKeyDictionary()
        self.defc_dict = weakref.WeakKeyDictionary()
        self.defi_dict = weakref.WeakKeyDictionary()

    def definition_add_port(self, definition, port):
        self.add_to_dict(self.defp_dict, definition, port)

    def definition_remove_port(self, definition, port):
        self.remove_from_dict(self.defp_dict, definition, port)

    def definition_add_child(self, definition, child):
        self.add_to_dict(self.defi_dict, definition, child)

    def definition_remove_child(self, definition, child):
        self.remove_from_dict(self.defi_dict, definition, child)

    def definition_add_cable(self, definition, cable):
        self.add_to_dict(self.defc_dict, definition, cable)

    def definition_remove_cable(self, definition, cable):
        self.remove_from_dict(self.defc_dict, definition, cable)

    def library_add_definition(self, library, definition):
        self.add_to_dict(self.lib_dict, library, definition)

    def library_remove_definition(self, library, definition):
        self.remove_from_dict(self.lib_dict, library, definition)

    def netlist_add_library(self, netlist, library):
        self.add_to_dict(self.net_dict, netlist, library)

    def netlist_remove_library(self, netlist, library):
        self.remove_from_dict(self.net_dict, netlist, library)

    def dictionary_set(self, element, key, value):
        if key != 'EDIF.identifier':
            return
        is_rename = False
        previous_value = None
        if "EDIF.identifier" in element:
            is_rename = True
            previous_value = element['EDIF.identifier']
            self.dictionary_delete(element, "EDIF.identifier")
        try:
            self.dict_set(element, value)
        except ValueError:
            if is_rename:
                self.dict_set(element, previous_value)
            raise

    def dictionary_delete(self, element, key):
        if key == 'EDIF.identifier':
            self.key_remover(element, key)

    def dictionary_pop(self, element, item):
        key = item
        if key != 'EDIF.identifier':
            return
        self.key_remover(element,key)

    def add_to_dict(self, container, parent, child):
        if "EDIF.identifier" in child:
            self.dict_set(child, child["EDIF.identifier"], container=container, parent=parent)

    def key_remover(self, element, key):
        if isinstance(element, Cable):
            self.remove_from_dict(self.defc_dict, element.definition, element)
        elif isinstance(element, Definition):
            self.remove_from_dict(self.lib_dict, element.library, element)
        elif isinstance(element, Library):
            self.netlist_remove_library(element.netlist, element)
        elif isinstance(element, Port):
            self.remove_from_dict(self.defp_dict, element.definition, element)
        elif isinstance(element, Instance):
            self.remove_from_dict(self.defi_dict, element.parent, element)

    def remove_from_dict(self, container, parent, child):
        if "EDIF.identifier" in child:
            assert parent in container and child["EDIF.identifier"] in container[parent], "Child object " + child.__class__.__name__ + " not present in given object's namespace " + parent.__class__.__name__
            container[parent].pop(child["EDIF.identifier"])

    def dict_set(self, child, value, container=None, parent=None):
        if container is None or parent is None:
            if isinstance(child, Cable):
                container = self.defc_dict
                parent = child.definition
            elif isinstance(child, Definition):
                container = self.lib_dict
                parent = child.library
            elif isinstance(child, Library):
                container = self.net_dict
                parent = child.netlist
            elif isinstance(child, Port):
                container = self.defp_dict
                parent = child.definition
            elif isinstance(child, Instance):
                container = self.defi_dict
                parent = child.parent

        if container is not None and parent is not None:
            if parent in container:
                if value in container[parent]:
                   raise ValueError("EDIF namespace violation while adding " + child.__class__.__name__ + " to " + parent.__class__.__name__)
            else:
                container[parent] = dict()
            container[parent][value] = child