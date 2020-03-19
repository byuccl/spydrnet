import unittest
import spydrnet as sdn


class TestGetHPins(unittest.TestCase):
    netlist = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.netlist = sdn.load_example_netlist_by_name('b13')

    def test_wild_card_search_on_netlist(self):
        hrefs = list(sdn.get_hpins(self.netlist))
        self.assertTrue(len(hrefs) == 22 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))

    def test_wild_card_search_on_netlist_recursive(self):
        hrefs = list(sdn.get_hpins(self.netlist, recursive=True))
        self.assertTrue(len(hrefs) == 510 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))

    def test_absolute_search_excluded(self):
        href = next(self.netlist.get_hpins('this_is_not_contained'), None)
        self.assertIsNone(href)

    def test_absolute_search(self):
        href = next(self.netlist.get_hpins('clock'), None)
        self.assertIsNotNone(href)
        self.assertIsInstance(href.item, sdn.InnerPin)

    def test_regex_search(self):
        hrefs = list(sdn.get_hpins(self.netlist, '.*dAtA.*', is_re=True, is_case=False))
        self.assertTrue(len(hrefs) == 9 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))

    def test_parameters(self):
        self.assertRaises(TypeError, sdn.get_hpins, self.netlist, r'.*FSM_onehot.*', patterns=r".*FSM_onehot.*")
        self.assertRaises(TypeError, sdn.get_hpins, self.netlist, parameter_does_not_exit=True)
        self.assertRaises(TypeError, sdn.get_hpins, object())

    def test_get_hpins_of_pin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        port = definition.ports[0]
        pin = port.pins[0]
        hrefs = list(sdn.get_hpins(pin))
        self.assertTrue(len(hrefs) == 1)
        self.assertIsInstance(hrefs[0].item, sdn.InnerPin)

    def test_get_hpins_of_wire(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hpins(wire))
        self.assertTrue(len(hrefs) == 2)
        self.assertIsInstance(hrefs[0].item, sdn.InnerPin)

    def test_get_hwire_of_invalid_reference(self):
        from spydrnet.util.hierarchical_reference import HRef
        invalid_href = HRef.from_parent_and_item(None, None)
        hrefs = list(sdn.get_hpins(invalid_href))
        self.assertTrue(len(hrefs) == 0)

    def test_get_hpin_from_href_pin(self):
        pin = self.netlist.libraries[1].definitions[0].ports[0].pins[0]
        href = next(pin.get_hpins())
        href_from_href = next(sdn.get_hpins(href))
        self.assertIs(href, href_from_href)

    def test_get_hpins_from_hrefs_of_cable_and_wire(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        cable_href = next(cable.get_hcables())
        wire_href = next(wire.get_hwires())
        href_cable_pins = set(sdn.get_hpins(cable_href))
        href_wire_pins = set(sdn.get_hpins(wire_href))
        self.assertTrue(len(href_cable_pins) > 0 and len(href_wire_pins) > 0)
        self.assertTrue(all(isinstance(x.item, sdn.InnerPin) for x in href_cable_pins))
        self.assertTrue(all(isinstance(x.item, sdn.InnerPin) for x in href_wire_pins))
        self.assertTrue(all(x in href_cable_pins for x in href_wire_pins))

    def test_get_hpins_from_hrefs_of_port_and_pin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        port = definition.ports[0]
        pin = port.pins[0]
        hrefs = list(sdn.get_hinstances(pin))
        href = hrefs[0]
        from spydrnet.util.hierarchical_reference import HRef
        port_href = HRef.from_parent_and_item(href, port)
        pin_href = HRef.from_parent_and_item(port_href, pin)
        href_result = next(sdn.get_hpins(port_href), None)
        self.assertTrue(href_result is pin_href)
        href_result = next(sdn.get_hpins(pin_href), None)
        self.assertTrue(href_result is pin_href)

    def test_from_href_of_instance(self):
        href = next(sdn.get_hinstances(self.netlist.top_instance))
        hrefs = list(sdn.get_hpins(href))
        self.assertTrue(len(hrefs) == 22 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))

    def test_from_instance(self):
        hrefs = list(sdn.get_hpins(self.netlist.top_instance))
        self.assertTrue(len(hrefs) == 22 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))

    def test_from_library(self):
        hrefs = list(sdn.get_hpins(self.netlist.libraries[0]))
        self.assertTrue(len(hrefs) == 488 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))

    def test_from_wire_and_cable(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hpins(wire))
        self.assertTrue(len(hrefs) == 2 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))
        hrefs = list(sdn.get_hpins(cable))
        self.assertTrue(len(hrefs) == 2 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))

    def test_from_outerpin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        instance = definition.children[0]
        outerpin = next(iter(instance.pins))
        hrefs = list(sdn.get_hpins(outerpin))
        self.assertTrue(len(hrefs) == 1 and all(isinstance(x.item, sdn.InnerPin) for x in hrefs))

    def test_bad_selection_type(self):
        self.assertRaises(TypeError, self.netlist.get_hpins, selection="NOT_AN_OPTION")
        self.assertRaises(TypeError, self.netlist.get_hpins, selection=None)

    def test_of_bad_instance(self):
        hrefs = list(sdn.get_hpins(sdn.Instance()))
        self.assertTrue(len(hrefs) == 0)

    def test_through_hierarchy_again(self):
        netlist = sdn.Netlist()

        library = netlist.create_library()
        library.name = 'work'

        leaf_def = library.create_definition()
        leaf_def.name = 'leaf'
        leaf_port = leaf_def.create_port()
        leaf_port.name = 'I'
        leaf_port.create_pins(1)

        bottom_def = library.create_definition()
        bottom_def.name = 'bottom'
        bottom_port = bottom_def.create_port()
        bottom_port.name = 'I'
        bottom_port.create_pins(1)
        leaf_inst = bottom_def.create_child()
        leaf_inst.name = 'leaf'
        leaf_inst.reference = leaf_def
        bottom_cable = bottom_def.create_cable()
        bottom_cable.name = 'bottom_cable'
        bottom_wire = bottom_cable.create_wire()
        bottom_wire.connect_pin(bottom_port.pins[0])
        bottom_wire.connect_pin(leaf_inst.pins[leaf_port.pins[0]])

        bottom_floating_wire = bottom_cable.create_wire()

        middle_def = library.create_definition()
        middle_def.name = 'middle'
        middle_port = middle_def.create_port()
        middle_port.name = "I"
        middle_port.create_pin()
        bottom_inst = middle_def.create_child()
        bottom_inst.name = 'bottom'
        bottom_inst.reference = bottom_def
        middle_cable = middle_def.create_cable()
        middle_cable.name = "middle_cable"
        middle_wire = middle_cable.create_wire()
        middle_wire.connect_pin(middle_port.pins[0])
        middle_wire.connect_pin(bottom_inst.pins[bottom_port.pins[0]])

        middle_floating_wire = middle_cable.create_wire()

        top_def = library.create_definition()
        top_def.name = 'top'
        top_port = top_def.create_port()
        top_port.name = "I"
        top_port.create_pin()
        middle_inst = top_def.create_child()
        middle_inst.name = 'middle'
        middle_inst.reference = middle_def
        top_cable = top_def.create_cable()
        top_cable.name = "top_cable"
        top_wire = top_cable.create_wire()
        top_wire.connect_pin(top_port.pins[0])
        top_wire.connect_pin(middle_inst.pins[middle_port.pins[0]])

        top_floating_wire = top_cable.create_wire()

        top_instance = sdn.Instance()
        top_instance.name = 'top'
        top_instance.reference = top_def
        netlist.top_instance = top_instance

        #look at wire_name
        href = next(netlist.get_hpins('I'))
        self.assertTrue('clock', href.name)
        hrefs = set(sdn.get_hpins(netlist.top_instance, recursive=True))
        self.assertTrue(href in hrefs)

        hrefs = set(sdn.get_hpins(middle_cable))
        href_top_pin = next(sdn.get_hpins(top_port.pins[0]))
        href_middle_pin = next(sdn.get_hpins(middle_port.pins[0]))
        href_bottom_pin = next(sdn.get_hpins(bottom_port.pins[0]))
        self.assertTrue(href_top_pin not in hrefs and href_middle_pin in hrefs and href_bottom_pin in hrefs)

        hrefs = set(sdn.get_hpins(top_def, recursive=True))
        self.assertTrue(href_top_pin in hrefs and href_middle_pin in hrefs and href_bottom_pin in hrefs)

        all_pins = set(netlist.get_hpins())
        self.assertTrue(len(all_pins) == 1)

        all_pins = set(netlist.get_hpins(recursive=True))
        self.assertTrue(len(all_pins) == 4)
