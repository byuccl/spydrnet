import unittest

from spydrnet.ir.first_class_element import FirstClassElement
from spydrnet.ir.pin import Pin


class TestPin(unittest.TestCase):
    def setUp(self):
        self.pin = Pin()

    def test_constructor(self):
        self.assertFalse(isinstance(self.pin, FirstClassElement))
        self.assertTrue(self.pin)
        pin2 = Pin()
        self.assertNotEqual(self.pin, pin2)

    def test_wire(self):
        self.assertIsNone(self.pin.wire)

    @unittest.expectedFailure
    def test_wire_set(self):
        self.pin.wire = None

    def test_no_wire(self):
        pin = Pin()
        self.assertTrue('Wire connected undefined' in pin.__str__())
