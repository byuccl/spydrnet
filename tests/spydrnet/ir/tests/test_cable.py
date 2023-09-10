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

    def test_check_concat(self):
        # TODO: test connections to inner_pins as well
        port0 = sdn.Port(name="p0", direction=sdn.Port.Direction.OUT)
        port1 = sdn.Port(name="p1", direction=sdn.Port.Direction.IN)
        port2 = sdn.Port(name="p2", direction=sdn.Port.Direction.IN)
        port0.create_pins(4)
        port1.create_pins(4)
        port2.create_pins(4)
        self.cable.create_wires(4)
        for wire in self.cable.wires:
            wire.connect_pin(port0.pins[wire.index()])
            wire.connect_pin(port1.pins[wire.index()])
            wire.connect_pin(port2.pins[wire.index()])
        self.assertTrue(self.cable.check_concat())
        port1._pins = port1.pins[::-1]
        self.assertFalse(self.cable.check_concat())
        port1._pins = port1.pins[::-1]
        self.assertTrue(self.cable.check_concat())
        self.cable.wires[-1].disconnect_pin(port2.pins[-1])
        self.assertFalse(self.cable.check_concat())
        self.cable.wires[-1].connect_pin(port2.pins[-1])
        self.assertTrue(self.cable.check_concat())
        new_pin = port2.create_pin()
        self.assertFalse(self.cable.check_concat())
        port2.remove_pin(new_pin)
        self.assertTrue(self.cable.check_concat())
        port2.add_pin(new_pin, position=0)
        self.assertFalse(self.cable.check_concat())

    def test_connect_port_1(self):
        port = sdn.Port(name="p0", direction=sdn.Port.Direction.IN)
        port.create_pins(4)
        w = self.cable.create_wires(4)
        self.assertIsNone(self.cable.connect_port(port))
        self.assertTrue(port.pins[0].wire is w[0])
        self.assertTrue(port.pins[1].wire is w[1])
        self.assertTrue(port.pins[2].wire is w[2])
        self.assertTrue(port.pins[3].wire is w[3])

    def test_connect_port_2(self):
        port = sdn.Port(name="p0",
                        direction=sdn.Port.Direction.IN,
                        is_downto=False)
        port.create_pins(4)
        w = self.cable.create_wires(4)
        self.assertIsNone(self.cable.connect_port(port))
        self.assertTrue(port.pins[0].wire is w[3])
        self.assertTrue(port.pins[1].wire is w[2])
        self.assertTrue(port.pins[2].wire is w[1])
        self.assertTrue(port.pins[3].wire is w[0])

    def test_connect_instance_port(self):
        top = sdn.Definition(name="top")
        module = sdn.Definition(name="module1")
        port = module.create_port(name="p0",
                            direction=sdn.Port.Direction.IN,
                            is_downto=False)
        port.create_pins(4)
        inst1 = top.create_child(name="inst1", reference=module)

        w = self.cable.create_wires(4)
        self.assertIsNone(self.cable.connect_instance_port(inst1, port))
        self.assertTrue(inst1.pins[port.pins[0]].wire is w[3])
        self.assertTrue(inst1.pins[port.pins[1]].wire is w[2])
        self.assertTrue(inst1.pins[port.pins[2]].wire is w[1])
        self.assertTrue(inst1.pins[port.pins[3]].wire is w[0])

    def test_merge_cables(self):
        cable1 = sdn.Cable()
        cable2 = sdn.Cable()
        w_1 = cable1.create_wires(2)
        w_2 = cable2.create_wires(4)
        self.cable.merge_cables([cable1, cable2])
        self.assertEqual(self.cable.size, 6)
        for indx, wire in enumerate(w_2[::-1] + w_1[::-1]):
            self.assertEqual(self.cable.wires[indx], wire)
        self.assertEqual(cable1.wires, [])
        self.assertEqual(cable1.wires, [])
    def test_scalar_false(self):
        cable = sdn.Cable()
        cable.create_wire()
        cable.create_wire()
        self.assertTrue("is_scalar: False;" in cable.__str__())
