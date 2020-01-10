from global_state import global_callback


class CallbackListener:
    '''
    extend this class to create a listener that can be used to make a plugin to spydrnet.
    In this class are all of the functions that are used as callbacks. There are also 2 
    register functions whos function is to register all the callback functions that are present.
    
    callbacks are netlist dependent. If a callback is registered to one netlist it is not automatically registered to all netlists.
    '''

    def cable_add_wire(self):
        raise NotImplementedError

    def cable_remove_wire(self):
        raise NotImplementedError

    def definition_add_port(self):
        raise NotImplementedError

    def definition_remove_port(self):
        raise NotImplementedError

    def definition_add_child(self):
        raise NotImplementedError

    def definition_remove_child(self):
        raise NotImplementedError

    def definition_add_cable(self):
        raise NotImplementedError

    def definition_remove_cable(self):
        raise NotImplementedError

    def instance_reference(self):
        raise NotImplementedError

    def library_add_definition(self):
        raise NotImplementedError

    def library_remove_definition(self):
        raise NotImplementedError

    def netlist_top_instance(self):
        raise NotImplementedError

    def netlist_add_library(self):
        raise NotImplementedError

    def netlist_remove_library(self):
        raise NotImplementedError

    def port_add_pin(self):
        raise NotImplementedError

    def port_remove_pin(self):
        raise NotImplementedError

    def wire_connect_pin(self):
        raise NotImplementedError

    def wire_disconnect_pin(self):
        raise NotImplementedError
                
    def register_cable_add_wire(self):
        global_callback.register_cable_add_wire(self.cable_add_wire)

    def register_cable_remove_wire(self):
        global_callback.register_cable_remove_wire(self.cable_remove_wire)

    def register_definition_add_port(self):
        global_callback.register_definition_add_port(self.definition_add_port)

    def register_definition_remove_port(self):
        global_callback.register_definition_remove_port(self.definition_remove_port)

    def register_definition_add_child(self):
        global_callback.register_definition_add_child(self.definition_add_child)

    def register_definition_remove_child(self):
        global_callback.register_definition_remove_child(self.definition_remove_child)

    def register_definition_add_cable(self):
        global_callback.register_definition_add_cable(self.definition_add_cable)

    def register_definition_remove_cable(self):
        global_callback.register_definition_remove_cable(self.definition_remove_cable)

    def register_instance_reference(self):
        global_callback.register_instance_reference(self.instance_reference)

    def register_library_add_definition(self):
        global_callback.register_library_add_definition(self.library_add_definition)

    def register_library_remove_definition(self):
        global_callback.register_library_remove_definition(self.library_remove_definition)

    def register_netlist_top_instance(self):
        global_callback.register_netlist_top_instance(self.netlist_top_instance)

    def register_netlist_add_library(self):
        global_callback.register_netlist_add_library(self.netlist_add_library)

    def register_netlist_remove_library(self):
        global_callback.register_netlist_remove_library(self.netlist_remove_library)

    def register_port_add_pin(self):
        global_callback.register_port_add_pin(self.port_add_pin)

    def register_port_remove_pin(self):
        global_callback.register_port_remove_pin(self.port_remove_pin)

    def register_wire_connect_pin(self):
        global_callback.register_wire_connect_pin(self.wire_connect_pin)

    def register_wire_disconnect_pin(self):
        global_callback.register_wire_disconnect_pin(self.wire_disconnect_pin)