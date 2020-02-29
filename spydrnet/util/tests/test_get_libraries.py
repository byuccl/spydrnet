import unittest
import spydrnet as sdn


class TestGetLibraries(unittest.TestCase):
    def test_parameter_checking(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        library.name = "MY_LIB"
        self.assertRaises(TypeError, sdn.get_libraries, netlist, "MY_LIB", patterns="MY_LIB")
        self.assertRaises(TypeError, sdn.get_libraries, netlist, "MY_LIB", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_libraries, None, "MY_LIB")
        self.assertRaises(TypeError, sdn.get_libraries, [None, netlist], "MY_LIB")

    def test_collection(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        library.name = "MY_LIB"
        ports = list(sdn.get_libraries([netlist, netlist]))
        self.assertEqual(len(ports), 1)
