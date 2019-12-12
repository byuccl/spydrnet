import unittest
import spydrnet as sdn
from spydrnet.ir import Element
from spydrnet.ir import Bundle
from spydrnet.ir import Pin
from spydrnet.ir import ListView
from spydrnet.ir import SetView
from spydrnet.ir import OuterPinsView


class TestElement(unittest.TestCase):
    def test_constructor(self):
        element1 = Element()
        self.assertTrue(element1, "Constructor return None type or empty collection")
        element2 = Element()
        self.assertNotEqual(element1, element2, "Unique objects are considered equal.")

    def test_dictionary(self):
        element = Element()
        self.assertFalse('NAME' in element)
        element['NAME'] = "TestName"
        self.assertTrue('NAME' in element)
        for key in element:
            self.assertEqual(element[key], "TestName")
        del element['NAME']
        self.assertFalse('NAME' in element)
        element['NAME'] = "DifferentName"
        name = element.pop('NAME')
        self.assertEqual(name, "DifferentName")


class TestNetlist(unittest.TestCase):
    def setUp(self):
        self.netlist = sdn.Netlist()

    def test_constructor(self):
        self.assertIsInstance(self.netlist, Element, "Netlist is not an element.")
        self.assertTrue(self.netlist, "Constructor return None type or empty collection")
        netlist2 = sdn.Netlist()
        self.assertNotEqual(self.netlist, netlist2, "Unique objects are considered equal.")

    def test_libraries(self):
        self.assertEqual(len(tuple(self.netlist.libraries)), 0)
        library = self.netlist.create_library()
        self.assertTrue(self.netlist.libraries[0] == library)
        visited = False
        for visited_library in self.netlist.libraries:
            visited = True
            self.assertEqual(library, visited_library)
        self.assertTrue(visited)

    def test_libraries_set(self):
        library1 = self.netlist.create_library()
        library2 = self.netlist.create_library()
        libraries = [library1, library2]
        self.assertEqual(self.netlist.libraries, libraries)
        self.netlist.libraries = reversed(libraries)
        self.assertEqual(self.netlist.libraries, list(reversed(libraries)))

    def test_top_instance(self):
        self.assertIsNone(self.netlist.top_instance)
        instance = sdn.Instance()
        self.netlist.top_instance = instance
        self.assertEqual(instance, self.netlist.top_instance)
        self.netlist.top_instance = None
        self.assertIsNone(self.netlist.top_instance)

    def test_create_library(self):
        library = self.netlist.create_library()
        self.assertTrue(library in self.netlist.libraries)
        self.assertEqual(library.netlist, self.netlist)

    def test_remove_library(self):
        library = self.netlist.create_library()
        self.netlist.remove_library(library)
        self.assertFalse(library in self.netlist.libraries)
        self.assertIsNone(library.netlist)

    def test_add_library(self):
        library = sdn.Library()
        self.netlist.add_library(library, position=0)
        self.assertTrue(library in self.netlist.libraries)
        self.assertEqual(library.netlist, self.netlist)
        self.assertEqual(list(self.netlist.libraries).count(library), 1)

    @unittest.expectedFailure
    def test_remove_libraries_from_outside_netlist(self):
        library1 = self.netlist.create_library()
        library2 = sdn.Library()
        self.netlist.remove_libraries_from([library1, library2])

    def test_remove_libraries_from(self):
        library = self.netlist.create_library()
        self.netlist.remove_libraries_from((library,))
        self.assertFalse(library in self.netlist)
        self.assertIsNone(library.netlist)
        library_included = self.netlist.create_library()
        library = self.netlist.create_library()
        self.netlist.remove_libraries_from({library})
        self.assertFalse(library in self.netlist)
        self.assertIsNone(library.netlist)
        self.assertTrue(library_included in self.netlist.libraries)
        self.assertEqual(library_included.netlist, self.netlist)


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = sdn.Library()

    def test_constructor(self):
        self.assertIsInstance(self.library, Element, "Netlist is not an element.")
        self.assertTrue(self.library, "Constructor return None type or empty collection")
        library2 = sdn.Netlist()
        self.assertNotEqual(self.library, library2, "Unique objects are considered equal.")

    def test_definitions_set(self):
        definition1 = self.library.create_definition()
        definition2 = self.library.create_definition()
        definitions = [definition1, definition2]
        self.assertEqual(self.library.definitions, definitions)
        self.library.definitions = reversed(definitions)
        self.assertEqual(self.library.definitions, list(reversed(definitions)))

    def test_create_definition(self):
        definition = self.library.create_definition()
        self.assertTrue(definition in self.library.definitions)
        self.assertEqual(definition.library, self.library)

    def test_add_definition(self):
        definition = sdn.Definition()
        self.library.add_definition(definition)
        self.assertTrue(definition in self.library.definitions)
        self.assertEqual(definition.library, self.library)
        self.assertEqual(list(self.library.definitions).count(definition), 1)

        definition = sdn.Definition()
        self.library.add_definition(definition, position=0)
        self.assertTrue(definition in self.library.definitions)
        self.assertEqual(definition.library, self.library)
        self.assertEqual(list(self.library.definitions).count(definition), 1)

    def test_remove_definition(self):
        definition = self.library.create_definition()
        self.library.remove_definition(definition)
        self.assertFalse(definition in self.library)
        self.assertIsNone(definition.library)

    @unittest.expectedFailure
    def test_remove_definitions_from_outside_library(self):
        definition = sdn.Definition()
        self.library.remove_definitions_from([definition])

    def test_remove_definitions_from(self):
        definition_included = self.library.create_definition()
        definition = self.library.create_definition()
        self.library.remove_definitions_from({definition})
        self.assertFalse(definition in self.library.definitions)
        self.assertIsNone(definition.library)
        self.assertTrue(definition_included in self.library.definitions)
        self.assertEqual(definition_included.library, self.library)


