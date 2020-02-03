import unittest

from spydrnet.clone import clone
from spydrnet.ir import *


class TestClone(unittest.TestCase):
    
    def setUp(self):
        #create a test netlist
        self.nl = self._create_netlist()
        #create my own backup of the test netlist (just create another that is identical)
        self.nl2 = self._create_netlist()

    def _create_netlist(self):
        netlist = Netlist()
        lib = netlist.create_library()
        defin = lib.create_definition()
        port = defin.create_port()
        cable = defin.create_cable()
        instance = defin.create_child()
        defin2 = lib.create_definition()
        instance.reference = defin2
        wire = cable.create_wire()
        port.create_pins(2)
        port2 = defin2.create_port()
        port2.create_pins(1)
        for pin in port.pins:
            wire.connect_pin(pin)
        for pin in instance.pins:
            wire.connect_pin(pin)
        return netlist

    #we need to use the built in compare functions


    def test_cable(self):
        #clone a cable and make sure the test netlist has not changed
        pass

    def test_definition(self):
        pass

    def test_element(self):
        pass

    def test_innerpin(self):
        pass

    def test_instance(self):
        pass

    def test_library(self):
        pass

    def test_netlist(self):
        pass

    def test_outerpin(self):
        pass

    def test_port(self):
        pass

    def test_wire(self):
        pass