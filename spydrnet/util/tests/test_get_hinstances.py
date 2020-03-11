import unittest
import spydrnet as sdn


class TestGetHInstances(unittest.TestCase):
    netlist = None
    @classmethod
    def setUpClass(cls) -> None:
        cls.netlist = sdn.load_example_netlist_by_name('b13')

    def test_absolute_search(self):
        href = next(self.netlist.get_hinstances('tx_end_reg'), None)
        self.assertIsNotNone(href)

    def test_regex_search(self):
        hrefs = list(sdn.get_hinstances(self.netlist, '.*FSM_onehot.*', is_re=True))
        self.assertTrue(len(hrefs) == 24)

    def test_parameters(self):
        self.assertRaises(TypeError, sdn.get_hinstances, self.netlist, r'.*FSM_onehot.*', patterns=r".*FSM_onehot.*")
        self.assertRaises(TypeError, sdn.get_hinstances, self.netlist, parameter_does_not_exit=True)
        self.assertRaises(TypeError, sdn.get_hinstances, object())

    def test_get_hinstances_of_pin(self):
        library = self.netlist.libraries[0]
        definition = library.definitions[0]
        port = definition.ports[0]
        pin = port.pins[0]
        hrefs = list(sdn.get_hinstances(pin))
        self.assertTrue(len(hrefs) == 7)

    def test_get_hinstances_of_wire(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hinstances(wire))
        self.assertTrue(len(hrefs) == 1)

    def test_get_hinstance_of_invalid_reference(self):
        from spydrnet.util.hierarchical_reference import HRef
        invalid_href = HRef.from_parent_and_item(None, None)
        hrefs = list(sdn.get_hinstances(invalid_href))
        self.assertTrue(len(hrefs) == 0)

    def test_get_hinstances_from_hrefs_of_cable_and_wire(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hinstances(wire))
        href_top = hrefs[0]
        from spydrnet.util.hierarchical_reference import HRef
        cable_href = HRef.from_parent_and_item(href_top, cable)
        href_result = next(sdn.get_hinstances(cable_href), None)
        self.assertTrue(href_result is href_top)
        wire_href = HRef.from_parent_and_item(cable_href, wire)
        href_result = next(sdn.get_hinstances(wire_href), None)
        self.assertTrue(href_result is href_top)

    def test_get_hinstances_from_hrefs_of_port_and_pin(self):
        library = self.netlist.libraries[0]
        definition = library.definitions[0]
        port = definition.ports[0]
        pin = port.pins[0]
        hrefs = list(sdn.get_hinstances(pin))
        href = hrefs[0]
        from spydrnet.util.hierarchical_reference import HRef
        port_href = HRef.from_parent_and_item(href, port)
        href_result = next(sdn.get_hinstances(port_href), None)
        self.assertTrue(href_result is href)
        pin_href = HRef.from_parent_and_item(port_href, pin)
        href_result = next(sdn.get_hinstances(pin_href), None)
        self.assertTrue(href_result is href)

    def test_from_href_of_instance(self):
        href = next(sdn.get_hinstances(self.netlist.top_instance))
        hrefs = list(sdn.get_hinstances(href))
        self.assertTrue(len(hrefs) == 102)

    def test_from_library(self):
        hrefs = list(sdn.get_hinstances(self.netlist.libraries[0]))
        self.assertTrue(len(hrefs) == 102)

    def test_from_wire_and_cable(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        cable = definition.cables[0]
        wire = cable.wires[0]
        hrefs = list(sdn.get_hinstances(self.netlist.top_instance))
        href_top = hrefs[0]
        href_result = next(sdn.get_hinstances(wire))
        self.assertTrue(href_top is href_result)
        href_result = next(sdn.get_hinstances(cable))
        self.assertTrue(href_top is href_result)

    def test_from_outerpin(self):
        library = self.netlist.libraries[1]
        definition = library.definitions[0]
        instance = definition.children[0]
        outerpin = next(iter(instance.pins))
        hrefs = list(sdn.get_hinstances(outerpin))
        self.assertTrue(len(hrefs) == 1)

    def test_of_bad_instance(self):
        hrefs = list(sdn.get_hinstances(sdn.Instance()))
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
        middle_inst.reference = middle_def

        leaf_inst = middle_def.create_child()
        leaf_def = library.create_definition()
        leaf_inst.reference = leaf_def

        hrefs = list(sdn.get_hinstances(leaf_inst))
        self.assertTrue(len(hrefs) == 1)

    @unittest.skip("Test takes too long at this time.")
    def test_recursive_memory_use(self):
        netlist = sdn.load_example_netlist_by_name('leon3mp_hierarchical')
        hrefs = list(sdn.get_hinstances(netlist))
        self.assertTrue(len(hrefs) > 0)
