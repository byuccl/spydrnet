import copy

from spydrnet.ir import *
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.utility.utility import Utility
import spydrnet.utility.utility as util
import spydrnet.support_files as files
from spydrnet.utility.Uniqueifier import Uniquifier


import networkx as nx
import matplotlib.pyplot as plt


class GraphBuilder:
    def __init__(self, ir=None):
        self.ir_graph = nx.DiGraph()
        self.pin_graph = None
        self.sequential_graph = None
        if ir is None:
            self.lookup = None
        else:
            self.lookup = HierarchicalLookup(ir)

    def build_graph(self, ir, add_ports=True):
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
                other_dictionary = dict()
                other_dictionary['type'] = instance.definition['EDIF.identifier']
                my_dictionary[instance] = other_dictionary
                visited.add(leaf_cell)
        nx.set_node_attributes(self.ir_graph, my_dictionary)
        if add_ports:
            self.add_ports(ir)
        self._build_sequential_graph()

    def add_ports(self, ir):
        for port in ir.top_instance.definition.ports:
            for pin in port.inner_pins:
                downstream_leaf_cells = self.get_downstream_leaf_cells_pin(pin)
                for downstream_leaf_cell in downstream_leaf_cells:
                    if port.direction == Port.Direction.IN:
                        self.ir_graph.add_edge(pin, downstream_leaf_cell)
                    elif port.direction == Port.Direction.OUT:
                        # self.ir_graph.add_edge(pin, downstream_leaf_cell)
                        self.ir_graph.add_edge(downstream_leaf_cell, pin)
                    else:
                        pass
                        # self.ir_graph.add_edge(pin, downstream_leaf_cell)
                for test in self.ir_graph.successors(pin):
                    pass
                    #print()
        #print()

    def _build_sequential_graph(self):
        new_graph = nx.DiGraph()
        for node in self.ir_graph.nodes():
            if isinstance(node, InnerPin):
                continue
            if util.is_combinational(node):
                continue
            new_graph.add_node(node)
            downstream = set()
            downstream = downstream.union(self._get_successors(node))
            while len(downstream) != 0:
                downstream_stream_node = downstream.pop()
                if isinstance(downstream_stream_node, InnerPin):
                    continue
                if util.is_sequential(downstream_stream_node):
                    new_graph.add_edge(node, downstream_stream_node)
                    continue
                downstream = downstream.union(self._get_successors(downstream_stream_node))
        self.sequential_graph = new_graph

    def _get_successors(self, node):
        successors = set()
        for successor in self.ir_graph.successors(node):
            successors.add(successor)
        return successors

    def get_downstream_leaf_cells_pin(self, port_pin):
        pins = list()
        pins.append(port_pin)
        instance_trace = list
        downstream_leaf_cells = set()
        visited = set()
        for pin in pins:
            if pin not in visited:
                wire = pin.wire
                for temp in wire.pins:
                    if temp not in visited:
                        pins.append(temp)
                if isinstance(pin, OuterPin):
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

    def get_downstream_leaf_cells(self, leaf_cell):
        pins = list()
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
                if isinstance(node, InnerPin):
                    new_graph.add_edge(node.port['EDIF.identifier'], successor['EDIF.identifier'])
                elif isinstance(successor, InnerPin):
                    new_graph.add_edge(node['EDIF.identifier'], successor.port['EDIF.identifier'])
                else:
                    new_graph.add_edge(node['EDIF.identifier'], successor['EDIF.identifier'])
        print(nx.info(graph))
        print(nx.info(new_graph))
        nx.draw(new_graph, with_labels=True)
        plt.show()


from spydrnet.parsers.edif.parser import EdifParser

if __name__ == '__main__':
    parser = EdifParser.from_filename(files.edif_files["fourBitCounter.edf"])
    # parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
    parser.parse()
    # uniquifier = Uniquifier()
    ir = parser.netlist
    # uniquifier.run(ir)
    builder = GraphBuilder()
    builder.build_graph(ir)
    builder.show_graph(builder.ir_graph)
    # ir_graph = builder.ir_graph
    # print(nx.info(ir_graph))
    # uniquifier.run(ir)
    # builder = GraphBuilder()
    # builder.build_graph(ir)
    # ir_graph = builder.ir_graph
    # print(nx.info(ir_graph))
    # new_graph = nx.DiGraph()
    # i = 0
    # for node in ir_graph.nodes:
    #    i += 1
    #    for successor in ir_graph.successors(node):
    #        new_graph.add_edge(node['EDIF.identifier'], successor['EDIF.identifier'])
    # nx.draw(new_graph, with_labels=True)
    # print(nx.info(new_graph))
    # plt.show()
    # builder.show_graph()
