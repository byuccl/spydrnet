import unittest
import spydrnet as sdn


class TestGetHWires(unittest.TestCase):
    netlist = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.netlist = sdn.load_example_netlist_by_name('b13')

    def test_wild_card_search_on_netlist(self):
        hrefs = list(sdn.get_hwires(self.netlist))
        self.assertTrue(len(hrefs) > 0)

    def test_absolute_search(self):
        href = next(self.netlist.get_hwires('<const0>'), None)
        self.assertIsNotNone(href)

    def test_regex_search(self):
        hrefs = list(sdn.get_hwires(self.netlist, '.*FSM_onehot.*', is_re=True))
        self.assertTrue(len(hrefs) == 21)

    def test_parameters(self):
        self.assertRaises(TypeError, sdn.get_hwires, self.netlist, r'.*FSM_onehot.*', patterns=r".*FSM_onehot.*")
        self.assertRaises(TypeError, sdn.get_hwires, self.netlist, parameter_does_not_exit=True)
        self.assertRaises(TypeError, sdn.get_hwires, object())

    def test_get_hwires_of_pin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        port = definition.ports[0]
        pin = port.pins[0]
        hrefs = list(sdn.get_hwires(pin))
        self.assertTrue(len(hrefs) == 1)

    def test_get_hwires_of_wire(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hwires(wire))
        self.assertTrue(len(hrefs) == 1)

    def test_get_hwire_of_invalid_reference(self):
        from spydrnet.util.hierarchical_reference import HRef
        invalid_href = HRef.from_parent_and_item(None, None)
        hrefs = list(sdn.get_hwires(invalid_href))
        self.assertTrue(len(hrefs) == 0)

    def test_get_hwires_from_hrefs_of_cable_and_wire(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hinstances(wire))
        href_top = hrefs[0]
        from spydrnet.util.hierarchical_reference import HRef
        cable_href = HRef.from_parent_and_item(href_top, cable)
        wire_href = HRef.from_parent_and_item(cable_href, wire)
        href_result = next(sdn.get_hwires(cable_href), None)
        self.assertTrue(href_result is wire_href)
        href_result = next(sdn.get_hwires(wire_href), None)
        self.assertTrue(href_result is wire_href)

    def test_get_hwires_from_hrefs_of_port_and_pin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        port = definition.ports[0]
        pin = port.pins[0]
        hrefs = list(sdn.get_hwires(pin))
        href = hrefs[0]
        from spydrnet.util.hierarchical_reference import HRef
        port_href = HRef.from_parent_and_item(href.parent.parent, port)
        href_result = next(sdn.get_hwires(port_href), None)
        self.assertTrue(href_result is href)
        pin_href = HRef.from_parent_and_item(port_href, pin)
        href_result = next(sdn.get_hwires(pin_href), None)
        self.assertTrue(href_result is href)

    def test_from_href_of_instance(self):
        href = next(sdn.get_hinstances(self.netlist.top_instance))
        hrefs = list(sdn.get_hwires(href))
        self.assertTrue(len(hrefs) == 114)

    def test_from_instance(self):
        hrefs = list(sdn.get_hwires(self.netlist.top_instance))
        self.assertTrue(len(hrefs) == 114)

    def test_from_library(self):
        hrefs = list(sdn.get_hwires(self.netlist.libraries[0], selection=sdn.OUTSIDE))
        self.assertTrue(len(hrefs) == 114)

    def test_from_wire_and_cable(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hwires(wire))
        self.assertTrue(len(hrefs) == 1)
        hrefs = list(sdn.get_hwires(cable))
        self.assertTrue(len(hrefs) == 1)

    def test_from_outerpin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        instance = definition.children[0]
        outerpin = next(iter(instance.pins))
        hrefs = list(sdn.get_hwires(outerpin, selection=sdn.OUTSIDE))
        self.assertTrue(len(hrefs) == 1)

    def test_of_bad_instance(self):
        hrefs = list(sdn.get_hwires(sdn.Instance()))
        self.assertTrue(len(hrefs) == 0)

    def test_through_hierarchy(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        instance = sdn.Instance()
        instance.reference = definition
        netlist.top_instance = instance

        middle_inst = definition.create_child()
        middle_def = library.create_definition()
        middle_cable = middle_def.create_cable()
        middle_wire = middle_cable.create_wire()
        middle_inst.reference = middle_def

        leaf_inst = middle_def.create_child()
        leaf_def = library.create_definition()
        leaf_inst.reference = leaf_def

        top_inst_href = next(sdn.get_hinstances(netlist.top_instance))
        hrefs = list(sdn.get_hwires(top_inst_href, recursive=True))
        self.assertTrue(len(hrefs) == 1)

        hrefs = list(sdn.get_hwires(middle_inst))
        self.assertTrue(len(hrefs) == 1)
