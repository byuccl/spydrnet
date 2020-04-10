
import unittest
import spydrnet as sdn
from spydrnet import Netlist, Instance, Definition
from spydrnet.flatten import flatten
from spydrnet.uniquify import uniquify

class TestUniquify(unittest.TestCase):
    def create_netlist(self):
        nl = Netlist()
        lib = nl.create_library()
        d1 = lib.create_definition()
        d1.name = ("d1")
        d2 = lib.create_definition()
        d2.name = ("d2")
        d3 = lib.create_definition()
        d3.name = ("d3")
        i11 = d1.create_child()
        i11.name = ("i11")
        i12 = d1.create_child()
        i12.name = ("i12")
        i13 = d1.create_child()
        i13.name = ("i13")
        i24 = d2.create_child()
        i24.name = ("i24")
        i25 = d2.create_child()
        i25.name = ("i25")
        i26 = d2.create_child()
        i26.name = ("i26")
        i27 = d2.create_child()
        d4 = lib.create_definition()
        d4.name = ("d4")
        i27.name = ("i27")
        i38 = d3.create_child()
        i38.name = ("i38")
        i39 = d3.create_child()
        i39.name = ("i39")
        i11.reference = d3
        i12.reference = d3
        i13.reference = d3
        i24.reference = d1
        i25.reference = d1
        i26.reference = d3
        i27.reference = d3
        i38.reference = d4
        i39.reference = d4
        nl.top_instance = Instance()
        nl.top_instance.reference = d2
        nl.top_instance.name = ("top_instance")
        return nl


    def simple_recursive_netlist_visualizer(self, netlist):
        #TODO put this code somewhere where people can use it to visualize simple netlists
        top_instance = netlist.top_instance
        #should look something like this:
        #top
        #   child1
        #       child1.child
        #   child2
        #       child2.child
        def recurse(instance, depth):
            s = depth * "\t"
            print(s, instance.name, "(", instance.reference.name, ")")
            for c in instance.reference.children:  
                recurse(c, depth + 1)
        
        recurse(top_instance, 0)

    def is_flat(self,nl):
        ti = nl.top_instance
        td = ti.reference
        for i in td.children:
            if not i.is_leaf():
                return False
        return True


    def test_flatten_instances(self):
        nl = self.create_netlist()
        uniquify(nl)
        flatten(nl)
        assert self.is_flat(nl)


    def test_flatten_cables(self):
        #create a netlist with some connections

        #uniquify the netlist

        pass