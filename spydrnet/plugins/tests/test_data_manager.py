import unittest
import spydrnet as sdn

from spydrnet.plugins.data_manager import DataManager
from spydrnet.global_state.global_netlist import current_netlist


class TestDataManager(unittest.TestCase):
    def gen_netlist(self):
        global current_netlist
        netlist = sdn.Netlist()
        current_netlist = netlist
        return netlist

    def gen_library(self):
        netlist = self.gen_netlist()
        lib = netlist.create_library()
        return lib

    def gen_definition(self):
        lib = self.gen_library()
        defin = lib.create_definition()
        return defin
        

    def test_basic_setup(self):
        netlist = self.gen_netlist()
        dm = DataManager()
        lib1 = netlist.create_library()
        lib2 = netlist.create_library()
        lib1['EDIF.identifier'] = "my_lib1"
        lib2['EDIF.identifier'] = "my_lib2"
        

    @unittest.expectedFailure
    def test_duplicate_library_name(self):
        netlist = self.gen_netlist()
        dm = DataManager()
        lib1 = netlist.create_library()
        lib2 = netlist.create_library()
        lib1['EDIF.identifier'] = "my_lib"
        lib2['EDIF.identifier'] = "my_lib"

    
    @unittest.expectedFailure
    def test_duplicate_definition_name(self):
        lib1 = self.gen_library()
        dm = DataManager()
        def1 = lib1.create_definition()
        def2 = lib1.create_definition()
        def1['EDIF.identifier'] = "my_lib"
        def2['EDIF.identifier'] = "my_lib"

    @unittest.expectedFailure
    def test_duplicate_definition_elements(self):
        def1 = self.gen_definition()
        dm = DataManager()
        port = def1.create_port()
        instance = def1.create_child()
        port['EDIF.identifier'] = "my_lib"
        instance['EDIF.identifier'] = "my_lib"


    '''tests TODO:
    rename an object
    orphan an object and see what happens
    ...
    '''