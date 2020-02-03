#COPYRIGHT BYUCCL 2020

from spydrnet.callback.callback_listener import CallbackListener

class DataManager(CallbackListener):
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
        # dictionary for each namespace
        # netlist simple dictionary
        self.net_dict = dict()
        # library dictionary from library to dictionary from name to value
        self.lib_dict = dict()
        # definition dictionary from defintion to dictionary from name to value
        self.def_dict = dict()
        # instance dictionary from instance to dictionary from name to value
        self.ins_dict = dict()
        # call this to register the listeners
        self.top_namespace = dict()

        super().__init__()
    

    def register_all_listeners(self):
        '''override the function that registers what listeners are available.'''
        #self.register_cable_add_wire()
        #self.register_cable_remove_wire()
        self.register_definition_add_port()
        self.register_definition_remove_port()
        self.register_definition_add_child()
        self.register_definition_remove_child()
        self.register_definition_add_cable()
        self.register_definition_remove_cable()
        self.register_instance_reference()
        self.register_library_add_definition()
        self.register_library_remove_definition()
        #self.register_netlist_top_instance()
        self.register_netlist_add_library()
        self.register_netlist_remove_library()
        #self.register_port_add_pin()
        #self.register_port_remove_pin()
        #self.register_wire_connect_pin()
        #self.register_wire_disconnect_pin()


    ######################################################
    #Override functions that listen
    ######################################################

    #def cable_add_wire(self, cable, wire):
    #    pass

    #def cable_remove_wire(self, cable, wire):
    #    pass

    def definition_add_port(self, definition, port):
        self.add_from_dict(self.def_dict, definition, port)

    def definition_remove_port(self, definition, port):
        self.remove_from_dict(self.def_dict, definition, port)

    def definition_add_child(self, definition, child):
        self.add_from_dict(self.def_dict, definition, child)

    def definition_remove_child(self, definition, child):
        self.remove_from_dict(self.def_dict, definition, child)

    def definition_add_cable(self, definition, cable):
        self.add_to_dict(self.def_dict, definition, cable)

    def definition_remove_cable(self, definition, cable):
        self.remove_from_dict(self.def_dict, definition, cable)

    def instance_reference(self, instance, reference):
        #TODO make this work out the change.
        pass

    def library_add_definition(self, library, definition):
        self.add_to_dict(self.lib_dict, library, definition)

    def library_remove_definition(self, library, definition):
        self.remove_from_dict(self.lib_dict, library, definition)

    #def netlist_top_instance(self, netlist, instance):
    #    pass

    def netlist_add_library(self, netlist, library):
        #add the library.edif.identifier to the data structure for netlists
        if(library.edif.identifier in self.netlistdict):
            raise ValueError("Edif namespace violation while adding Library to Netlist")
        else:
            self.netlistdict[library.edif.identifier] = library

    def netlist_remove_library(self, netlist, library):
        #remove the library.edif.identifier from the data structure for netlists
        if(library.edif.identifier not in self.netlistdict):
            raise ValueError("Library not present in given object netlist")
        else:
            if self.netlistdict[library.edif.identifier] != library:
                raise ValueError("Library not present in given object netlist")
            else:
                self.netlistdict.pop(library.edif.identifier)
    #def port_add_pin(self, port, pin):
    #    pass

    #def port_remove_pin(self, port, pin):
    #   pass

    #def wire_connect_pin(self, wire, pin):
    #    pass

    #def wire_disconnect_pin(self, wire, pin):
    #   pass

    #################################################################################
    # Helper functions
    #################################################################################

    def add_to_dict(self, container, parent, child):
        if parent in container:
            if child.edif.identifier in container[parent]:
               raise ValueError("Edif namespace violation while adding " + child.__class__.__name__ + " to " + parent.__class__.__name__)
            else:
                container[parent][child.edif.identifier] = child
        else:
            container[parent] = dict()
            container[parent][child.edif.identifier] = child

    def remove_from_dict(self, container, parent, child):
        if parent not in container:
            raise ValueError("Child object " + child.__class__.__name__ + " not present in given object " + parent.__class__.__name__)
        else:
            if child.edif.identifier not in container[parent]:
                raise ValueError("Child object " + child.__class__.__name__ + " not present in given object " + parent.__class__.__name__)
            else:
                container[parent].pop(child.edif.identifier)
