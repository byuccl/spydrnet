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
    filename = "ports_diff_modules.edf"
    out_filename = "ports_diff_modules_test.edf"
    parser = EdifParser.from_filename(filename)
    parser.parse()
    ir = parser.netlist

    triplicater = TMR()
    # cell_test = ['j_INST_0', 'b_INST_0', 'f_INST_0', "d_INST_0", 'h_INST_0', 'boston_INST_0']
    # net_test = ["h", "boston", "j"]
    cell_test = ["d_INST_0", "a"]
    # cell_test = ["a", "b"]
    net_test = ["d"]

    triplicater.run(cell_test, net_test, ir)
    compose = ComposeEdif()

    compose.run(ir, out_filename)
