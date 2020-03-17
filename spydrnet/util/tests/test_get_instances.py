import unittest
import spydrnet as sdn


class TestGetInstances(unittest.TestCase):
    def test_parameter_checking(self):
        definition = sdn.Definition()
        instance = definition.create_child()
        instance.name = "MY_INST"
        self.assertRaises(TypeError, sdn.get_instances, definition, "MY_INST", patterns="MY_INST")
        self.assertRaises(TypeError, sdn.get_instances, definition, "MY_INST", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_instances, definition, "MY_INST", selection=sdn.BOTH)
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

    def test_get_instances_from_objects(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        instance = definition.create_child()
        instance.name = "MY_INST"
        top_instance = sdn.Instance()
        top_instance.name = "TOP_INST"
        top_instance.reference = definition
        netlist.top_instance = top_instance

        leaf_definition = library.create_definition()
        leaf_cable = leaf_definition.create_cable()
        leaf_wire = leaf_cable.create_wire()
        instance.reference = leaf_definition

        instance1 = next(sdn.get_instances(netlist))
        self.assertEqual(instance, instance1)

        instance1 = next(sdn.get_instances(library))
        self.assertEqual(instance, instance1)

        instance1 = list(sdn.get_instances(definition, recursive=True))
        self.assertEqual(instance, instance1[0])

        instance1 = list(sdn.get_instances(definition, selection="OUTSIDE", recursive=True))
        self.assertEqual(top_instance, instance1[0])

        instance1 = list(sdn.get_instances(leaf_definition, selection="OUTSIDE", recursive=True))
        self.assertTrue(top_instance in instance1 and instance in instance1)

        instance1 = next(sdn.get_instances(top_instance, recursive=True))
        self.assertEqual(instance, instance1)

        instance1 = list(sdn.get_instances(instance, selection="OUTSIDE", recursive=True))
        self.assertEqual(top_instance, instance1[0])

        cable = definition.create_cable()
        wire = cable.create_wire()
        port = definition.create_port()
        pin = port.create_pin()
        outer_pin = top_instance.pins[pin]

        instance1 = next(sdn.get_instances(wire))
        self.assertIs(top_instance, instance1)

        instance1 = next(sdn.get_instances(outer_pin, "TOP_INST"))
        self.assertIs(top_instance, instance1)

        top_href = next(sdn.get_hinstances(netlist.top_instance))
        instance1 = next(sdn.get_instances(top_href))
        self.assertIs(top_instance, instance1)

        port_href = next(sdn.get_hports(port))
        instance1 = next(sdn.get_instances(port_href))
        self.assertIs(top_instance, instance1)
