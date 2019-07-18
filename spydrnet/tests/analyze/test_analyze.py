import json
import unittest

import spydrnet.support_files as files
from spydrnet.parsers.edif.parser import EdifParser
import spydrnet.analyze.analyze as analyze
from spydrnet.graph.Graph_Builder import GraphBuilder
import spydrnet.analyze.fannout_voter_selection as voter_selection

from spydrnet.utility.Uniqueifier import Uniquifier

class test_analyze(unittest.TestCase):

    def test_cells_to_replicate(self):
        f = open('config.json', 'r')
        contents = f.read()
        config = json.loads(contents)
        f.close()
        parser = EdifParser.from_filename(files.edif_files['fourBitCounter.edf'])
        parser.parse()
        ir = parser.netlist

        instances = analyze.determine_cells_to_replicate(ir, config)
        self.assertTrue(len(instances) == 8)
        for instance in instances:
            self.assertFalse(instance.definition['EDIF.identifier'] == 'BUFG')
            self.assertFalse(instance.definition['EDIF.identifier'] == 'IBUF')
            self.assertFalse(instance.definition['EDIF.identifier'] == 'OBUF')

    def test_cells_to_replicate_exclude_LUT4(self):
        f = open('config.json', 'r')
        contents = f.read()
        config = json.loads(contents)
        f.close()
        config['replicate_black_list'].append('LUT4')
        parser = EdifParser.from_filename(files.edif_files['fourBitCounter.edf'])
        parser.parse()
        ir = parser.netlist

        instances = analyze.determine_cells_to_replicate(ir, config)
        self.assertTrue(len(instances) == 7)
        for instance in instances:
            self.assertFalse(instance.definition['EDIF.identifier'] == 'BUFG')
            self.assertFalse(instance.definition['EDIF.identifier'] == 'IBUF')
            self.assertFalse(instance.definition['EDIF.identifier'] == 'OBUF')
            self.assertFalse(instance.definition['EDIF.identifier'] == 'LUT4')

    def test_get_leaf_instances(self):
        parser = EdifParser.from_filename(files.edif_files['fourBitCounter.edf'])
        parser.parse()
        ir = parser.netlist

        leaf_cells = analyze._get_leaf_instances(ir.top_instance.definition)
        self.assertTrue(len(leaf_cells) == 17)



    def test_get_leaf_instances_hierarchy(self):
        parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
        parser.parse()
        ir = parser.netlist

        test = Uniquifier()
        test.run(ir)

        leaf_cells = analyze._get_leaf_instances(ir.top_instance.definition)
        self.assertTrue(len(leaf_cells) == 95)

    def test_determine_other_voters_empty_cell_target_empty_voter_target(self):
        parser = EdifParser.from_filename(files.edif_files['fourBitCounter.edf'])
        parser.parse()
        ir = parser.netlist

        result = analyze.determine_other_voters(ir, [], [])
        self.assertTrue(len(result) == 0)

    def test_determine_other_voters_empty_voter_target(self):
        parser = EdifParser.from_filename(files.edif_files['fourBitCounter.edf'])
        parser.parse()
        ir = parser.netlist

        cell_target = [ir.top_instance.definition.instances[7]]
        result = analyze.determine_other_voters(ir, cell_target, [])
        self.assertTrue(len(result) == 1)
        self.assertTrue(result[0] == 'out_3__i_1_n_0')

    def test_determine_clock_domains(self):
        parser = EdifParser.from_filename(files.edif_files['fourBitCounter.edf'])
        parser.parse()
        ir = parser.netlist
        builder = GraphBuilder()
        builder.build_graph(ir)

        domains = analyze.determine_clock_domains(graph=builder.sequential_graph)
        self.assertTrue(len(domains) == 1)
        self.assertTrue(len(domains[0]) == 5)

    def test_find_clock_crossing_no_crossings(self):
        parser = EdifParser.from_filename(files.edif_files['fourBitCounter.edf'])
        parser.parse()
        ir = parser.netlist
        builder = GraphBuilder()
        builder.build_graph(ir)

        analyze.determine_clock_domains(graph=builder.sequential_graph)
        crossings = analyze.find_clock_crossing(builder.sequential_graph)
        self.assertTrue(len(crossings) == 0)

    def test_find_clock_crossing_one_crossing(self):
        parser = EdifParser.from_filename(files.edif_files['basic_clock_crossing.edf'])
        parser.parse()
        ir = parser.netlist
        builder = GraphBuilder()
        builder.build_graph(ir)

        analyze.determine_clock_domains(graph=builder.sequential_graph)
        crossings = analyze.find_clock_crossing(builder.sequential_graph)
        self.assertTrue(len(crossings) == 4)
        driven = set()
        for pair in crossings:
            driven.add(pair[1])
        self.assertTrue(len(driven) == 1)

    def test_find_synchronizers(self):
        parser = EdifParser.from_filename(files.edif_files['basic_synchronizer.edf'])
        parser.parse()
        ir = parser.netlist
        builder = GraphBuilder()
        builder.build_graph(ir)

        analyze.determine_clock_domains(graph=builder.sequential_graph)
        crossings = analyze.find_clock_crossing(builder.sequential_graph)
        synchronizers = analyze.find_synchronizers(crossings, builder.ir_graph)
        self.assertTrue(len(synchronizers) == 1)
        self.assertTrue(synchronizers[0][0]['EDIF.identifier'] == "sync_reg_0_")
        self.assertTrue(synchronizers[0][1]['EDIF.identifier'] == "sync_reg_1_")
        print('test')

    def test_find_synchronizers_2_fails_1_corrrect(self):
        parser = EdifParser.from_filename(files.edif_files['three_stage_synchronizer.edf'])
        parser.parse()
        ir = parser.netlist
        builder = GraphBuilder()
        builder.build_graph(ir)

        analyze.determine_clock_domains(graph=builder.sequential_graph)
        crossings = analyze.find_clock_crossing(builder.sequential_graph)
        synchronizers = analyze.find_synchronizers(crossings, builder.ir_graph)
        self.assertTrue(len(synchronizers) == 1)
        self.assertTrue(synchronizers[0][0]['EDIF.identifier'] == "sync_reg_0_")
        self.assertTrue(synchronizers[0][1]['EDIF.identifier'] == "sync_reg_1_")
        self.assertTrue(synchronizers[0][2]['EDIF.identifier'] == "sync_reg_2_")

if __name__ == '__main__':
    unittest.main()