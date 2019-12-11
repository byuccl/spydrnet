import unittest
import spydrnet as sdn
from spydrnet.ir import Element
from spydrnet.ir import Bundle
from spydrnet.ir import ListView
from spydrnet.ir import SetView


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


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = sdn.Library()

    def test_constructor(self):
        self.assertIsInstance(self.library, Element, "Netlist is not an element.")
        self.assertTrue(self.library, "Constructor return None type or empty collection")
        library2 = sdn.Netlist()
        self.assertNotEqual(self.library, library2, "Unique objects are considered equal.")

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
        definition = self.library.create_definition()
        self.library.remove_definitions_from({definition})


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
        port = self.definition.create_port()
        self.definition.remove_ports_from((port,))
        self.assertFalse(port in self.definition.ports)
        self.assertIsNone(port.definition)

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
        cable = self.definition.create_cable()
        self.definition.remove_cables_from({cable})
        self.assertFalse(cable in self.definition.cables)
        self.assertIsNone(cable.definition)

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
        instance = self.definition.create_child()
        self.definition.remove_children_from((instance,))

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
        pin = self.port.create_pin()
        self.port.remove_pins_from((pin,))
        self.assertFalse(pin in self.port.pins)
        self.assertIsNone(pin.port)

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
        self.assertEqual(len(self.list_view*2), 20)
        self.assertEqual(len(2*self.list_view), 20)

    def test_add(self):
        result = list(range(10, 20)) + self.list_view
        print(result)
        self.assertEqual(len(result), 20)
        result = self.list_view + list(range(10,20))
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