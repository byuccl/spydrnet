import unittest

import spydrnet as sdn


class TestCable(unittest.TestCase):
    def setUp(self) -> None:
        self.cable = sdn.Cable()

    def test__items(self):
        self.assertEqual(self.cable._items(), self.cable._wires)

    def test_initialize_wires(self):
        self.cable.create_wires(2)
        self.assertEqual(len(self.cable.wires), 2)
        self.cable.remove_wires_from(self.cable.wires)
        self.assertEqual(len(self.cable.wires), 0)

    def test_wires_set(self):
        wire1 = self.cable.create_wire()
        wire2 = self.cable.create_wire()
        self.assertEqual(self.cable.wires, [wire1, wire2])
        self.cable.wires = [wire2, wire1]
        self.assertEqual(self.cable.wires, [wire2, wire1])

    def test_create_wire(self):
        wire = self.cable.create_wire()
        self.assertTrue(wire in self.cable.wires)
        self.assertEqual(wire.cable, self.cable)

    def test_add_wire(self):
        wire = sdn.Wire()
        self.cable.add_wire(wire, position=0)
        self.assertTrue(wire in self.cable.wires)
        self.assertEqual(wire.cable, self.cable)

    def test_remove_wire(self):
        wire = self.cable.create_wire()
        self.cable.remove_wire(wire)
        self.assertFalse(wire in self.cable.wires)
        self.assertIsNone(wire.cable)

    def test_remove_wire_from(self):
        wire_included = self.cable.create_wire()
        wire = self.cable.create_wire()
        self.cable.remove_wires_from({wire})
        self.assertFalse(wire in self.cable.wires)
        self.assertIsNone(wire.cable)
        self.assertTrue(wire_included in self.cable.wires)
        self.assertEqual(wire_included.cable, self.cable)

    def test_scalar_false(self):
        cable = sdn.Cable()
        cable.create_wire()
        cable.create_wire()
        self.assertTrue('is_scalar: False;' in cable.__str__())
