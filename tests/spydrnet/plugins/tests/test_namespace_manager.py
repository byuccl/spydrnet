import unittest
import spydrnet as sdn


class TestNamespaceManager(unittest.TestCase):

    def test_naming_after_assignments(self):
        library = sdn.Library()
        definition = library.create_definition()
        definition2 = library.create_definition()
        definition.name = "Hello"
        definition.name = "World"
        definition2.name = "Hello"
        caught_conflict = False
        try:
            definition2.name = "World"
        except ValueError:
            caught_conflict = True
        self.assertTrue(caught_conflict)
