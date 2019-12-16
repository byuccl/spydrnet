import unittest

from spydrnet.ir.element import Element


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

    def test_data_view(self):
        element = Element()
        element['NAME'] = "TestName"
        self.assertEqual(element.data, {'NAME': 'TestName'})
