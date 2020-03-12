import unittest

import spydrnet as sdn
from spydrnet.ir.first_class_element import FirstClassElement


class TestInstance(unittest.TestCase):
    def setUp(self) -> None:
        self.instance = sdn.Instance()

    def test_constructor(self):
        self.assertIsInstance(self.instance, FirstClassElement, "Instance should extend element")
        instance2 = sdn.Instance()
        self.assertNotEqual(self.instance, instance2, "Unique objects are considered equal")

    def test_reference_assignment(self):
        definition = sdn.Definition()
        self.instance.reference = definition
        self.assertEqual(self.instance.reference, definition)
        self.assertTrue(self.instance in definition.references)

    def test_reference_assignment_with_pins(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()

        self.instance.reference = definition
        self.assertTrue(pin1 in self.instance.pins)
        self.assertTrue(pin2 in self.instance.pins)
        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]
        self.assertIsInstance(outer_pin1, sdn.OuterPin)
        self.assertIsInstance(outer_pin2, sdn.OuterPin)
        self.assertEqual(outer_pin1.instance, self.instance)
        self.assertEqual(outer_pin2.instance, self.instance)
        self.assertEqual(outer_pin1.inner_pin, pin1)
        self.assertEqual(outer_pin2.inner_pin, pin2)

        wire = sdn.Wire()
        wire.connect_pin(outer_pin1)
        wire.connect_pin(outer_pin2)
        self.instance.reference = None
        self.assertEqual(len(self.instance.pins), 0)
        self.assertIsNone(outer_pin1.wire)
        self.assertIsNone(outer_pin2.wire)
        self.assertIsNone(outer_pin1.instance)
        self.assertIsNone(outer_pin2.instance)
        self.assertIsNone(outer_pin2.inner_pin)
        self.assertIsNone(outer_pin2.inner_pin)

    def test_post_assignment_pin_and_port_removal(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()

        self.instance.reference = definition
        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]

        wire = sdn.Wire()
        wire.connect_pin(outer_pin1)
        wire.connect_pin(outer_pin2)

        port.remove_pin(pin1)
        definition.remove_port(port)

        self.assertIsNone(outer_pin1.wire)
        self.assertIsNone(outer_pin1.instance)
        self.assertIsNone(outer_pin1.inner_pin)
        self.assertIsNone(outer_pin2.wire)
        self.assertIsNone(outer_pin2.instance)
        self.assertIsNone(outer_pin2.inner_pin)
        self.assertFalse(outer_pin1 in wire.pins)
        self.assertFalse(outer_pin2 in wire.pins)
        self.assertFalse(outer_pin1 in self.instance.pins)
        self.assertFalse(outer_pin2 in self.instance.pins)
        self.assertFalse(pin1 in self.instance.pins)
        self.assertFalse(pin2 in self.instance.pins)

    def test_post_assignment_pin_and_port_creation(self):
        definition = sdn.Definition()
        self.instance.reference = definition
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()
        port2 = sdn.Port()
        pin3 = port2.create_pin()
        definition.add_port(port2)
        pin4 = port2.create_pin()

        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]
        outer_pin3 = self.instance.pins[pin3]
        outer_pin4 = self.instance.pins[pin4]

        wire = sdn.Wire()
        wire.connect_pin(outer_pin1)
        wire.connect_pin(outer_pin2)
        wire.connect_pin(outer_pin3)
        wire.connect_pin(outer_pin4)
        inner_pins = [pin1, pin2, pin3, pin4]
        outer_pins = [outer_pin1, outer_pin2, outer_pin3, outer_pin4]
        for outer_pin, inner_pin in zip(outer_pins, inner_pins):
            self.assertEqual(outer_pin.wire, wire)
            self.assertTrue(outer_pin in wire.pins)
            self.assertEqual(outer_pin.instance, self.instance)
            self.assertEqual(outer_pin.inner_pin, inner_pin)
            self.assertTrue(outer_pin in self.instance.pins)
            self.assertTrue(inner_pin in self.instance.pins)

    def test_reference_reassignment(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()
        self.instance.reference = definition
        self.assertTrue(self.instance in definition.references)
        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]

        definition2 = sdn.Definition()
        port = definition2.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()
        self.instance.reference = definition2
        self.assertTrue(self.instance not in definition.references)
        self.assertTrue(self.instance in definition2.references)
        self.assertEqual(outer_pin1, self.instance.pins[pin1])
        self.assertEqual(outer_pin2, self.instance.pins[pin2])

    def test_reference_removal(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()
        self.instance.reference = definition
        self.assertTrue(self.instance in definition.references)
        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]
        self.assertEqual(outer_pin1.inner_pin, pin1)
        self.assertEqual(outer_pin2.inner_pin, pin2)

        del self.instance.reference
        self.assertTrue(self.instance not in definition.references)
        self.assertIsNone(outer_pin1.inner_pin)
        self.assertIsNone(outer_pin2.inner_pin)

