import unittest
import spydrnet as sdn


class TestGetNetlists(unittest.TestCase):
    def test_parameter_checking(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        library.name = "MY_LIB"
        self.assertRaises(TypeError, sdn.get_netlists, netlist, "MY_LIB", patterns="MY_LIB")
        self.assertRaises(TypeError, sdn.get_netlists, netlist, "MY_LIB", unsupported_keyword=None)
        self.assertRaises(TypeError, sdn.get_netlists, None, "MY_LIB")
        self.assertRaises(TypeError, sdn.get_netlists, [None, netlist], "MY_LIB")

    def test_collection(self):
        netlist = sdn.Netlist()
        library = netlist.create_library()
        library.name = "MY_LIB"
        netlists = list(sdn.get_netlists([netlist, netlist]))
        self.assertEqual(len(netlists), 1)

    def test_pin_and_wire_chain(self):
        netlist = sdn.Netlist()
        netlist.name = "MY_NETLIST"
        library = netlist.create_library()
        definition = library.create_definition()
        port = definition.create_port()
        pin = port.create_pin()
        cable = definition.create_cable()
        wire = cable.create_wire()
        instance = sdn.Instance()
        instance.name = "MY_INST"
        instance.reference = definition
        netlist.top_instance = instance

        netlist_lookup = next(wire.get_netlists(), None)
        self.assertIs(netlist, netlist_lookup)

        cable.remove_wire(wire)
        netlist_lookup = next(sdn.get_netlists(wire), None)
        self.assertIsNone(netlist_lookup)

        definition.remove_cable(cable)
        netlist_lookup = next(sdn.get_netlists(cable), None)
        self.assertIsNone(netlist_lookup)

        outer_pin = instance.pins[pin]
        netlist_lookup = next(sdn.get_netlists(outer_pin), None)
        self.assertIs(netlist, netlist_lookup)

        port.remove_pin(pin)
        netlist_lookup = next(sdn.get_netlists(pin), None)
        self.assertIsNone(netlist_lookup)

        self.assertIsNone(outer_pin.inner_pin)
        self.assertIsNone(outer_pin.instance)

        top_instance_href = next(sdn.get_hinstances(netlist.top_instance))
        netlist_lookup = next(sdn.get_netlists(top_instance_href))
        self.assertIs(netlist, netlist_lookup)

        definition.remove_port(port)
        netlist_lookup = next(sdn.get_netlists(port), None)
        self.assertIsNone(netlist_lookup)

        instance.reference = None
        netlist_lookup = next(sdn.get_netlists(instance), None)
        self.assertIsNone(netlist_lookup)

        library.remove_definition(definition)
        netlist_lookup = next(sdn.get_netlists(definition), None)
        self.assertIsNone(netlist_lookup)

        netlist.remove_library(library)
        netlist_lookup = next(sdn.get_netlists(library), None)
        self.assertIsNone(netlist_lookup)

        netlist_lookup = next(sdn.get_netlists(netlist, "MY_NETLIST"))
        self.assertTrue(netlist is netlist_lookup)
