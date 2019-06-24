import unittest

from spydrnet.utility.Uniqueifier import Uniquifier
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.compare.compare_netlists import Comparer
from spydrnet.ir import *

class test_Uniquifier(unittest.TestCase):

    def test_make_definition_copy(self):
        parser = EdifParser.from_filename('unique_challenge.edf')
        parser.parse()
        ir = parser.netlist
        definition = ir.libraries[-1].definitions[0]
        uniquifer = Uniquifier()
        copies = uniquifer._make_definition_copies(definition, 3)
        compare = Comparer('', '')
        for copy in copies:
            compare.compare_definition(definition, copy, check_identifier=False)
        pass

    def test_run(self, file=None):
        if file is None:
            parser = EdifParser.from_filename('unique_challenge.edf')
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
                    to_continue = False
                    for inner_pin, outer_pin in instance.outer_pins.items():
                        self.assertTrue(outer_pin.instance.definition == inner_pin.port.definition)
        pass

    def test_trace(self):
        parser = EdifParser.from_filename('unique_challenge.edf')
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