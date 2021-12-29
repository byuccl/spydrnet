import unittest

import spydrnet as sdn
from spydrnet.ir import FirstClassElement


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.library = sdn.Library()

    def test_constructor(self):
        self.assertIsInstance(self.library, FirstClassElement, "Netlist is not an element.")
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

    def test_no_parent_netlist(self):
        library = sdn.Library()
        self.assertTrue('parent netlist undefined' in library.__str__())

    def test_no_parent_netlist_name(self):
        netlist = sdn.Netlist()
        library = sdn.Library()
        netlist.add_library(library)
        self.assertTrue('parent netlist.name undefined' in library.__str__())
