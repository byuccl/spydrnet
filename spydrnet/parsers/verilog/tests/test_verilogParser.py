import unittest
import spydrnet as sdn
# from spydrnet.parsers.verilog.parser import VerilogParser
from spydrnet import parsers
import os

class TestVerilogParser(unittest.TestCase):
    def test_simple_parse(self):
        directory = os.path.join(sdn.base_dir, "support_files", "verilog_netlists", "4bitadder.v.zip")
        #parser = parse#VerilogParser.from_filename(directory)
        netlist = parsers.parse(directory)
        print("hierarchy")
        self.simple_recursive_netlist_visualizer(netlist)
        print("Connectivity")
        self.simple_definition_information_visualizer(netlist)
        #assert False


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
            if instance.reference is None:
                print(s, instance.name, "(", "None", ")")
            else:
                print(s, instance.name, "(", instance.reference.name, ")")
                for c in instance.reference.children:
                    if c is None:
                        print("None child of", instance.name)    
                    recurse(c, depth + 1)
        
        recurse(top_instance, 0)


    def simple_definition_information_visualizer(self,netlist):
        for lib in netlist.libraries:
            print("Library", lib.name)
            for definition in lib.definitions:
                print("\t",definition.name)
                print("\t\t****PORTS****")
                for p in definition.ports:
                    print("\t\t\t",p.name)
                print("\t\t****CABLES****")
                for c in definition.cables:
                    print("\t\t\t",c.name)


if __name__ == '__main__':
    unittest.main()