import unittest

import spydrnet.global_state.global_callback as gc
from spydrnet.plugins import namespace_manager


class TestGlobalCallback(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        namespace_manager.deregister_all_listeners()

    @classmethod
    def tearDownClass(cls) -> None:
        namespace_manager.register_all_listeners()

    def setUp(self) -> None:
        self.arg1 = 1
        self.arg2 = 2
        self.kwarg = 3
        self.callcount = 0
        self.callcount2 = 0

    def mycall(self, a1, a2, ka = 0):
        self.callcount += 1
        assert(a1 is self.arg1)
        assert(a2 is self.arg2)
        assert(ka is self.kwarg)

    def mycall2(self, a1, a2, ka = 0):
        self.callcount2 += 1
        assert(a1 is self.arg1)
        assert(a2 is self.arg2)
        assert(ka is self.kwarg)

    def test_cable_add_wire(self):
        self.call_for_each(gc._container_cable_add_wire, gc.register_cable_add_wire, gc._call_cable_add_wire, gc.deregister_cable_add_wire)

    def test_cable_remove_wire(self):
        self.call_for_each(gc._container_cable_remove_wire, gc.register_cable_remove_wire, gc._call_cable_remove_wire, gc.deregister_cable_remove_wire)

    def test_definition_add_port(self):
        self.call_for_each(gc._container_definition_add_port, gc.register_definition_add_port, gc._call_definition_add_port, gc.deregister_definition_add_port)

    def test_definition_remove_port(self):
        self.call_for_each(gc._container_definition_remove_port, gc.register_definition_remove_port, gc._call_definition_remove_port, gc.deregister_definition_remove_port)

    def test_definition_add_child(self):
        self.call_for_each(gc._container_definition_add_child, gc.register_definition_add_child, gc._call_definition_add_child, gc.deregister_definition_add_child)

    def test_definition_remove_child(self):
        self.call_for_each(gc._container_definition_remove_child, gc.register_definition_remove_child, gc._call_definition_remove_child, gc.deregister_definition_remove_child)

    def test_definition_add_cable(self):
        self.call_for_each(gc._container_definition_add_cable, gc.register_definition_add_cable, gc._call_definition_add_cable, gc.deregister_definition_add_cable)

    def test_definition_remove_cable(self):
        self.call_for_each(gc._container_definition_remove_cable, gc.register_definition_remove_cable, gc._call_definition_remove_cable, gc.deregister_definition_remove_cable)

    def test_instance_reference(self):
        self.call_for_each(gc._container_instance_reference, gc.register_instance_reference, gc._call_instance_reference, gc.deregister_instance_reference)

    def test_library_add_definition(self):
        self.call_for_each(gc._container_library_add_definition, gc.register_library_add_definition, gc._call_library_add_definition, gc.deregister_library_add_definition)

    def test_library_remove_definition(self):
        self.call_for_each(gc._container_library_remove_definition, gc.register_library_remove_definition, gc._call_library_remove_definition, gc.deregister_library_remove_definition)

    def test_netlist_top_instance(self):
        self.call_for_each(gc._container_netlist_top_instance, gc.register_netlist_top_instance, gc._call_netlist_top_instance, gc.deregister_netlist_top_instance)

    def test_netlist_add_library(self):
        self.call_for_each(gc._container_netlist_add_library, gc.register_netlist_add_library, gc._call_netlist_add_library, gc.deregister_netlist_add_library)

    def test_netlist_remove_library(self):
        self.call_for_each(gc._container_netlist_remove_library, gc.register_netlist_remove_library, gc._call_netlist_remove_library, gc.deregister_netlist_remove_library)

    def test_port_add_pin(self):
        self.call_for_each(gc._container_port_add_pin, gc.register_port_add_pin, gc._call_port_add_pin, gc.deregister_port_add_pin)

    def test_port_remove_pin(self):
        self.call_for_each(gc._container_port_remove_pin, gc.register_port_remove_pin, gc._call_port_remove_pin, gc.deregister_port_remove_pin)

    def test_wire_connect_pin(self):
        self.call_for_each(gc._container_wire_connect_pin, gc.register_wire_connect_pin, gc._call_wire_connect_pin, gc.deregister_wire_connect_pin)

    def test_wire_disconnect_pin(self):
        self.call_for_each(gc._container_wire_disconnect_pin, gc.register_wire_disconnect_pin, gc._call_wire_disconnect_pin, gc.deregister_wire_disconnect_pin)

    def test_dictionary_delete(self):
        self.call_for_each(gc._container_dictionary_delete, gc.register_dictionary_delete, gc._call_dictionary_delete, gc.deregister_dictionary_delete)

    def test_dictionary_pop(self):
        self.call_for_each(gc._container_dictionary_pop, gc.register_dictionary_pop, gc._call_dictionary_pop, gc.deregister_dictionary_pop)
    
    def test_dictionary_add(self):
        self.call_for_each(gc._container_dictionary_set, gc.register_dictionary_set, gc._call_dictionary_set, gc.deregister_dictionary_set)

    def call_for_each(self, container, register, call, deregister):
        '''
        general strategy:
        check to make sure the _container is empty
        register a function
        check to make sure the function is registered
        call the function with some parameters
        check to make sure the function was called with the parameters
        deregister the function
        check to make sure the function was deregistered
        call the function
        check to make sure the funciton was not called
        '''
        assert self.mycall not in container
        assert self.mycall2 not in container
        register(self.mycall)
        assert self.mycall in container
        register(self.mycall2)
        assert self.mycall2 in container
        call(self.arg1, self.arg2, ka=self.kwarg)
        assert self.callcount == 1 and self.callcount2 == 1
        deregister(self.mycall)
        assert self.mycall not in container
        call(self.arg1, self.arg2, ka=self.kwarg)
        assert self.callcount2 == 2 and self.callcount == 1
        deregister(self.mycall2)
        assert self.mycall2 not in container
        call(self.arg1, self.arg2, ka=self.kwarg)
        assert self.callcount == 1 and self.callcount2 == 2