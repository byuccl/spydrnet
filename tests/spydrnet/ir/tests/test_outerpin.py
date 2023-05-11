import unittest

import spydrnet as sdn
from spydrnet.ir import Pin


class TestOuterPin(unittest.TestCase):
    def setUp(self) -> None:
        self.pin = sdn.OuterPin()

    def test_constructor(self):
        self.assertIsInstance(self.pin, Pin)
        self.assertTrue(self.pin)

    def test_equal(self):
        outer_pin = sdn.OuterPin()
        self.assertEqual(outer_pin, self.pin)
        inner_pin = sdn.InnerPin()
        instance = sdn.Instance()
        outer_pin1 = sdn.OuterPin.from_instance_and_inner_pin(instance, inner_pin)
        outer_pin2 = sdn.OuterPin.from_instance_and_inner_pin(instance, inner_pin)
        self.assertEqual(outer_pin1, outer_pin2)
        self.assertNotEqual(self.pin, outer_pin1)
        self.assertNotEqual(self.pin, None)

    def test_hash(self):
        outer_pin = sdn.OuterPin()
        self.assertEqual(hash(outer_pin), hash(self.pin))
        inner_pin = sdn.InnerPin()
        instance = sdn.Instance()
        outer_pin1 = sdn.OuterPin.from_instance_and_inner_pin(instance, inner_pin)
        outer_pin2 = sdn.OuterPin.from_instance_and_inner_pin(instance, inner_pin)
        self.assertEqual(hash(outer_pin1), hash(outer_pin2))