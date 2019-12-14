import unittest
import spydrnet as sdn


class TestParsers(unittest.TestCase):
    def test_parse(self):
        self.assertRaises(RuntimeError, sdn.parse, "fakefile.fakeext")
