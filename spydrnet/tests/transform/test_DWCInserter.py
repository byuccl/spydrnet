import unittest

from spydrnet.transform.DWCInserter import DWCInserter
from spydrnet.parsers.edif.parser import EdifParser
import spydrnet.support_files as files
from spydrnet.transform.DWC import DWC
from spydrnet.ir import *

class test_DWCInserter(unittest.TestCase):

    def test_black_box_ports(self):
        parser = EdifParser.from_filename(files.edif_files["three_layer_hierarchy.edf"])
        parser.parse()
        ir = parser.netlist

        duplicaater = DWC()
        cell_test = ["b_INST_0", "beta_INST_0", 'y_INST_0', 'battleship_OBUF_inst_i_1']
        net_test = ["b", "beta", 'y', 'battleship_OBUF']
        duplicaater.run(cell_test, net_test, ir)
        top_definition = ir.top_instance.definition
        dwc_jtag_interface = top_definition.lookup_element(Instance, 'EDIF.identifier', 'dwc_jtag_interface')
        I0_port = dwc_jtag_interface.definition.lookup_element(Port, 'EDIF.identifier', 'I0')
        I1_port = dwc_jtag_interface.definition.lookup_element(Port, 'EDIF.identifier', 'I1')
        for x in range(len(I0_port.inner_pins)):
            I0_outer_pin = dwc_jtag_interface.outer_pins[I0_port.inner_pins[x]]
            I0_cable = I0_outer_pin.wire.cable
            I1_outer_pin = dwc_jtag_interface.outer_pins[I1_port.inner_pins[x]]
            I1_cable = I1_outer_pin.wire.cable
            self.assertTrue(I0_cable.comparator is I1_cable.comparator.partner_comparator)
            self.assertTrue(I1_cable.comparator is I0_cable.comparator.partner_comparator)


if __name__ == '__main__':
    unittest.main()