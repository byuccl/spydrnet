import unittest
import spydrnet as sdn


class TestGetDefinitions(unittest.TestCase):
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

        top_floating_wire = top_cable.create_wire()

        top_instance = sdn.Instance()
        top_instance.name = 'top'
        top_instance.reference = top_def
        cls.netlist.top_instance = top_instance

    def test_parameter_checking(self):
        library = sdn.Library()
        definition = library.create_definition()
        definition.name = "MY_DEF"
        self.assertRaises(TypeError, sdn.get_definitions, library, "MY_DEF", patterns="MY_DEF")
        self.assertRaises(TypeError, sdn.get_definitions, library, "MY_DEF", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_definitions, library, "MY_DEF", selection="BOTH")
        self.assertRaises(TypeError, sdn.get_definitions, None, "MY_DEF")
        self.assertRaises(TypeError, sdn.get_definitions, [None, library], "MY_DEF")

    def test_collection(self):
        library = sdn.Library()
        definition = library.create_definition()
        definition.name = "MY_DEF"
        ports = list(sdn.get_definitions([library, library]))
        self.assertEqual(len(ports), 1)

    def test_get_definition_of_instances_outside(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[0].definitions[0].references,
                                                    selection="OUTSIDE"))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.bottom_inst.reference)

    def test_get_definition_of_instances_inside(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[0].definitions[0].references,
                                               selection="INSIDE"))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.leaf_inst.reference)

    def test_get_definition_of_instances_recursive_down(self):
        definition_query = set(sdn.get_definitions(self.netlist.top_instance, recursive=True))
        self.assertTrue(len(definition_query) == 4)

    def test_get_definition_of_instances_recursive_up(self):
        definition_query = list(sdn.get_definitions(self.leaf_inst, selection="OUTSIDE", recursive=True))
        self.assertTrue(len(definition_query) == 3 and self.leaf_inst.reference not in definition_query)

    def test_get_definition_of_library(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[1]))
        self.assertTrue(len(definition_query) == 3 and self.leaf_inst.reference not in definition_query)

    def test_get_definition_of_library_outside(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[0], selection="OUTSIDE"))
        self.assertTrue(len(definition_query) == 1 and self.leaf_inst.reference not in definition_query)

    def test_get_definition_of_library_outside_recursive(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[0], selection="OUTSIDE", recursive=True))
        self.assertTrue(len(definition_query) == 3 and self.leaf_inst.reference not in definition_query)

    def test_get_definition_of_library_recursive(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[1], recursive=True))
        self.assertTrue(len(definition_query) == 4 and self.leaf_inst.reference in definition_query)

    def test_get_definition_of_library_recursive_absolute_pattern(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[1], "leaf", recursive=True))
        self.assertTrue(len(definition_query) == 1 and self.leaf_inst.reference is definition_query[0])

    def test_get_definition_of_definition_inside(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[1].definitions[0],
                                                    selection="INSIDE"))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.netlist.libraries[0].definitions[0])

    def test_get_definition_of_definition_outside(self):
        definition_query = list(sdn.get_definitions(self.netlist.libraries[0].definitions[0],
                                               selection="OUTSIDE"))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.netlist.libraries[1].definitions[0])

    def test_get_definition_of_definition_inside_recursive(self):
        definition_query = list(sdn.get_definitions(self.netlist.top_instance.reference,
                                               selection="INSIDE", recursive=True))
        self.assertTrue(len(definition_query) == 3 and self.netlist.top_instance.reference not in definition_query)

    def test_get_definition_from_outer_pins(self):
        definition_query = list(sdn.get_definitions(self.leaf_inst.pins))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.leaf_inst.reference)

    def test_get_definition_from_inner_pins(self):
        definition_query = list(sdn.get_definitions(self.leaf_inst.reference.ports[0].pins[0]))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.leaf_inst.reference)

    def test_get_definition_from_wire(self):
        definition_query = list(sdn.get_definitions(self.netlist.top_instance.reference.cables[0].wires[0]))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.netlist.top_instance.reference)

    def test_get_definition_from_href(self):
        href = next(sdn.get_hinstances(self.netlist.top_instance))
        definition_query = list(sdn.get_definitions(href))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.netlist.top_instance.reference)

    def test_unique_query_return(self):
        definition_query = list(sdn.get_definitions([self.netlist.libraries[0], self.leaf_inst], "leaf"))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.leaf_inst.reference)

    def test_absolute_pattern_from_relative_query(self):
        definition_query = list(sdn.get_definitions(self.leaf_inst, "leaf"))
        self.assertTrue(len(definition_query) == 1 and definition_query[0] == self.leaf_inst.reference)
