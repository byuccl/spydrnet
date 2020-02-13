import unittest

from spydrnet.clone import clone
from spydrnet.ir import *
from spydrnet.compare.compare_netlists import Comparer


class TestClone(unittest.TestCase):
    
    def _get_two_netlists(self):
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


    def create_and_clone_cable(self, wirecount, array, downto, index, key, value):
        definition = Definition()
        p1 = definition.create_cable()
        p1[key] = value
        p1.create_wires(wirecount)
        p1.is_array = array
        p1.is_downto = downto
        p1.lower_index = index
        p2 = clone(p1)
        assert p2.lower_index == index
        assert p2.is_downto == downto
        assert p2.is_array == array
        assert len(p2.wires) == wirecount
        assert p2[key] == value
        assert p2.definition == None
        for pin in p2.wires:
            assert pin.cable is p2
            assert len(pin.pins) == 0

    def test_cable_array(self):
        pincount = 10
        array = True
        downto = False
        index = 5
        key = "EDIF.identifier"
        value = "myPort"
        self.create_and_clone_cable(pincount, array, downto, index, key, value)

    def test_cable_not_array(self):
        pincount = 1
        array = False
        downto = True
        index = 0
        key = "Name"
        value = "myPortName"
        self.create_and_clone_cable(pincount, array, downto, index, key, value)        

    def test_cable_single_bit_array(self):
        pincount = 1
        array = True
        downto = False
        index = 0
        key = "garbage_key"
        value = "garbage_value"
        self.create_and_clone_cable(pincount, array, downto, index, key, value)        

    def test_definition(self):
        pass

    def test_innerpin(self):
        port = Port()
        pin = port.create_pin()
        pin2 = pin.clone()
        assert pin2.wire == None
        assert pin2.port == None
        
    def test_instance(self):
        def1 = Definition()
        def2 = Definition()
        por2 = def2.create_port()
        por2.create_pins(5)
        child = def1.create_child()
        child.reference = def2
        inst2 = clone(child)
        assert inst2.parent == None
        assert inst2.reference is def2
        assert set(inst2.pins.keys()).difference(set(child.pins.keys())) == set()
        for v in inst2.pins.values():
            assert v not in child.pins.values()


    def test_library(self):
        pass

    def check_overlap_references(self, nl1, nl2):
        assert nl2 != nl1, "The netlist references cannot be the same"
        for library in nl1.libraries:
            assert library not in nl2.libraries, "library references cannot be the same between netlists"
            for library2 in nl2.libraries:
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
                            for port2 in definition2.ports:
                                for pin1 in port1.pins:
                                    assert pin1 not in port2.pins, "pin in 2 netlists"
                                    for pin2 in port2.pins:
                                        assert pin1.wire != pin2.wire, "wire referenced accross netlist bounds"

    def test_netlist(self):
        nl1, nl2 = self._get_two_netlists()
        nl3 = clone(nl1)
        self._compare_netlists(nl1, nl3)
        self._compare_netlists(nl1, nl2)
        #now check that no references overlap.
        self.check_overlap_references(nl1, nl3)

    def test_netlist_empty_top_instance(self):
        nl1 = self._create_netlist()
        nl1.top_instance = None
        nl2 = clone(nl1)
        self._compare_netlists(nl1, nl2)
        self.check_overlap_references(nl1, nl2)

    def test_netlist_top_instance_instanced_elsewhere(self):
        nl1 = self._create_netlist()
        in1 = nl1.libraries[0].definitions[0].create_child()
        in1.reference = nl1.libraries[0].create_definition()
        nl1.top_instance = in1

        nl2 = clone(nl1)
        self._compare_netlists(nl1, nl2)
        self.check_overlap_references(nl1, nl2)

    def test_outerpin(self):
        op = OuterPin()
        wire = Wire()
        inner = InnerPin()
        op._wire = wire
        op._inner_pin = inner
        op2 = clone(op)
        assert op2.wire == None
        assert op2.instance == None
        assert op2.inner_pin == None

    def create_and_clone_port(self, pincount, direction, array, downto, index, key, value):
        definition = Definition()
        p1 = definition.create_port()
        p1[key] = value
        p1.create_pins(pincount)
        p1.direction = direction
        p1.is_array = array
        p1.is_downto = downto
        p1.lower_index = index
        p2 = clone(p1)
        assert p2.lower_index == index
        assert p2.is_downto == downto
        assert p2.is_array == array
        assert p2.direction == direction
        assert len(p2.pins) == pincount
        assert p2[key] == value
        assert p2.definition == None
        for pin in p2.pins:
            assert pin.port is p2
            assert pin.wire == None

    def test_port_array(self):
        pincount = 10
        direction = Port.Direction.IN
        array = True
        downto = False
        index = 5
        key = "EDIF.identifier"
        value = "myPort"
        self.create_and_clone_port(pincount, direction, array, downto, index, key, value)        
    
    def test_port_not_array(self):
        pincount = 1
        direction = Port.Direction.OUT
        array = False
        downto = True
        index = 0
        key = "Name"
        value = "myPortName"
        self.create_and_clone_port(pincount, direction, array, downto, index, key, value)        

    def test_port_single_bit_array(self):
        pincount = 1
        direction = Port.Direction.INOUT
        array = True
        downto = False
        index = 0
        key = "garbage_key"
        value = "garbage_value"
        self.create_and_clone_port(pincount, direction, array, downto, index, key, value)        

    def test_port_with_connectivity(self):
        pass

    def test_wire(self):
        cable = Cable()
        wire = cable.create_wire()
        wire2 = clone(wire)
        assert len(wire2.pins) == 0
        assert wire2.cable == None