import unittest
import spydrnet as sdn
from spydrnet.util.hierarchical_reference import HRef


class TestHRefBase(unittest.TestCase):
    def test_is_unique(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition1 = library.create_definition()
        instance1 = definition1.create_child()

        definition2 = library.create_definition()
        instance2a = definition2.create_child()
        instance2a.reference = definition1
        instance2b = definition2.create_child()
        instance2b.reference = definition1

        instance3 = sdn.Instance()
        instance3.reference = definition2
        netlist.top_instance = instance3

        href1 = HRef.from_sequence([instance3, instance2a, instance1])
        href2 = HRef.from_sequence([instance3, instance2b, instance1])

        # Another test for test_flyweight stuffed in here :)
        self.assertTrue(href1.parent.parent is href2.parent.parent)
        self.assertTrue(href1.is_valid)
        self.assertTrue(href2.is_valid)
        self.assertFalse(href2.is_unique)

        self.assertFalse(href1.is_unique)
        definition2.remove_child(instance2b)
        self.assertFalse(href2.is_valid)
        self.assertFalse(href2.is_unique)
        self.assertTrue(href1.is_unique)

        definition4 = library.create_definition()
        definition4.add_child(instance2b)
        instance4 = sdn.Instance()
        instance4.reference = definition4
        definition2.add_child(instance4)
        self.assertFalse(href1.is_unique)

    def test_flyweight(self):
        instance = sdn.Instance()
        href1 = HRef.from_parent_and_item(None, instance)
        href2 = HRef.from_parent_and_item(None, instance)
        self.assertTrue(href1 is href2)
        import weakref
        w_href1 = weakref.ref(href1)
        w_href2 = weakref.ref(href2)
        href1 = None
        href2 = None
        import gc
        gc.collect()
        self.assertIsNone(w_href1())
        self.assertIsNone(w_href2())

        instance2 = sdn.Instance()
        href1 = HRef.from_sequence([instance, instance2])
        href2_parent = HRef(instance, None)
        href2 = HRef.from_parent_and_item(href2_parent, instance2)
        self.assertTrue(href1 is href2)

    def test_href_valid(self):
        instance = sdn.Instance()
        href = HRef.from_parent_and_item(None, instance)
        self.assertFalse(href.is_valid)

        definition = sdn.Definition()
        instance.reference = definition
        self.assertFalse(href.is_valid)

        library = sdn.Library()
        library.add_definition(definition)
        self.assertFalse(href.is_valid)

        netlist = sdn.Netlist()
        netlist.add_library(library)
        self.assertFalse(href.is_valid)

        netlist.top_instance = instance
        self.assertTrue(href.is_valid)

        cable = sdn.Cable()
        wire = sdn.Wire()

        href = HRef.from_sequence([instance, cable, wire])
        self.assertFalse(href.is_valid)

        cable.add_wire(wire)
        self.assertFalse(href.is_valid)

        definition.add_cable(cable)
        self.assertTrue(href.is_valid)

        instance.reference = None
        self.assertFalse(href.is_valid)

        port = sdn.Port()
        pin  = sdn.InnerPin()

        href = HRef.from_sequence([instance, port, pin])
        self.assertFalse(href.is_valid)

        port.add_pin(pin)
        self.assertFalse(href.is_valid)

        definition.add_port(port)
        self.assertFalse(href.is_valid)

        instance.reference = definition
        self.assertTrue(href.is_valid)

        higher_definition = library.create_definition()
        higher_definition.add_child(instance)
        self.assertTrue(href.is_valid)

        higher_instance = sdn.Instance()
        higher_instance.reference = higher_definition
        netlist.top_instance = higher_instance
        self.assertFalse(href.is_valid)

        href = HRef.from_sequence([higher_instance, instance, cable, wire])
        self.assertTrue(href.is_valid)
        higher_instance.reference = None
        self.assertFalse(href.is_valid)
        higher_definition.remove_child(instance)
        self.assertFalse(href.is_valid)

        definition.remove_cable(cable)
        self.assertFalse(href.is_valid)

        cable.remove_wire(wire)
        self.assertFalse(href.is_valid)

        cable.add_wire(wire)
        href = HRef.from_sequence([cable, wire])
        self.assertFalse(href.is_valid)

        cable.remove_wire(wire)
        new_cable = sdn.Cable()
        new_cable.add_wire(wire)
        self.assertFalse(href.is_valid)

        href = HRef.from_parent_and_item(None, wire)
        self.assertFalse(href.is_valid)

        port.remove_pin(pin)
        new_port = sdn.Port()
        new_port.add_pin(pin)
        href = HRef.from_sequence([port, pin])
        self.assertFalse(href.is_valid)

        href = HRef.from_parent_and_item(None, pin)
        self.assertFalse(href.is_valid)

        href = HRef.from_parent_and_item(None, definition)
        self.assertFalse(href.is_valid)

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
        href1 = HRef.from_sequence(sequence)
        href2 = HRef.from_sequence(sequence)
        self.assertEqual(href1, href1)
        self.assertNotEqual(href1, None)
        self.assertEqual(href1, href2)
        self.assertNotEqual(href1, href2.parent)
        href3 = HRef.from_sequence(sequence[1:])
        self.assertNotEqual(href1, href3)

    def test_href_inst_name(self):
        instance = sdn.Instance()
        instance.name = "MY_INST"
        href = HRef.from_parent_and_item(None, instance)
        self.assertEqual('', href.name)

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
        self.assertEqual("CABLE[0]", HRef.from_sequence(sequence).name)

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
        self.assertEqual("PORT[0]", HRef.from_sequence(sequence).name)

    def test_href_str_and_repr(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        instance = sdn.Instance()
        instance.reference = definition
        netlist.top_instance = instance

        cable = definition.create_cable()
        cable.name = "MY_CABLE"
        cable.create_wires(8)
        href = HRef.from_sequence([instance, cable])
        href_str = str(href)
        self.assertTrue(href_str == "MY_CABLE")
        href_repr = repr(href)
        self.assertTrue(HRef.__name__ in href_repr)
        self.assertTrue(cable.__class__.__name__ in href_repr)

    def test_get_all_hrefs_of_item(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        instance = sdn.Instance()
        instance.reference = definition
        netlist.top_instance = instance

        href = next(HRef.get_all_hrefs_of_item(instance))
        self.assertTrue(href.item is instance)

        href = next(HRef.get_all_hrefs_of_item(definition))
        self.assertTrue(href.item is instance)

        port = definition.create_port()
        href = next(HRef.get_all_hrefs_of_item(port))
        self.assertTrue(href.is_valid and href.item is port)
