import unittest
import spydrnet as sdn


class TestGetInstances(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        instance = definition.create_child()
        instance.name = "MY_INST"
        top_instance = sdn.Instance()
        top_instance.name = "TOP_INST"
        top_instance.reference = definition
        netlist.top_instance = top_instance
        cls.netlist = netlist
        cls.library = library
        cls.definition = definition
        cls.instance = instance
        cls.top_instance = top_instance

        leaf_definition = library.create_definition()
        leaf_cable = leaf_definition.create_cable()
        leaf_wire = leaf_cable.create_wire()
        instance.reference = leaf_definition
        cls.leaf_definition = leaf_definition
        cls.leaf_cable = leaf_cable
        cls.leaf_wire = leaf_wire

        cable = definition.create_cable()
        wire = cable.create_wire()
        port = definition.create_port()
        pin = port.create_pin()
        outer_pin = top_instance.pins[pin]
        cls.cable = cable
        cls.wire = wire
        cls.port = port
        cls.pin = pin
        cls.outer_pin = outer_pin

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
        instances = list(sdn.get_instances([self.definition, self.definition]))
        self.assertEqual(len(instances), 1)

    def test_get_instances_in_library(self):
        instance1 = next(self.library.get_instances("MY_INST"))
        self.assertEqual(self.instance, instance1)

    def test_get_instances_in_netlist(self):
        instance1 = next(self.netlist.get_instances("MY_INST"))
        self.assertEqual(self.instance, instance1)

    def test_get_instances_from_netlist(self):
        instance1 = next(sdn.get_instances(self.netlist))
        self.assertEqual(self.instance, instance1)

    def test_get_instances_from_library(self):
        instance1 = next(sdn.get_instances(self.library))
        self.assertEqual(self.instance, instance1)

    def test_get_instances_from_definition_recursive(self):
        instance1 = list(sdn.get_instances(self.definition, recursive=True))
        self.assertEqual(self.instance, instance1[0])

    def test_from_definition_outside_recursive(self):
        instance1 = list(sdn.get_instances(self.definition, selection="OUTSIDE", recursive=True))
        self.assertEqual(self.top_instance, instance1[0])

    def test_from_leaf_definition_outside_recursive(self):
        instance1 = list(sdn.get_instances(self.leaf_definition, selection="OUTSIDE", recursive=True))
        self.assertEqual(len(instance1), 2)
        self.assertTrue(self.top_instance in instance1 and self.instance in instance1)

    def test_from_instance_recursive(self):
        instance1 = next(sdn.get_instances(self.top_instance, recursive=True))
        self.assertEqual(self.instance, instance1)

    def test_from_instance_outside_resursive(self):
        instance1 = list(sdn.get_instances(self.instance, selection="OUTSIDE", recursive=True))
        self.assertEqual(self.top_instance, instance1[0])

    def test_from_wire(self):
        instance1 = next(sdn.get_instances(self.wire))
        self.assertIs(self.top_instance, instance1)

    def test_from_outer_pin(self):
        instance1 = next(sdn.get_instances(self.outer_pin, "TOP_INST"))
        self.assertIs(self.top_instance, instance1)

    def test_from_inner_pin(self):
        instance1 = next(sdn.get_instances(self.pin, "TOP_INST"))
        self.assertIs(self.top_instance, instance1)

    def test_from_href_of_instance(self):
        top_href = next(sdn.get_hinstances(self.netlist.top_instance))
        instance1 = next(sdn.get_instances(top_href))
        self.assertIs(self.top_instance, instance1)

    def test_from_href_of_port(self):
        port_href = next(sdn.get_hports(self.port))
        instance1 = next(sdn.get_instances(port_href))
        self.assertIs(self.top_instance, instance1)
