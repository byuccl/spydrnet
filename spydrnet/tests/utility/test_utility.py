import unittest

from spydrnet.ir import *
import spydrnet.utility.utility as util
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
import spydrnet.support_files as files

class test_utility(unittest.TestCase):

    def test_is_sequential(self):
        definition = Definition()
        instance = Instance()
        instance.definition = definition
        definition['EDIF.identifier'] = 'FDCE'

        self.assertTrue(util.is_sequential(definition))
        definition['EDIF.identifier'] = 'BUFMRCE'
        self.assertTrue(util.is_sequential(instance))
        definition['EDIF.identifier'] = 'RAMS64E'
        self.assertTrue(util.is_sequential(instance))
        definition['EDIF.identifier'] = 'FDRE'
        self.assertTrue(util.is_sequential(instance))

    def test_is_sequential_false(self):
        definition = Definition()
        instance = Instance()
        instance.definition = definition
        definition['EDIF.identifier'] = 'IBUF'

        self.assertFalse(util.is_sequential(definition))
        definition['EDIF.identifier'] = 'LUT3'
        self.assertFalse(util.is_sequential(instance))
        definition['EDIF.identifier'] = 'BUFG'
        self.assertFalse(util.is_sequential(instance))
        definition['EDIF.identifier'] = 'CARRY4'
        self.assertFalse(util.is_sequential(instance))

    def test_is_combinational(self):
        definition = Definition()
        instance = Instance()
        instance.definition = definition
        definition['EDIF.identifier'] = 'IBUF'

        self.assertTrue(util.is_combinational(definition))
        definition['EDIF.identifier'] = 'LUT3'
        self.assertTrue(util.is_combinational(instance))
        definition['EDIF.identifier'] = 'BUFG'
        self.assertTrue(util.is_combinational(instance))
        definition['EDIF.identifier'] = 'CARRY4'
        self.assertTrue(util.is_combinational(instance))

    def test_is_combinational_false(self):
        definition = Definition()
        instance = Instance()
        instance.definition = definition
        definition['EDIF.identifier'] = 'FDCE'

        self.assertFalse(util.is_combinational(definition))
        definition['EDIF.identifier'] = 'BUFMRCE'
        self.assertFalse(util.is_combinational(instance))
        definition['EDIF.identifier'] = 'RAMS64E'
        self.assertFalse(util.is_combinational(instance))
        definition['EDIF.identifier'] = 'FDRE'
        self.assertFalse(util.is_combinational(instance))
        pass

    def test_trace_pin(self):
        parser = EdifParser.from_filename(files.edif_files['TMR_hierarchy.edf'])
        parser.parse()
        ir = parser.netlist
        cell = ir.libraries[-1].definitions[0].instances[0]
        pin = cell.get_pin('O')

        lookup = HierarchicalLookup(ir)
        stack = lookup.get_instance_from_name('top/delta/omega/b_INST_0')
        stack.pop()
        trace = util.trace_pin(pin, stack)
        self.assertTrue(len(trace) == 1)
        pass

    def test_get_hierarchical_name(self):
        parser = EdifParser.from_filename(files.edif_files['TMR_hierarchy.edf'])
        parser.parse()
        ir = parser.netlist
        cell = ir.libraries[-1].definitions[0].instances[0]

        name = util.get_hierarchical_name(cell)
        self.assertTrue(name == 'top/delta/omega/b_INST_0')
        pass

    def test_move_definition(self):
        pass

    def test_get_leaf_cells(self):
        parser = EdifParser.from_filename(files.edif_files['TMR_hierarchy.edf'])
        parser.parse()
        ir = parser.netlist


        utility = util.Utility()
        cells = utility.get_leaf_cells(ir)
        self.assertTrue(len(cells) == 8)


if __name__ == '__main__':
    unittest.main()