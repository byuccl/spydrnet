from spydrnet.global_state.global_netlist import current_netlist

_container_cable_add_wire = dict()
_container_cable_remove_wire = dict()
_container_definition_add_port = dict()
_container_definition_remove_port = dict()
_container_definition_add_child = dict()
_container_definition_remove_child = dict()
_container_definition_add_cable = dict()
_container_definition_remove_cable = dict()
_container_instance_reference = dict()
_container_library_add_definition = dict()
_container_library_remove_definition = dict()
_container_netlist_top_instance = dict()
_container_netlist_add_library = dict()
_container_netlist_remove_library = dict()
_container_port_add_pin = dict()
_container_port_remove_pin = dict()
_container_wire_connect_pin = dict()
_container_wire_disconnect_pin = dict()
#dictionary containers
_container_dictionary_set = dict()
_container_dictionary_delete = dict()
_container_dictionary_pop = dict()

#look into inlining this function perhaps
def _call(dictionary_to_call, *args, **kwargs):
    if current_netlist in dictionary_to_call:
        for func in dictionary_to_call[current_netlist]:
            func(*args, **kwargs)

def _call_cable_add_wire(*args, **kwargs):
    _call(_container_cable_add_wire, *args, **kwargs)

def _call_cable_remove_wire(*args, **kwargs):
    _call(_container_cable_remove_wire, *args, **kwargs)

def _call_definition_add_port(*args, **kwargs):
    _call(_container_definition_add_port, *args, **kwargs)

def _call_definition_remove_port(*args, **kwargs):
    _call(_container_definition_remove_port, *args, **kwargs)

def _call_definition_add_child(*args, **kwargs):
    _call(_container_definition_add_child, *args, **kwargs)

def _call_definition_remove_child(*args, **kwargs):
    _call(_container_definition_remove_child, *args, **kwargs)

def _call_definition_add_cable(*args, **kwargs):
    _call(_container_definition_add_cable, *args, **kwargs)

def _call_definition_remove_cable(*args, **kwargs):
    _call(_container_definition_remove_cable, *args, **kwargs)

def _call_instance_reference(*args, **kwargs):
    _call(_container_instance_reference, *args, **kwargs)

def _call_library_add_definition(*args, **kwargs):
    _call(_container_library_add_definition, *args, **kwargs)

def _call_library_remove_definition(*args, **kwargs):
    _call(_container_library_remove_definition, *args, **kwargs)

def _call_netlist_top_instance(*args, **kwargs):
    _call(_container_netlist_top_instance, *args, **kwargs)

def _call_netlist_add_library(*args, **kwargs):
    _call(_container_netlist_add_library, *args, **kwargs)

def _call_netlist_remove_library(*args, **kwargs):
    _call(_container_netlist_remove_library, *args, **kwargs)

def _call_port_add_pin(*args, **kwargs):
    _call(_container_port_add_pin, *args, **kwargs)

def _call_port_remove_pin(*args, **kwargs):
    _call(_container_port_remove_pin, *args, **kwargs)

def _call_wire_connect_pin(*args, **kwargs):
    _call(_container_wire_connect_pin, *args, **kwargs)

def _call_wire_disconnect_pin(*args, **kwargs):
    _call(_container_wire_disconnect_pin, *args, **kwargs)

#dictionary functions

def _call_dictionary_set(*args, **kwargs):
    _call(_container_dictionary_set, *args, **kwargs)

def _call_dictionary_delete(*args, **kwargs):
    _call(_container_dictionary_delete, *args, **kwargs)

def _call_dictionary_pop(*args, **kwargs):
    _call(_container_dictionary_pop, *args, **kwargs)

'''register functions'''

#look into inlining this function perhaps
def _register(dictionary_to_register, method):
    if current_netlist in dictionary_to_register:
        assert(method not in dictionary_to_register[current_netlist])
        dictionary_to_register[current_netlist].append(method)
    else:
        dictionary_to_register[current_netlist] = []
        dictionary_to_register[current_netlist].append(method)

def register_cable_add_wire(method):
    _register(_container_cable_add_wire, method)

