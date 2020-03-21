import unittest

import spydrnet as sdn
from spydrnet.ir.first_class_element import FirstClassElement


class TestNetlist(unittest.TestCase):
    def setUp(self):
        self.netlist = sdn.Netlist()

    def test_constructor(self):
        self.assertIsInstance(self.netlist, FirstClassElement, "Netlist is not an element.")
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