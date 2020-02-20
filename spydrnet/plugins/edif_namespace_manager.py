#COPYRIGHT BYUCCL 2020

from spydrnet.callback.callback_listener import CallbackListener
from spydrnet.ir import Library, Definition, Instance, Port, Cable


class EdifNamespaceManager(CallbackListener):
    '''
    this class is a plugin using the callback listener to manage a database for name management.
    
    This class implements and registers all listeners and presents to the user
    the ability to do quick lookups based on name.
    '''

    ######################################################
    #User access functions to use datamanager
    ######################################################

    
    ######################################################
    #Override funcitons to register listeners
    ######################################################

    def __init__(self):
        super().__init__()
        # dictionary for each namespace
        # netlist simple dictionary
        self.net_dict = dict()
        # library dictionary from library to dictionary from name to value
        self.lib_dict = dict()
        # definition dictionary from defintion to dictionary from name to value
        self.defp_dict = dict()
        self.defc_dict = dict()
        self.defi_dict = dict()


    ######################################################
    #Override functions that listen
    ######################################################

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

    def dictionary_delete(self, element, key):
        if key != 'EDIF.identifier':
            return
        self.key_remover(element,key)

    def dictionary_set(self, element, key, value):
        if key != 'EDIF.identifier':
            return
        if "EDIF.identifier" in element:
            #this is a rename we must remove first.
            self.dictionary_delete(element, "EDIF.identifier")
        if isinstance(element, Cable):
            if element.definition is None:
                return
            self.dict_set(self.defc_dict, element.definition, element, value)
        if isinstance(element, Definition):
            if element.library is None:
                return
            self.dict_set(self.lib_dict, element.library, element, value)
        if isinstance(element, Library):
            if element.netlist is None:
                return
            self.net_dict_set(self.net_dict, element.netlist, element, value)
        if isinstance(element, Port):
            if element.definition is None:
                return
            self.dict_set(self.defp_dict, element.definition, element, value)
        if isinstance(element, Instance):
            if element.parent is None:
                return
            self.dict_set(self.defi_dict, element.parent, element, value)

    def dictionary_pop(self, element, item):
        key = item
        if key != 'EDIF.identifier':
            return
        self.key_remover(element,key)

    def netlist_add_library(self, netlist, library):
        #add the library["EDIF.identifier"] to the data structure for netlists
        if "EDIF.identifier" not in library:
            return
        self.net_dict_set(self.net_dict, netlist, library, library["EDIF.identifier"])

    def netlist_remove_library(self, netlist, library):
        if "EDIF.identifier" not in library:
            return
        #remove the library["EDIF.identifier"] from the data structure for netlists
        assert library["EDIF.identifier"] in self.net_dict and self.net_dict[library["EDIF.identifier"]] == library, "Library not present in given object netlist"
        self.net_dict.pop(library["EDIF.identifier"])


    #################################################################################
    # Helper functions
    #################################################################################

    def add_to_dict(self, container, parent, child):
        if "EDIF.identifier" not in child:
            return
        self.dict_set(container, parent, child, child["EDIF.identifier"])

    def key_remover(self, element, key):
        if isinstance(element, Cable):
            self.remove_from_dict(self.defc_dict, element.definition, element)
        if isinstance(element, Definition):
            self.remove_from_dict(self.lib_dict, element.library, element)
        if isinstance(element, Library):
            self.netlist_remove_library(element.netlist, element)
        if isinstance(element, Port):
            self.remove_from_dict(self.defp_dict, element.definition, element)
        if isinstance(element, Instance):
            self.remove_from_dict(self.defi_dict, element.parent, element)

    def remove_from_dict(self, container, parent, child):
        if "EDIF.identifier" not in child:
            return
        assert parent in container and child["EDIF.identifier"] in container[parent], "Child object " + child.__class__.__name__ + " not present in given object's namespace " + parent.__class__.__name__
        container[parent].pop(child["EDIF.identifier"])
    

    def dict_set(self, container, parent, child, value):
        if parent in container:
            if value in container[parent]:
               raise ValueError("Edif namespace violation while adding " + child.__class__.__name__ + " to " + parent.__class__.__name__)
            else:
                container[parent][value] = child
        else:
            container[parent] = dict()
            container[parent][value] = child

    def net_dict_set(self, container, parent, child, value):
        if(value in self.net_dict):
            raise ValueError("Edif namespace violation while adding Library to Netlist")
        else:
            self.net_dict[value] = child