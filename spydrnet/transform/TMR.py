from spydrnet.transform.replicate import Replicator
from spydrnet.transform.inserter import TMRInserter
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif

class TMR:
    def __init__(self):
        self.replicator = Replicator(3)
        self.inserter = TMRInserter()

    def run(self, cell_target, net_target, ir=None):
        self.replicator.run(cell_target, ir)
        self.inserter.run(net_target, ir)


if __name__ == "__main__":
<<<<<<< transformation-unit_test
<<<<<<< transformation-unit_test
    filename = "ports_diff_modules.edf"
    out_filename = "ports_diff_modules_test.edf"
=======
    filename = "add.edf"
    out_filename = "add_test.edf"
>>>>>>> Add basic TMR functionality
=======
    filename = "ports_diff_modules.edf"
    out_filename = "ports_diff_modules_test.edf"
>>>>>>> Implemented TMR across hierarchy
    parser = EdifParser.from_filename(filename)
    parser.parse()
    ir = parser.netlist

    triplicater = TMR()
<<<<<<< transformation-unit_test
<<<<<<< transformation-unit_test
=======
>>>>>>> Implemented TMR across hierarchy
    # cell_test = ['j_INST_0', 'b_INST_0', 'f_INST_0', "d_INST_0", 'h_INST_0', 'boston_INST_0']
    # net_test = ["h", "boston", "j"]
    cell_test = ["d_INST_0", "a"]
    # cell_test = ["a", "b"]
    net_test = ["d"]
<<<<<<< transformation-unit_test
=======
    cell_test = ["add0", "co_INST_0", "add7", "a", "seg", "seg2"]
    # net_test = ["segment_OBUF_7_"]
    net_test = ["s_0_", "c_0", "co", "c_7", "s_7_", "led_OBUF_0_", "led_OBUF_1_", "led_OBUF_2_", "led_OBUF_3_",
                "led_OBUF_4_", "led_OBUF_5_", "led_OBUF_6_", "led_OBUF_7_", "led_OBUF_8_", "segment_OBUF_6_",
                "segment_OBUF_5_", "segment_OBUF_4_", "segment_OBUF_3_", "segment_OBUF_2_", "segment_OBUF_1_",
                "segment_OBUF_0_", "segment_2_"]
    # net_test = ["segment_OBUF_6_", "segment_OBUF_5_", "segment_OBUF_4_", "segment_OBUF_3_",
    #             "segment_OBUF_2_", "segment_OBUF_1_", "segment_OBUF_0_", "segment1_2_", "segment1_3_"]
    # cell_test = ["out_0__i_1", "out_reg_0_", "out_reg_1_"]
    # cell_test = ["out_0__i_1", "out_reg_0_", "out_1__i_1", "out_reg_1_", "out_2__i_1", "out_reg_2_", "out_3__i_1",
    #             "out_reg_3_"]
    # net_test = ["out_OBUF_0_", "out_OBUF_1_"]
    # net_test = ["out_OBUF_0_", "out_OBUF_1_", "out_OBUF_2_", "out_OBUF_3_"]
>>>>>>> Add basic TMR functionality
=======
>>>>>>> Implemented TMR across hierarchy

    triplicater.run(cell_test, net_test, ir)
    compose = ComposeEdif()

    compose.run(ir, out_filename)
