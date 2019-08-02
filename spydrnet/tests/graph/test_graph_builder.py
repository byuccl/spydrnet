import unittest

from spydrnet.graph.Graph_Builder import GraphBuilder
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.utility.Uniqueifier import Uniquifier
from spydrnet.utility.utility import Utility
import spydrnet.utility.utility as util
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
import spydrnet.support_files as files
from spydrnet.ir import *


# TODO needs more test cases

class TestGraphBuilder(unittest.TestCase):
    def test_all(self):
        parser = EdifParser.from_filename(files.edif_files["TMR_hierarchy.edf"])
        parser.parse()
        ir = parser.netlist
        uniquifier = Uniquifier()
        uniquifier.run(ir)
        builder = GraphBuilder()
        builder.build_graph(ir)
        graph = builder.ir_graph
        nodes = graph.nodes()
        node = ir.libraries[-1].definitions[1].instances[0]
        self._check_successor(graph, node)
        pass

    def test_all_hierarchy(self):
        parser = EdifParser.from_filename(files.edif_files['register_file.edf'])
        parser.parse()
        ir = parser.netlist
        uniquifier = Uniquifier()
        uniquifier.run(ir)
        builder = GraphBuilder()
        builder.build_graph(ir)
        graph = builder.ir_graph
        nodes = graph.nodes()
        node = ir.libraries[-1].definitions[1].instances[0]
        self._check_successor(graph, node)
        pass

    def test_get_downstream_leaf_cells(self):
        parser = EdifParser.from_filename(files.edif_files['fourBitCounter.edf'])
        parser.parse()
        ir = parser.netlist
        cell = ir.top_instance.definition.lookup_element(Instance, 'EDIF.identifier', 'out_reg_0_')

        builder = GraphBuilder(ir)
        downstream_cells = builder.get_downstream_leaf_cells(cell)
        self.assertTrue(len(downstream_cells) == 5)

    def test_get_downstream_leaf_cells_hierarchy(self):
        parser = EdifParser.from_filename(files.edif_files['register_file.edf'])
        parser.parse()
        ir = parser.netlist
        cell = ir.libraries[-1].definitions[8].lookup_element(Instance, 'EDIF.identifier', 'dataout2_2__INST_0')

        builder = GraphBuilder(ir)
        downstream_cells = builder.get_downstream_leaf_cells(cell)
        self.assertTrue(len(downstream_cells) == 4)

    def _check_successor(self, graph, node):
        utility = Utility()
        lookup = HierarchicalLookup(node.parent_definition.library.environment)
        name = util.get_hierarchical_name(node)
        order = lookup.get_instance_from_name(name)
        order.pop()
        graph_successors = graph.successors(node)
        graph_predecessors = graph.predecessors(node)
        ir_successors = list()
        ir_predecessors = list()
        for inner_pin, outer_pin in node.outer_pins.items():
            if inner_pin.port.direction == Port.Direction.OUT:
                ir_successors.extend(self._trace_pin(outer_pin, order))
            else:
                ir_predecessors.extend(self._trace_pin(outer_pin, order))
        ir_successors = set(ir_successors)
        ir_successors = set(ir_successors)

        for instance in graph_successors:
            self.assertTrue(instance in ir_successors)
            ir_successors.remove(instance)
        self.assertTrue(len(ir_successors) == 0)

        for instance in graph_predecessors:
            self.assertTrue(instance in ir_predecessors)
            ir_predecessors.remove(instance)
        self.assertTrue(len(ir_predecessors) == 0)

    def _trace_pin(self, pin, instance_stack):
        instances = list()
        for wire_pin in pin.wire.pins:
            if wire_pin is pin:
                continue
            if isinstance(wire_pin, OuterPin):
                if wire_pin.inner_pin.wire is None:
                    instances.append(wire_pin.instance)
                    continue
                instance_stack.append(wire_pin.instance)
                instances.extend(self._trace_pin(wire_pin.inner_pin, instance_stack))
                instance_stack.pop()
            else:
                instance = instance_stack.pop()
                for inner_pin, outer_pin in instance.outer_pins.items():
                    if inner_pin is wire_pin:
                        instances.extend(self._trace_pin(outer_pin, instance_stack))
                        break
                instance_stack.append(instance)
        return instances


if __name__ == '__main__':
    unittest.main()
