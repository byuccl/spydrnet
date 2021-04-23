import unittest
import spydrnet as sdn


class TestGetHCables(unittest.TestCase):
    netlist = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.netlist = sdn.load_example_netlist_by_name('b13')

    def test_wild_card_search_on_netlist(self):
        hrefs = list(sdn.get_hcables(self.netlist))
        self.assertTrue(len(hrefs) == 76 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

    def test_absolute_search(self):
        href = next(self.netlist.get_hcables('<const0>'), None)
        self.assertIsNotNone(href)
        self.assertIsInstance(href.item, sdn.Cable)

    def test_regex_search(self):
        hrefs = list(sdn.get_hcables(
            self.netlist, '.*FSM_onehot.*', is_re=True))
        self.assertTrue(len(hrefs) == 8 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

    def test_parameters(self):
        self.assertRaises(TypeError, sdn.get_hcables, self.netlist,
                          r'.*FSM_onehot.*', patterns=r".*FSM_onehot.*")
        self.assertRaises(TypeError, sdn.get_hcables,
                          self.netlist, parameter_does_not_exit=True)
        self.assertRaises(TypeError, sdn.get_hcables, object())

    def test_get_hcables_of_pin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        port = definition.ports[0]
        pin = port.pins[0]
        hrefs = list(sdn.get_hcables(pin))
        self.assertTrue(len(hrefs) == 1)
        self.assertIsInstance(hrefs[0].item, sdn.Cable)

    def test_get_hcables_of_wire(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hcables(wire))
        self.assertTrue(len(hrefs) == 1)
        self.assertIsInstance(hrefs[0].item, sdn.Cable)

    def test_get_hwire_of_invalid_reference(self):
        from spydrnet.util.hierarchical_reference import HRef
        invalid_href = HRef.from_parent_and_item(None, None)
        hrefs = list(sdn.get_hcables(invalid_href))
        self.assertTrue(len(hrefs) == 0)

    def test_get_hcables_from_hrefs_of_cable_and_wire(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hinstances(wire))
        href_top = hrefs[0]
        from spydrnet.util.hierarchical_reference import HRef
        cable_href = HRef.from_parent_and_item(href_top, cable)
        self.assertIsInstance(cable_href.item, sdn.Cable)
        wire_href = HRef.from_parent_and_item(cable_href, wire)
        href_result = next(sdn.get_hcables(cable_href), None)
        self.assertTrue(href_result is cable_href)
        href_result = next(sdn.get_hcables(wire_href), None)
        self.assertTrue(href_result is cable_href)

    def test_get_hcables_from_hrefs_of_port_and_pin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        port = definition.ports[0]
        pin = port.pins[0]
        hrefs = list(sdn.get_hcables(pin))
        href = hrefs[0]
        self.assertIsInstance(href.item, sdn.Cable)
        from spydrnet.util.hierarchical_reference import HRef
        port_href = HRef.from_parent_and_item(href.parent, port)
        href_result = next(sdn.get_hcables(port_href), None)
        self.assertTrue(href_result is href)
        pin_href = HRef.from_parent_and_item(port_href, pin)
        href_result = next(sdn.get_hcables(pin_href), None)
        self.assertTrue(href_result is href)

    def test_from_href_of_instance(self):
        href = next(sdn.get_hinstances(self.netlist.top_instance))
        hrefs = list(sdn.get_hcables(href))
        self.assertTrue(len(hrefs) == 76 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

    def test_from_instance(self):
        hrefs = list(sdn.get_hcables(self.netlist.top_instance))
        self.assertTrue(len(hrefs) == 76 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

    def test_from_library(self):
        hrefs = list(sdn.get_hcables(
            self.netlist.libraries[0], selection=sdn.OUTSIDE))
        self.assertTrue(len(hrefs) == 76 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

    def test_from_wire_and_cable(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hcables(wire))
        self.assertTrue(len(hrefs) == 1 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))
        hrefs = list(sdn.get_hcables(cable))
        self.assertTrue(len(hrefs) == 1 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

    def test_from_outerpin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        instance = definition.children[0]
        outerpin = next(iter(instance.pins))
        hrefs = list(sdn.get_hcables(outerpin, selection="OUTSIDE"))
        self.assertTrue(len(hrefs) == 1 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

    def test_bad_selection_type(self):
        self.assertRaises(TypeError, self.netlist.get_hcables,
                          selection="NOT_AN_OPTION")
        self.assertRaises(TypeError, self.netlist.get_hcables, selection=None)

    def test_of_bad_instance(self):
        hrefs = list(sdn.get_hcables(sdn.Instance()))
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
        hrefs = list(sdn.get_hcables(top_inst_href, recursive=True))
        self.assertTrue(len(hrefs) == 1 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

        hrefs = list(sdn.get_hcables(middle_inst))
        self.assertTrue(len(hrefs) == 1 and all(
            isinstance(x.item, sdn.Cable) for x in hrefs))

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

        href = next(sdn.get_hcables(top_floating_wire))
        hrefs = set(sdn.get_hcables(netlist.top_instance))
        self.assertTrue(href in hrefs)

        # look at wire_name
        href = next(sdn.get_hcables(middle_floating_wire))
        self.assertTrue('middle/middle_cable[1]', href.name)
        hrefs = set(sdn.get_hcables(netlist.top_instance, recursive=True))
        self.assertTrue(href in hrefs)

        hrefs = set(sdn.get_hcables(middle_cable, selection="OUTSIDE"))
        href_top_wire = next(sdn.get_hcables(top_cable.wires[0]))
        href_middle_wire = next(sdn.get_hcables(middle_cable.wires[0]))
        href_bottom_wire = next(sdn.get_hcables(bottom_cable.wires[0]))
        self.assertTrue(
            href_top_wire in hrefs and href_middle_wire not in hrefs and href_bottom_wire in hrefs)

        hrefs = set(sdn.get_hcables(middle_cable, selection="ALL"))
        href_middle_floating_wire = next(sdn.get_hcables(middle_floating_wire))
        self.assertTrue(href_top_wire in hrefs and href_middle_wire in hrefs and href_bottom_wire in hrefs and
                        href_middle_floating_wire in hrefs)

        all_wires = set(netlist.get_hcables())
        self.assertTrue(len(all_wires) == 1)

        all_wires = set(netlist.get_hcables(recursive=True))
        self.assertTrue(len(all_wires) == 3)