class TestDefinition(unittest.TestCase):
    def setUp(self):
        self.definition = sdn.Definition()

    def test_constructor(self):
        self.assertIsInstance(self.definition, Element, "Definition is not an element.")
        self.assertTrue(self.definition, "Constructor returns None type or empty collection.")
        definition2 = sdn.Definition()
        self.assertNotEqual(self.definition, definition2, "Unique objects are considered equal.")

    @unittest.expectedFailure
    def test_assign_library(self):
        library = sdn.Library()
        self.definition.library = library

    def test_ports_set(self):
        port1 = self.definition.create_port()
        port2 = self.definition.create_port()
        self.assertEqual(self.definition.ports, [port1, port2])
        self.definition.ports = [port2, port1]
        self.assertEqual(self.definition.ports, [port2, port1])

    def test_create_port(self):
        port = self.definition.create_port()
        self.assertTrue(port in self.definition.ports)
        self.assertEqual(port.definition, self.definition)

    def test_add_port(self):
        port = sdn.Port()
        self.definition.add_port(port, position=0)
        self.assertTrue(port in self.definition.ports)
        self.assertEqual(port.definition, self.definition)
        self.assertEqual(self.definition.ports.count(port), 1)

    def test_remove_port(self):
        port = self.definition.create_port()
        self.definition.remove_port(port)
        self.assertFalse(port in self.definition.ports)
        self.assertIsNone(port.definition)

    @unittest.expectedFailure
    def test_remove_ports_from_outside_definition(self):
        port = sdn.Port()
        self.definition.remove_ports_from((port,))

    def test_remove_ports_from(self):
        port_included = self.definition.create_port()
        port = self.definition.create_port()
        self.definition.remove_ports_from((port,))
        self.assertFalse(port in self.definition.ports)
        self.assertIsNone(port.definition)

        port = self.definition.create_port()
        self.definition.remove_ports_from({port})
        self.assertFalse(port in self.definition.ports)
        self.assertIsNone(port.definition)

        self.assertTrue(port_included in self.definition.ports)
        self.assertEqual(port_included.definition, self.definition)

    def test_cables_set(self):
        cable1 = self.definition.create_cable()
        cable2 = self.definition.create_cable()
        self.assertEqual(self.definition.cables, [cable1, cable2])
        self.definition.cables = [cable2, cable1]
        self.assertEqual(self.definition.cables, [cable2, cable1])

    def test_create_cable(self):
        cable = self.definition.create_cable()
        self.assertTrue(cable in self.definition.cables)
        self.assertEqual(self.definition, cable.definition)

    def test_add_cable(self):
        cable = sdn.Cable()
        self.definition.add_cable(cable, position=0)
        self.assertTrue(cable in self.definition.cables)
        self.assertEqual(cable.definition, self.definition)
        self.assertEqual(self.definition.cables.count(cable), 1)

    def test_remove_cable(self):
        cable = self.definition.create_cable()
        self.definition.remove_cable(cable)
        self.assertFalse(cable in self.definition.cables)
        self.assertIsNone(cable.definition)

    @unittest.expectedFailure
    def test_remove_cables_from_outside_definition(self):
        cable = sdn.Cable()
        self.definition.remove_cables_from({cable})

    def test_remove_cables_from(self):
        cable_included = self.definition.create_cable()
        cable = self.definition.create_cable()
        self.definition.remove_cables_from({cable})
        self.assertFalse(cable in self.definition.cables)
        self.assertIsNone(cable.definition)
        self.assertTrue(cable_included in self.definition.cables)
        self.assertEqual(cable_included.definition, self.definition)

    def test_children_set(self):
        child1 = self.definition.create_child()
        child2 = self.definition.create_child()
        self.assertEqual(self.definition.children, [child1, child2])
        self.definition.children = [child2, child1]
        self.assertEqual(self.definition.children, [child2, child1])

    def test_create_child(self):
        instance = self.definition.create_child()
        self.assertTrue(instance in self.definition.children)
        self.assertEqual(instance.parent, self.definition)

    def test_add_child(self):
        instance = sdn.Instance()
        self.definition.add_child(instance, position=0)
        self.assertTrue(instance in self.definition.children)
        self.assertEqual(instance.parent, self.definition)
        self.assertEqual(self.definition.children.count(instance), 1)

    def test_remove_child(self):
        instance = self.definition.create_child()
        self.definition.remove_child(instance)
        self.assertFalse(instance in self.definition.children)
        self.assertIsNone(instance.parent)

    @unittest.expectedFailure
    def test_remove_children_from_outside_definition(self):
        instance = sdn.Instance()
        self.definition.remove_children_from((instance,))

    def test_remove_children_from(self):
        instance_included = self.definition.create_child()

        instance = self.definition.create_child()
        self.definition.remove_children_from((instance,))
        self.assertFalse(instance in self.definition.children)
        self.assertIsNone(instance.parent)

        instance = self.definition.create_child()
        self.definition.remove_children_from({instance})
        self.assertFalse(instance in self.definition.children)
        self.assertIsNone(instance.parent)

        self.assertTrue(instance_included in self.definition.children)
        self.assertEqual(instance_included.parent, self.definition)

    def test_is_leaf(self):
        self.assertTrue(self.definition.is_leaf()), "Empty definition is not considered a leaf cell"
        self.definition.create_port()
        self.assertTrue(self.definition.is_leaf()), "Empty definition with a port is not considered a leaf cell"
        self.definition.create_cable()
        self.assertFalse(self.definition.is_leaf()), "Definition with a cable is considered a leaf cell"
        self.definition.remove_cables_from(self.definition.cables)
        self.definition.create_child()
        self.assertFalse(self.definition.is_leaf()), "Definition with a child instance is considered a leaf cell"
        self.definition.create_cable()
        self.assertFalse(self.definition.is_leaf()), "Definition with a cable and child instance is considered a leaf" \
                                                     " cell"


