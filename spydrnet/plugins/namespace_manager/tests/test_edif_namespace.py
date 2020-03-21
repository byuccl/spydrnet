import unittest
import spydrnet as sdn


class TestEdifNamespace(unittest.TestCase):
    original_default = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.original_default = sdn.namespace_manager.default
        sdn.namespace_manager.default = "EDIF"

    @classmethod
    def tearDownClass(cls) -> None:
        sdn.namespace_manager.default = cls.original_default

    def gen_netlist(self):
        netlist = sdn.Netlist()
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
        c1['EDIF.identifier'] = "&1"
        i1['EDIF.identifier'] = "&1"
        p1['EDIF.identifier'] = "&1"
        c2['EDIF.identifier'] = "&2"
        i2['EDIF.identifier'] = "&2"
        p2['EDIF.identifier'] = "&2"

    def test_dont_track_orphaned(self):
        netlist = self.gen_netlist()
        lib1 = sdn.Library()
        lib2 = sdn.Library()
        lib1['EDIF.identifier'] = "my_lib1"
        lib2['EDIF.identifier'] = "my_lib1"

    @unittest.expectedFailure
    def test_duplicate_library_name(self):
        netlist = self.gen_netlist()
        lib1 = netlist.create_library()
        lib2 = netlist.create_library()
        lib1['EDIF.identifier'] = "my_lib"
        lib2['EDIF.identifier'] = "my_lib"

    @unittest.expectedFailure
    def test_duplicate_definition_name(self):
        lib1 = self.gen_library()
        def1 = lib1.create_definition()
        def2 = lib1.create_definition()
        def1['EDIF.identifier'] = "my_lib"
        def2['EDIF.identifier'] = "my_lib"

    def test_duplicate_definition_elements(self):
        def1 = self.gen_definition()
        port = def1.create_port()
        instance = def1.create_child()
        cable = def1.create_cable()
        port['EDIF.identifier'] = "my_lib"
        instance['EDIF.identifier'] = "my_lib"
        cable['EDIF.identifier'] = "my_lib"

    @unittest.expectedFailure
    def test_duplicate_definition_ports(self):
        def1 = self.gen_definition()
        port = def1.create_port()
        port2 = def1.create_port()
        port['EDIF.identifier'] = "my_lib"
        port2['EDIF.identifier'] = "my_lib"

    @unittest.expectedFailure
    def test_duplicate_definition_cables(self):
        def1 = self.gen_definition()
        cable = def1.create_cable()
        cable2 = def1.create_cable()
        cable['EDIF.identifier'] = "my_lib"
        cable2['EDIF.identifier'] = "my_lib"

    @unittest.expectedFailure
    def test_duplicate_definition_children(self):
        def1 = self.gen_definition()
        instance = def1.create_child()
        instance2 = def1.create_child()
        instance['EDIF.identifier'] = "my_lib"
        instance2['EDIF.identifier'] = "my_lib"

    def test_rename(self):
        netlist = self.gen_netlist()
        lib1 = netlist.create_library()
        lib1['EDIF.identifier'] = "my_lib1"
        lib1['EDIF.identifier'] = "my_lib2"
        lib1['EDIF.identifier'] = "my_lib1"
        lib2 = netlist.create_library()
        lib2['EDIF.identifier'] = "my_lib2"
        def1 = lib1.create_definition()
        def1['EDIF.identifier'] = "my_lib1"
        def1['EDIF.identifier'] = "my_lib2"
        def1['EDIF.identifier'] = "my_lib1"
        def2 = lib1.create_definition()
        def2['EDIF.identifier'] = "my_lib2"
        c = def1.create_cable()
        c['EDIF.identifier'] = "&1"
        c['EDIF.identifier'] = "&2"
        c['EDIF.identifier'] = "&1"
        p = def1.create_port()
        p['EDIF.identifier'] = "&1"
        p['EDIF.identifier'] = "&2"
        p['EDIF.identifier'] = "&1"
        i = def1.create_child()
        i['EDIF.identifier'] = "&1"
        i['EDIF.identifier'] = "&2"
        i['EDIF.identifier'] = "&1"

    def test_remove(self):
        netlist = self.gen_netlist()
        lib1 = netlist.create_library()
        lib1['EDIF.identifier'] = "my_lib1"
        netlist.remove_library(lib1)
        lib2 = netlist.create_library()
        lib2['EDIF.identifier'] = "my_lib1"
        def1 = lib2.create_definition()
        def1['EDIF.identifier'] = "my_lib1"
        lib2.remove_definition(def1)
        def2 = lib2.create_definition()
        def2['EDIF.identifier'] = "my_lib1"
        c1 = def2.create_cable()
        c2 = def2.create_cable()
        p1 = def2.create_port()
        p2 = def2.create_port()
        i1 = def2.create_child()
        i2 = def2.create_child()
        c1['EDIF.identifier'] = "&1"
        def2.remove_cable(c1)
        c2['EDIF.identifier'] = "&1"
        p1['EDIF.identifier'] = "&1"
        def2.remove_port(p1)
        p2['EDIF.identifier'] = "&1"
        i1['EDIF.identifier'] = "&1"
        def2.remove_child(i1)
        i2['EDIF.identifier'] = "&1"

    def test_orphaned_add(self):
        netlist = self.gen_netlist()
        lib1 = sdn.Library()
        lib1["EDIF.identifier"] = '&1'
        netlist.add_library(lib1)

    @unittest.expectedFailure
    def test_orphaned_add_collision(self):
        netlist = self.gen_netlist()
        lib1 = sdn.Library()
        lib1["EDIF.identifier"] = '&1'
        netlist.add_library(lib1)
        lib2 = sdn.Library()
        lib2["EDIF.identifier"] = '&1'
        netlist.add_library(lib2)

    def test_remove_twice_library(self):
        netlist = self.gen_netlist()
        lib1 = netlist.create_library()
        lib1['EDIF.identifier'] = "my_lib1"
        netlist.remove_library(lib1)
        self.assertRaises(Exception, netlist.remove_library, lib1)

    def test_remove_twice_definition(self):
        lib = self.gen_library()
        d1 = lib.create_definition()
        d1['EDIF.identifier'] = "&1"
        lib.remove_definition(d1)
        self.assertRaises(Exception, lib.remove_definition, d1)

    def test_remove_untracked(self):
        netlist = self.gen_netlist()
        lib1 = netlist.create_library()
        def1 = lib1.create_definition()
        c1 = def1.create_cable()
        p1 = def1.create_port()
        i1 = def1.create_child()
        def1.remove_cable(c1)
        def1.remove_child(i1)
        def1.remove_port(p1)
        lib1.remove_definition(def1)
        netlist.remove_library(lib1)

    def test_remove_tracked(self):
        netlist = self.gen_netlist()
        lib1 = netlist.create_library()
        lib1["EDIF.identifier"] = "test"
        def1 = lib1.create_definition()
        def1["EDIF.identifier"] = "test"
        c1 = def1.create_cable()
        c1["EDIF.identifier"] = "test"
        p1 = def1.create_port()
        p1["EDIF.identifier"] = "test"
        i1 = def1.create_child()
        i1["EDIF.identifier"] = "test"
        def1.remove_cable(c1)
        def1.remove_child(i1)
        def1.remove_port(p1)
        lib1.remove_definition(def1)
        netlist.remove_library(lib1)

    def test_pop_name(self):
        netlist = self.gen_netlist()
        lib1 = netlist.create_library()
        lib1['EDIF.identifier'] = "my_lib1"
        lib1.pop('EDIF.identifier')
        lib2 = netlist.create_library()
        lib2['EDIF.identifier'] = "my_lib1"
        def1 = lib2.create_definition()
        def1['EDIF.identifier'] = "my_lib1"
        def1.pop('EDIF.identifier')
        def2 = lib2.create_definition()
        def2['EDIF.identifier'] = "my_lib1"
        c1 = def2.create_cable()
        c2 = def2.create_cable()
        p1 = def2.create_port()
        p2 = def2.create_port()
        i1 = def2.create_child()
        i2 = def2.create_child()
        c1['EDIF.identifier'] = "&1"
        c1.pop('EDIF.identifier')
        c2['EDIF.identifier'] = "&1"
        p1['EDIF.identifier'] = "&1"
        p1.pop('EDIF.identifier')
        p2['EDIF.identifier'] = "&1"
        i1['EDIF.identifier'] = "&1"
        i1.pop('EDIF.identifier')
        i2['EDIF.identifier'] = "&1"

    # TODO: rename an object
    # TODO: orphan an object and see what happens
