import unittest
import spydrnet as sdn
from spydrnet.ir import Element


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

    def test_netlist_constructor(self):
        self.assertIsInstance(self.netlist, Element, "Netlist is not an element.")
        self.assertTrue(self.netlist, "Constructor return None type or empty collection")
        netlist2 = sdn.Netlist()
        self.assertNotEqual(self.netlist, netlist2, "Unique objects are considered equal.")

    def test_libraries(self):
        self.assertEqual(len(tuple(self.netlist.libraries)), 0)

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


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = sdn.Library()

    def test_netlist_constructor(self):
        self.assertIsInstance(self.library, Element, "Netlist is not an element.")
        self.assertTrue(self.library, "Constructor return None type or empty collection")
        library2 = sdn.Netlist()
        self.assertNotEqual(self.library, library2, "Unique objects are considered equal.")

    def test_create_definition(self):
        definition = self.library.create_definition()
        self.assertTrue(definition in self.library.definitions)
        self.assertEqual(definition.library, self.library)

    def test_add_library(self):
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