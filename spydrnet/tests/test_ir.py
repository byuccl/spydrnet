import unittest
import spydrnet as sdn
from spydrnet.ir import Element
from spydrnet.ir import ListView


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
    def test_remove_port_from_outside_definition(self):
        port = sdn.Port()
        self.definition.remove_ports_from((port,))

    def test_remove_port_from(self):
        port = self.definition.create_port()
        self.definition.remove_ports_from((port,))
        self.assertFalse(port in self.definition.ports)
        self.assertIsNone(port.definition)


    def test_is_leaf(self):
        self.assertTrue(self.definition.is_leaf()), "Empty definition is not considered a leaf cell"
        # TODO: Check definition with ports is considered a leaf cell
        # TODO: check definition with cables is conidered a non leaf cell
        # TODO: check definition with instances is considered a non leaf cell
        # TODO: Check definition with both cables and instances is consideredered a leaf cell


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