class TestBundle(unittest.TestCase):
    def setUp(self) -> None:
        self.bundle = Bundle()

    def test_constructor(self):
        self.assertIsInstance(self.bundle, Element, "Bundle is not an element.")
        self.assertTrue(self.bundle, "Constructor returns None type or empty collection.")
        bundle2 = Bundle()
        self.assertNotEqual(self.bundle, bundle2, "Unique objects are considered equal.")

    def test_definition(self):
        self.assertIsNone(self.bundle.definition)

    @unittest.expectedFailure
    def test_definition_assignment(self):
        definition = sdn.Definition()
        self.bundle.definition = definition

    def test_isdownto(self):
        self.assertTrue(self.bundle.is_downto)
        self.bundle.is_downto = False
        self.assertFalse(self.bundle.is_downto)

    def test_lower_index(self):
        self.assertEqual(self.bundle.lower_index, 0)
        self.bundle.lower_index = 1
        self.assertEqual(self.bundle.lower_index, 1)

    def test__item(self):
        self.assertIsNone(self.bundle._items())


class TestPort(unittest.TestCase):
    def setUp(self) -> None:
        self.port = sdn.Port()

    def test_direction_enum(self):
        self.assertEqual(sdn.Port.Direction.UNDEFINED, sdn.UNDEFINED)
        self.assertEqual(sdn.Port.Direction.IN, sdn.IN)
        self.assertEqual(sdn.Port.Direction.OUT, sdn.OUT)
        self.assertEqual(sdn.Port.Direction.INOUT, sdn.INOUT)

    def test_constructor(self):
        self.assertIsInstance(self.port, Bundle)
        self.assertTrue(self.port, "Constructor returns None type or empty collection.")
        port2 = sdn.Port()
        self.assertNotEqual(self.port, port2, "Unique objects are considered equal.")

    def test_pins_set(self):
        pin1 = self.port.create_pin()
        pin2 = self.port.create_pin()
        self.assertEqual(self.port.pins, [pin1, pin2])
        self.port.pins = [pin2, pin1]
        self.assertEqual(self.port.pins, [pin2, pin1])

    def test_direction(self):
        for ii in range(4):
            self.port.direction = ii
            self.assertEqual(self.port.direction.value, ii)
        directions = ['undefined', 'in', 'out', 'inout']
        for direction in directions:
            self.port.direction = direction
            self.assertEqual(self.port.direction.name.lower(), direction.lower())
        for direction in sdn.Port.Direction:
            self.port.direction = direction
            self.assertEqual(self.port.direction, direction)

    @unittest.expectedFailure
    def test_direction_set_bad_type(self):
        self.port.direction = list()

    def test_initialize_pins(self):
        self.port.initialize_pins(2)
        self.assertEqual(len(self.port.pins), 2)
        self.assertNotEqual(self.port.pins[0], self.port.pins[1])

    def test_create_pin(self):
        pin = self.port.create_pin()
        self.assertTrue(pin in self.port.pins)
        self.assertEqual(pin.port, self.port)

    def test_add_pin(self):
        pin = sdn.InnerPin()
        self.port.add_pin(pin, position=0)
        self.assertTrue(pin in self.port.pins)
        self.assertEqual(pin.port, self.port)
        self.assertEqual(self.port.pins.count(pin), 1)

    def test_remove_pin(self):
        pin = self.port.create_pin()
        self.port.remove_pin(pin)
        self.assertFalse(pin in self.port)
        self.assertIsNone(pin.port)

    @unittest.expectedFailure
    def test_remove_pins_outside_port(self):
        pin = sdn.InnerPin()
        self.port.remove_pins_from((pin,))

    def test_remove_pins_from(self):
        pin_included = self.port.create_pin()
        pin = self.port.create_pin()
        self.port.remove_pins_from({pin})
        self.assertFalse(pin in self.port.pins)
        self.assertIsNone(pin.port)
        self.assertTrue(pin_included in self.port.pins)
        self.assertEqual(pin_included.port, self.port)

    def test_is_scalar(self):
        self.assertTrue(self.port.is_scalar)
        self.port.is_scalar = False
        self.assertFalse(self.port.is_scalar)
        self.port.is_scalar = True
        self.assertTrue(self.port.is_scalar)
        self.port.initialize_pins(2)
        self.assertFalse(self.port.is_scalar)
        self.port.is_scalar = False
        self.port.remove_pins_from(self.port.pins)
        self.assertFalse(self.port.is_scalar)

    @unittest.expectedFailure
    def test_is_scalar_set_on_array_bundle(self):
        self.port.initialize_pins(2)
        self.port.is_scalar = True

    def test_is_array(self):
        self.assertFalse(self.port.is_array)
        self.port.is_array = True
        self.assertTrue(self.port.is_array)
        self.port.is_array = False
        self.assertFalse(self.port.is_array)
        self.port.initialize_pins(2)
        self.assertTrue(self.port.is_array)
        self.port.is_array = True
        self.port.remove_pins_from(self.port.pins)
        self.assertTrue(self.port.is_array)

    @unittest.expectedFailure
    def test_is_array_clear_on_array_bundle(self):
        self.port.initialize_pins(2)
        self.port.is_array = False


