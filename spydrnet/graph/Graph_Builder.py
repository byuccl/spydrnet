from spydrnet.ir import *
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.utility.utility import Utility

import networkx as nx
import matplotlib.pyplot as plt

class Graph_Buider:
    def __init__(self):
        self.ir_graph = nx.DiGraph()
        self.lookup = None

    def build_graph(self, ir):
        self.lookup = HierarchicalLookup(ir)
        util = Utility()
        leaf_cells = util.get_leaf_cells(ir)
        visited = set()
        for leaf_cell in leaf_cells:
            if leaf_cell not in visited:
                instance = self.lookup.get_instance_from_name(leaf_cell)[-1]
                downstream_leaf_cells = self.get_downstream_leaf_cells(instance)
                for downstream_leaf_cell in downstream_leaf_cells:
                    self.ir_graph.add_edge(instance.__getitem__("EDIF.identifier"), downstream_leaf_cell.__getitem__("EDIF.identifier"))
                visited.add(leaf_cell)
        self.show_graph()

    def get_downstream_leaf_cells(self, leaf_cell):
        pins = list()
        util = Utility()
        hierarchical_name = util.get_hierarchical_name(leaf_cell)
        instance_trace = self.lookup.get_instance_from_name(hierarchical_name)
        instance_trace.pop()
        downstream_leaf_cells = set()
        for inner_pin, outer_pin in leaf_cell.outer_pins.items():
            if inner_pin.port.direction == Port.Direction.OUT:
                pins.append(outer_pin)
        visited = set()
        for pin in pins:
            if pin not in visited:
                wire = pin.wire
                for temp in wire.pins:
                    if temp not in visited:
                        pins.append(temp)
                if isinstance(pin, OuterPin):
                    if pin.instance is not leaf_cell:
                        if pin.inner_pin.wire is None:
                            downstream_leaf_cells.add(pin.instance)
                        else:
                            pins.append(pin.inner_pin)
                            instance_trace.append(pin.instance)
                else:
                    try:
                        if pin.port.direction == Port.Direction.OUT:
                            instance = instance_trace.pop()
                        for inner_pin, outer_pin in instance.outer_pins.items():
                            if inner_pin == pin:
                                pins.append(outer_pin)
                    except:
                        print()
                        pass
                    print()
            visited.add(pin)
        return downstream_leaf_cells

    def show_graph(self):
        print(nx.info(self.ir_graph))
        nx.draw(self.ir_graph, with_labels=True)
        plt.show()


from spydrnet.parsers.edif.parser import EdifParser

if __name__ == '__main__':
    parser = EdifParser.from_filename("passthrough_test.edf")
    parser.parse()
    ir = parser.netlist
    builder = Graph_Buider()
    builder.build_graph(ir)
