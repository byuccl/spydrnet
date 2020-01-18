#COPYRIGHT BYUCCL 2020

from spydrnet.callback.callback_manager import CallbackListener

class data_manager(CallbackListener):
    '''
    this class is a plugin using the callback listener to manage a database for name management.
    
    This class implements and registers all listeners and presents to the user
    the ability to do quick lookups based on name.
    '''

    ######################################################
    #User access funcitons
    ######################################################

    ######################################################
    #Override funcitons to register listeners
    ######################################################

    def register_all_listeners(self):
        '''override the function that registers what listeners are available.'''
        self.register_cable_add_wire()
        self.register_cable_remove_wire()
        self.register_definition_add_port()
        self.register_definition_remove_port()
        self.register_definition_add_child()
        self.register_definition_remove_child()
        self.register_definition_add_cable()
        self.register_definition_remove_cable()
        self.register_instance_reference()
        self.register_library_add_definition()
        self.register_library_remove_definition()
        self.register_netlist_top_instance()
        self.register_netlist_add_library()
        self.register_netlist_remove_library()
        self.register_port_add_pin()
        self.register_port_remove_pin()
        self.register_wire_connect_pin()
        self.register_wire_disconnect_pin()


    ######################################################
    #Override functions that listen
    ######################################################
