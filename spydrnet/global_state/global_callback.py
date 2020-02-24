_container_create_netlist = list()
_container_create_library = list()
_container_create_definition = list()
_container_create_port = list()
_container_create_cable = list()
_container_create_instance = list()
_container_cable_add_wire = list()
_container_cable_remove_wire = list()
_container_definition_add_port = list()
_container_definition_remove_port = list()
_container_definition_add_child = list()
_container_definition_remove_child = list()
_container_definition_add_cable = list()
_container_definition_remove_cable = list()
_container_instance_reference = list()
_container_library_add_definition = list()
_container_library_remove_definition = list()
_container_netlist_top_instance = list()
_container_netlist_add_library = list()
_container_netlist_remove_library = list()
_container_port_add_pin = list()
_container_port_remove_pin = list()
_container_wire_connect_pin = list()
_container_wire_disconnect_pin = list()
_container_dictionary_set = list()
_container_dictionary_delete = list()
_container_dictionary_pop = list()


def _call_create_netlist(*args, **kwargs):
    for func in _container_create_netlist:
        func(*args, **kwargs)


def _call_create_library(*args, **kwargs):
    for func in _container_create_library:
        func(*args, **kwargs)


def _call_create_definition(*args, **kwargs):
    for func in _container_create_definition:
        func(*args, **kwargs)


def _call_create_port(*args, **kwargs):
    for func in _container_create_port:
        func(*args, **kwargs)


def _call_create_cable(*args, **kwargs):
    for func in _container_create_cable:
        func(*args, **kwargs)


def _call_create_instance(*args, **kwargs):
    for func in _container_create_instance:
        func(*args, **kwargs)


def _call_cable_add_wire(*args, **kwargs):
    for func in _container_cable_add_wire:
        func(*args, **kwargs)


def _call_cable_remove_wire(*args, **kwargs):
    for func in _container_cable_remove_wire:
        func(*args, **kwargs)


def _call_definition_add_port(*args, **kwargs):
    for func in _container_definition_add_port:
        func(*args, **kwargs)


def _call_definition_remove_port(*args, **kwargs):
    for func in _container_definition_remove_port:
        func(*args, **kwargs)


def _call_definition_add_child(*args, **kwargs):
    for func in _container_definition_add_child:
        func(*args, **kwargs)


def _call_definition_remove_child(*args, **kwargs):
    for func in _container_definition_remove_child:
        func(*args, **kwargs)


def _call_definition_add_cable(*args, **kwargs):
    for func in _container_definition_add_cable:
        func(*args, **kwargs)


def _call_definition_remove_cable(*args, **kwargs):
    for func in _container_definition_remove_cable:
        func(*args, **kwargs)


def _call_instance_reference(*args, **kwargs):
    for func in _container_instance_reference:
        func(*args, **kwargs)


def _call_library_add_definition(*args, **kwargs):
    for func in _container_library_add_definition:
        func(*args, **kwargs)


def _call_library_remove_definition(*args, **kwargs):
    for func in _container_library_remove_definition:
        func(*args, **kwargs)


def _call_netlist_top_instance(*args, **kwargs):
    for func in _container_netlist_top_instance:
        func(*args, **kwargs)


def _call_netlist_add_library(*args, **kwargs):
    for func in _container_netlist_add_library:
        func(*args, **kwargs)


def _call_netlist_remove_library(*args, **kwargs):
    for func in _container_netlist_remove_library:
        func(*args, **kwargs)


def _call_port_add_pin(*args, **kwargs):
    for func in _container_port_add_pin:
        func(*args, **kwargs)


def _call_port_remove_pin(*args, **kwargs):
    for func in _container_port_remove_pin:
        func(*args, **kwargs)


def _call_wire_connect_pin(*args, **kwargs):
    for func in _container_wire_connect_pin:
        func(*args, **kwargs)


def _call_wire_disconnect_pin(*args, **kwargs):
    for func in _container_wire_disconnect_pin:
        func(*args, **kwargs)


def _call_dictionary_set(*args, **kwargs):
    for func in _container_dictionary_set:
        func(*args, **kwargs)


def _call_dictionary_delete(*args, **kwargs):
    for func in _container_dictionary_delete:
        func(*args, **kwargs)


def _call_dictionary_pop(*args, **kwargs):
    for func in _container_dictionary_pop:
        func(*args, **kwargs)


def register_create_netlist(method):
    _register(_container_create_netlist, method)


def register_create_library(method):
    _register(_container_create_library, method)


def register_create_definition(method):
    _register(_container_create_definition, method)


def register_create_port(method):
    _register(_container_create_port, method)


def register_create_cable(method):
    _register(_container_create_cable, method)


def register_create_instance(method):
    _register(_container_create_instance, method)


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


def _register(container_to_register, method):
    # TODO: look into inlining this function perhaps, not not be necessary since is won't be called often.
    assert method not in container_to_register
    container_to_register.append(method)


def deregister_create_netlist(method):
    _deregister(_container_create_netlist, method)


def deregister_create_library(method):
    _deregister(_container_create_library, method)


def deregister_create_definition(method):
    _deregister(_container_create_definition, method)


def deregister_create_port(method):
    _deregister(_container_create_port, method)


def deregister_create_cable(method):
    _deregister(_container_create_cable, method)


def deregister_create_instance(method):
    _deregister(_container_create_instance, method)


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


def _deregister(container_to_deregister, method):
    # TODO: look into inlining this function perhaps, may not be necessary since it won't be called often.
    assert method in container_to_deregister
    container_to_deregister.remove(method)
