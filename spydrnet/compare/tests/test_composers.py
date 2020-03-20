import unittest
import spydrnet as sdn

class TestComposers(unittest.TestCase):
    def test_compose(self):
        netlist = sdn.Netlist()
        self.assertRaises(RuntimeError, sdn.compose, netlist, "fakefile.fakeext")
