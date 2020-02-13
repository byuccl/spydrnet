import unittest

from spydrnet.clone import clone
from spydrnet.ir import *
from spydrnet.compare.compare_netlists import Comparer


class TestClone(unittest.TestCase):
    
    def _run_first(self):
        #create a test netlist
        nl = self._create_netlist()
        #create my own backup of the test netlist (just create another that is identical)
        nl2 = self._create_netlist()
        
        #both netlists are created and checkout as the same.
        return nl, nl2

    def _compare_netlists(self, n1, n2):
        comparer = Comparer(n1, n2)
        comparer.compare()

    def _create_netlist(self):
        netlist = Netlist()
        lib = netlist.create_library()
        defin = lib.create_definition()
        netlist.top_instance = Instance()
        netlist.top_instance.reference = defin
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
        nl1, nl2 = self._run_first()
        

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
        nl1, nl2 = self._run_first()
        nl3 = clone(nl1)
        self._compare_netlists(nl1, nl3)
        self._compare_netlists(nl1, nl2)
        #now check that no references overlap.
        assert nl3 != nl1, "The netlist references cannot be the same"
        for library in nl1.libraries:
            assert library not in nl3.libraries, "library references cannot be the same between netlists"
            for library2 in nl3.libraries:
                for definition1 in library.definitions:
                    assert definition1 not in library2.definitions, "definition references cannot be in both netlists libraries"
                    for definition2 in library2:
                        for instance1 in definition1.references:
                            assert instance1 not in definition2.references, "reference cannot cross netlist bounds"
                            for instance2 in definition2.references:
                                assert instance2.reference != instance1.reference, "references cannot be the same in 2 netlists."
                        for instance1 in definition1.children:
                            assert instance1 not in definition2.children, "instance cannot belong in definitions in 2 netlists"
                            for instance2 in definition2.references:
                                for pin1 in instance1.pins:
                                    assert pin1 not in instance2.pins, "pins can't be in 2 netlists"
                                    for pin2 in instance2.pins:
                                        assert pin1.wire != pin2.wire, "wires can't be referenced between 2 netlists"
                        for cable1 in definition1.cables:
                            assert cable1 not in definition2.cables, "cable cannot belong in definitions in 2 netlists"
                            for cable2 in definition2.cables:
                                for wire1 in cable1.wires:
                                    assert wire1 not in cable2.wires, "wire in 2 netlists"
                                    for wire2 in cable2.wires:
                                        for pin1 in wire1.pins:
                                            assert pin1 not in wire2.pins, "pin referenced accross netlist bounds"
                        for port1 in definition1.ports:
                            assert port1 not in definition2.ports, "port cannot belong in definitions in 2 netlists"
                            for port2 in definition2.ports:
                                for pin1 in port1.pins:
                                    assert pin1 not in port2.pins, "pin in 2 netlists"
                                    for pin2 in port2.pins:
                                        assert pin1.wire != pin2.wire, "wire referenced accross netlist bounds"

    def test_outerpin(self):
        pass

    def test_port(self):
        pass

    def test_wire(self):
        pass