import unittest
import os
import spydrnet as sdn
from spydrnet import base_dir
from spydrnet.util.selection import Selection

"""
Test the EBLIFParser by parsing in a simple netlist and making sure that:
    - Everything is there
    - Everything is working together as a netlist as it should (to be sure things were created and placed in the netlist correctly)
"""
class TestEBLIFParser(unittest.TestCase):
    def setUp(self):
        self.netlist = sdn.parse(os.path.join(base_dir, 'support_files', 'eblif_netlists', "toggle.eblif.zip"))
        self.definition_list = ["INV","BUFG","FDRE","IBUF","OBUF","toggle", "logic-gate_0"]

    def test_name(self):
        self.assertEqual(self.netlist.name,"toggle")

    def test_definitions(self):
        count = 0
        for definition in self.netlist.get_definitions():
            self.assertTrue(definition.name in self.definition_list, definition.name + " not found in list")
            count+=1
        self.assertEqual(count,len(self.definition_list))
    
    def test_instances(self):
        self.assertEqual(self.netlist.top_instance.name,"toggle")
        for instance in self.netlist.get_instances():
            self.assertTrue(instance.reference.name in self.definition_list)
            self.assertTrue(self.netlist_is_own_netlist(instance))
            if "logic-gate_0" in instance.reference.name:
                self.assertEqual(instance["EBLIF.type"],"EBLIF.names")
            else:
                self.assertEqual(instance["EBLIF.type"],"EBLIF.subckt")

    def test_top_level_ports(self):
        input_port_list = ["clk","reset"]
        output_port_list = ["out"]
        for port in self.netlist.get_hports():
            if port.item.direction is sdn.IN:
                self.assertTrue(port.item.name in input_port_list,port.item.name+" is not in "+str(input_port_list))
                self.assertTrue(self.netlist_is_own_netlist(port))
            elif port.item.direction is sdn.OUT:
                self.assertTrue(port.item.name in output_port_list,port.item.name+" is not in "+str(output_port_list))
                self.assertTrue(self.netlist_is_own_netlist(port))

    def test_cables(self):
        count = 0
        for cable in self.netlist.get_cables():
            self.assertTrue(self.netlist_is_own_netlist(cable))
            count+=1
        self.assertEqual(count, 11)

    def netlist_is_own_netlist(self,object):
        netlist_list = list(x for x in object.get_netlists())
        if (self.netlist in netlist_list):
            return True
        return False
        
    def test_flip_flop_connections(self):
        instance = next(self.netlist.get_instances(filter=lambda x: x.reference.name == "FDRE"))
        pin_connections = {"C":"clk"}
        for input_pin in instance.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.direction is sdn.IN):
            self.assertTrue(input_pin.wire is not None, input_pin.inner_pin.port.name + " does not have a wire")
            # driver_pin = next(pin for pin in input_pin.wire.pins)
            # get the driver
            # make sure it's the right driver

    # TODO add wire and connections tests
