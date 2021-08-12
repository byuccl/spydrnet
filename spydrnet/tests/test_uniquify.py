
import unittest
from spydrnet import Netlist, Instance
from spydrnet.uniquify import uniquify

class TestUniquify(unittest.TestCase):
    def create_netlist(self):
        nl = Netlist()
        lib = nl.create_library()
        d1 = lib.create_definition()
        d2 = lib.create_definition()
        d3 = lib.create_definition(name='instance_name')
        i11 = d1.create_child()
        i12 = d1.create_child()
        i13 = d1.create_child()
        i24 = d2.create_child()
        i25 = d2.create_child()
        i26 = d2.create_child()
        i27 = d2.create_child()
        d4 = lib.create_definition()
        i38 = d3.create_child()
        i39 = d3.create_child()
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
        return nl

    def is_unique(self, netlist):
        #get all the definitions that are instanced below the top instance
        top_inst = netlist.top_instance
        top_def = top_inst.reference
        inst = []
        inst.append(top_inst)
        index = 1
        for c in top_def.children:
            inst.append(c)
        while index != len(inst):
            for c in inst[index].reference.children:
                inst.append(c)
            index += 1

        #now we have a list of all the instances in the netlist make sure all references are unique to the netlist
        refs = set()
        for i in inst:
            if i.reference.is_leaf():
                continue
            if i.reference in refs:
                return False #the instance references a previously referenced definition, instances are not unique
            refs.add(i.reference)
        return True

    def test_already_unique(self):
        nl = Netlist()
        lib = nl.create_library()
        d1 = lib.create_definition()
        d2 = lib.create_definition()
        d3 = lib.create_definition()
        i1 = d1.create_child()
        i2 = d1.create_child()
        i1.reference = d2
        i2.reference = d3
        top = Instance()
        top.reference = d1
        nl.top_instance = top
        assert self.is_unique(nl), "netlist should be unique upon creation in this test"
        uniquify(nl)
        assert self.is_unique(nl), "netlist should remain unique in this test. somehow uniquify made the netlist un-unique"

    # def simple_recursive_netlist_visualizer(self, netlist):
    #     #TODO put this code somewhere where people can use it to visualize simple netlists
    #     top_instance = netlist.top_instance
    #     #should look something like this:
    #     #top
    #     #   child1
    #     #       child1.child
    #     #   child2
    #     #       child2.child
    #     def recurse(instance, depth):
    #         s = depth * "\t"
    #         print(s, instance.name, "(", instance.reference.name, ")")
    #         for c in instance.reference.children:  
    #             recurse(c, depth + 1)
        
    #     recurse(top_instance, 0)


    def test_uniquify_simple_with_names(self):
        '''simple test with 2 definitions.'''
        nl = Netlist()
        lib = nl.create_library()
        d1 = lib.create_definition()
        d1.name = "definition1"
        d2 = lib.create_definition()
        d2.name = "definition2"
        d3 = lib.create_definition()
        d3.name = "leaf definition"
        i1 = d1.create_child()
        i1.name = "instance1"
        i2 = d1.create_child()
        i2.name = "instance2"
        i1.reference = d2
        i2.reference = d2
        i3 = d2.create_child()
        i3.name = "leaf cell"
        i3.reference = d3
        top = Instance()
        top.name = "top instance"
        top.reference = d1
        nl.top_instance = top
        assert not self.is_unique(nl), "initial netlist should not be unique in this test"
        uniquify(nl)
        assert self.is_unique(nl), "netlist should have been uniquified."

    def test_uniquify(self):
        nl = self.create_netlist()
        assert not self.is_unique(nl), "our test netlist should not be unique"
        uniquify(nl)
        assert self.is_unique(nl), "our netlist should have been uniquified"