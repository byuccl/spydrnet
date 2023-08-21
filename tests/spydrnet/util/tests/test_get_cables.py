import unittest
import spydrnet as sdn


class TestGetCables(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.netlist = sdn.Netlist()

        leaf_library = cls.netlist.create_library()
        leaf_library.name = 'primitives'

        library = cls.netlist.create_library()
        library.name = 'work'

        leaf_def = leaf_library.create_definition()
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
        cls.leaf_inst = leaf_inst

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
        cls.bottom_inst = bottom_inst

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
        cls.middle_inst = middle_inst

        top_floating_wire = top_cable.create_wire()

        top_instance = sdn.Instance()
        top_instance.name = 'top'
        top_instance.reference = top_def
        cls.netlist.top_instance = top_instance

    def test_parameter_checking(self):
        definition = sdn.Definition()
        cable = definition.create_cable()
        cable.name = "MY_CABLE"
        self.assertRaises(TypeError, sdn.get_cables, definition, "MY_CABLE", patterns="MY_CABLE")
        self.assertRaises(TypeError, sdn.get_cables, definition, "MY_CABLE", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_cables, definition, "MY_CABLE", selection=None)
        self.assertRaises(TypeError, sdn.get_cables, None, "MY_CABLE")
        self.assertRaises(TypeError, sdn.get_cables, [None, definition], "MY_CABLE")

    def test_collection(self):
        definition = sdn.Definition()
        cable = definition.create_cable()
        cable.name = "MY_CABLE"
        cables = list(sdn.get_cables([definition, definition]))
        self.assertEqual(len(cables), 1)

    def test_get_cables_in_library(self):
        library = sdn.Library()
        definition = library.create_definition()
        cable = definition.create_cable()
        cable.name = "MY_PORT"
        instance = sdn.Instance()
        instance.reference = definition
        port1 = next(library.get_cables("MY_PORT"))
        self.assertEqual(cable, port1)

    def test_get_cables_in_netlist(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        cables = definition.create_cable()
        cables.name = "MY_PORT"
        instance = sdn.Instance()
        instance.reference = definition
        port1 = next(netlist.get_cables("MY_PORT"))
        self.assertEqual(cables, port1)

    def test_select_all(self):
        middle_def = self.middle_inst.reference
        search = list(sdn.get_cables(middle_def, selection="ALL"))
        self.assertEqual(len(search), 3)

    def test_href_to_cable(self):
        href = next(sdn.get_hcables(self.middle_inst))
        search = next(sdn.get_cables(href))
        self.assertEqual(href.item, search)

    def test_href_to_cable_all(self):
        href = next(sdn.get_hcables(self.middle_inst))
        search = list(sdn.get_cables(href, selection="ALL"))
        self.assertEqual(len(search), 3)

    def test_port(self):
        port = self.netlist.top_instance.reference.ports[0]
        search = list(sdn.get_cables(port))
        self.assertEqual(len(search), 1)
        self.assertEqual(port.pins[0].wire.cable, search[0])

    def test_outer_pin(self):
        search = list(sdn.get_cables(self.middle_inst.pins, selection="ALL"))
        self.assertEqual(len(search), 3)

    def test_wire_inside(self):
        search = list(sdn.get_cables(self.netlist.top_instance.reference.cables[0].wires[0]))
        self.assertEqual(len(search), 1)
        self.assertEqual(search[0].name, "top_cable")

    def test_wire_outside(self):
        search = list(sdn.get_cables(self.netlist.top_instance.reference.cables[0].wires[0], selection="OUTSIDE"))
        self.assertEqual(len(search), 1)
        self.assertEqual(search[0].name, "middle_cable")

    def test_wires_all(self):
        search = list(sdn.get_cables(self.netlist.top_instance.reference.cables[0].wires[0], selection="ALL"))
        self.assertEqual(len(search), 3)

    def test_absolute_name_from_relative_reference(self):
        search = next(sdn.get_cables(self.middle_inst, "middle_cable"))
        self.assertEqual(search, self.middle_inst.reference.cables[0])
