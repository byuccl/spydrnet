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
        lib1 = netlist.create_library()
        lib2 = netlist.create_library()
        def1 = lib1.create_definition()
        def2 = lib2.create_definition()
        def3 = lib1.create_definition()
        def4 = lib2.create_definition()
        ins1 = def1.create_child()
        ins2 = def2.create_child()
        ins3 = def3.create_child()
        def4.create_child()
        ins1.reference = def2
        ins2.reference = def3
        ins3.reference = def4
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
        lib = Library()
        def1 = lib.create_definition()
        def2 = lib.create_definition()
        ins1 = def2.create_child()
        ins2 = def2.create_child()
        ins1.reference = def1
        ins2.reference = def1
        def2.create_port()
        def2.create_cable()
        def3 = clone(def2)
        assert def3.library == None
        assert len(def3.children) == len(def2.children)
        assert len(def3.cables) == len(def2.cables)
        assert len(def3.ports) == len(def2.ports)
        for p in def3.ports:
            assert p not in def2.ports
        for c in def3.cables:
            assert c not in def2.cables
        for c in def3.children:
            assert c not in def2.children
            assert c in def1.references
        assert len(def1.references) == 4

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


    def test_library_instance_references(self):
        lib1 = Library()
        lib2 = Library()
        def1 = lib1.create_definition()
        def2 = lib1.create_definition()
        def3 = lib2.create_definition()
        ins2 = def1.create_child()
        ins3 = def1.create_child()
        ins2.reference = def2
        ins3.reference = def3
        lib3 = clone(lib1)
        assert lib3.netlist == None
        assert len(lib3.definitions) == len(lib1.definitions)
        for d in lib3.definitions:
            assert d not in lib1.definitions
        def1c = lib3.definitions[0]
        def2c = lib3.definitions[1]
        ins2c = def1c.children[0]
        ins3c = def1c.children[1]
        assert ins2c in def2c.references
        assert ins2c not in def2.references
        assert ins3c in def3.references
        assert ins2c.reference is def2c
        assert ins3c.reference is def3
        assert ins2 in def2.references
        assert ins2 not in def2c.references
        assert len(def3.references) == 2


    def test_library_definition_references(self):
        lib1 = Library()
        lib2 = Library()
        def1 = lib1.create_definition()
        def2 = lib2.create_definition()
        ins1 = def2.create_child()
        ins1.reference = def1
        lib3 = clone(lib1)
        def1c = lib3.definitions[0]
        assert len(def1c.references) == 0
        assert ins1.reference is def1

    def check(self, r1, e):
        if e is None:
            return
        assert e not in r1

    def not_among_all_references(self,r1, nl1):
        self.check(r1, nl1)
        self.check(r1, nl1.top_instance)
        for l in nl1.libraries:
            self.check(r1, l)
            for d in l.definitions:
                self.check(r1, d)
                for c in d.children:
                    self.check(r1, c)
                    self.check(r1, c.reference)
                    for k, v in c.pins.items():
                        self.check(r1, k)
                        self.check(r1, v)
                for r in d.references:
                    self.check(r1, r)
                for c in d.cables:
                    self.check(r1, c)
                    for w in c.wires:
                        self.check(r1, w)
                for p in d.ports:
                    self.check(r1, p)
                    for pi in p.pins:
                        self.check(r1, pi)

    def add_all_references(self,r1, nl1):
        r1.add(nl1)
        r1.add(nl1.top_instance)
        for l in nl1.libraries:
            r1.add(l)
            for d in l.definitions:
                r1.add(d)
                for c in d.children:
                    r1.add(c)
                    r1.add(c.reference)
                    for k, v in c.pins.items():
                        r1.add(k)
                        r1.add(v)
                for r in d.references:
                    r1.add(r)
                for c in d.cables:
                    r1.add(c)
                    for w in c.wires:
                        r1.add(w)
                for p in d.ports:
                    r1.add(p)
                    for pi in p.pins:
                        r1.add(pi)

    def check_overlap_references(self, nl1, nl2):
        r1 = set()
        self.add_all_references(r1, nl1)
        self.not_among_all_references(r1, nl2)
        
    def test_netlist_several_lib(self):
        netlist = Netlist()
        lib1 = netlist.create_library()
        lib2 = netlist.create_library()
        lib3 = netlist.create_library()
        lib4 = netlist.create_library()
        def1a = lib1.create_definition()
        def2a = lib2.create_definition()
        def3a = lib3.create_definition()
        def4a = lib4.create_definition()
        def1b = lib1.create_definition()
        def2b = lib2.create_definition()
        def3b = lib3.create_definition()
        def4b = lib4.create_definition()
        ins1a = def1a.create_child()
        ins2a = def2a.create_child()
        ins3a = def3a.create_child()
        ins4a = def4a.create_child()
        ins1b = def1b.create_child()
        ins2b = def2b.create_child()
        ins3b = def3b.create_child()
        def4b.create_child()
        ins1a.reference = def2a
        ins2a.reference = def3a
        ins3a.reference = def4a
        ins4a.reference = def1b
        ins1b.reference = def2b
        ins2b.reference = def3b
        ins3b.reference = def4b
        netlist2 = clone(netlist)
        self._compare_netlists(netlist, netlist2)
        self.check_overlap_references(netlist, netlist2)
        
    def test_netlist_change_top_instance(self):
        nl1 = Netlist()
        lib1 = nl1.create_library()
        def1 = lib1.create_definition()
        nl1.top_instance = Instance()
        nl1.top_instance.reference = def1
        nl1.top_instance = None
        nl2 = clone(nl1)
        self._compare_netlists(nl1, nl2)
        self.check_overlap_references(nl1, nl2)


    def test_library_change_top_instace(self):
        nl1 = Netlist()
        nl2 = Netlist()
        lib1 = nl1.create_library()
        def1 = lib1.create_definition()
        nl1.top_instance = Instance()
        nl1.top_instance.reference = def1
        nl1.top_instance = None
        lib2 = clone(lib1)
        nl2.add_library(lib2)
        self._compare_netlists(nl1, nl2)
        self.check_overlap_references(nl1, nl2)
        
    
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
        pass #TODO

    def test_wire(self):
        cable = Cable()
        wire = cable.create_wire()
        wire2 = clone(wire)
        assert len(wire2.pins) == 0
        assert wire2.cable == None