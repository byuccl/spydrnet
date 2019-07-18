import unittest

from spydrnet.utility.Uniqueifier import Uniquifier
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
from spydrnet.compare.compare_netlists import Comparer
import spydrnet.support_files as files
from spydrnet.ir import *

class test_Uniquifier(unittest.TestCase):

    file = 'unique_challenge.edf'

    def test_trace_definition(self):
        parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
        parser.parse()
        ir = parser.netlist
        a_def = ir.libraries[-1].definitions[-2]
        b_def = ir.libraries[-1].definitions[-3]
        c_def = ir.libraries[-1].definitions[-4]
        uniqufier = Uniquifier()

        c_trace = uniqufier._trace_definition(c_def)
        c_trace_name = list()
        correct_c_trace = ['c']
        for definition in c_trace:
            c_trace_name.append(definition['EDIF.identifier'])
        self.assertTrue(c_trace_name == correct_c_trace, 'Did not trace C correctly')

        b_trace = uniqufier._trace_definition(b_def)
        b_trace_name = list()
        correct_b_trace = ['c', 'c', 'c', 'b']
        for definition in b_trace:
            b_trace_name.append(definition['EDIF.identifier'])
        self.assertTrue(b_trace_name == correct_b_trace, 'Did not trace B correctly')

        a_trace = uniqufier._trace_definition(a_def)
        a_trace_name = list()
        correct_a_trace = ['c', 'c', 'c', 'b', 'c', 'c', 'c', 'b', 'c', 'c', 'c', 'b', 'a']
        for definition in a_trace:
            a_trace_name.append(definition['EDIF.identifier'])
        self.assertTrue(a_trace_name == correct_a_trace, 'Did not trace A correctly')

    def test_get_reverse_topological_order(self):
        parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
        parser.parse()
        ir = parser.netlist
        uniqufier = Uniquifier()
        order = uniqufier._get_reverse_topological_order(ir)
        correct_order = ['c', 'b', 'a']
        name = list()
        for definition in order:
            identifier = definition['EDIF.identifier']
            self.assertTrue(identifier in correct_order, "Gave definition with unknown name")
            name.append(identifier)
        self.assertTrue(name == correct_order, "Did not give definitions in correct order")

    def test_copy_metadata(self):
        parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
        parser.parse()
        ir = parser.netlist
        uniqufier = Uniquifier()
        c_def = ir.libraries[-1].definitions[-4]
        c_def_copy = Definition()
        uniqufier._copy_metadata(c_def, c_def_copy, 0)
        for key, day in c_def._metadata.items():
            if key == 'EDIF.identifier' or key == 'EDIF.original_identifier':
                c_def[key] + '_0' == c_def_copy[key]
            else:
                c_def[key] == c_def_copy[key]


    def test_make_definition_copy(self):
        parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
        parser.parse()
        ir = parser.netlist
        definition = ir.libraries[-1].definitions[0]
        uniquifer = Uniquifier()
        copies = uniquifer._make_definition_copies(definition, 3)
        compare = Comparer('', '')
        for copy in copies:
            compare.compare_definition(definition, copy, check_identifier=False)
        pass

    def test_run_2(self):
        ir = self.test_run(files.edif_files['riscv_multi_core.edf'])
        compose = ComposeEdif()
        compose.run(ir, 'test.edf')

    def test_run(self, file=None):
        if file is None:
            parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
        else:
            parser = EdifParser.from_filename(file)
        parser.parse()
        ir = parser.netlist
        uniquifer = Uniquifier()
        uniquifer.run(ir)
        seen_definitions = set()
        for library in ir.libraries:
            for definition in library.definitions:
                for instance in definition.instances:
                    to_continue = False
                    for inner_pin in instance.outer_pins.keys():
                        if inner_pin.wire is None:
                            to_continue = True
                            break
                    if to_continue:
                        continue
                    self.assertTrue(instance.definition not in seen_definitions)
                    seen_definitions.add(instance.definition)
        for library in ir.libraries:
            for definition in library.definitions:
                for instance in definition.instances:
                    for inner_pin, outer_pin in instance.outer_pins.items():
                        self.assertTrue(outer_pin.instance.definition == inner_pin.port.definition)
        return ir

    def test_trace(self):
        parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
        parser.parse()
        ir = parser.netlist
        definition = ir.libraries[-1].definitions[-1]
        count = dict()
        instances = dict()
        uniquifer = Uniquifier()
        uniquifer._trace_definition(definition)
        count = uniquifer.definition_count
        for definition, number in count.items():
            if definition.__getitem__("EDIF.identifier") == 'a':
                self.assertTrue(number == 3)
            elif definition.__getitem__('EDIF.identifier') == 'b':
                self.assertTrue(number == 9)
            elif definition.__getitem__('EDIF.identifier') == 'c':
                self.assertTrue(number == 27)

    # def test_make_definition_copy_bad_copy_number(self):
    #     parser = EdifParser.from_filename('unique_challenge.edf')
    #     parser.parse()
    #     ir = parser.netlist
    #     definition = ir.libraries[-1].definitions[0]
    #     uniquifer = Uniquifier()
    #     self.assertRaises(AssertionError, uniquifer._make_definition_copies, definition, 0)
    #     self.assertRaises(AssertionError, uniquifer._make_definition_copies, definition, -1)
    #     self.assertRaises(AssertionError, uniquifer._make_definition_copies, definition, 1.5)
    #     self.assertRaises(AssertionError, uniquifer._make_definition_copies, definition, 0.9)

    # def test_make_definition_copy_bad_definition(self):
    #     parser = EdifParser.from_filename('unique_challenge.edf')
    #     parser.parse()
    #     ir = parser.netlist
    #     definition = ir.libraries[-1].definitions[0]
    #     uniquifer = Uniquifier()
    #     self.assertRaises(AssertionError, uniquifer._make_definition_copies, Instance, 3)
    #     self.assertRaises(AssertionError, uniquifer._make_definition_copies, Library, 3)
    #     self.assertRaises(AssertionError, uniquifer._make_definition_copies, Definition(), 3)


if __name__ == '__main__':
    unittest.main()