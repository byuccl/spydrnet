import unittest
import spydrnet as sdn
from spydrnet import get_libraries


class TestUtil(unittest.TestCase):
    def test_single_object(self):
        netlist = sdn.Netlist()
        library1 = netlist.create_library()
        library1.name = "work"
        library2 = netlist.create_library()
        library2.name = "hdi_primitives"
        library = next(get_libraries(netlist, "work"))
        self.assertEqual(library1, library)

    def test_multiple_objects(self):
        netlist1 = sdn.Netlist()
        library1 = netlist1.create_library()
        netlist2 = sdn.Netlist()
        library2 = netlist2.create_library()
        get_libraries([netlist1, netlist2])

