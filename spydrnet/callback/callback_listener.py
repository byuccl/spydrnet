from spydrnet.global_state import global_callback


class CallbackListener:
    """
    extend this class to create a listener that can be used to make a plugin to spydrnet.
    In this class are all of the functions that are used as callbacks. There are also
    register methods whos function is to register the callback functions that are present.

    callbacks are netlist dependent. If a callback is registered to one netlist it is not automatically registered to all netlists.
    """

    def __init__(self):
        self.register_all_listeners()

    def create_netlist(self, netlist):
        raise NotImplementedError

    def create_library(self, library):
        raise NotImplementedError

    def create_definition(self, definition):
        raise NotImplementedError

    def create_port(self, port):
        raise NotImplementedError

    def create_cable(self, cable):
        raise NotImplementedError

    def create_instance(self, instance):
        raise NotImplementedError

    def cable_add_wire(self, cable, wire):
        raise NotImplementedError

    def cable_remove_wire(self, cable, wire):
        raise NotImplementedError

    def definition_add_port(self, definition, port):
        raise NotImplementedError

    def definition_remove_port(self, definition, port):
        raise NotImplementedError

    def definition_add_child(self, definition, child):
        raise NotImplementedError

    def definition_remove_child(self, definition, child):
        raise NotImplementedError

    def definition_add_cable(self, definition, cable):
        raise NotImplementedError

    def definition_remove_cable(self, definition, cable):
        raise NotImplementedError

    def instance_reference(self, instance, reference):
        raise NotImplementedError

    def library_add_definition(self, library, definition):
        raise NotImplementedError

    def library_remove_definition(self, library, definition):
        raise NotImplementedError

    def netlist_top_instance(self, netlist, instance):
        raise NotImplementedError

    def netlist_add_library(self, netlist, library):
        raise NotImplementedError

    def netlist_remove_library(self, netlist, library):
        raise NotImplementedError

    def port_add_pin(self, port, pin):
        raise NotImplementedError

    def port_remove_pin(self, port, pin):
        raise NotImplementedError

    def wire_connect_pin(self, wire, pin):
        raise NotImplementedError

    def wire_disconnect_pin(self, wire, pin):
        raise NotImplementedError
    
    def dictionary_set(self, element, key, value):
        raise NotImplementedError

    def dictionary_delete(self, element, key):
        raise NotImplementedError

    def dictionary_pop(self, element, key):
        raise NotImplementedError

    def register_all_listeners(self):
        if self.create_netlist.__func__ is not CallbackListener.create_netlist:
            self.register_create_netlist()

        if self.create_library.__func__ is not CallbackListener.create_library:
            self.register_create_library()

        if self.create_definition.__func__ is not CallbackListener.create_definition:
            self.register_create_definition()

        if self.create_port.__func__ is not CallbackListener.create_port:
            self.register_create_port()

        if self.create_cable.__func__ is not CallbackListener.create_cable:
            self.register_create_cable()

        if self.create_instance.__func__ is not CallbackListener.create_instance:
            self.register_create_instance()

        if self.cable_add_wire.__func__ is not CallbackListener.cable_add_wire:
            self.register_cable_add_wire()

        if self.cable_remove_wire.__func__ is not CallbackListener.cable_remove_wire:
            self.register_cable_remove_wire()

        if self.definition_add_port.__func__ is not CallbackListener.definition_add_port:
            self.register_definition_add_port()

        if self.definition_remove_port.__func__ is not CallbackListener.definition_remove_port:
            self.register_definition_remove_port()

        if self.definition_add_child.__func__ is not CallbackListener.definition_add_child:
            self.register_definition_add_child()

        if self.definition_remove_child.__func__ is not CallbackListener.definition_remove_child:
            self.register_definition_remove_child()

        if self.definition_add_cable.__func__ is not CallbackListener.definition_add_cable:
            self.register_definition_add_cable()

        if self.definition_remove_cable.__func__ is not CallbackListener.definition_remove_cable:
            self.register_definition_remove_cable()

        if self.instance_reference.__func__ is not CallbackListener.instance_reference:
            self.register_instance_reference()

        if self.library_add_definition.__func__ is not CallbackListener.library_add_definition:
            self.register_library_add_definition()

        if self.library_remove_definition.__func__ is not CallbackListener.library_remove_definition:
            self.register_library_remove_definition()

        if self.netlist_top_instance.__func__ is not CallbackListener.netlist_top_instance:
            self.register_netlist_top_instance()

        if self.netlist_add_library.__func__ is not CallbackListener.netlist_add_library:
            self.register_netlist_add_library()

        if self.netlist_remove_library.__func__ is not CallbackListener.netlist_remove_library:
            self.register_netlist_remove_library()

        if self.port_add_pin.__func__ is not CallbackListener.port_add_pin:
            self.register_port_add_pin()

        if self.port_remove_pin.__func__ is not CallbackListener.port_remove_pin:
            self.register_port_remove_pin()

        if self.wire_connect_pin.__func__ is not CallbackListener.wire_connect_pin:
            self.register_wire_connect_pin()

        if self.wire_disconnect_pin.__func__ is not CallbackListener.wire_disconnect_pin:
            self.register_wire_disconnect_pin()

        if self.dictionary_set.__func__ is not CallbackListener.dictionary_set:
            self.register_dictionary_set()

        if self.dictionary_delete.__func__ is not CallbackListener.dictionary_delete:
            self.register_dictionary_delete()

        if self.dictionary_pop.__func__ is not CallbackListener.dictionary_pop:
            self.register_dictionary_pop()
                
    def register_create_netlist(self):
        global_callback.register_create_netlist(self.create_netlist)

    def register_create_library(self):
        global_callback.register_create_library(self.create_library)

    def register_create_definition(self):
        global_callback.register_create_definition(self.create_definition)

    def register_create_port(self):
        global_callback.register_create_port(self.create_port)

    def register_create_cable(self):
        global_callback.register_create_cable(self.create_cable)

    def register_create_instance(self):
        global_callback.register_create_instance(self.create_instance)

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

    def register_dictionary_set(self):
        global_callback.register_dictionary_set(self.dictionary_set)

    def register_dictionary_delete(self):
        global_callback.register_dictionary_delete(self.dictionary_delete)

    def register_dictionary_pop(self):
        global_callback.register_dictionary_pop(self.dictionary_pop)

    def deregister_all_listeners(self):
        if self.create_netlist.__func__ is not CallbackListener.create_netlist:
            self.deregister_create_netlist()

        if self.create_library.__func__ is not CallbackListener.create_library:
            self.deregister_create_library()

        if self.create_definition.__func__ is not CallbackListener.create_definition:
            self.deregister_create_definition()

        if self.create_port.__func__ is not CallbackListener.create_port:
            self.deregister_create_port()

        if self.create_cable.__func__ is not CallbackListener.create_cable:
            self.deregister_create_cable()

        if self.create_instance.__func__ is not CallbackListener.create_instance:
            self.deregister_create_instance()

        if self.cable_add_wire.__func__ is not CallbackListener.cable_add_wire:
            self.deregister_cable_add_wire()

        if self.cable_remove_wire.__func__ is not CallbackListener.cable_remove_wire:
            self.deregister_cable_remove_wire()

        if self.definition_add_port.__func__ is not CallbackListener.definition_add_port:
            self.deregister_definition_add_port()

        if self.definition_remove_port.__func__ is not CallbackListener.definition_remove_port:
            self.deregister_definition_remove_port()

        if self.definition_add_child.__func__ is not CallbackListener.definition_add_child:
            self.deregister_definition_add_child()

        if self.definition_remove_child.__func__ is not CallbackListener.definition_remove_child:
            self.deregister_definition_remove_child()

        if self.definition_add_cable.__func__ is not CallbackListener.definition_add_cable:
            self.deregister_definition_add_cable()

        if self.definition_remove_cable.__func__ is not CallbackListener.definition_remove_cable:
            self.deregister_definition_remove_cable()

        if self.instance_reference.__func__ is not CallbackListener.instance_reference:
            self.deregister_instance_reference()

        if self.library_add_definition.__func__ is not CallbackListener.library_add_definition:
            self.deregister_library_add_definition()

        if self.library_remove_definition.__func__ is not CallbackListener.library_remove_definition:
            self.deregister_library_remove_definition()

        if self.netlist_top_instance.__func__ is not CallbackListener.netlist_top_instance:
            self.deregister_netlist_top_instance()

        if self.netlist_add_library.__func__ is not CallbackListener.netlist_add_library:
            self.deregister_netlist_add_library()

        if self.netlist_remove_library.__func__ is not CallbackListener.netlist_remove_library:
            self.deregister_netlist_remove_library()

        if self.port_add_pin.__func__ is not CallbackListener.port_add_pin:
            self.deregister_port_add_pin()

        if self.port_remove_pin.__func__ is not CallbackListener.port_remove_pin:
            self.deregister_port_remove_pin()

        if self.wire_connect_pin.__func__ is not CallbackListener.wire_connect_pin:
            self.deregister_wire_connect_pin()

        if self.wire_disconnect_pin.__func__ is not CallbackListener.wire_disconnect_pin:
            self.deregister_wire_disconnect_pin()

        if self.dictionary_set.__func__ is not CallbackListener.dictionary_set:
            self.deregister_dictionary_set()

        if self.dictionary_delete.__func__ is not CallbackListener.dictionary_delete:
            self.deregister_dictionary_delete()

        if self.dictionary_pop.__func__ is not CallbackListener.dictionary_pop:
            self.deregister_dictionary_pop()

    def deregister_create_netlist(self):
        global_callback.deregister_create_netlist(self.create_netlist)

    def deregister_create_library(self):
        global_callback.deregister_create_library(self.create_library)

    def deregister_create_definition(self):
        global_callback.deregister_create_definition(self.create_definition)

    def deregister_create_port(self):
        global_callback.deregister_create_port(self.create_port)

    def deregister_create_cable(self):
        global_callback.deregister_create_cable(self.create_cable)

    def deregister_create_instance(self):
        global_callback.deregister_create_instance(self.create_instance)

    def deregister_cable_add_wire(self):
        global_callback.deregister_cable_add_wire(self.cable_add_wire)

    def deregister_cable_remove_wire(self):
        global_callback.deregister_cable_remove_wire(self.cable_remove_wire)

    def deregister_definition_add_port(self):
        global_callback.deregister_definition_add_port(self.definition_add_port)

    def deregister_definition_remove_port(self):
        global_callback.deregister_definition_remove_port(self.definition_remove_port)

    def deregister_definition_add_child(self):
        global_callback.deregister_definition_add_child(self.definition_add_child)

    def deregister_definition_remove_child(self):
        global_callback.deregister_definition_remove_child(self.definition_remove_child)

    def deregister_definition_add_cable(self):
        global_callback.deregister_definition_add_cable(self.definition_add_cable)

    def deregister_definition_remove_cable(self):
        global_callback.deregister_definition_remove_cable(self.definition_remove_cable)

    def deregister_instance_reference(self):
        global_callback.deregister_instance_reference(self.instance_reference)

    def deregister_library_add_definition(self):
        global_callback.deregister_library_add_definition(self.library_add_definition)

    def deregister_library_remove_definition(self):
        global_callback.deregister_library_remove_definition(self.library_remove_definition)

    def deregister_netlist_top_instance(self):
        global_callback.deregister_netlist_top_instance(self.netlist_top_instance)

    def deregister_netlist_add_library(self):
        global_callback.deregister_netlist_add_library(self.netlist_add_library)

    def deregister_netlist_remove_library(self):
        global_callback.deregister_netlist_remove_library(self.netlist_remove_library)

    def deregister_port_add_pin(self):
        global_callback.deregister_port_add_pin(self.port_add_pin)

    def deregister_port_remove_pin(self):
        global_callback.deregister_port_remove_pin(self.port_remove_pin)

    def deregister_wire_connect_pin(self):
        global_callback.deregister_wire_connect_pin(self.wire_connect_pin)

    def deregister_wire_disconnect_pin(self):
        global_callback.deregister_wire_disconnect_pin(self.wire_disconnect_pin)

    def deregister_dictionary_set(self):
        global_callback.deregister_dictionary_set(self.dictionary_set)

    def deregister_dictionary_delete(self):
        global_callback.deregister_dictionary_delete(self.dictionary_delete)

    def deregister_dictionary_pop(self):
        global_callback.deregister_dictionary_pop(self.dictionary_pop)