class TestPin(unittest.TestCase):
    def setUp(self):
        self.pin = Pin()

    def test_constructor(self):
        self.assertFalse(isinstance(self.pin, Element))
        self.assertTrue(self.pin)
        pin2 = Pin()
        self.assertNotEqual(self.pin, pin2)

    def test_wire(self):
        self.assertIsNone(self.pin.wire)

    @unittest.expectedFailure
    def test_wire_set(self):
        self.pin.wire = None


class TestInnerPin(unittest.TestCase):
    def setUp(self) -> None:
        self.pin = sdn.InnerPin()

    def test_constructor(self):
        self.assertIsInstance(self.pin, Pin)
        self.assertTrue(self.pin)
        pin2 = sdn.InnerPin()
        self.assertNotEqual(self.pin, pin2)

    def test_port(self):
        self.assertIsNone(self.pin.port)

    @unittest.expectedFailure
    def test_port_set(self):
        self.pin.port = None


class TestOuterPin(unittest.TestCase):
    def setUp(self) -> None:
        self.pin = sdn.OuterPin()

    def test_constructor(self):
        self.assertIsInstance(self.pin, Pin)
        self.assertTrue(self.pin)

    def test_equal(self):
        outer_pin = sdn.OuterPin()
        self.assertEqual(outer_pin, self.pin)
        inner_pin = sdn.InnerPin()
        instance = sdn.Instance()
        outer_pin1 = sdn.OuterPin.from_instance_and_inner_pin(instance, inner_pin)
        outer_pin2 = sdn.OuterPin.from_instance_and_inner_pin(instance, inner_pin)
        self.assertEqual(outer_pin1, outer_pin2)
        self.assertNotEqual(self.pin, outer_pin1)
        self.assertNotEqual(self.pin, None)

    def test_hash(self):
        outer_pin = sdn.OuterPin()
        self.assertEqual(hash(outer_pin), hash(self.pin))
        inner_pin = sdn.InnerPin()
        instance = sdn.Instance()
        outer_pin1 = sdn.OuterPin.from_instance_and_inner_pin(instance, inner_pin)
        outer_pin2 = sdn.OuterPin.from_instance_and_inner_pin(instance, inner_pin)
        self.assertEqual(hash(outer_pin1), hash(outer_pin2))


