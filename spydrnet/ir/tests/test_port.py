import unittest

import spydrnet as sdn
from spydrnet.ir import Bundle


class TestPort(unittest.TestCase):
    def setUp(self) -> None:
        self.port = sdn.Port()

    def test_direction_enum(self):
        self.assertEqual(sdn.Port.Direction.UNDEFINED, sdn.UNDEFINED)
        self.assertEqual(sdn.Port.Direction.IN, sdn.IN)
        self.assertEqual(sdn.Port.Direction.OUT, sdn.OUT)
        self.assertEqual(sdn.Port.Direction.INOUT, sdn.INOUT)

    def test_constructor(self):
        self.assertIsInstance(self.port, Bundle)
        self.assertTrue(self.port, "Constructor returns None type or empty collection.")
        port2 = sdn.Port()
        self.assertNotEqual(self.port, port2, "Unique objects are considered equal.")

    def test_pins_set(self):
        pin1 = self.port.create_pin()
        pin2 = self.port.create_pin()
        self.assertEqual(self.port.pins, [pin1, pin2])
        self.port.pins = [pin2, pin1]
        self.assertEqual(self.port.pins, [pin2, pin1])

    def test_direction(self):
        for ii in range(4):
            self.port.direction = ii
            self.assertEqual(self.port.direction.value, ii)
        directions = ['undefined', 'in', 'out', 'inout']
        for direction in directions:
            self.port.direction = direction
            self.assertEqual(self.port.direction.name.lower(), direction.lower())
        for direction in sdn.Port.Direction:
            self.port.direction = direction
            self.assertEqual(self.port.direction, direction)

    def test_direction_2(self):
        port = sdn.Port(direction=sdn.IN)
        self.assertTrue(port.direction is sdn.IN)

    @unittest.expectedFailure
    def test_direction_set_bad_type(self):
        self.port.direction = list()

    def test_initialize_pins(self):
        self.port.create_pins(2)
        self.assertEqual(len(self.port.pins), 2)
        self.assertNotEqual(self.port.pins[0], self.port.pins[1])

    def test_create_pin(self):
        pin = self.port.create_pin()
        self.assertTrue(pin in self.port.pins)
        self.assertEqual(pin.port, self.port)

    def test_add_pin(self):
        pin = sdn.InnerPin()
        self.port.add_pin(pin, position=0)
        self.assertTrue(pin in self.port.pins)
        self.assertEqual(pin.port, self.port)
        self.assertEqual(self.port.pins.count(pin), 1)

    def test_remove_pin(self):
        pin = self.port.create_pin()
        self.port.remove_pin(pin)
        self.assertFalse(pin in self.port)
        self.assertIsNone(pin.port)

    @unittest.expectedFailure
    def test_remove_pins_outside_port(self):
        pin = sdn.InnerPin()
        self.port.remove_pins_from((pin,))

    def test_remove_pins_from(self):
        pin_included = self.port.create_pin()
        pin = self.port.create_pin()
        self.port.remove_pins_from({pin})
        self.assertFalse(pin in self.port.pins)
        self.assertIsNone(pin.port)
        self.assertTrue(pin_included in self.port.pins)
        self.assertEqual(pin_included.port, self.port)

    def test_is_scalar(self):
        self.assertTrue(self.port.is_scalar)
        self.port.is_scalar = False
        self.assertFalse(self.port.is_scalar)
        self.port.is_scalar = True
        self.assertTrue(self.port.is_scalar)
        self.port.create_pins(2)
        self.assertFalse(self.port.is_scalar)
        self.port.is_scalar = False
        self.port.remove_pins_from(self.port.pins)
        self.assertFalse(self.port.is_scalar)

    @unittest.expectedFailure
    def test_is_scalar_set_on_array_bundle(self):
        self.port.create_pins(2)
        self.port.is_scalar = True

    def test_is_array(self):
        self.assertFalse(self.port.is_array)
        self.port.is_array = True
        self.assertTrue(self.port.is_array)
        self.port.is_array = False
        self.assertFalse(self.port.is_array)
        self.port.create_pins(2)
        self.assertTrue(self.port.is_array)
        self.port.is_array = True
        self.port.remove_pins_from(self.port.pins)
        self.assertTrue(self.port.is_array)

    @unittest.expectedFailure
    def test_is_array_clear_on_array_bundle(self):
        self.port.create_pins(2)
        self.port.is_array = False
