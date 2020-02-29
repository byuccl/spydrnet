import unittest
import spydrnet as sdn


class TestGetCables(unittest.TestCase):
    def test_parameter_checking(self):
        definition = sdn.Definition()
        cable = definition.create_cable()
        cable.name = "MY_CABLE"
        self.assertRaises(TypeError, sdn.get_cables, definition, "MY_CABLE", patterns="MY_CABLE")
        self.assertRaises(TypeError, sdn.get_cables, definition, "MY_CABLE", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_cables, None, "MY_CABLE")
        self.assertRaises(TypeError, sdn.get_cables, [None, definition], "MY_CABLE")

    def test_collection(self):
        definition = sdn.Definition()
        cable = definition.create_cable()
        cable.name = "MY_CABLE"
        cables = list(sdn.get_cables([definition, definition]))
        self.assertEqual(len(cables), 1)

    def test_get_cables_in_library(self):
        library = sdn.Library()
        definition = library.create_definition()
        cable = definition.create_cable()
        cable.name = "MY_PORT"
        instance = sdn.Instance()
        instance.reference = definition
        port1 = next(library.get_cables("MY_PORT"))
        self.assertEqual(cable, port1)

    def test_get_cables_in_netlist(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        cables = definition.create_cable()
        cables.name = "MY_PORT"
        instance = sdn.Instance()
        instance.reference = definition
        port1 = next(netlist.get_cables("MY_PORT"))
        self.assertEqual(cables, port1)
