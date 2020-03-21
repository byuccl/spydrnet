import unittest
import spydrnet as sdn

class TestGlobalServiceWithoutPlugins(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        sdn.namespace_manager.deregister_all_listeners()
        cls.netlist = sdn.load_example_netlist_by_name("b13")

    @classmethod
    def tearDownClass(cls) -> None:
        sdn.namespace_manager.register_all_listeners()

    def test_double_register_lookup(self):
        from spydrnet.global_state.global_service import register_lookup
        register_lookup("TEST", None)
        self.assertRaises(ValueError, register_lookup, "TEST", None)

    def test_lookup_library(self):
        library = self.netlist.libraries[0]
        library_name = library.name
        lib1 = next(self.netlist.get_libraries(library_name))
        self.assertEqual(library, lib1)
        lib2 = next(self.netlist.get_libraries(library_name, key='EDIF.identifier'))
        self.assertEqual(library, lib2)
        lib3 = next(sdn.get_libraries(self.netlist, library_name))
        self.assertEqual(library, lib3)
        lib4 = next(sdn.get_libraries(self.netlist, library_name, key='EDIF.identifier'))
        self.assertEqual(library, lib4)

    def test_lookup_definition(self):
        library = self.netlist.libraries[0]
        definition = library.definitions[0]
        definition_name = definition.name
        def1 = next(self.netlist.get_definitions(definition_name))
        self.assertEqual(definition, def1)
        def2 = next(self.netlist.get_definitions(definition_name, key='EDIF.identifier'))
        self.assertEqual(definition, def2)
        def3 = next(sdn.get_definitions(self.netlist, definition_name))
        self.assertEqual(definition, def3)
        def4 = next(sdn.get_definitions(self.netlist, definition_name, key='EDIF.identifier'))
        self.assertEqual(definition, def4)
        def5 = next(library.get_definitions(definition_name))
        self.assertEqual(definition, def5)
        def6 = next(library.get_definitions(definition_name, key='EDIF.identifier'))
        self.assertEqual(definition, def6)
        def7 = next(sdn.get_definitions(library, definition_name))
        self.assertEqual(definition, def7)
        def8 = next(sdn.get_definitions(library, definition_name, key='EDIF.identifier'))
        self.assertEqual(definition, def8)

    def test_lookup_port_cables_instances(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        port = definition.ports[0]
        port_name = port.name
        cable = definition.cables[0]
        cable_name = cable.name
        instance = definition.children[0]
        instance_name = instance.name
        port1 = next(definition.get_ports(port_name))
        self.assertEqual(port, port1)
        cable1 = next(definition.get_cables(cable_name))
        self.assertEqual(cable, cable1)
        instance1 = next(definition.get_instances(instance_name))
        self.assertEqual(instance, instance1)

    def test_lookup_something_that_does_not_exist(self):
        item = next(self.netlist.get_libraries("DOES_NOT_EXIST"), None)
        self.assertIsNone(item)
