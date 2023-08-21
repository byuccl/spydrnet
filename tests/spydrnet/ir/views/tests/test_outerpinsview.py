import unittest
import spydrnet as sdn


class TestOuterPinsView(unittest.TestCase):
    def setUp(self) -> None:
        definition = sdn.Definition()
        port = definition.create_port()
        self.inner_pins = port.create_pins(10)
        self.instance = sdn.Instance()
        self.instance.reference = definition
        self.outer_pins_view = self.instance.pins

    def test_contains(self):
        self.assertTrue(all(x in self.outer_pins_view for x in self.inner_pins))
        self.assertTrue(all(sdn.OuterPin(self.instance, x) in self.outer_pins_view for x in self.inner_pins))

    def test_equal(self):
        self.assertEqual(self.outer_pins_view, dict(map(lambda x: (x, sdn.OuterPin(self.instance, x)),
                                                        self.inner_pins)))

    def test_getitem(self):
        self.assertTrue(all(self.outer_pins_view[x] == sdn.OuterPin(self.instance, x) for x in self.inner_pins))
        self.assertTrue(all(self.outer_pins_view[x] is self.outer_pins_view[sdn.OuterPin(self.instance, x)] for x in
                            self.inner_pins))

    def test_iter(self):
        self.assertTrue(all(isinstance(x, sdn.OuterPin) for x in self.outer_pins_view))

    def test_len(self):
        self.assertEqual(len(self.outer_pins_view), 10)

    def test_get(self):
        self.assertEqual(self.outer_pins_view.get(self.inner_pins[0]), sdn.OuterPin(self.instance, self.inner_pins[0]))
        self.assertEqual(self.outer_pins_view.get(sdn.OuterPin(self.instance, self.inner_pins[0])),
                         sdn.OuterPin(self.instance, self.inner_pins[0]))
