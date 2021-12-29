import unittest

import spydrnet as sdn
from spydrnet.ir import FirstClassElement
from spydrnet.util.selection import Selection

class TestWire(unittest.TestCase):
    def setUp(self):
        self.definition_top = sdn.Definition()
        self.port_top = self.definition_top.create_port()
        self.inner_pin = self.port_top.create_pin()
        self.cable = self.definition_top.create_cable()
        self.wire = self.cable.create_wire()
        self.definition_leaf = sdn.Definition()
        self.port = self.definition_leaf.create_port()
        self.pin1 = self.port.create_pin()
        self.pin2 = self.port.create_pin()
        self.instance = self.definition_top.create_child()
        self.instance.reference = self.definition_leaf

    def test_constructor(self):
        self.assertFalse(isinstance(self.wire, FirstClassElement), "Wire should not extend element")
        wire2 = sdn.Wire()
        self.assertNotEqual(self.wire, wire2, "Unique items are considered equal")

    def test_pins_assignement(self):
        self.wire.connect_pin(self.instance.pins[self.pin1])
        self.wire.connect_pin(self.instance.pins[self.pin2])
        self.assertEqual(self.wire.pins, [self.instance.pins[self.pin1], self.instance.pins[self.pin2]])
        self.wire.pins = [self.instance.pins[self.pin2], self.instance.pins[self.pin1]]
        self.assertEqual(self.wire.pins, [self.instance.pins[self.pin2], self.instance.pins[self.pin1]])

    def test_connect_and_disconnect_inner_port(self):
        self.wire.connect_pin(self.inner_pin)
        self.assertTrue(self.inner_pin in self.wire.pins)
        self.assertEqual(self.inner_pin.wire, self.wire)
        self.assertEqual(len(self.wire.pins), 1)

        self.wire.disconnect_pin(self.inner_pin)
        self.assertFalse(self.inner_pin in self.wire.pins)
        self.assertIsNone(self.inner_pin.wire)
        self.assertEqual(len(self.wire.pins), 0)

    def test_connect_and_disconnect_outer_pin_by_reference(self):
        self.wire.connect_pin(self.instance.pins[self.pin1])
        self.assertEqual(len(self.wire.pins), 1)
        self.assertTrue(all(x is self.instance.pins[x] for x in self.wire.pins))
        self.assertTrue(all(x.wire is self.wire for x in self.wire.pins))
        self.assertTrue(all(x.instance is self.instance for x in self.wire.pins))
        self.assertEqual(self.instance.pins[self.pin1].inner_pin, self.pin1)

        self.wire.disconnect_pin(self.instance.pins[self.pin1])
        self.assertEqual(len(self.wire.pins), 0)
        self.assertFalse(self.instance.pins[self.pin1] in self.wire.pins)
        self.assertIsNone(self.instance.pins[self.pin1].wire)
        self.assertTrue(self.pin1 in self.instance.pins)

    def test_connect_and_disconnect_outer_pin_by_object(self):
        self.wire.connect_pin(sdn.OuterPin.from_instance_and_inner_pin(self.instance, self.pin2), position=0)
        self.assertEqual(len(self.wire.pins), 1)
        self.assertTrue(all(x is self.instance.pins[x] for x in self.wire.pins))
        self.assertTrue(all(x.wire is self.wire for x in self.wire.pins))
        self.assertTrue(all(x.instance is self.instance for x in self.wire.pins))
        self.assertEqual(self.instance.pins[self.pin2].inner_pin, self.pin2)

        self.wire.disconnect_pin(sdn.OuterPin(self.instance, self.pin2))
        self.assertEqual(len(self.wire.pins), 0)
        self.assertFalse(self.instance.pins[self.pin2] in self.wire.pins)
        self.assertIsNone(self.instance.pins[self.pin1].wire)
        self.assertTrue(self.pin1 in self.instance.pins)

    def test_disconnect_pin_from(self):
        self.wire.connect_pin(self.inner_pin)
        self.wire.connect_pin(self.instance.pins[self.pin1])
        self.wire.connect_pin(self.instance.pins[self.pin2])
        self.wire.disconnect_pins_from(iter((self.inner_pin, self.instance.pins[self.pin1])))
        self.wire.disconnect_pins_from({self.instance.pins[self.pin2]})
        self.assertEqual(len(self.wire.pins), 0)
        self.assertTrue(self.pin1 in self.instance.pins and isinstance(self.instance.pins[self.pin1], sdn.OuterPin) and
                        self.instance.pins[self.pin1].inner_pin == self.pin1)
        self.assertIsNone(self.inner_pin.wire)
        self.assertIsNone(self.instance.pins[self.pin1].wire)
        self.assertIsNone(self.instance.pins[self.pin2].wire)
        self.assertTrue(self.pin1 in self.instance.pins and isinstance(self.instance.pins[self.pin2], sdn.OuterPin) and
                        self.instance.pins[self.pin2].inner_pin == self.pin2)

    def test_get_driver(self):
        netlist = sdn.load_example_netlist_by_name('toggle')
        instance = next(netlist.get_instances('out_reg'))
        input_pin = next(instance.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.direction is sdn.IN and 'D' in x.inner_pin.port.name))
        driver = list(x for x in input_pin.wire.get_driver())
        self.assertTrue(len(driver) == 1)
        self.assertTrue('out_i_1' in driver[0].instance.name)
        self.assertEqual(driver[0].inner_pin.port.name, 'O')

    def test_get_driver_2(self):
        netlist = sdn.load_example_netlist_by_name('adder')
        instance = next(netlist.get_instances('a'))
        cable = next(instance.get_cables('a'))
        wire = cable.wires[0]
        driver = list(x for x in wire.get_driver())
        self.assertTrue(len(driver) == 1)
        self.assertTrue('a[8:0]' in driver[0].port.name)

    @unittest.expectedFailure
    def test_disconnect_inner_pin_from_outside_wire(self):
        inner_pin = sdn.InnerPin()
        self.wire.disconnect_pins_from([inner_pin])

    @unittest.expectedFailure
    def test_disconnect_outer_pin_from_outside_wire(self):
        outer_pin = sdn.OuterPin()
        self.wire.disconnect_pins_from([outer_pin])

    def test_print_no_cable(self):
        wire = sdn.Wire()
        self.assertTrue('Not contained by any Cable' in wire.__str__())

    def test_print_cable_name(self):
        cable = sdn.Cable('cable')
        wire = cable.create_wire()
        self.assertTrue("Contained by Cable.name 'cable'" in wire.__str__())
