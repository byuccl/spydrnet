import copy

from spydrnet.ir import *
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.utility.utility import Utility
import spydrnet.utility.utility as util


import networkx as nx
import matplotlib.pyplot as plt


class GraphBuilder:
    def __init__(self):
        self.ir_graph = nx.DiGraph()
        self.pin_graph = None
        self.sequential_graph = None
        self.lookup = None

    def build_graph(self, ir):
        self.lookup = HierarchicalLookup(ir)
        utililty = Utility()
        leaf_cells = utililty.get_leaf_cells(ir)
        visited = set()
        my_dictionary = dict()
        for leaf_cell in leaf_cells:
            if leaf_cell not in visited:
                instance = self.lookup.get_instance_from_name(leaf_cell)[-1]
                downstream_leaf_cells = self.get_downstream_leaf_cells(instance)
                for downstream_leaf_cell in downstream_leaf_cells:
                    self.ir_graph.add_edge(instance, downstream_leaf_cell)
                    # self.ir_graph.add_edge(instance['EDIF.identifier'], downstream_leaf_cell['EDIF.identifier'])
                other_dictionary = dict()
                other_dictionary['type'] = instance.definition['EDIF.identifier']
                my_dictionary[instance] = other_dictionary
                visited.add(leaf_cell)
        nx.set_node_attributes(self.ir_graph, my_dictionary)
        self._build_sequential_graph()
        # self.show_graph()

    def _build_sequential_graph(self):
        new_graph = nx.DiGraph()
        # self.show_graph(self.ir_graph)
        for node in self.ir_graph.nodes():
            if util.is_combinational(node):
                continue
            new_graph.add_node(node)
            downstream = set()
            downstream = downstream.union(self._get_successors(node))
            while len(downstream) != 0:
                downstream_stream_node = downstream.pop()
                if util.is_sequential(downstream_stream_node):
                    new_graph.add_edge(node, downstream_stream_node)
                    continue
                downstream = downstream.union(self._get_successors(downstream_stream_node))
        self.sequential_graph = new_graph
        # self.show_graph(self.sequential_graph)

    def _get_successors(self, node):
        successors = set()
        for successor in self.ir_graph.successors(node):
            successors.add(successor)
        return successors

    def get_downstream_leaf_cells(self, leaf_cell):
        pins = list()
        # util = Utility()
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
                        pass
            visited.add(pin)
        return downstream_leaf_cells

    def show_graph(self, graph):
        new_graph = nx.DiGraph()
        for node in graph.nodes:
            for successor in graph.successors(node):
                new_graph.add_edge(node['EDIF.identifier'], successor['EDIF.identifier'])
        print(nx.info(new_graph))
        nx.draw(new_graph, with_labels=True)
        plt.show()


from spydrnet.parsers.edif.parser import EdifParser

if __name__ == '__main__':
    parser = EdifParser.from_filename("fourBitCounter.edf")
    parser.parse()
    ir = parser.netlist
    builder = GraphBuilder()
    builder.build_graph(ir)
    # builder.show_graph()
