import unittest


from spydrnet.ir import FirstClassElement
from spydrnet.ir import Instance
from spydrnet.ir import Definition
from spydrnet.ir import Netlist
from spydrnet.ir import Cable
from spydrnet.ir import Wire
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.ir import Library
from spydrnet.ir import Port

class TestShortcuts(unittest.TestCase):
    def test_hRef_shortcut(self):
        item = Instance("myCable")
        def2 = Definition("Hello")
        item.reference = def2
        hr = HRef(item)
        self.assertEqual(hr.item.name,item.name,'Href item shorcut error')


    def test_netlist_top_instance_definition_shortcut(self):
        top_definition = Definition('this is my name')
        netlist = Netlist()
        netlist.top_instance = top_definition
        self.assertEqual(netlist.top_instance.reference.name,top_definition.name,'Netlist\'s top instance\'s shorcut error')

    def test_if_leaf_shortcut(self):
        instance = Instance()
        definition = Definition()
        instance.reference = definition
        self.assertEqual(definition.is_leaf(), instance.is_leaf(), 'is_leaf shortcut error')
        definition.create_cable()
        instance.reference = definition
        self.assertEqual(definition.is_leaf(), instance.is_leaf(), 'is_leaf shortcut error')

    def test_wire_index_shortcut(self):
        cable = Cable()
        cable.create_wires(3)
        wire = Wire()
        cable.add_wire(wire,1)
        self.assertEqual(wire.cable.wires.index(wire), wire.index(), 'wire index shorcut error')
        self.assertEqual(wire.index(), 1, 'wire index shorcut error')
        wire2 = Wire()
        cable.add_wire(wire2,3)
        self.assertEqual(wire2.cable.wires.index(wire2), wire2.index(), 'wire index shorcut error')
        self.assertEqual(wire2.index(), 3, 'wire index shorcut error')

    def test_name_init_shortcut(self):
        d = Definition('d_name')
        self.assertEqual(d.name, 'd_name', 'Definition name init shorcut error')
        l = Library('l_name')
        self.assertEqual(l.name, 'l_name', 'Library name init shorcut error')
        n = Netlist('n_name')
        self.assertEqual(n.name, 'n_name', 'Netlist name init shorcut error')
        i = Instance('i_name')
        self.assertEqual(i.name, 'i_name', 'Instance name init shorcut error')
        c = Cable('c_name')
        self.assertEqual(c.name, 'c_name', 'Cable name init shorcut error')
        p = Port('p_name')
        self.assertEqual(p.name, 'p_name', 'Port name init shorcut error')

    def test_cable_shortcut(self):
        c = Cable('c_name', None,  False, True, 2)
        self.assertEqual(c.name, 'c_name', 'Cable name init shorcut error')
        self.assertEqual(c.is_downto, False, 'Cable is_downto init shorcut error')
        self.assertEqual(c.is_scalar, True, 'Cable is_scalar init shorcut error')
        self.assertEqual(c.lower_index, 2, 'Cable lower_index init shorcut error')

        c2 = Cable(is_scalar =  False)
        self.assertEqual(c2.name, None, 'Cable name init shorcut error')
        self.assertEqual(c2.is_downto, True, 'Cable is_downto init shorcut error')
        self.assertEqual(c2.is_scalar, False, 'Cable is_scalar init shorcut error')
        self.assertEqual(c2.lower_index, 0, 'Cable lower_index init shorcut error')


    def test_port_shortcut(self):
        p = Port('p_name', None, False, True, 4)

        self.assertEqual(p.name, 'p_name', 'Port name init shorcut error')
        self.assertEqual(p.is_downto, False, 'Port is_downto init shorcut error')
        self.assertEqual(p.is_scalar, True, 'Port is_scalar init shorcut error')
        self.assertEqual(p.lower_index, 4, 'Port lower_index init shorcut error')

        p2 = Port(is_downto =  False)
        self.assertEqual(p2.name, None, 'Port name init shorcut error')
        self.assertEqual(p2.is_downto, False, 'Port is_downto init shorcut error')
        self.assertEqual(p2.is_scalar, True, 'Port is_scalar init shorcut error')
        self.assertEqual(p2.lower_index, 0, 'Port lower_index init shorcut error')

    def test_properties_init_shortcut(self):

        d = Definition('d_name',{'key1':1, 'key2':'value2' })
        self.assertEqual(d['key1'], 1, 'Definition properties init shorcut error')

        l = Library('l_name',{'key1':'value1', 'key2':'value2' })
        self.assertEqual(l['key1'], 'value1', 'Library properties init shorcut error')

        n = Netlist('n_name',{'key1':'value1', 'key2': 63 })
        self.assertEqual(n['key2'], 63, 'Netlist properties init shorcut error')

        i = Instance('i_name',{'key1':'value1', 'key2':'value2' })
        self.assertEqual(i['key1'], 'value1', 'Instance properties init shorcut error')

        c = Cable('c_name',{'key1':'value1', 'key2':'value2' })
        self.assertEqual(c['key2'], 'value2', 'Cable properties init shorcut error')

        p = Port('p_name',{'key1':'value1', 'key2':'value2' })
        self.assertEqual(p['key1'], 'value1', 'Port properties init shorcut error')

    def test_library_child_instance_creation(self):
        l = Library('l_name',{'key1':'value1', 'key2':'value2' })
        self.assertEqual(l['key1'], 'value1', 'Library properties init shorcut error')

        l.create_definition("l_d_name", {'key1': 50, 'key2':'value2' })
        self.assertEqual('l_d_name', l.definitions[0].name, 'library\'s definition cretion shorcut error')
        self.assertEqual(l.definitions[0]['key1'], 50, 'library\'s definition cretion shorcut error')

        l2 = Library()
        l2.create_definition(properties = {'key1': 50, 'key2':'value2' })
        self.assertEqual(l2.definitions[0]['key1'], 50, 'library\'s definition cretion shorcut error')

    def test_definition_child_instance_creation(self):
        d = Definition('d_name',{'key1':1, 'key2':'value2' })
        self.assertEqual(d['key1'], 1, 'Definition properties init shorcut error')

        d.create_port('p_name')
        self.assertEqual(d.ports[0].name, 'p_name', 'Port name init shorcut error')
        d.create_port(properties = {'key1':'value1', 'key2':'value2' })
        self.assertEqual(d.ports[1]['key1'], 'value1', 'Port properties init shorcut error')

        d.create_port(properties = {'key1':'value1', 'key2':'value2' })
        self.assertEqual(d.ports[1]['key1'], 'value1', 'Port properties init shorcut error')

        d.create_child('d_c_name', {'key1':1, 'key2':'value2' })
        self.assertEqual(d.children[0]['key1'], 1, 'Definition properties init shorcut error')
        self.assertEqual(d['key1'], 1, 'Definition properties init shorcut error')

        d.create_cable('c_name', None,  False, True, 2)
        self.assertEqual(d.cables[0].name, 'c_name', 'Cable name init shorcut error')
        self.assertEqual(d.cables[0].is_downto, False, 'Cable is_downto init shorcut error')
        self.assertEqual(d.cables[0].is_scalar, True, 'Cable is_scalar init shorcut error')
        self.assertEqual(d.cables[0].lower_index, 2, 'Cable lower_index init shorcut error')

        d.create_cable(is_scalar =  False)
        self.assertEqual(d.cables[1].name, None, 'Cable name init shorcut error')
        self.assertEqual(d.cables[1].is_downto, True, 'Cable is_downto init shorcut error')
        self.assertEqual(d.cables[1].is_scalar, False, 'Cable is_scalar init shorcut error')
        self.assertEqual(d.cables[1].lower_index, 0, 'Cable lower_index init shorcut error')

    def test_netlist_child_instance_creation(self):
        n = Netlist('n_name')
        self.assertEqual(n.name, 'n_name', 'Netlist name init shorcut error')
        n.create_library('l_name',{'key1':'value1', 'key2':'value2' })
        self.assertEqual(n.libraries[0]['key1'], 'value1', 'Library properties init shorcut error')








