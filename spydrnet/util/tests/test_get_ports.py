import unittest
import spydrnet as sdn


class TestGetPorts(unittest.TestCase):
    def test_parameter_checking(self):
        definition = sdn.Definition()
        port = definition.create_port()
        port.name = "MY_PORT"
        self.assertRaises(TypeError, sdn.get_ports, definition, "MY_PORT", patterns="MY_PORT")
        self.assertRaises(TypeError, sdn.get_ports, definition, "MY_PORT", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_ports, None, "MY_PORT")
        self.assertRaises(TypeError, sdn.get_ports, [None, definition], "MY_PORT")

    def test_collection(self):
        definition = sdn.Definition()
        port = definition.create_port()
        port.name = "MY_PORT"
        instance = sdn.Instance()
        instance.name = "MY_INST"
        ports = list(sdn.get_ports([definition, instance]))
        self.assertEqual(len(ports), 1)

    def test_get_ports_on_instance(self):
        definition = sdn.Definition()
        port = definition.create_port()
        port.name = "MY_PORT"
        instance = sdn.Instance()
        instance.reference = definition
        port1 = next(instance.get_ports("MY_PORT"))
        self.assertEqual(port, port1)

    def test_get_ports_in_library(self):
        library = sdn.Library()
        definition = library.create_definition()
        port = definition.create_port()
        port.name = "MY_PORT"
        instance = sdn.Instance()
        instance.reference = definition
        port1 = next(library.get_ports("MY_PORT"))
        self.assertEqual(port, port1)

    def test_get_ports_in_netlist(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        port = definition.create_port()
        port.name = "MY_PORT"
        instance = sdn.Instance()
        instance.reference = definition
        port1 = next(netlist.get_ports("MY_PORT"))
        self.assertEqual(port, port1)
