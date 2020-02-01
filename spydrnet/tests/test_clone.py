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
        return netlist

    def _compare_netlists(self, nl1, nl2):
        pass


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