import unittest

import spydrnet as sdn
from spydrnet.ir import Pin


class TestInnerPin(unittest.TestCase):
    def setUp(self) -> None:
        self.pin = sdn.InnerPin()

    def test_constructor(self):
        self.assertIsInstance(self.pin, Pin)
        self.assertTrue(self.pin)
        pin2 = sdn.InnerPin()
        self.assertNotEqual(self.pin, pin2)

    def test_port(self):
        self.assertIsNone(self.pin.port)

    @unittest.expectedFailure
    def test_port_set(self):
        self.pin.port = None