def register_cable_remove_wire(method):
    _register(_container_cable_remove_wire, method)

def register_definition_add_port(method):
    _register(_container_definition_add_port, method)

def register_definition_remove_port(method):
    _register(_container_definition_remove_port, method)

def register_definition_add_child(method):
    _register(_container_definition_add_child, method)

def register_definition_remove_child(method):
    _register(_container_definition_remove_child, method)

def register_definition_add_cable(method):
    _register(_container_definition_add_cable, method)

def register_definition_remove_cable(method):
    _register(_container_definition_remove_cable, method)

def register_instance_reference(method):
    _register(_container_instance_reference, method)

def register_library_add_definition(method):
    _register(_container_library_add_definition, method)

def register_library_remove_definition(method):
    _register(_container_library_remove_definition, method)

def register_netlist_top_instance(method):
    _register(_container_netlist_top_instance, method)

def register_netlist_add_library(method):
    _register(_container_netlist_add_library, method)

def register_netlist_remove_library(method):
    _register(_container_netlist_remove_library, method)

def register_port_add_pin(method):
    _register(_container_port_add_pin, method)

def register_port_remove_pin(method):
    _register(_container_port_remove_pin, method)

def register_wire_connect_pin(method):
    _register(_container_wire_connect_pin, method)

def register_wire_disconnect_pin(method):
    _register(_container_wire_disconnect_pin, method)

def register_dictionary_set(*args, **kwargs):
    _register(_container_dictionary_set, *args, **kwargs)

def register_dictionary_delete(*args, **kwargs):
    _register(_container_dictionary_delete, *args, **kwargs)

def register_dictionary_pop(*args, **kwargs):
    _register(_container_dictionary_pop, *args, **kwargs)

'''deregister functions'''

#look into inlining this function perhaps
def _deregister(dictionary_to_deregister, method):
    assert(current_netlist in dictionary_to_deregister)
    assert(method in dictionary_to_deregister[current_netlist])
    dictionary_to_deregister[current_netlist].remove(method)

def deregister_cable_add_wire(method):
    _deregister(_container_cable_add_wire, method)

def deregister_cable_remove_wire(method):
    _deregister(_container_cable_remove_wire, method)

def deregister_definition_add_port(method):
    _deregister(_container_definition_add_port, method)

def deregister_definition_remove_port(method):
    _deregister(_container_definition_remove_port, method)

def deregister_definition_add_child(method):
    _deregister(_container_definition_add_child, method)

def deregister_definition_remove_child(method):
    _deregister(_container_definition_remove_child, method)

def deregister_definition_add_cable(method):
    _deregister(_container_definition_add_cable, method)

def deregister_definition_remove_cable(method):
    _deregister(_container_definition_remove_cable, method)

def deregister_instance_reference(method):
    _deregister(_container_instance_reference, method)

def deregister_library_add_definition(method):
    _deregister(_container_library_add_definition, method)

def deregister_library_remove_definition(method):
    _deregister(_container_library_remove_definition, method)

def deregister_netlist_top_instance(method):
    _deregister(_container_netlist_top_instance, method)

def deregister_netlist_add_library(method):
    _deregister(_container_netlist_add_library, method)

def deregister_netlist_remove_library(method):
    _deregister(_container_netlist_remove_library, method)

def deregister_port_add_pin(method):
    _deregister(_container_port_add_pin, method)

def deregister_port_remove_pin(method):
    _deregister(_container_port_remove_pin, method)

def deregister_wire_connect_pin(method):
    _deregister(_container_wire_connect_pin, method)

def deregister_wire_disconnect_pin(method):
    _deregister(_container_wire_disconnect_pin, method)

def deregister_dictionary_set(*args, **kwargs):
    _deregister(_container_dictionary_set, *args, **kwargs)

def deregister_dictionary_delete(*args, **kwargs):
    _deregister(_container_dictionary_delete, *args, **kwargs)

def deregister_dictionary_pop(*args, **kwargs):
    _deregister(_container_dictionary_pop, *args, **kwargs)
