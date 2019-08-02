from spydrnet.transform.replicate import Replicator
from spydrnet.transform.DWCInserter import DWCInserter
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
import spydrnet.support_files as files

class DWC:
    def __init__(self):
        self.replicator = Replicator(2)
        self.inserter = DWCInserter()

    def run(self, cell_target, net_target, ir=None):
        self.replicator.run(cell_target, ir)
        self.inserter.run(net_target, ir)


if __name__ == "__main__":
    filename = files.edif_files["three_layer_hierarchy.edf"]
    out_filename = "three_layer_hierarchyy_test.edf"
    parser = EdifParser.from_filename(filename)
    parser.parse()
    ir = parser.netlist

    triplicater = DWC()
    # cell_test = ['j_INST_0', 'b_INST_0', 'f_INST_0', "d_INST_0", 'h_INST_0', 'boston_INST_0']
    # net_test = ["h", "boston", "j"]
    cell_test = ["b_INST_0", "beta_INST_0", 'y_INST_0']
    # cell_test = ["a", "b"]
    net_test = ["b", "beta", 'y']

    triplicater.run(cell_test, net_test, ir)
    compose = ComposeEdif()

    compose.run(ir, out_filename)