class TestCable(unittest.TestCase):
    def setUp(self) -> None:
        self.cable = sdn.Cable()

    def test__items(self):
        self.assertEqual(self.cable._items(), self.cable._wires)

    def test_initialize_wires(self):
        self.cable.initialize_wires(2)
        self.assertEqual(len(self.cable.wires), 2)
        self.cable.remove_wires_from(self.cable.wires)
        self.assertEqual(len(self.cable.wires), 0)

    def test_wires_set(self):
        wire1 = self.cable.create_wire()
        wire2 = self.cable.create_wire()
        self.assertEqual(self.cable.wires, [wire1, wire2])
        self.cable.wires = [wire2, wire1]
        self.assertEqual(self.cable.wires, [wire2, wire1])

    def test_create_wire(self):
        wire = self.cable.create_wire()
        self.assertTrue(wire in self.cable.wires)
        self.assertEqual(wire.cable, self.cable)

    def test_add_wire(self):
        wire = sdn.Wire()
        self.cable.add_wire(wire, position=0)
        self.assertTrue(wire in self.cable.wires)
        self.assertEqual(wire.cable, self.cable)

    def test_remove_wire(self):
        wire = self.cable.create_wire()
        self.cable.remove_wire(wire)
        self.assertFalse(wire in self.cable.wires)
        self.assertIsNone(wire.cable)

    def test_remove_wire_from(self):
        wire_included = self.cable.create_wire()
        wire = self.cable.create_wire()
        self.cable.remove_wires_from({wire})
        self.assertFalse(wire in self.cable.wires)
        self.assertIsNone(wire.cable)
        self.assertTrue(wire_included in self.cable.wires)
        self.assertEqual(wire_included.cable, self.cable)


