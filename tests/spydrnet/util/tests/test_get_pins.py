import unittest
import spydrnet as sdn


class TestGetPins(unittest.TestCase):
    def test_parameter_checking(self):
        definition = sdn.Definition()
        cable = definition.create_cable()
        cable.name = "MY_CABLE"
        self.assertRaises(TypeError, sdn.get_pins, definition, "MY_CABLE")
        self.assertRaises(TypeError, sdn.get_pins, definition, unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_pins, definition, selection=None)
        self.assertRaises(TypeError, sdn.get_pins, None)
        self.assertRaises(TypeError, sdn.get_pins, [None, definition])

    def test_of_port_inside_and_outside(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin = port.create_pin()
        instance = sdn.Instance()
        instance.reference = definition

        search = next(sdn.get_pins(instance))
        self.assertEqual(search, pin)

        search = next(sdn.get_pins(instance, selection="OUTSIDE"))
        self.assertEqual(search, instance.pins[pin])

    def test_of_inner_pin_outside(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin = port.create_pin()
        instance = sdn.Instance()
        instance.reference = definition

        search = next(sdn.get_pins(pin, selection="OUTSIDE"))
        self.assertEqual(search, instance.pins[pin])

    def test_of_definition(self):
        definition = sdn.Definition()
        port = definition.create_port()
        pin = port.create_pin()
        instance = sdn.Instance()
        instance.reference = definition

        search = next(sdn.get_pins(definition))
        self.assertEqual(search, pin)

    def test_of_href_to_cable(self):
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

        search = next(sdn.get_pins(href))
        self.assertEqual(search, pin)

    def test_of_netlist_and_library_and_port(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        definition = library.create_definition()
        port = definition.create_port()
        pin = port.create_pin()
        instance = sdn.Instance()
        instance.reference = definition

        search = next(netlist.get_pins())
        self.assertEqual(search, pin)

        search = next(sdn.get_pins(library))
        self.assertEqual(search, pin)

        search = next(sdn.get_pins(port))
        self.assertEqual(search, pin)
