import unittest
import spydrnet as sdn

from spydrnet.plugins.data_manager import DataManager
from spydrnet.global_state.global_netlist import set_current_netlist, get_current_netlist


class TestDataManager(unittest.TestCase):
    def gen_netlist(self):
        netlist = sdn.Netlist()
        set_current_netlist(netlist)
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
        def1 = lib1.create_definition()
        def1['EDIF.identifier'] = "d1"
        def2 = lib2.create_definition()
        def2['EDIF.identifier'] = "d1"
        def3 = lib1.create_definition()
        def3['EDIF.identifier'] = "my_lib1"
        c1 = def1.create_cable()
        p1 = def1.create_port()
        i1 = def1.create_child()
        c2 = def1.create_cable()
        p2 = def1.create_port()
        i2 = def1.create_child()
        c1['EDIF.identifier'] = "1"
        i1['EDIF.identifier'] = "1"
        p1['EDIF.identifier'] = "1"
        c2['EDIF.identifier'] = "2"
        i2['EDIF.identifier'] = "2"
        p2['EDIF.identifier'] = "2"

        

    def test_dont_track_orphaned(self):
        netlist = self.gen_netlist()
        dm = DataManager()
        lib1 = sdn.Library()
        lib2 = sdn.Library()
        lib1['EDIF.identifier'] = "my_lib1"
        lib2['EDIF.identifier'] = "my_lib1"

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

    def test_duplicate_definition_elements(self):
        def1 = self.gen_definition()
        dm = DataManager()
        port = def1.create_port()
        instance = def1.create_child()
        cable = def1.create_cable()
        port['EDIF.identifier'] = "my_lib"
        instance['EDIF.identifier'] = "my_lib"
        cable['EDIF.identifier'] = "my_lib"

    @unittest.expectedFailure
    def test_duplicate_definition_ports(self):
        def1 = self.gen_definition()
        dm = DataManager()
        port = def1.create_port()
        port2 = def1.create_port()
        port['EDIF.identifier'] = "my_lib"
        port2['EDIF.identifier'] = "my_lib"

    @unittest.expectedFailure
    def test_duplicate_definition_cables(self):
        def1 = self.gen_definition()
        dm = DataManager()
        cable = def1.create_cable()
        cable2 = def1.create_cable()
        cable['EDIF.identifier'] = "my_lib"
        cable2['EDIF.identifier'] = "my_lib"

    @unittest.expectedFailure
    def test_duplicate_definition_children(self):
        def1 = self.gen_definition()
        dm = DataManager()
        instance = def1.create_child()
        instance2 = def1.create_child()
        instance['EDIF.identifier'] = "my_lib"
        instance2['EDIF.identifier'] = "my_lib"

    def test_rename(self):
        netlist = self.gen_netlist()
        dm = DataManager()
        lib1 = netlist.create_library()
        lib2 = netlist.create_library()
        lib1['EDIF.identifier'] = "my_lib1"
        lib2['EDIF.identifier'] = "my_lib2"
        #lib1['EDIF.identifier'] = "my_lib3"
        #lib2['EDIF.identifier'] = "my_lib"

    '''tests TODO:
    rename an object
    orphan an object and see what happens
    ...
    '''