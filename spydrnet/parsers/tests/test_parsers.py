import unittest
import os
import spydrnet as sdn
from spydrnet.util.netlist_type import VERILOG, EBLIF
from spydrnet.util.architecture import XILINX_7SERIES


class TestParsers(unittest.TestCase):
    def test_parse(self):
        self.assertRaises(RuntimeError, sdn.parse, "fakefile.fakeext")



class TestParseWithArchitecture(unittest.TestCase):
    def test_verilog(self):
        netlist = sdn.load_example_netlist_by_name("b13", VERILOG)
        netlist.compose("b13.v", write_blackbox = False)

        netlist_1 = sdn.parse("b13.v")
        for definition in netlist_1.get_definitions():
            if definition is not netlist_1.top_instance.reference:
                for port in definition.get_ports():
                    self.assertEqual(port.direction, sdn.UNDEFINED)

        netlist_2 = sdn.parse("b13.v", XILINX_7SERIES)
        for definition in netlist_2.get_definitions():
            if definition is not netlist_2.top_instance.reference:
                for port in definition.get_ports():
                    self.assertNotEqual(port.direction, sdn.UNDEFINED, definition.name)

        os.remove("b13.v")
    
    def test_eblif(self):
        netlist = sdn.load_example_netlist_by_name("toggle", EBLIF)
        netlist.compose("toggle.eblif", write_blackbox = False)

        netlist_1 = sdn.parse("toggle.eblif")
        for definition in netlist_1.get_definitions():
            if definition is not netlist_1.top_instance.reference and "logic-gate" not in definition.name:
                for port in definition.get_ports():
                    self.assertEqual(port.direction, sdn.UNDEFINED, definition.name)

        netlist_2 = sdn.parse("toggle.eblif", XILINX_7SERIES)
        for definition in netlist_2.get_definitions():
            if definition is not netlist_2.top_instance.reference:
                for port in definition.get_ports():
                    self.assertNotEqual(port.direction, sdn.UNDEFINED, definition.name)

        os.remove("toggle.eblif")