class TestWire(unittest.TestCase):
    def setUp(self):
        self.definition_top = sdn.Definition()
        self.port_top = self.definition_top.create_port()
        self.inner_pin = self.port_top.create_pin()
        self.cable = self.definition_top.create_cable()
        self.wire = self.cable.create_wire()
        self.definition_leaf = sdn.Definition()
        self.port = self.definition_leaf.create_port()
        self.pin1 = self.port.create_pin()
        self.pin2 = self.port.create_pin()
        self.instance = self.definition_top.create_child()
        self.instance.reference = self.definition_leaf

    def test_constructor(self):
        self.assertFalse(isinstance(self.wire, Element), "Wire should not extend element")
        wire2 = sdn.Wire()
        self.assertNotEqual(self.wire, wire2, "Unique items are considered equal")

    def test_pins_assignement(self):
        self.wire.connect_pin(self.instance.pins[self.pin1])
        self.wire.connect_pin(self.instance.pins[self.pin2])
        self.assertEqual(self.wire.pins, [self.instance.pins[self.pin1], self.instance.pins[self.pin2]])
        self.wire.pins = [self.instance.pins[self.pin2], self.instance.pins[self.pin1]]
        self.assertEqual(self.wire.pins, [self.instance.pins[self.pin2], self.instance.pins[self.pin1]])

    def test_connect_and_disconnect_inner_port(self):
        self.wire.connect_pin(self.inner_pin)
        self.assertTrue(self.inner_pin in self.wire.pins)
        self.assertEqual(self.inner_pin.wire, self.wire)
        self.assertEqual(len(self.wire.pins), 1)

        self.wire.disconnect_pin(self.inner_pin)
        self.assertFalse(self.inner_pin in self.wire.pins)
        self.assertIsNone(self.inner_pin.wire)
        self.assertEqual(len(self.wire.pins), 0)

    def test_connect_and_disconnect_outer_pin_by_reference(self):
        self.wire.connect_pin(self.instance.pins[self.pin1])
        self.assertEqual(len(self.wire.pins), 1)
        self.assertTrue(all(x is self.instance.pins[x] for x in self.wire.pins))
        self.assertTrue(all(x.wire is self.wire for x in self.wire.pins))
        self.assertTrue(all(x.instance is self.instance for x in self.wire.pins))
        self.assertEqual(self.instance.pins[self.pin1].inner_pin, self.pin1)

        self.wire.disconnect_pin(self.instance.pins[self.pin1])
        self.assertEqual(len(self.wire.pins), 0)
        self.assertFalse(self.instance.pins[self.pin1] in self.wire.pins)
        self.assertIsNone(self.instance.pins[self.pin1].wire)
        self.assertTrue(self.pin1 in self.instance.pins)

    def test_connect_and_disconnect_outer_pin_by_object(self):
        self.wire.connect_pin(sdn.OuterPin.from_instance_and_inner_pin(self.instance, self.pin2), position=0)
        self.assertEqual(len(self.wire.pins), 1)
        self.assertTrue(all(x is self.instance.pins[x] for x in self.wire.pins))
        self.assertTrue(all(x.wire is self.wire for x in self.wire.pins))
        self.assertTrue(all(x.instance is self.instance for x in self.wire.pins))
        self.assertEqual(self.instance.pins[self.pin2].inner_pin, self.pin2)

        self.wire.disconnect_pin(sdn.OuterPin(self.instance, self.pin2))
        self.assertEqual(len(self.wire.pins), 0)
        self.assertFalse(self.instance.pins[self.pin2] in self.wire.pins)
        self.assertIsNone(self.instance.pins[self.pin1].wire)
        self.assertTrue(self.pin1 in self.instance.pins)

    def test_disconnect_pin_from(self):
        self.wire.connect_pin(self.inner_pin)
        self.wire.connect_pin(self.instance.pins[self.pin1])
        self.wire.connect_pin(self.instance.pins[self.pin2])
        self.wire.disconnect_pins_from(iter((self.inner_pin, self.instance.pins[self.pin1])))
        self.wire.disconnect_pins_from({self.instance.pins[self.pin2]})
        self.assertEqual(len(self.wire.pins), 0)
        self.assertTrue(self.pin1 in self.instance.pins and isinstance(self.instance.pins[self.pin1], sdn.OuterPin) and
                        self.instance.pins[self.pin1].inner_pin == self.pin1)
        self.assertIsNone(self.inner_pin.wire)
        self.assertIsNone(self.instance.pins[self.pin1].wire)
        self.assertIsNone(self.instance.pins[self.pin2].wire)
        self.assertTrue(self.pin1 in self.instance.pins and isinstance(self.instance.pins[self.pin2], sdn.OuterPin) and
                        self.instance.pins[self.pin2].inner_pin == self.pin2)

    @unittest.expectedFailure
    def test_disconnect_inner_pin_from_outside_wire(self):
        inner_pin = sdn.InnerPin()
        self.wire.disconnect_pins_from([inner_pin])

    @unittest.expectedFailure
    def test_disconnect_outer_pin_from_outside_wire(self):
        outer_pin = sdn.OuterPin()
        self.wire.disconnect_pins_from([outer_pin])


