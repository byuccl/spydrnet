#Copyright 2021
#Author Dallin Skouson
#see the license for details
#
#Tests the verilog composers functions and output

from collections import OrderedDict
import unittest
from unittest.case import expectedFailure
import spydrnet as sdn
from spydrnet.composers.verilog.composer import Composer
from collections import OrderedDict

class TestVerilogComposerUnit(unittest.TestCase):

    class TestFile:
        '''represents a file (has a write function for the composer)
        can be used as a drop in replacement for the composer file.write function
        saves all written stuff to a string'''
        def __init__(self):
            self.written = ""

        def write(self, text):
            self.written += text

        def clear(self):
            self.written = ""

        def compare(self, text, should_match = True):
            self.written = self.written.lstrip()
            if (text == self.written) == should_match:
                return True
            else:
                print("The composer wrote:")
                print('"' + self.written + '"')
                print("This was compared to:")
                print('"' + text + '"')
                if not should_match:
                    print("and these are not supposed to match")
                else:
                    print("and these should have matched")
                print("\n")
                return False


    def initialize_tests(self):
        composer = Composer()
        composer.file = self.TestFile()
        return composer

    def initialize_netlist(self):
        netlist = sdn.Netlist()
        netlist.name = "test_netlist"
        return netlist

    def initialize_library(self):
        netlist = self.initialize_netlist()
        library = netlist.create_library()
        library.name = "test_library"
        return library

    def initialize_definition(self):
        library = self.initialize_library()
        definition = library.create_definition()
        definition.name = "test_definition"
        return definition

    def initialize_instance_parameters(self, instance):
        instance["VERILOG.Parameters"] = OrderedDict()
        instance["VERILOG.Parameters"]["key"] = "value"
        instance["VERILOG.Parameters"]["key2"] = "value2"

        expected1 = ".key(value)"
        expected2 = ".key2(value2)"

        return expected1, expected2

    def initialize_instance_port_connections(self, instance, definition):
        ref_def = definition.library.create_definition()
        instance.reference = ref_def
        ref_def.name = "reference_definition"

        single_bit_port = ref_def.create_port()
        single_bit_port.create_pin()
        single_bit_port.is_downto = True
        single_bit_port.name = "single_bit_port"

        single_bit_cable = definition.create_cable()
        single_bit_cable.name = "single_bit_cable"
        single_bit_cable.is_downto = True
        single_bit_cable.create_wire()


        multi_bit_port = ref_def.create_port()
        multi_bit_port.is_downto = True
        multi_bit_port.create_pins(4)
        multi_bit_port.name = "multi_bit_port"

        multi_bit_port_offset = ref_def.create_port()
        multi_bit_port_offset.lower_index = 4
        multi_bit_port_offset.is_downto = True
        multi_bit_port_offset.create_pins(4)
        multi_bit_port_offset.name = "multi_bit_port_offset"

        partial_port = ref_def.create_port()
        partial_port.create_pins(2)
        partial_port.is_downto = True
        partial_port.name = "partial_port"

        multi_bit_cable = definition.create_cable()
        multi_bit_cable.create_wires(4)
        multi_bit_cable.name = "multi_bit_cable"
        multi_bit_cable.is_downto = True


        concatenated_port = ref_def.create_port()
        concatenated_port.create_pins(4)
        concatenated_port.name = "concatenated_port"

        ccs = []
        for i in range(4):
            cable = definition.create_cable()
            cable.create_wire()
            cable.is_downto = True
            cable.name = "cc_" + str(i)
            ccs.append(cable)


        single_bit_cable.wires[0].connect_pin(instance.pins[single_bit_port.pins[0]])

        for i in range(4):
            multi_bit_cable.wires[i].connect_pin(instance.pins[multi_bit_port.pins[i]])
            multi_bit_cable.wires[i].connect_pin(instance.pins[multi_bit_port_offset.pins[i]])
            ccs[i].wires[0].connect_pin(instance.pins[concatenated_port.pins[i]])

        for i in range(2):
            multi_bit_cable.wires[i].connect_pin(instance.pins[partial_port.pins[i]])

        single_bit_expected = "." + single_bit_port.name + "(" + single_bit_cable.name + ")"

        multi_bit_expected = "." + multi_bit_port.name + "(" + multi_bit_cable.name + ")"

        offset_expected = "." + multi_bit_port_offset.name + "(" + multi_bit_cable.name + ")"

        partial_expected = "." + partial_port.name + "(" + multi_bit_cable.name + "[1:0])"

        concatenated_expected = "." + concatenated_port.name + "({" + ccs[0].name + ', ' + ccs[1].name + ', ' + ccs[2].name + ', ' + ccs[3].name + "})"

        return single_bit_port, single_bit_expected, \
            multi_bit_port, multi_bit_expected, \
            multi_bit_port_offset, offset_expected, \
            partial_port, partial_expected,\
            concatenated_port, concatenated_expected\

    def test_write_header(self):
        composer = self.initialize_tests()
        netlist = sdn.Netlist()
        netlist.name = "Netlist_name"
        composer._write_header(netlist)
        assert composer.file.compare("//Generated from netlist by SpyDrNet\n//netlist name: Netlist_name\n")

    def test_write_brackets_single_bit(self):
        #def _write_brackets(self, bundle, low_index, high_index):
        composer = self.initialize_tests()

        port = sdn.Port()
        cable = sdn.Cable()

        cable_name = "my_cable"
        port_name = "my_port"

        port.name = port_name
        cable.name = cable_name

        port.create_pin()
        cable.create_wire()

        composer._write_brackets(port, None, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, 0, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, None, 0)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, 0, 0)
        assert composer.file.compare("")
        composer.file.clear()

        composer._write_brackets(cable, None, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, 0, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, None, 0)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, 0, 0)
        assert composer.file.compare("")
        composer.file.clear()
        #none of these should write because they are all single bit.

    def test_write_brackets_single_bit_offset(self):
        #def _write_brackets(self, bundle, low_index, high_index):
        composer = self.initialize_tests()

        port = sdn.Port()
        cable = sdn.Cable()

        cable_name = "my_cable"
        port_name = "my_port"

        port.name = port_name
        cable.name = cable_name

        port.create_pin()
        cable.create_wire()

        port.lower_index = 4
        cable.lower_index = 4

        composer._write_brackets(port, None, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, 4, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, None, 4)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, 4, 4)
        assert composer.file.compare("")
        composer.file.clear()

        composer._write_brackets(cable, None, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, 4, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, None, 4)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, 4, 4)
        assert composer.file.compare("")
        composer.file.clear()
        #none of these should write because they are all single bit.

    def test_write_brackets_multi_bit(self):
        composer = self.initialize_tests()

        port = sdn.Port()
        cable = sdn.Cable()

        cable_name = "my_cable"
        port_name = "my_port"

        port.name = port_name
        cable.name = cable_name

        port.create_pins(4) #input [3:0] my_input;
        port.is_downto = True
        cable.create_wires(4) #wire [3:0] my_wire;
        cable.is_downto = True

        composer._write_brackets(port, None, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, 1, None)
        assert composer.file.compare("[1]")
        composer.file.clear()
        composer._write_brackets(port, None, 2)
        assert composer.file.compare("[2]")
        composer.file.clear()
        composer._write_brackets(port, 2, 2)
        assert composer.file.compare("[2]")
        composer.file.clear()
        composer._write_brackets(port, 0, 3)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, 1, 2)
        assert composer.file.compare("[2:1]")
        composer.file.clear()

        composer._write_brackets(cable, None, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, 1, None)
        assert composer.file.compare("[1]")
        composer.file.clear()
        composer._write_brackets(cable, None, 2)
        assert composer.file.compare("[2]")
        composer.file.clear()
        composer._write_brackets(cable, 2, 2)
        assert composer.file.compare("[2]")
        composer.file.clear()
        composer._write_brackets(cable, 0, 3)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, 1, 2)
        assert composer.file.compare("[2:1]")
        composer.file.clear()


    def test_write_brackets_multi_bit_offset(self):
        composer = self.initialize_tests()

        port = sdn.Port()
        cable = sdn.Cable()

        cable_name = "my_cable"
        port_name = "my_port"

        port.name = port_name
        cable.name = cable_name

        port.create_pins(4) #input [3:0] my_input;
        port.is_downto = True
        port.lower_index = 4
        cable.create_wires(4) #wire [3:0] my_wire;
        cable.is_downto = True
        cable.lower_index = 4

        composer._write_brackets(port, None, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, 5, None)
        assert composer.file.compare("[5]")
        composer.file.clear()
        composer._write_brackets(port, None, 6)
        assert composer.file.compare("[6]")
        composer.file.clear()
        composer._write_brackets(port, 6, 6)
        assert composer.file.compare("[6]")
        composer.file.clear()
        composer._write_brackets(port, 4, 7)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(port, 5, 6)
        assert composer.file.compare("[6:5]")
        composer.file.clear()

        composer._write_brackets(cable, None, None)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, 5, None)
        assert composer.file.compare("[5]")
        composer.file.clear()
        composer._write_brackets(cable, None, 6)
        assert composer.file.compare("[6]")
        composer.file.clear()
        composer._write_brackets(cable, 6, 6)
        assert composer.file.compare("[6]")
        composer.file.clear()
        composer._write_brackets(cable, 4, 7)
        assert composer.file.compare("")
        composer.file.clear()
        composer._write_brackets(cable, 5, 6)
        assert composer.file.compare("[6:5]")
        composer.file.clear()

    def test_write_brackets_fail(self):
        pass #we should add some tests to test out of bounds on the brackets.

    def test_write_brackets_defining(self):

        composer = self.initialize_tests()

        def initialize_bundle(bundle, offset, width):
            if isinstance(bundle, sdn.Port):
                bundle.create_pins(width)
            else: #it's a cable
                bundle.create_wires(width)
            bundle.is_downto = True
            bundle.lower_index = offset
            return bundle

        b1 = initialize_bundle(sdn.Port(), 0, 1)
        b2 = initialize_bundle(sdn.Cable(), 4, 1)
        b3 = initialize_bundle(sdn.Port(), 0, 4)
        b4 = initialize_bundle(sdn.Cable(), 4, 4)

        composer._write_brackets_defining(b1)
        assert composer.file.compare("")
        composer.file.clear()

        composer._write_brackets_defining(b2)
        assert composer.file.compare("[4:4]")
        composer.file.clear()

        composer._write_brackets_defining(b3)
        assert composer.file.compare("[3:0]")
        composer.file.clear()

        composer._write_brackets_defining(b4)
        assert composer.file.compare("[7:4]")
        composer.file.clear()

    def test_write_name(self):
        composer = self.initialize_tests()
        o = sdn.Cable() #Type of this shouldn't really matter
        valid_names = ["basic_name", "\\escaped ", "\\fads#@%!$!@#%$[0:4320] "]
        for n in valid_names:
            o.name = n
            composer._write_name(o)
            assert composer.file.compare(n)
            composer.file.clear()

    @unittest.expectedFailure
    def test_write_none_name(self):
        composer = self.initialize_tests()
        o = sdn.Cable()
        composer._write_name(o)

    @unittest.expectedFailure
    def test_write_invalid_name(self):
        composer = self.initialize_tests()
        o = sdn.Cable()
        o.name = "\\escaped_no_space"
        composer._write_name(o)

    def test_write_instance_port(self):
        composer = self.initialize_tests()
        definition = self.initialize_definition()
        instance = definition.create_child()
        instance.name = "ports_test"

        single_bit_port, single_bit_expected, \
            multi_bit_port, multi_bit_expected, \
            multi_bit_port_offset, offset_expected, \
            partial_port, partial_expected, \
            concatenated_port, concatenated_expected\
            = self.initialize_instance_port_connections(instance, definition)

        composer._write_instance_port(instance, single_bit_port)
        assert composer.file.compare(single_bit_expected)
        composer.file.clear()

        composer._write_instance_port(instance, multi_bit_port)
        assert composer.file.compare(multi_bit_expected)
        composer.file.clear()

        composer._write_instance_port(instance, multi_bit_port_offset)
        assert composer.file.compare(offset_expected)
        composer.file.clear()

        composer._write_instance_port(instance, partial_port)
        assert composer.file.compare(partial_expected)
        composer.file.clear()

        composer._write_instance_port(instance, concatenated_port)
        assert composer.file.compare(concatenated_expected)
        composer.file.clear()

        composer._write_instance_ports(instance)
        expected = "(\n"
        first = True
        expected_strs = [single_bit_expected, multi_bit_expected, offset_expected, partial_expected, concatenated_expected]
        for i in expected_strs:
            if not first:
                expected += ",\n"
            expected +=  "        "
            expected += i
            first = False
        expected += "\n    );"
        assert composer.file.compare(expected)

    def test_write_instance_parameters(self):
        composer = self.initialize_tests()
        definition = self.initialize_definition()
        instance = definition.create_child()
        instance.name = "ports_test"
        ref_def = definition.library.create_definition()
        instance.reference = ref_def

        expected1, expected2 =self.initialize_instance_parameters(instance)
        #instance["VERILOG.Parameters"]["no_value"] = None #always has value?

        composer._write_instance_parameter("key", "value")
        assert composer.file.compare(expected1)
        composer.file.clear()

        composer._write_instance_parameter("key2", "value2")
        assert composer.file.compare(expected2)
        composer.file.clear()


        # composer._write_instance_parameter("no_value", None)
        # expected3 = ".key()"
        # assert composer.file.compare(expected2)
        # composer.file.clear()

        composer._write_instance_parameters(instance)
        expected = "#(\n        " + expected1 + ",\n        " + expected2 + "\n    )\n"
        assert composer.file.compare(expected)


    def test_write_full_instance(self):
        composer = self.initialize_tests()
        definition = self.initialize_definition()
        instance = definition.create_child()
        instance.name = "instance_test"

        expected1, expected2 = self.initialize_instance_parameters(instance)
        parameters_expected = "#(\n        " + expected1 + ",\n        " + expected2 + "\n    )\n"
        single_bit_port, single_bit_expected, \
            multi_bit_port, multi_bit_expected, \
            multi_bit_port_offset, offset_expected, \
            partial_port, partial_expected, \
            concatenated_port, concatenated_expected\
            = self.initialize_instance_port_connections(instance, definition)

        port_expected = "\n    (\n"
        first = True
        expected_strs = [single_bit_expected, multi_bit_expected, offset_expected, partial_expected, concatenated_expected]
        for i in expected_strs:
            if not first:
                port_expected += ",\n"
            port_expected +=  "        "
            port_expected += i
            first = False
        port_expected += "\n    );"

        composer._write_module_body_instance(instance)

        expected = instance.reference.name + " " + parameters_expected + "    " + instance.name + port_expected + "\n"
        assert composer.file.compare(expected)

    def test_write_module_header(self):
        composer = self.initialize_tests()
        definition = self.initialize_definition()
        definition["VERILOG.Parameters"] = OrderedDict()

        definition["VERILOG.Parameters"]["key"] = "value"
        definition["VERILOG.Parameters"]["no_default"] = None

        port = definition.create_port()
        port.name = "my_port"
        port.create_pin()

        port = definition.create_port()
        port.name = "my_port2"
        port.create_pin()

        port.direction = sdn.Port.Direction.IN

        composer._write_module_header(definition)
        expected = "module " + definition.name + "\n#(\n    parameter key = value,\n    parameter no_default\n)(\n    my_port,\n    my_port2\n);\n\n"
        assert composer.file.compare(expected)

    def test_write_module_ports_header_and_body_alias(self):
        composer = self.initialize_tests()
        definition = self.initialize_definition()

        port_alias = definition.create_port()
        port_alias.name = "aliased"
        port_alias.create_pins(2)
        port_alias.direction = sdn.Port.Direction.IN

        c1 = definition.create_cable("c1")
        c2 = definition.create_cable("c2")
        c1.create_wire()
        c2.create_wire()

        c1.wires[0].connect_pin(port_alias.pins[0])
        c2.wires[0].connect_pin(port_alias.pins[1])

        composer._write_module_header_port(port_alias)
        assert composer.file.compare("." + port_alias.name + "({"+ c1.name + ", " + c2.name +"})")
        composer.file.clear()
        composer._write_module_body_port(port_alias)
        assert composer.file.compare("input " + c1.name + ";\n    " + "input " + c2.name + ";\n")
        composer.file.clear()


    def test_write_module_ports_header_and_body_multi(self):
        composer = self.initialize_tests()
        definition = self.initialize_definition()

        port_multi = definition.create_port("multi_bit")
        port_multi.name = "multi_bit"
        port_multi.create_pins(4)
        port_multi.direction = sdn.Port.Direction.OUT

        cable_multi = definition.create_cable("multi_bit")
        cable_multi.create_wires(4)

        for i in range(4):
            cable_multi.wires[i].connect_pin(port_multi.pins[i])

        composer._write_module_header_port(port_multi)
        assert composer.file.compare(port_multi.name)
        composer.file.clear()
        composer._write_module_body_port(port_multi)
        assert composer.file.compare("output [3:0]" + port_multi.name + ";\n")
        composer.file.clear()


    def test_write_module_ports_header_and_body_disconnect(self):
        composer = self.initialize_tests()
        definition = self.initialize_definition()

        port_disconnect = definition.create_port("disconnected")
        port_disconnect.direction = sdn.Port.Direction.INOUT
        port_disconnect.create_pin()

        composer._write_module_header_port(port_disconnect)
        assert composer.file.compare(port_disconnect.name)
        composer.file.clear()
        composer._write_module_body_port(port_disconnect)
        assert composer.file.compare("inout " + port_disconnect.name + ';\n')
        composer.file.clear()

    def test_write_module_body_cables(self):
        composer = self.initialize_tests()
        definition = self.initialize_definition()

        cable = definition.create_cable(name = "test_cable", is_downto = True)
        cable.create_wires(4)

        composer._write_module_body_cable(cable)
        assert composer.file.compare("wire [3:0]" + cable.name + ";\n")


    def test_assignment_single_bit(self):
        pass

    def test_assignment_multi_bit(self):
        pass

