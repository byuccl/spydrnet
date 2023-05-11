import unittest

import spydrnet as sdn
from spydrnet.ir import Bundle
from spydrnet.ir import FirstClassElement


class TestBundle(unittest.TestCase):
    def setUp(self) -> None:
        self.bundle = Bundle()

    def test_constructor(self):
        self.assertIsInstance(self.bundle, FirstClassElement, "Bundle is not an element.")
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
        self.assertRaises(NotImplementedError, self.bundle._items)
