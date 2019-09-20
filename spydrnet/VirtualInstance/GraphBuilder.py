import networkx as nx
import matplotlib.pyplot as plt

from spydrnet.ir import *
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.VirtualInstance.VirtualTree import VirtualTree
from spydrnet.utility.utility import Utility
import spydrnet.utility.utility as util
import spydrnet.support_files as files

class GraphBuilder:

    def __init__(self, ir=None):
        self.ir_graph = nx.DiGraph()
        self.pin_graph = None
        self.sequential_graph = None
        if ir is None:
            self.lookup = None
        else:
            self.lookup = HierarchicalLookup(ir)

    def build_graph(self, ir):
        self.lookup = HierarchicalLookup(ir)
        if not hasattr(ir, "tree"):
            ir.tree = VirtualTree()
            ir.tree.build_tree(ir)
        leaf_cells = self._get_leaf_cells(ir.tree)
        my_dictionary = dict()
        for leaf_cell in leaf_cells:
            downstream_cells = self._get_downstream_cells(leaf_cell)
            for driven_cell in downstream_cells:
                self.ir_graph.add_edge(leaf_cell, driven_cell)
            other_dictionay = dict()
            other_dictionay['type'] = leaf_cell.physical_instance['EDIF.identifier']
            my_dictionary[leaf_cell] = other_dictionay
        nx.set_node_attributes(self.ir_graph, my_dictionary)
        self._build_sequential_graph()

    def _build_sequential_graph(self):
        new_graph = nx.DiGraph()
        for node in self.ir_graph.nodes():
            if util.is_combinational(node.physical_instance):
                continue
            new_graph.add_node(node)
            downstream = self._get_successors(node)
            while len(downstream):
                downstream_node = downstream.pop()
                if util.is_sequential(downstream_node.physical_instance):
                    new_graph.add_edge(node, downstream_node)
                else:
                    downstream = downstream.union(self._get_get_successors())
        self.sequential_graph = new_graph

    def _get_successors(self, node):
        successors = set()
        for successor in self.ir_graph.successors(node):
            successors.add(successor)
        return successors

    def _get_leaf_cells(self, virtual_tree):
        leaf_cells = set()
        instances = set()
        instances.add(virtual_tree.root)
        while len(instances) is not 0:
            virtual_instance = instances.pop()
            if util.is_leaf(virtual_instance.physical_instance):
                leaf_cells.add(virtual_instance)
            instances.update(virtual_instance.children)
        return leaf_cells

    def _get_downstream_cells(self, driving_cell):
        downstream_cells = set()
        instance = driving_cell.physical_instance
        pins = set()
        for inner_pin, outer_pin in instance.outer_pins.items():
            if inner_pin.port.direction == Port.Direction.OUT:
                pins.add((outer_pin, driving_cell.parent))
        while pins:
            temp = pins.pop()
            pin = temp[0]
            working_cell = temp[1]
            for wire_pin in pin.wire.pins:
                if wire_pin is pin:
                    continue
                if isinstance(wire_pin, OuterPin):
                    if util.is_leaf(wire_pin.instance):
                        downstream_cells.add(self._get_child(working_cell, wire_pin.instance))
                    else:
                        pins.add((wire_pin.inner_pin, self._get_child(working_cell, wire_pin.instance)))
                else:
                    instance = working_cell.physical_instance
                    if working_cell.parent is not None:
                        outer_pin = instance.outer_pins[wire_pin]
                        pins.add((outer_pin, working_cell.parent))
        return downstream_cells

        # preform depth first search to find driven leaf cells
        # need a pointer to position in virtual_tree to keep track which specific instance is being looked at
        # when leaf cell is determine, add leaf cell to downstream_cells

    #Might better belong in VirtualTree
    def _get_child(self, virtual_instance, instance):
        for child in virtual_instance.children:
            if child.physical_instance is instance:
                return child
        return None

    def show_graph(self, graph):
        new_graph = nx.DiGraph()
        for node in graph.nodes:
            for successor in graph.successors(node):
                new_graph.add_edge(node.physical_instance['EDIF.identifier'], successor.physical_instance['EDIF.identifier'])
        print(nx.info(graph))
        print(nx.info(new_graph))
        nx.draw(new_graph, with_labels=True)
        plt.show()

from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
import spydrnet.support_files as files

if __name__ == '__main__':
    parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
    parser.parse()
    ir = parser.netlist
    graph_builder = GraphBuilder()
    graph_builder.build_graph(ir)