class TestInstance(unittest.TestCase):
    def setUp(self) -> None:
        self.instance = sdn.Instance()

    def test_constructor(self):
        self.assertIsInstance(self.instance, Element, "Instance should extend element")
        instance2 = sdn.Instance()
        self.assertNotEqual(self.instance, instance2, "Unique objects are considered equal")

    def test_reference_assignment(self):
        definition = sdn.Definition()
        self.instance.reference = definition
        self.assertEqual(self.instance.reference, definition)
        self.assertTrue(self.instance in definition.references)

    def test_reference_assignment_with_pins(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()

        self.instance.reference = definition
        self.assertTrue(pin1 in self.instance.pins)
        self.assertTrue(pin2 in self.instance.pins)
        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]
        self.assertIsInstance(outer_pin1, sdn.OuterPin)
        self.assertIsInstance(outer_pin2, sdn.OuterPin)
        self.assertEqual(outer_pin1.instance, self.instance)
        self.assertEqual(outer_pin2.instance, self.instance)
        self.assertEqual(outer_pin1.inner_pin, pin1)
        self.assertEqual(outer_pin2.inner_pin, pin2)

        wire = sdn.Wire()
        wire.connect_pin(outer_pin1)
        wire.connect_pin(outer_pin2)
        self.instance.reference = None
        self.assertEqual(len(self.instance.pins), 0)
        self.assertIsNone(outer_pin1.wire)
        self.assertIsNone(outer_pin2.wire)
        self.assertIsNone(outer_pin1.instance)
        self.assertIsNone(outer_pin2.instance)
        self.assertIsNone(outer_pin2.inner_pin)
        self.assertIsNone(outer_pin2.inner_pin)

    def test_post_assignment_pin_and_port_removal(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()

        self.instance.reference = definition
        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]

        wire = sdn.Wire()
        wire.connect_pin(outer_pin1)
        wire.connect_pin(outer_pin2)

        port.remove_pin(pin1)
        definition.remove_port(port)

        self.assertIsNone(outer_pin1.wire)
        self.assertIsNone(outer_pin1.instance)
        self.assertIsNone(outer_pin1.inner_pin)
        self.assertIsNone(outer_pin2.wire)
        self.assertIsNone(outer_pin2.instance)
        self.assertIsNone(outer_pin2.inner_pin)
        self.assertFalse(outer_pin1 in wire.pins)
        self.assertFalse(outer_pin2 in wire.pins)
        self.assertFalse(outer_pin1 in self.instance.pins)
        self.assertFalse(outer_pin2 in self.instance.pins)
        self.assertFalse(pin1 in self.instance.pins)
        self.assertFalse(pin2 in self.instance.pins)

    def test_post_assignment_pin_and_port_creation(self):
        definition = sdn.Definition()
        self.instance.reference = definition
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()
        port2 = sdn.Port()
        pin3 = port2.create_pin()
        definition.add_port(port2)
        pin4 = port2.create_pin()

        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]
        outer_pin3 = self.instance.pins[pin3]
        outer_pin4 = self.instance.pins[pin4]

        wire = sdn.Wire()
        wire.connect_pin(outer_pin1)
        wire.connect_pin(outer_pin2)
        wire.connect_pin(outer_pin3)
        wire.connect_pin(outer_pin4)
        inner_pins = [pin1, pin2, pin3, pin4]
        outer_pins = [outer_pin1, outer_pin2, outer_pin3, outer_pin4]
        for outer_pin, inner_pin in zip(outer_pins, inner_pins):
            self.assertEqual(outer_pin.wire, wire)
            self.assertTrue(outer_pin in wire.pins)
            self.assertEqual(outer_pin.instance, self.instance)
            self.assertEqual(outer_pin.inner_pin, inner_pin)
            self.assertTrue(outer_pin in self.instance.pins)
            self.assertTrue(inner_pin in self.instance.pins)

    def test_reference_reassignment(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()
        self.instance.reference = definition
        outer_pin1 = self.instance.pins[pin1]
        outer_pin2 = self.instance.pins[pin2]

        definition2 = sdn.Definition()
        port = definition2.create_port()
        pin1 = port.create_pin()
        pin2 = port.create_pin()
        self.instance.reference = definition2
        self.assertEqual(outer_pin1, self.instance.pins[pin1])
        self.assertEqual(outer_pin2, self.instance.pins[pin2])


class TestListView(unittest.TestCase):
    def setUp(self) -> None:
        self.list_view = ListView(list(range(10)))

    def test_getitem(self):
        self.assertTrue(self.list_view[0] == 0)

    def test_contains(self):
        self.assertTrue(5 in self.list_view)

    def test_comparison(self):
        list_copy = list(range(10))
        self.assertEqual(self.list_view, list_copy)
        empty_list = list()
        self.assertNotEqual(self.list_view, empty_list)

    def test_iter(self):
        aggregate = 0
        for item in self.list_view:
            aggregate += item
        self.assertEqual(sum(range(10)), aggregate)

    def test_len(self):
        self.assertEqual(len(self.list_view), 10)

    def test_reversed(self):
        self.assertEqual(next(iter(reversed(self.list_view))), 9)

    def test_copy(self):
        self.assertEqual(self.list_view, self.list_view.copy())

    def test_count(self):
        self.assertEqual(self.list_view.count(5), 1)

    def test_index(self):
        self.assertEqual(self.list_view.index(5), 5)

    def test_slice(self):
        self.assertEqual(self.list_view[1:4], list(range(1, 4)))

    def test_multiply(self):
        self.assertEqual(len(self.list_view * 2), 20)
        self.assertEqual(len(2 * self.list_view), 20)

    def test_add(self):
        result = list(range(10, 20)) + self.list_view
        print(result)
        self.assertEqual(len(result), 20)
        result = self.list_view + list(range(10, 20))
        print(result)
        self.assertEqual(len(result), 20)

    @unittest.expectedFailure
    def test_multiply_assignment(self):
        self.list_view *= 2

    @unittest.expectedFailure
    def test_add_assignment(self):
        self.list_view += list(range(10))


class TestSetView(unittest.TestCase):
    def setUp(self) -> None:
        self.set_view = SetView(set(range(10)))

    def test_and(self):
        self.assertEqual(len(set(range(10, 20)) & self.set_view), 0)
        self.assertEqual(len(self.set_view & set(range(10, 20))), 0)

    def test_or(self):
        self.assertEqual(len(set(range(10, 20)) | self.set_view), 20)
        self.assertEqual(len(self.set_view | set(range(10, 20))), 20)

    def test_min(self):
        self.assertEqual(len(set(range(10, 20)) - self.set_view), 10)
        self.assertEqual(len(self.set_view - set(range(10, 20))), 10)

    def test_xor(self):
        self.assertEqual(len(set(range(10, 20)) ^ self.set_view), 20)
        self.assertEqual(len(self.set_view ^ set(range(10, 20))), 20)

    @unittest.expectedFailure
    def test_and_assignment(self):
        self.set_view &= set(range(5))

    @unittest.expectedFailure
    def test_or_assignment(self):
        self.set_view |= set(range(5))

    @unittest.expectedFailure
    def test_min_assignment(self):
        self.set_view -= set(range(5))

    @unittest.expectedFailure
    def test_xor_assignment(self):
        self.set_view ^= set(range(5))


class TestOuterPinsView(unittest.TestCase):
    def setUp(self) -> None:
        definition = sdn.Definition()
        port = definition.create_port()
        self.inner_pins = port.initialize_pins(10)
        self.instance = sdn.Instance()
        self.instance.reference = definition
        self.outer_pins_view = self.instance.pins

    def test_contains(self):
        self.assertTrue(all(x in self.outer_pins_view for x in self.inner_pins))
        self.assertTrue(all(sdn.OuterPin(self.instance, x) in self.outer_pins_view for x in self.inner_pins))

    def test_equal(self):
        self.assertEqual(self.outer_pins_view, dict(map(lambda x: (x, sdn.OuterPin(self.instance, x)),
                                                        self.inner_pins)))

    def test_getitem(self):
        self.assertTrue(all(self.outer_pins_view[x] == sdn.OuterPin(self.instance, x) for x in self.inner_pins))
        self.assertTrue(all(self.outer_pins_view[x] is self.outer_pins_view[sdn.OuterPin(self.instance, x)] for x in
                            self.inner_pins))

    def test_iter(self):
        self.assertTrue(all(isinstance(x, sdn.OuterPin) for x in self.outer_pins_view))

    def test_len(self):
        self.assertEqual(len(self.outer_pins_view), 10)

    def test_get(self):
        self.assertEqual(self.outer_pins_view.get(self.inner_pins[0]), sdn.OuterPin(self.instance, self.inner_pins[0]))
        self.assertEqual(self.outer_pins_view.get(sdn.OuterPin(self.instance, self.inner_pins[0])),
                         sdn.OuterPin(self.instance, self.inner_pins[0]))
