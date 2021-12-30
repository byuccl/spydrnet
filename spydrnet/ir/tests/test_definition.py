import unittest

import spydrnet as sdn
from spydrnet.ir import FirstClassElement


class TestDefinition(unittest.TestCase):
    def setUp(self):
        self.definition = sdn.Definition()

    def test_constructor(self):
        self.assertIsInstance(self.definition, FirstClassElement, "Definition is not an element.")
        self.assertTrue(self.definition, "Constructor returns None type or empty collection.")
        definition2 = sdn.Definition()
        self.assertNotEqual(self.definition, definition2, "Unique objects are considered equal.")

    @unittest.expectedFailure
    def test_assign_library(self):
        library = sdn.Library()
        self.definition.library = library

    def test_ports_set(self):
        port1 = self.definition.create_port()
        port2 = self.definition.create_port()
        self.assertEqual(self.definition.ports, [port1, port2])
        self.definition.ports = [port2, port1]
        self.assertEqual(self.definition.ports, [port2, port1])

    def test_create_port(self):
        port = self.definition.create_port("Port1", pins=2)
        self.assertEqual(port.name, "Port1")
        self.assertEqual(len(port.pins), 2)
        self.assertTrue(port in self.definition.ports)
        self.assertEqual(port.definition, self.definition)

    def test_add_port(self):
        port = sdn.Port()
        self.definition.add_port(port, position=0)
        self.assertTrue(port in self.definition.ports)
        self.assertEqual(port.definition, self.definition)
        self.assertEqual(self.definition.ports.count(port), 1)

    def test_remove_port(self):
        port = self.definition.create_port()
        self.definition.remove_port(port)
        self.assertFalse(port in self.definition.ports)
        self.assertIsNone(port.definition)

    def test_remove_multiple_ports(self):
        port = self.definition.create_port()
        port_2 = self.definition.create_port()
        self.definition.remove_ports_from([port,port_2])
        self.assertFalse(port in self.definition.ports)
        self.assertFalse(port_2 in self.definition.ports)
        self.assertIsNone(port.definition)
        self.assertIsNone(port_2.definition)

    @unittest.expectedFailure
    def test_remove_ports_from_outside_definition(self):
        port = sdn.Port()
        self.definition.remove_ports_from((port,))

    def test_remove_ports_from(self):
        port_included = self.definition.create_port()
        port = self.definition.create_port()
        self.definition.remove_ports_from((port,))
        self.assertFalse(port in self.definition.ports)
        self.assertIsNone(port.definition)

        port = self.definition.create_port()
        self.definition.remove_ports_from({port})
        self.assertFalse(port in self.definition.ports)
        self.assertIsNone(port.definition)

        self.assertTrue(port_included in self.definition.ports)
        self.assertEqual(port_included.definition, self.definition)

    def test_cables_set(self):
        cable1 = self.definition.create_cable()
        cable2 = self.definition.create_cable()
        self.assertEqual(self.definition.cables, [cable1, cable2])
        self.definition.cables = [cable2, cable1]
        self.assertEqual(self.definition.cables, [cable2, cable1])

    def test_create_cable(self):
        cable = self.definition.create_cable("cable1", wires=2)
        self.assertEqual(cable.name, "cable1")
        self.assertEqual(len(cable.wires), 2)
        self.assertTrue(cable in self.definition.cables)
        self.assertEqual(self.definition, cable.definition)

    def test_add_cable(self):
        cable = sdn.Cable()
        self.definition.add_cable(cable, position=0)
        self.assertTrue(cable in self.definition.cables)
        self.assertEqual(cable.definition, self.definition)
        self.assertEqual(self.definition.cables.count(cable), 1)

    def test_remove_cable(self):
        cable = self.definition.create_cable()
        self.definition.remove_cable(cable)
        self.assertFalse(cable in self.definition.cables)
        self.assertIsNone(cable.definition)

    @unittest.expectedFailure
    def test_remove_cables_from_outside_definition(self):
        cable = sdn.Cable()
        self.definition.remove_cables_from({cable})

    def test_remove_cables_from(self):
        cable_included = self.definition.create_cable()
        cable = self.definition.create_cable()
        self.definition.remove_cables_from({cable})
        self.assertFalse(cable in self.definition.cables)
        self.assertIsNone(cable.definition)
        self.assertTrue(cable_included in self.definition.cables)
        self.assertEqual(cable_included.definition, self.definition)

    def test_children_set(self):
        child1 = self.definition.create_child()
        child2 = self.definition.create_child()
        self.assertEqual(self.definition.children, [child1, child2])
        self.definition.children = [child2, child1]
        self.assertEqual(self.definition.children, [child2, child1])

    def test_create_child(self):
        instance = self.definition.create_child()
        self.assertTrue(instance in self.definition.children)
        self.assertEqual(instance.parent, self.definition)

    def test_add_child(self):
        instance = sdn.Instance()
        self.definition.add_child(instance, position=0)
        self.assertTrue(instance in self.definition.children)
        self.assertEqual(instance.parent, self.definition)
        self.assertEqual(self.definition.children.count(instance), 1)

    def test_remove_child(self):
        instance = self.definition.create_child()
        self.definition.remove_child(instance)
        self.assertFalse(instance in self.definition.children)
        self.assertIsNone(instance.parent)

    @unittest.expectedFailure
    def test_remove_children_from_outside_definition(self):
        instance = sdn.Instance()
        self.definition.remove_children_from((instance,))

    def test_remove_children_from(self):
        instance_included = self.definition.create_child()

        instance = self.definition.create_child()
        self.definition.remove_children_from((instance,))
        self.assertFalse(instance in self.definition.children)
        self.assertIsNone(instance.parent)

        instance = self.definition.create_child()
        self.definition.remove_children_from({instance})
        self.assertFalse(instance in self.definition.children)
        self.assertIsNone(instance.parent)

        self.assertTrue(instance_included in self.definition.children)
        self.assertEqual(instance_included.parent, self.definition)

    def test_is_leaf(self):
        self.assertTrue(self.definition.is_leaf()), "Empty definition is not considered a leaf cell"
        self.definition.create_port()
        self.assertTrue(self.definition.is_leaf()), "Empty definition with a port is not considered a leaf cell"
        self.definition.create_cable()
        self.assertFalse(self.definition.is_leaf()), "Definition with a cable is considered a leaf cell"
        self.definition.remove_cables_from(self.definition.cables)
        self.definition.create_child()
        self.assertFalse(self.definition.is_leaf()), "Definition with a child instance is considered a leaf cell"
        self.definition.create_cable()
        self.assertFalse(self.definition.is_leaf()), "Definition with a cable and child instance is considered a leaf" \
                                                     " cell"

    def test_library_name(self):
        definition = sdn.Definition()
        library = sdn.Library()
        library.add_definition(definition)
        self.assertTrue('Library.name undefined' in definition.__str__())
        library.name = 'library'
        self.assertTrue('Library.name \'library\'' in definition.__str__())
