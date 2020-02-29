import unittest
import spydrnet as sdn


class TestGetLibraries(unittest.TestCase):
    def test_parameter_checking(self):
        library = sdn.Library()
        definition = library.create_definition()
        definition.name = "MY_DEF"
        self.assertRaises(TypeError, sdn.get_definitions, library, "MY_DEF", patterns="MY_DEF")
        self.assertRaises(TypeError, sdn.get_definitions, library, "MY_DEF", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_definitions, None, "MY_DEF")
        self.assertRaises(TypeError, sdn.get_definitions, [None, library], "MY_DEF")

    def test_collection(self):
        library = sdn.Library()
        definition = library.create_definition()
        definition.name = "MY_DEF"
        ports = list(sdn.get_definitions([library, library]))
        self.assertEqual(len(ports), 1)
