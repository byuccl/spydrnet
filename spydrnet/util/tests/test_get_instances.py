import unittest
import spydrnet as sdn


class TestGetInstances(unittest.TestCase):
    def test_parameter_checking(self):
        definition = sdn.Definition()
        instance = definition.create_child()
        instance.name = "MY_INST"
        self.assertRaises(TypeError, sdn.get_instances, definition, "MY_INST", patterns="MY_INST")
        self.assertRaises(TypeError, sdn.get_instances, definition, "MY_INST", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_instances, None, "MY_INST")
        self.assertRaises(TypeError, sdn.get_instances, [None, definition], "MY_INST")

    def test_collection(self):
        definition = sdn.Definition()
        instance = definition.create_child()
        instance.name = "MY_INST"
        instances = list(sdn.get_instances([definition, definition]))
        self.assertEqual(len(instances), 1)

    def test_get_instances_in_library(self):
        library = sdn.Library()
        definition = library.create_definition()
        instance = definition.create_child()
        instance.name = "MY_INST"
        instance1 = next(library.get_instances("MY_INST"))
        self.assertEqual(instance, instance1)

    def test_get_instances_in_netlist(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        instance = definition.create_child()
        instance.name = "MY_INST"
        instance1 = next(netlist.get_instances("MY_INST"))
        self.assertEqual(instance, instance1)
