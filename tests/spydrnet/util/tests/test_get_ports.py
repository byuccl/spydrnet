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

    def test_get_port_reflection(self):
        port = sdn.Port()
        port.name = "MY_PORT"
        search = next(sdn.get_ports(port, "MY_PORT"))
        self.assertEqual(port, search)

    def test_get_port_inner_pin(self):
        port = sdn.Port()
        pin = port.create_pin()
        search = next(sdn.get_ports(pin))
        self.assertEqual(port, search)
        port.remove_pin(pin)
        search = next(sdn.get_ports(pin), None)
        self.assertIsNone(search)

    def test_get_port_instance_and_outer_pin(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin = port.create_pin()
        instance = sdn.Instance()
        instance.reference = definition

        search = next(sdn.get_ports(instance))
        self.assertIs(port, search)

        outer_pin = instance.pins[pin]
        search = next(sdn.get_ports(outer_pin))
        self.assertIs(port, search)

    def test_get_ports_href_cable(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        port = definition.create_port()
        pin = port.create_pin()
        cable = definition.create_cable()
        wire = cable.create_wire()
        wire.connect_pin(pin)
        instance = sdn.Instance()
        instance.reference = definition
        netlist.top_instance = instance
        href = next(sdn.get_hcables(cable))

        search = next(sdn.get_ports(href))
        self.assertIs(port, search)

    def test_unique(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        port = definition.create_port()
        pin = port.create_pin()
        cable = definition.create_cable()
        wire = cable.create_wire()
        wire.connect_pin(pin)
        instance = sdn.Instance()
        instance.reference = definition

        search = list(sdn.get_ports([netlist, cable]))
        self.assertIs(port, search[0])

        search = list(sdn.get_ports(cable))
        self.assertIs(port, search[0])
