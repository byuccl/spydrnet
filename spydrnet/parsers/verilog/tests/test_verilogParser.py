import unittest
import spydrnet as sdn
from spydrnet.parsers.verilog.parser import VerilogParser


class TestVerilogParser(unittest.TestCase):
    def test_simple_parse(self):
        parser = VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/4bitadder.v.zip")
        netlist = parser.parse()
        print("hierarchy")
        self.simple_recursive_netlist_visualizer(netlist)
        print("Connectivity")
        self.simple_definition_information_visualizer(netlist)
        assert False


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

    # def test_simple(self):
    #     f = open('simpleVerilog.v', 'r')
    #     s = f.read()
    #     f.close()
    #     parser = verilogParser()
    #     result = parser.parse(s)
    #     library = result.libraries[0]
    #     self.assertEqual(len(library.definitions), 1)
    #     definition = library.definitions[0]
    #     self.assertEqual(definition.name, 'foo')
    #     self.assertEqual(len(definition.ports), 1)
    #     port = definition.ports[0]
    #     self.assertEqual(port.name, 'a')
    #     self.assertEqual(port.direction, sdn.IN)
    #     self.assertEqual(len(port.pins), 1)
    #     self.assertEqual(len(definition.cables), 1)
    #     cable = definition.cables[0]
    #     self.assertEqual(cable.name, 'a')
    #     self.assertEqual(len(cable.wires), 1)

    # def test_port_direction_1(self):
    #     f = open('portDirection1.v', 'r')
    #     s = f.read()
    #     f.close()
    #     parser = verilogParser()
    #     result = parser.parse(s)
    #     definition = result.libraries[0].definitions[0]
    #     self.assertEqual(len(definition.ports), 6)
    #     ports = definition.ports
    #     port = ports[0]
    #     self.assertEqual(port.direction, sdn.IN)
    #     port = ports[1]
    #     self.assertEqual(port.direction, sdn.IN)
    #     port = ports[2]
    #     self.assertEqual(port.direction, sdn.INOUT)
    #     port = ports[3]
    #     self.assertEqual(port.direction, sdn.INOUT)
    #     port = ports[4]
    #     self.assertEqual(port.direction, sdn.OUT)
    #     port = ports[5]
    #     self.assertEqual(port.direction, sdn.OUT)

    # def test_port_direction_1(self):
    #     f = open('portDirection2.v', 'r')
    #     s = f.read()
    #     f.close()
    #     parser = verilogParser()
    #     result = parser.parse(s)
    #     definition = result.libraries[0].definitions[0]
    #     self.assertEqual(len(definition.ports), 6)
    #     ports = definition.ports
    #     port = ports[0]
    #     self.assertEqual(port.direction, sdn.IN)
    #     port = ports[1]
    #     self.assertEqual(port.direction, sdn.IN)
    #     port = ports[2]
    #     self.assertEqual(port.direction, sdn.INOUT)
    #     port = ports[3]
    #     self.assertEqual(port.direction, sdn.INOUT)
    #     port = ports[4]
    #     self.assertEqual(port.direction, sdn.OUT)
    #     port = ports[5]
    #     self.assertEqual(port.direction, sdn.OUT)


if __name__ == '__main__':
    unittest.main()
