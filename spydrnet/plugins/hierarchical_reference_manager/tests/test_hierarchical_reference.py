import unittest
import spydrnet as sdn
from spydrnet.plugins.hierarchical_reference_manager.hierarchical_reference import HRef, HRefBase


class TestHRefBase(unittest.TestCase):
    def test_href_equality(self):
        top = sdn.Instance()
        top_def = sdn.Definition()
        top.reference = top_def
        middle = top_def.create_child()
        middle_def = sdn.Definition()
        middle.reference = middle_def
        leaf = middle_def.create_child()
        leaf_def = sdn.Definition()
        leaf.reference = leaf_def
        sequence = [top, middle, leaf]
        href1 = HRefBase.from_sequence(sequence)
        href2 = HRefBase.from_sequence(sequence)
        self.assertEqual(href1, href1)
        self.assertNotEqual(href1, None)
        self.assertEqual(href1, href2)
        self.assertNotEqual(href1, href2.parent)
        href3 = HRefBase.from_sequence(sequence[1:])
        self.assertNotEqual(href1, href3)

    def test_href_wire_name(self):
        top = sdn.Instance()
        top.name = "TOP"
        top_def = sdn.Definition()
        top.reference = top_def
        cable = top_def.create_cable()
        cable.name = "CABLE"
        cable.create_wires(1)
        cable.is_array = True
        wire = cable.wires[0]
        sequence = [top, cable, wire]
        self.assertEqual("TOP/CABLE[0]", HRefBase.from_sequence(sequence).name)

    def test_href_pin_name(self):
        top = sdn.Instance()
        top.name = "TOP"
        top_def = sdn.Definition()
        top.reference = top_def
        port = top_def.create_port()
        port.name = "PORT"
        port.create_pins(1)
        port.is_array = True
        wire = port.pins[0]
        sequence = [top, port, wire]
        self.assertEqual("TOP/PORT[0]", HRefBase.from_sequence(sequence).name)


class TestHRef(unittest.TestCase):
    def test_create_href_from_item_without_parent_or_netlist(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        instance = sdn.Instance()
        instance.reference = definition
        href = HRef.from_item(instance)
