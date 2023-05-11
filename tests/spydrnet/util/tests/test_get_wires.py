import unittest
import spydrnet as sdn


class TestGetWires(unittest.TestCase):
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
        library = sdn.Library()
        definition = library.create_definition()
        definition.name = "MY_DEF"
        self.assertRaises(TypeError, sdn.get_wires, library, "MY_DEF")
        self.assertRaises(TypeError, sdn.get_wires, library, unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_wires, library, selection=None)
        self.assertRaises(TypeError, sdn.get_wires, None)
        self.assertRaises(TypeError, sdn.get_wires, [None, library])

    def test_collection(self):
        wires = list(sdn.get_wires([self.netlist.libraries[1], self.netlist.libraries[1]]))
        self.assertEqual(len(wires), 6)

    def test_inside(self):
        wires = list(self.middle_inst.get_wires(selection="INSIDE", recursive=True))
        self.assertEqual(len(wires), 4)

    def test_both(self):
        wires = list(sdn.get_wires(self.middle_inst, selection="BOTH", recursive=True))
        self.assertEqual(len(wires), 2)

    def test_outside(self):
        wires = list(sdn.get_wires(self.middle_inst, selection="OUTSIDE", recursive=True))
        self.assertEqual(len(wires), 1)

    def test_wire_inside(self):
        wires = list(sdn.get_wires(self.middle_inst.reference.cables[0].wires[0]))
        self.assertEqual(len(wires), 1)
        self.assertIs(wires[0], self.middle_inst.reference.cables[0].wires[0])

    def test_wire_outside(self):
        wires = list(sdn.get_wires(self.middle_inst.reference.cables[0].wires[0], selection="OUTSIDE"))
        self.assertEqual(len(wires), 2)
        self.assertTrue(self.middle_inst.reference.cables[0].wires[0] not in wires)

    def test_port_outside(self):
        wires = list(sdn.get_wires(self.middle_inst.reference.ports[0], selection="OUTSIDE"))
        self.assertEqual(len(wires), 1)
        self.assertTrue(wires[0].cable.name == 'top_cable')

    def test_cable_outside(self):
        wires = list(sdn.get_wires(self.middle_inst.reference.cables[0], selection="OUTSIDE"))
        self.assertEqual(len(wires), 2)
        self.assertTrue(all(x not in wires for x in self.middle_inst.reference.cables[0].wires))

    def test_cable_all(self):
        wires = list(sdn.get_wires(self.netlist.top_instance.reference.cables[0].wires[0], selection="ALL"))
        self.assertEqual(len(wires), 3)

    def test_pin_all(self):
        wires = list(sdn.get_wires(self.middle_inst.reference.ports[0].pins[0], selection="ALL"))
        self.assertEqual(len(wires), 3)

    def test_pin_inside(self):
        wires = list(sdn.get_wires(self.middle_inst.reference.ports[0].pins[0]))
        self.assertEqual(len(wires), 1)
        self.assertIs(wires[0], self.middle_inst.reference.cables[0].wires[0])

    def test_outer_pin_inside(self):
        inner_pin = self.middle_inst.reference.ports[0].pins[0]
        outer_pin = self.middle_inst.pins[inner_pin]
        wires = list(sdn.get_wires(outer_pin))
        self.assertEqual(len(wires), 1)
        self.assertIs(wires[0], self.middle_inst.reference.cables[0].wires[0])

    def test_outer_pin_outside(self):
        inner_pin = self.middle_inst.reference.ports[0].pins[0]
        outer_pin = self.middle_inst.pins[inner_pin]
        wires = list(sdn.get_wires(outer_pin, selection="OUTSIDE"))
        self.assertEqual(len(wires), 1)
        self.assertIs(wires[0], self.netlist.top_instance.reference.cables[0].wires[0])

    def test_netlist(self):
        wires = list(sdn.get_wires(self.netlist))
        self.assertEqual(len(wires), 6)

    def test_href(self):
        href = next(sdn.get_hinstances(self.netlist.top_instance))
        wires = list(sdn.get_wires(href, recursive=True))
        self.assertEqual(len(wires), 6)
