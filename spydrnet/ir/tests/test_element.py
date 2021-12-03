import unittest

from spydrnet.ir import FirstClassElement


class TestElement(unittest.TestCase):
    def setUp(self) -> None:
        self.element = FirstClassElement()

    def test_constructor(self):
        element1 = FirstClassElement()
        self.assertTrue(element1, "Constructor return None type or empty collection")
        element2 = FirstClassElement()
        self.assertNotEqual(element1, element2, "Unique objects are considered equal.")

    def test_dictionary(self):
        self.assertFalse('NAME' in self.element)
        self.element['NAME'] = "TestName"
        self.assertTrue('NAME' in self.element)
        for key in self.element:
            self.assertEqual(self.element[key], "TestName")
        del self.element['NAME']
        self.assertFalse('NAME' in self.element)
        self.element['NAME'] = "DifferentName"
        name = self.element.pop('NAME')
        self.assertEqual(name, "DifferentName")

    def test_name(self):
        self.element.name = "TestName"
        self.assertTrue(".NAME" in self.element)
        self.assertEqual(self.element.name, "TestName")

    def test_del_name(self):
        self.assertIsNone(self.element.name)
        self.element.name = None
        self.element.name = "TestName"
        self.element.name = None
        self.assertFalse(".NAME" in self.element)
        self.element.name = "TestName"
        del self.element.name
        self.assertFalse(".NAME" in self.element)

    def test_data_view(self):
        self.element['NAME'] = "TestName"
        self.assertEqual(self.element.data, {'NAME': 'TestName'})
