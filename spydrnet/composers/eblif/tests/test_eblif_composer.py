import unittest
import os
import spydrnet as sdn
from spydrnet import base_dir

"""
Test the EBLIF composer. The best way I can think to do this is to parse a netlist, compose it, then parse it again to see if anything changed. It should all be the same
"""

class TestEBLIFComposer(unittest.TestCase):
    def setUp(self):
        self.netlist_1 = sdn.parse(os.path.join(base_dir, 'support_files', 'eblif_netlists', "toggle.eblif.zip"))
        self.definition_list = ["INV","BUFG","FDRE","IBUF","OBUF","toggle"]
        sdn.compose(self.netlist_1,"temp_for_composer_test.eblif")
        self.netlist_2 = sdn.parse("temp_for_composer_test.eblif")
        os.remove("temp_for_composer_test.eblif")
    
    def test_netlist_name(self):
        self.assertEqual(self.netlist_1.name,self.netlist_2.name)
    
    def test_top_instance(self):
        self.assertEqual(self.netlist_1.top_instance.name,self.netlist_2.top_instance.name)
    
    def test_instances(self):
        instances_1 = list(instance.name for instance in self.netlist_1.get_instances())
        instances_2 = list(instance.name for instance in self.netlist_2.get_instances())
        self.assertEqual(instances_1,instances_2)
        self.assertEqual(len(instances_1),len(instances_2))
    
    def test_definitions(self):
        definitions_1 = list(definition.name for definition in self.netlist_1.get_definitions())
        definitions_2 = list(definition.name for definition in self.netlist_2.get_definitions())
        self.assertEqual(definitions_1,definitions_2)
        self.assertEqual(len(definitions_1),len(definitions_2))
    
    def test_cables(self):
        cables_1 = list(cable.name for cable in self.netlist_1.get_cables())
        cables_2 = list(cable.name for cable in self.netlist_2.get_cables())
        self.assertEqual(cables_1,cables_2)
        self.assertEqual(len(cables_1),len(cables_2))

    # TODO add wires and connections tests
        