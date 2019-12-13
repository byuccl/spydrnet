import unittest

from spydrnet.ir.element import Element
from spydrnet.ir.pin import Pin


class TestPin(unittest.TestCase):
    def setUp(self):
        self.pin = Pin()

    def test_constructor(self):
        self.assertFalse(isinstance(self.pin, Element))
        self.assertTrue(self.pin)
        pin2 = Pin()
        self.assertNotEqual(self.pin, pin2)

    def test_wire(self):
        self.assertIsNone(self.pin.wire)

    @unittest.expectedFailure
    def test_wire_set(self):
        self.pin.wire = None