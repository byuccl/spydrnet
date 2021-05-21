# Copyright 2021 please see the license
# Author Dallin Skouson

import unittest
import spydrnet as sdn
from spydrnet.parsers.verilog.parser import VerilogParser
import spydrnet.parsers.verilog.verilog_tokens as vt
from spydrnet import parsers
import os

class TestVerilogParser(unittest.TestCase):

    class TestTokenizer:
        def __init__(self, tokenlist):
            self.tokens = tokenlist
            self.index = 0
            self.highest = len(tokenlist)

        @property
        def line_number(self):
            return self.index

        def has_next(self):
            return self.index < self.highest

        def next(self):
            token = self.tokens[self.index]
            self.index += 1
            return token
        
        def peek(self):
            token = self.tokens[self.index]
            return token

    ###################################################
    ##Module Headers
    ###################################################

    def test_module_header_parameter_parsing(self):
        expected = dict()
        expected["INIT"] = "1'h1"
        expected["[1:0] INIT0"] = "2'h0"
        expected["[0] INIT1"] = "1'b0"
        tokens = ["#", "(", "parameter", "INIT", "=", "1'h1", ",",\
            "parameter", "[", "1", ":", "0", "]", "INIT0", "=", "2'h0", ",",\
            "parameter", "[", "0", "]", "INIT1", "=", "1'b0", ")"]

        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        parser.current_definition = sdn.Definition()

        parser.parse_module_header_parameters()

        assert "VERILOG.Parameters" in parser.current_definition, "expected parameters in the definition"
        parameters = parser.current_definition["VERILOG.Parameters"]
        for k, v in expected.items():
            assert k in parameters, "expected to see " + k + " in the definition parameters"
            assert parameters[k] == v, "expected value of k to be " + v + " but got instead " + parameters[k]
        
        for k, v in parameters.items():
            assert k in expected, "unexpected value " + k + " in the definition parameters"
        
    def test_module_header_port_name_only(self):
        #expected = [(direction, left, right, name)]
        expected = ["PORT0", "PORT1", "PORT2", "PORT3", "PORT4"]
        tokens = ["("]
        first_run = True
        for p in expected:
            if first_run:
                tokens.append(p)
                first_run = False
            else:
                tokens.append(",")
                tokens.append(p)
        tokens.append(")")

        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.current_definition = sdn.Definition()
        parser.tokenizer = tokenizer

        parser.parse_module_header_ports()

        assert len(parser.current_definition.ports) == len(expected), \
            "port count mismatch definition: " + str(len(parser.current_definition.ports)) + " expected: " + str(len(expected))

        for i in range(len(expected)):
            assert expected[i] == parser.current_definition.ports[i].name

    def test_module_header_port_name_and_direction(self):
        #expected = [(direction, left, right, name)]
        expected = [("PORT0", "output"), ("PORT1", "input"), ("PORT2", "inout"), ("PORT3", "output"), ("PORT4", "input")]
        tokens = ["("]
        first_run = True
        for p in expected:
            if first_run:
                tokens.append(p[1])
                tokens.append(p[0])
                first_run = False
            else:
                tokens.append(",")
                tokens.append(p[1])
                tokens.append(p[0])
        tokens.append(")")

        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.current_definition = sdn.Definition()
        parser.tokenizer = tokenizer

        parser.parse_module_header_ports()

        assert len(parser.current_definition.ports) == len(expected), \
            "port count mismatch definition: " + str(len(parser.current_definition.ports)) + " expected: " + str(len(expected))

        for i in range(len(expected)):
            assert expected[i][0] == parser.current_definition.ports[i].name,\
                "ports names don't match. Definition: " + parser.current_definition.ports[i].name + " expected " + expected[i][0]
            expected_direction = vt.string_to_port_direction(expected[i][1])
            definition_direction = parser.current_definition.ports[i].direction
            assert expected_direction == definition_direction, \
                "directions do not match up expected " + str(expected_direction) + " but got " + definition_direction

    def test_module_heaader_port_name_and_index(self):
        #expected = [(direction, left, right, name)]
        expected = [("PORT0", "5" , "0"), ("PORT1", "8","-2"), ("PORT2", "0","0"), ("PORT3", "16","8"), ("PORT4", "3","0")]
        tokens = ["("]
        first_run = True
        for p in expected:
            if first_run:
                first_run = False
            else:
                tokens.append(",")
            tokens.append("[")
            tokens.append(p[1])
            tokens.append(":")
            tokens.append(p[2])
            tokens.append("]")
            tokens.append(p[0])
        tokens.append(")")

        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.current_definition = sdn.Definition()
        parser.tokenizer = tokenizer

        parser.parse_module_header_ports()

        assert len(parser.current_definition.ports) == len(expected), \
            "port count mismatch definition: " + str(len(parser.current_definition.ports)) + " expected: " + str(len(expected))

        for i in range(len(expected)):
            assert expected[i][0] == parser.current_definition.ports[i].name,\
                "ports names don't match. Definition: " + parser.current_definition.ports[i].name + " expected " + expected[i][0]
            expected_lower = min(int(expected[i][2]), int(expected[i][1]))
            definition_lower = parser.current_definition.ports[i].lower_index

            expected_width = max(int(expected[i][2]), int(expected[i][1])) - expected_lower + 1
            definition_width = len(parser.current_definition.ports[i].pins)
            assert expected_lower == definition_lower, \
                "lower indicies do not match up expected " + str(expected_lower) + " but got " + str(definition_lower)
            
            assert expected_width == definition_width, \
                "widths do not match up expected " + str(expected_width) + " but got " + str(definition_width)


    def test_module_header_all_present(self):
        expected = [("PORT0", "5" , "0", "input"), ("PORT1", "8","-2", "output"), ("PORT2", "0","0", "inout"),\
            ("PORT3", "16","8", "input"), ("PORT4", "3","0", "output")]
        tokens = ["("]
        first_run = True
        for p in expected:
            if first_run:
                first_run = False
            else:
                tokens.append(",")
            tokens.append(p[3])
            tokens.append("[")
            tokens.append(p[1])
            tokens.append(":")
            tokens.append(p[2])
            tokens.append("]")
            tokens.append(p[0])
        tokens.append(")")

        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.current_definition = sdn.Definition()
        parser.tokenizer = tokenizer

        parser.parse_module_header_ports()

        assert len(parser.current_definition.ports) == len(expected), \
            "port count mismatch definition: " + str(len(parser.current_definition.ports)) + " expected: " + str(len(expected))

        for i in range(len(expected)):
            assert expected[i][0] == parser.current_definition.ports[i].name,\
                "ports names don't match. Definition: " + parser.current_definition.ports[i].name + " expected " + expected[i][0]
            expected_lower = min(int(expected[i][2]), int(expected[i][1]))
            definition_lower = parser.current_definition.ports[i].lower_index

            expected_width = max(int(expected[i][2]), int(expected[i][1])) - expected_lower + 1
            definition_width = len(parser.current_definition.ports[i].pins)
            assert expected_lower == definition_lower, \
                "lower indicies do not match up expected " + str(expected_lower) + " but got " + str(definition_lower)
            
            assert expected_width == definition_width, \
                "widths do not match up expected " + str(expected_width) + " but got " + str(definition_width)

            expected_direction = vt.string_to_port_direction(expected[i][3])
            definition_direction = parser.current_definition.ports[i].direction
            assert expected_direction == definition_direction, \
                "directions do not match up expected " + str(expected_direction) + " but got " + definition_direction

    def test_port_aliasing(self):
        parser = VerilogParser()
        token_list = [".", "portName", "(", "{", "cable1", ",", "cable2", ",", "cable3", "}", ")"]
        parser.tokenizer = self.TestTokenizer(token_list)

        d = sdn.Definition()
        parser.current_definition = d

        parser.parse_module_header_port_alias()
        assert len(d.ports) == 1, "definition has the wrong number of ports, should have 1 has " + str(len(d.ports))
        assert d.ports[0].name == "portName", "port has the wrong name it should be portName but is " + d.ports[0].name
        assert len(d.ports[0].pins) == 3
        assert len(d.cables) == 3
        names = [d.cables[0].name, d.cables[1].name, d.cables[2].name]
        assert "cable1" in names and "cable2" in names and "cable3" in names

    def test_port_aliasing_single(self):
        parser = VerilogParser()
        token_list = [".", "portName", "(", "cable1", ")"]
        parser.tokenizer = self.TestTokenizer(token_list)

        d = sdn.Definition()
        parser.current_definition = d

        parser.parse_module_header_port_alias()

        assert len(d.ports) == 1
        assert d.ports[0].name == "portName"
        assert len(d.cables) == 1
        assert len(d.ports[0].pins) == 1
        assert len(d.cables[0].wires) == 1
        assert d.cables[0].name == "cable1"

    def test_non_zero_lower_port_index(self):
        '''this test based on an issue found while parsing riscv_multi_core.v in the support files
        to see the problem lines that caused this test see line 89 and line 41'''

        parser = VerilogParser()
        token_list = ["module", "alu", "(", "instruction", ")", ";", "output", "[", "27", ":", "26", "]", "instruction", ";", "endmodule"]
        tokenizer = self.TestTokenizer(token_list)
        parser.tokenizer = tokenizer
        parser.current_library = sdn.Library(name = "TestLibrary")
        parser.netlist = sdn.Netlist()
        parser.netlist.add_library(parser.current_library)
        
        parser.parse_module()

        assert len(parser.current_definition.ports) == 1
        assert len(parser.current_definition.cables) == 1
        c = parser.current_definition.cables[0]
        p = parser.current_definition.ports[0]
        assert c.name == "instruction"
        assert len(c.wires) == 2
        assert p.name == "instruction"
        assert len(p.pins) == 2
        assert c.lower_index == 26
        assert p.lower_index == 26

        for w in c.wires:
            assert w.pins[0] in p.pins

    def test_port_cable_resize_post_creation(self):
        '''we need a test that creates a port and then resizes it on definition
        
        module something(port);
        input [3:0] port;
        endmodule'''
        parser = VerilogParser()
        token_list = ["module", "alu", "(", "instruction", ")", ";", "output", "[", "3", ":", "0", "]", "instruction", ";", "endmodule"]
        tokenizer = self.TestTokenizer(token_list)
        parser.tokenizer = tokenizer
        parser.current_library = sdn.Library(name = "TestLibrary")
        parser.netlist = sdn.Netlist()
        parser.netlist.add_library(parser.current_library)
        
        parser.parse_module()

        assert len(parser.current_definition.ports) == 1
        assert len(parser.current_definition.cables) == 1
        c = parser.current_definition.cables[0]
        p = parser.current_definition.ports[0]
        assert c.name == "instruction"
        assert len(c.wires) == 4
        assert p.name == "instruction"
        assert len(p.pins) == 4
        assert c.lower_index == 0
        assert p.lower_index == 0

        for w in c.wires:
            assert w.pins[0] in p.pins

    def test_port_resize_on_aliased_port(self):
        '''example of this found in sha3_core.v on line 63176 or 63177 something to do with \\byte_num[0] '''
        tokens = ["module", "keccak", "(",\
            '.','byte_num','(','{','\\byte_num[2] ',',','\\byte_num[1] ', ',','\\byte_num[0] ','}',')',\
            ")", ";", "input", '\\byte_num[0] ', ';', 'input', '\\byte_num[1] ', ';', 'input', '\\byte_num[2] ',';', "endmodule"]
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        parser.current_library = sdn.Library(name = "TestLibrary")
        parser.netlist = sdn.Netlist()
        parser.netlist.add_library(parser.current_library)
        
        parser.parse_module()

        assert len(parser.current_definition.ports) == 1
        assert len(parser.current_definition.cables) == 3
        names = []
        for c in parser.current_definition.cables:
            names.append(c.name)
            assert len(c.wires) == 1
        assert '\\byte_num[2] ' in names
        assert '\\byte_num[1] ' in names
        assert '\\byte_num[0] ' in names
        assert parser.current_definition.ports[0].name == 'byte_num'



    def test_parse_empty_module_header(self):
        '''example in bram.v in the support files on line 18'''
        tokens = ["(", ")", ";"]
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        parser.current_definition = sdn.Definition

        parser.parse_module_header() #intent is to just make sure this does not crash
        #todo add some aserts to check to make sure the number of cables and ports is still 0


    ###################################################
    ##Array Slicing
    ###################################################

    def test_array_slicing_good_single(self):
        left_expected = 2334
        right_expected = None
        tokens = ["[", str(left_expected), "]"]
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        left, right = parser.parse_brackets()
        assert(left == left_expected)
        assert(right == right_expected)

    def test_array_slicing_good_both(self):
        left_expected = 2334
        right_expected = 231
        tokens = ["[", str(left_expected), ":", str(right_expected), "]"]
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        left, right = parser.parse_brackets()
        assert(left == left_expected)
        assert(right == right_expected)

    @unittest.expectedFailure
    def test_array_slicing_bad_colon(self):
        left_expected = 2334
        right_expected = 231
        tokens = ["[", str(left_expected), ",", str(right_expected), "]"]
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        left, right = parser.parse_brackets()
        assert(left == left_expected)
        assert(right == right_expected)
    
    @unittest.expectedFailure
    def test_array_slicing_bad_ending(self):
        left_expected = 2334
        right_expected = 231
        tokens = ["[", str(left_expected), ":", str(right_expected), "something_else"]
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        left, right = parser.parse_brackets()
        assert(left == left_expected)
        assert(right == right_expected)

    @unittest.expectedFailure
    def test_array_slicing_bad_non_numbers(self):
        left_expected = "not a number"
        right_expected = None
        tokens = ["[", str(left_expected), ":", str(right_expected), "something_else"]
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        left, right = parser.parse_brackets()
        assert(left == left_expected)
        assert(right == right_expected)
        

    ###################################################
    ##Cable Creation and modification
    ###################################################

    def init_cable_creation(self):
        parser = VerilogParser()
        
        my_def = sdn.Definition()
        my_def.name = "testing_definition"
        c1 = my_def.create_cable()
        c1.name = "preexisting1" #[15:8]
        c1.create_wires(8)
        c1.lower_index = 8
        c2 = my_def.create_cable()
        c2.name = "preexisting2" #[15:0]
        c2.create_wires(16)
        c3 = my_def.create_cable()
        c3.name = "preexisting3" #[19:16]
        c3.is_downto = False
        c3.lower_index = 16
        c3.create_wires(4)
        
        parser.current_definition = my_def

        return parser, c1, c2, c3

    def add_to_cable_helper(self, tests, parser):
        #tests is a list of tuples that contain
        #name,left,right,type,cable,expected_lower,expected_width, expected_downto

        for entry in tests:
            name, left_index, right_index, var_type, cable, expected_lower, expected_width = entry
            expected_downto = cable.is_downto #the cable should not update it's downto once that has been decided.
            c = parser.create_or_update_cable(name, left_index, right_index, var_type)
            assert c is cable, "the cable is not the expected cable, " + name
            assert len(c.wires) == expected_width, "the cable is not the proper width, " + name
            assert c.lower_index == expected_lower, "the cable does not have the proper lower index, " + name
            assert c.is_downto == expected_downto, "the cable changed downto, " + name


    def create_cable_helper(self, tests, parser):
        #tests is a list of tuples that contain
        #name,left,right,type,cable,expected_lower,expected_width, expected_downto
        start_size = len(parser.current_definition.cables)
        count = 0
        for entry in tests:
            count += 1
            name, left_index, right_index, var_type, cable, expected_lower, expected_width, expected_downto = entry
            c = parser.create_or_update_cable(name, left_index, right_index, var_type)
            assert len(c.wires) == expected_width, "the cable is not the proper width, " + name
            assert c.lower_index == expected_lower, "the cable does not have the proper lower index, " + name
            assert c.is_downto == expected_downto
        assert len(parser.current_definition.cables) == count + start_size, "the wrong number of cables were added"


    def test_add_to_front_of_cable(self):
        parser, c1, c2, c3 = self.init_cable_creation()
        
        tests =\
            [("preexisting1", 15, 0, None, c1, 0, 16),\
            ("preexisting2", 0, -16, None, c2, -16, 32),\
            ("preexisting3", 17, 0, None, c3, 0, 20)]
        self.add_to_cable_helper(tests, parser)


    def test_add_to_back_of_cable(self):
        parser, c1, c2, c3 = self.init_cable_creation()
        
        tests =\
            [("preexisting1", 31, 16, None, c1, 8, 24),\
            ("preexisting2", 31, 8, None, c2, 0, 32),\
            ("preexisting3", 63, 0, None, c3, 0, 64)]
        self.add_to_cable_helper(tests, parser)


    def test_create_cable(self):
        parser, c1, c2, c3 = self.init_cable_creation()
        
        tests =\
            [("new_cable1", 31, 16, None, None, 16, 16, True),\
            ("new_cable2", 0, -7, None, None, -7, 8, True),\
            ("new_cable3", 63, 0, None, None, 0, 64, True)]
        self.create_cable_helper(tests, parser)


    def test_create_cable_downto(self):
        parser, c1, c2, c3 = self.init_cable_creation()
        
        tests =\
            [("new_cable1", 7, 0, None, None, 0, 8, True),\
            ("new_cable2", 0, 7, None, None, 0, 8, False)]
        self.create_cable_helper(tests, parser)

    def test_change_cable_type(self):
        pass #TODO

    def test_dont_change_cable(self):
        parser, c1, c2, c3 = self.init_cable_creation()
        
        tests =\
            [("preexisting1", 15, 8, None, c1, 8, 8),\
            ("preexisting2", 15, 0, None, c2, 0, 16),\
            ("preexisting3", 19, 16, None, c3, 16, 4)]
        self.add_to_cable_helper(tests, parser)

    def test_single_index_cable(self):
        parser, c1, c2, c3 = self.init_cable_creation()
        tests_create =\
            [("new_cable1", 31, None, None, None, 31, 1, True),\
            ("new_cable2", 0, None, None, None, 0, 1, True),\
            ("new_cable3", 63, None, None, None, 63, 1, True)]
        self.create_cable_helper(tests_create, parser)

        parser, c1, c2, c3 = self.init_cable_creation()
        tests_modify =\
            [("preexisting1", 0, None, None, c1, 0, 16),\
            ("preexisting2", 8, None, None, c2, 0, 16),\
            ("preexisting3", 0, None, None, c3, 0, 20)]
        self.add_to_cable_helper(tests_modify, parser)


    def test_change_cable_downto(self):
        #i don't think the cable downto-ness should ever change. this is tested in the add to cable helper
        parser, c1, c2, c3 = self.init_cable_creation()
        
        tests =\
            [("preexisting1", 15, 8, None, c1, 8, 8),\
            ("preexisting1", 8, 15, None, c1, 8, 8)]
        self.add_to_cable_helper(tests, parser)

    def test_cable_prepend_wires(self):
        parser, c1, c2, c3 = self.init_cable_creation()
        c1_width = len(c1.wires)
        c1_lower = c1.lower_index
        c1_wires = set()
        for wire in c1.wires:
            c1_wires.add(wire)
        c2_width = len(c2.wires)
        c2_lower = c2.lower_index
        c2_wires = set()
        for wire in c2.wires:
            c2_wires.add(wire)
        c3_width = len(c3.wires)
        c3_lower = c3.lower_index
        c3_wires = set()
        for wire in c3.wires:
            c3_wires.add(wire)

        print(c1_wires)
        print()
        
        prepend_count = 8

        parser.prepend_wires(c1, prepend_count)
        print(c1_wires)
        print()
        print(c1.wires)
        print()
        assert len(c1.wires) == prepend_count + c1_width, "tried to add 8 wires to c1"
        assert c1.lower_index == c1_lower - prepend_count
        for wire in c1.wires[:prepend_count]:
            assert wire not in c1_wires, "a wire was in the wrong location for the prepend"
        for wire in c1.wires[prepend_count:]:
            assert wire in c1_wires, "a wire seems to have disappeared"

        parser.prepend_wires(c2, prepend_count)
        assert len(c2.wires) == prepend_count + c2_width, "tried to add 8 wires to c2"
        assert c2.lower_index == c2_lower - prepend_count
        for wire in c2.wires[:prepend_count]:
            assert wire not in c2_wires, "a wire was in the wrong location for the prepend"
        for wire in c2.wires[prepend_count:]:
            assert wire in c2_wires, "a wire seems to have disappeared"

        parser.prepend_wires(c3, prepend_count)
        assert len(c3.wires) == prepend_count + c3_width, "tried to add 8 wires to c3"
        assert c3.lower_index == c3_lower - prepend_count
        for wire in c3.wires[:prepend_count]:
            assert wire not in c3_wires, "a wire was in the wrong location for the prepend"
        for wire in c3.wires[prepend_count:]:
            assert wire in c3_wires, "a wire seems to have disappeared"

    def test_cable_postpend_wires(self):
        parser, c1, c2, c3 = self.init_cable_creation()
        c1_width = len(c1.wires)
        c1_lower = c1.lower_index
        c1_wires = set()
        for wire in c1.wires:
            c1_wires.add(wire)
        c2_width = len(c2.wires)
        c2_lower = c2.lower_index
        c2_wires = set()
        for wire in c2.wires:
            c2_wires.add(wire)
        c3_width = len(c3.wires)
        c3_lower = c3.lower_index
        c3_wires = set()
        for wire in c3.wires:
            c3_wires.add(wire)
        
        postpend_count = 8

        parser.postpend_wires(c1, postpend_count)
        assert len(c1.wires) == postpend_count + c1_width, "tried to add 8 wires to c1"
        assert c1.lower_index == c1_lower
        for wire in c1.wires[c1_width:]:
            assert wire not in c1_wires, "a wire was in the wrong location for the postpend"
        for wire in c1.wires[:c1_width]:
            assert wire in c1_wires, "a wire seems to have disappeared"

        parser.postpend_wires(c2, postpend_count)
        assert len(c2.wires) == postpend_count + c2_width, "tried to add 8 wires to c2"
        assert c2.lower_index == c2_lower
        for wire in c2.wires[c2_width:]:
            assert wire not in c2_wires, "a wire was in the wrong location for the postpend"
        for wire in c2.wires[:c2_width]:
            assert wire in c2_wires, "a wire seems to have disappeared"

        parser.postpend_wires(c3, postpend_count)
        assert len(c3.wires) == postpend_count + c3_width, "tried to add 8 wires to c3"
        assert c3.lower_index == c3_lower
        for wire in c3.wires[c3_width:]:
            assert wire not in c3_wires, "a wire was in the wrong location for the postpend"
        for wire in c3.wires[:c3_width]:
            assert wire in c3_wires, "a wire seems to have disappeared"

    def test_populate_new_cable(self):
        parser = VerilogParser()
        
        test_data = [("test_name", 2, 0, "wire"), ("\\escaped#$@_[213] ", 15,8,"wire"), ("some_name", 7,4,"reg")]

        for name, left, right, cable_type in test_data:
            cable = sdn.Cable()
            parser.populate_new_cable(cable,name,left,right,cable_type)
            assert cable.name == name
            assert cable.is_downto == (left >= right)
            assert cable["VERILOG.CableType"] == cable_type
            assert cable.lower_index == min(left,right)

    def test_parse_variable_instantiation(self):
        pass

    def test_parse_cable_concatenation(self):
        parser = VerilogParser()
        
        wire_names = ["wire1", "wire2", "wire3", "wire4"]
        token_list = ["{"]
        first = True
        for wn in wire_names:
            if first:
                first = False
            else:
                token_list.append(",")
            token_list.append(wn)
        token_list.append("}")

        tokenizer = self.TestTokenizer(token_list)
        parser.tokenizer = tokenizer
        parser.current_definition = sdn.Definition()

        wires = parser.parse_cable_concatenation()

        assert len(wires) == len(wire_names), "expected " + str(len(wire_names)) +  " wires to be created instead got " + str(len(wires))
        assert len(parser.current_definition.cables) == len(wire_names), "expected " + str(len(wire_names)) +  " cables to be created instead got " + str(len(parser.current_definition.cables))

        for i in range(len(wire_names)):
            assert parser.current_definition.cables[i].name == wire_names[i], " the wires created do not have matching names"
            assert wires[i].cable.name == wire_names[i], "the wires returned are not in order."
            
    ############################################################################
    ##Instance instantiation
    ############################################################################

    def test_parse_instantiation(self):
        pass

    def test_parse_empty_port_map(self):
        parser = VerilogParser()
        definition = sdn.Definition()
        parser.current_definition = definition
        parser.current_instance = definition.create_child()
        parser.current_instance.reference = parser.blackbox_holder.get_blackbox("definition_name")
        
        port_name = "port_name"
        
        tokens = [".", port_name, "(", ")"]

        tokenizer = self.TestTokenizer(tokens)

        parser.tokenizer = tokenizer

        parser.parse_port_map_single()

        assert len(parser.current_instance.reference.ports) == 1
        assert parser.current_instance.reference.ports[0].name == port_name
        assert len(parser.current_instance.reference.ports[0].pins) == 1

        assert tokenizer.has_next() == False

    def test_parse_parameter_map(self):
        parser = VerilogParser()
        tokens = ["#", "(", ".", "INIT", "(", "1'h123210", ")", ",", ".", "PARAM2", "(", "1'b0", ")", ")"]
        tokenizer = self.TestTokenizer(tokens)
        parser.tokenizer = tokenizer

        parser.current_definition = sdn.Definition()

        params = parser.parse_parameter_mapping()

        assert len(params.keys()) == 2
        assert params['INIT'] == "1'h123210"
        assert params["PARAM2"] == "1'b0"

    def test_parse_port_map(self):
        parser = VerilogParser()
        tokens = ["("]
        port_names = ["port1", "port2", "port3"]
        cable_names = ["cable1", "cable2", "cable3"]

        first = True
        for i in range(len(port_names)):
            if first:
                first = False
            else:
                tokens.append(",")
            tokens.append(".")
            tokens.append(port_names[i])
            tokens.append("(")
            tokens.append(cable_names[i])
            tokens.append(")")
        tokens.append(")")

        tokenizer = self.TestTokenizer(tokens)
        parser.tokenizer = tokenizer

        parser.current_definition = sdn.Definition()
        parser.current_instance = parser.current_definition.create_child()
        parser.current_instance.reference = parser.blackbox_holder.get_blackbox("definition1")

        parser.parse_port_mapping()

        assert len(parser.current_instance.reference.ports) == len(port_names)
        assert len(parser.current_instance.pins) == len(port_names)
        assert len(parser.current_definition.cables) == len(cable_names)
        for p in parser.current_instance.reference.ports:
            assert len(p.pins) == 1
        for c in parser.current_definition.cables:
            assert len(c.wires) ==1
        for i in range(len(port_names)):
            assert parser.current_definition.cables[i].name == cable_names[i]
            assert parser.current_instance.reference.ports[i].name == port_names[i]
            for p in parser.current_definition.cables[i].wires[0].pins:
                assert p in parser.current_instance.pins
            

    def test_parse_parameter_map_single(self):
        parser = VerilogParser()
        tokens = [".","INIT", "(", "1hABCD1230", ")"]
        tokenizer = self.TestTokenizer(tokens)
        parser.tokenizer = tokenizer

        k,v = parser.parse_parameter_map_single()

        assert k == "INIT"
        assert v == "1hABCD1230"
    

    def test_parse_parameter_map_single_multi_token_value(self):
        parser = VerilogParser()
        tokens = [".","INIT", "(", "200.000000", ")"]
        tokenizer = self.TestTokenizer(tokens)
        parser.tokenizer = tokenizer

        k,v = parser.parse_parameter_map_single()

        assert k == "INIT"
        assert v == "200.000000"
        assert parser.tokenizer.has_next() == False

    def test_parse_port_map_single(self):
        parser = VerilogParser()
        definition = sdn.Definition()
        parser.current_definition = definition
        parser.current_instance = definition.create_child()
        parser.current_instance.reference = parser.blackbox_holder.get_blackbox("definition_name")
        cable = definition.create_cable()
        cable_name = "cable_name"
        cable_width = 4
        port_name = "port_name"
        cable.name = cable_name
        cable.lower_index = 0
        cable.create_wires(cable_width)
        tokens = [".", port_name, "(", cable_name, "[", "3", ":", "0", "]", ")"]

        tokenizer = self.TestTokenizer(tokens)

        parser.tokenizer = tokenizer

        parser.parse_port_map_single()

        assert len(parser.current_instance.reference.ports) == 1
        assert parser.current_instance.reference.ports[0].name == port_name
        assert len(parser.current_instance.reference.ports[0].pins) == cable_width
        w_pins = []
        for w in cable.wires:
            assert w.pins[0] in parser.current_instance.pins
            w_pins.append(w.pins[0])
        for p in parser.current_instance.pins:
            assert p in w_pins

    ############################################################################
    ##Port creation and modification
    ############################################################################

    def init_port_creation(self):
        parser = VerilogParser()
        
        my_def = sdn.Definition()
        my_def.name = "testing_definition"
        c1 = my_def.create_port()
        c1.name = "preexisting1" #[15:8]
        c1.create_pins(8)
        c1.lower_index = 8
        c2 = my_def.create_port()
        c2.name = "preexisting2" #[15:0]
        c2.create_pins(16)
        c3 = my_def.create_port()
        c3.name = "preexisting3" #[19:16]
        c3.is_downto = False
        c3.lower_index = 16
        c3.create_pins(4)
        
        parser.current_definition = my_def

        return parser, c1, c2, c3

    def add_to_port_helper(self, tests, parser):
        #tests is a list of tuples that contain
        #name,left,right,direction,port,expected_lower,expected_width, expected_downto

        for entry in tests:
            name, left_index, right_index, direction, port, expected_lower, expected_width = entry
            expected_downto = port.is_downto #the port should not update it's downto once that has been decided.
            c = parser.create_or_update_port(name, left_index, right_index, direction)
            assert c is port, "the port is not the expected port, " + name
            assert len(c.pins) == expected_width, "the port is not the proper width, " + name
            assert c.lower_index == expected_lower, "the port does not have the proper lower index, " + name
            assert c.is_downto == expected_downto, "the port changed downto, " + name
            assert c.direction == direction, "the port is no longer "+ direction+ " it is now "+ c.direction+ " " + name


    def create_port_helper(self, tests, parser):
        #tests is a list of tuples that contain
        #name,left,right,direction,port,expected_lower,expected_width, expected_downto
        start_size = len(parser.current_definition.ports)
        count = 0
        for entry in tests:
            count += 1
            name, left_index, right_index, direction, port, expected_lower, expected_width, expected_downto = entry
            c = parser.create_or_update_port(name, left_index, right_index, direction)
            assert len(c.pins) == expected_width, "the port is not the proper width, " + name
            assert c.lower_index == expected_lower, "the port does not have the proper lower index, " + name
            assert c.is_downto == expected_downto
            assert c.direction == direction, "the port is no longer " + direction + " it is now " + c.direction+ " " + name
        assert len(parser.current_definition.ports) == count + start_size, "the wrong number of ports were added"


    def test_add_to_front_of_port(self):
        parser, c1, c2, c3 = self.init_port_creation()
        
        tests =\
            [("preexisting1", 15, 0, sdn.Port.Direction.IN, c1, 0, 16),\
            ("preexisting2", 0, -16, sdn.Port.Direction.OUT, c2, -16, 32),\
            ("preexisting3", 17, 0, sdn.Port.Direction.INOUT, c3, 0, 20)]
        self.add_to_port_helper(tests, parser)


    def test_add_to_back_of_port(self):
        parser, c1, c2, c3 = self.init_port_creation()
        
        tests =\
            [("preexisting1", 31, 16, sdn.Port.Direction.UNDEFINED, c1, 8, 24),\
            ("preexisting2", 31, 8, sdn.Port.Direction.IN, c2, 0, 32),\
            ("preexisting3", 63, 0, sdn.Port.Direction.OUT, c3, 0, 64)]
        self.add_to_port_helper(tests, parser)


    def test_create_port(self):
        parser, c1, c2, c3 = self.init_port_creation()
        
        tests =\
            [("new_port1", 31, 16, sdn.Port.Direction.IN, None, 16, 16, True),\
            ("new_port2", 0, -7, sdn.Port.Direction.INOUT, None, -7, 8, True),\
            ("new_port3", 63, 0, sdn.Port.Direction.UNDEFINED, None, 0, 64, True)]
        self.create_port_helper(tests, parser)


    def test_create_port_downto(self):
        parser, c1, c2, c3 = self.init_port_creation()
        
        tests =\
            [("new_port1", 7, 0, sdn.Port.Direction.OUT, None, 0, 8, True),\
            ("new_port2", 0, 7, sdn.Port.Direction.INOUT, None, 0, 8, False)]
        self.create_port_helper(tests, parser)

    def test_change_port_direction(self):
        pass #TODO not sure yet how I should deal with this.

    def test_dont_change_port(self):
        parser, c1, c2, c3 = self.init_port_creation()
        
        tests =\
            [("preexisting1", 15, 8, sdn.Port.Direction.OUT, c1, 8, 8),\
            ("preexisting2", 15, 0, sdn.Port.Direction.IN, c2, 0, 16),\
            ("preexisting3", 19, 16, sdn.Port.Direction.INOUT, c3, 16, 4)]
        self.add_to_port_helper(tests, parser)

    def test_single_index_port(self):
        parser, c1, c2, c3 = self.init_port_creation()
        tests_create =\
            [("new_port1", 31, None, sdn.Port.Direction.OUT, None, 31, 1, True),\
            ("new_port2", 0, None, sdn.Port.Direction.UNDEFINED, None, 0, 1, True),\
            ("new_port3", 63, None, sdn.Port.Direction.IN, None, 63, 1, True)]
        self.create_port_helper(tests_create, parser)

        parser, c1, c2, c3 = self.init_port_creation()
        tests_modify =\
            [("preexisting1", 0, None, sdn.Port.Direction.INOUT, c1, 0, 16),\
            ("preexisting2", 8, None, sdn.Port.Direction.OUT, c2, 0, 16),\
            ("preexisting3", 0, None, sdn.Port.Direction.IN, c3, 0, 20)]
        self.add_to_port_helper(tests_modify, parser)


    def test_change_port_downto(self):
        #i don't think the port downto-ness should ever change. this is tested in the add to port helper
        parser, c1, c2, c3 = self.init_port_creation()
        
        tests =\
            [("preexisting1", 15, 8, sdn.Port.Direction.UNDEFINED, c1, 8, 8),\
            ("preexisting1", 8, 15, sdn.Port.Direction.UNDEFINED, c1, 8, 8)]
        self.add_to_port_helper(tests, parser)

    def test_port_prepend_pins(self):
        parser, c1, c2, c3 = self.init_port_creation()
        c1_width = len(c1.pins)
        c1_lower = c1.lower_index
        c1_pins = set()
        for pin in c1.pins:
            c1_pins.add(pin)
        c2_width = len(c2.pins)
        c2_lower = c2.lower_index
        c2_pins = set()
        for pin in c2.pins:
            c2_pins.add(pin)
        c3_width = len(c3.pins)
        c3_lower = c3.lower_index
        c3_pins = set()
        for pin in c3.pins:
            c3_pins.add(pin)

        print(c1_pins)
        print()
        
        prepend_count = 8

        parser.prepend_pins(c1, prepend_count)
        print(c1_pins)
        print()
        print(c1.pins)
        print()
        assert len(c1.pins) == prepend_count + c1_width, "tried to add 8 pins to c1"
        assert c1.lower_index == c1_lower - prepend_count
        for pin in c1.pins[:prepend_count]:
            assert pin not in c1_pins, "a pin was in the wrong location for the prepend"
        for pin in c1.pins[prepend_count:]:
            assert pin in c1_pins, "a pin seems to have disappeared"

        parser.prepend_pins(c2, prepend_count)
        assert len(c2.pins) == prepend_count + c2_width, "tried to add 8 pins to c2"
        assert c2.lower_index == c2_lower - prepend_count
        for pin in c2.pins[:prepend_count]:
            assert pin not in c2_pins, "a pin was in the wrong location for the prepend"
        for pin in c2.pins[prepend_count:]:
            assert pin in c2_pins, "a pin seems to have disappeared"

        parser.prepend_pins(c3, prepend_count)
        assert len(c3.pins) == prepend_count + c3_width, "tried to add 8 pins to c3"
        assert c3.lower_index == c3_lower - prepend_count
        for pin in c3.pins[:prepend_count]:
            assert pin not in c3_pins, "a pin was in the wrong location for the prepend"
        for pin in c3.pins[prepend_count:]:
            assert pin in c3_pins, "a pin seems to have disappeared"

    def test_port_postpend_pins(self):
        parser, c1, c2, c3 = self.init_port_creation()
        c1_width = len(c1.pins)
        c1_lower = c1.lower_index
        c1_pins = set()
        for pin in c1.pins:
            c1_pins.add(pin)
        c2_width = len(c2.pins)
        c2_lower = c2.lower_index
        c2_pins = set()
        for pin in c2.pins:
            c2_pins.add(pin)
        c3_width = len(c3.pins)
        c3_lower = c3.lower_index
        c3_pins = set()
        for pin in c3.pins:
            c3_pins.add(pin)
        
        postpend_count = 8

        parser.postpend_pins(c1, postpend_count)
        assert len(c1.pins) == postpend_count + c1_width, "tried to add 8 pins to c1"
        assert c1.lower_index == c1_lower
        for pin in c1.pins[c1_width:]:
            assert pin not in c1_pins, "a pin was in the wrong location for the postpend"
        for pin in c1.pins[:c1_width]:
            assert pin in c1_pins, "a pin seems to have disappeared"

        parser.postpend_pins(c2, postpend_count)
        assert len(c2.pins) == postpend_count + c2_width, "tried to add 8 pins to c2"
        assert c2.lower_index == c2_lower
        for pin in c2.pins[c2_width:]:
            assert pin not in c2_pins, "a pin was in the wrong location for the postpend"
        for pin in c2.pins[:c2_width]:
            assert pin in c2_pins, "a pin seems to have disappeared"

        parser.postpend_pins(c3, postpend_count)
        assert len(c3.pins) == postpend_count + c3_width, "tried to add 8 pins to c3"
        assert c3.lower_index == c3_lower
        for pin in c3.pins[c3_width:]:
            assert pin not in c3_pins, "a pin was in the wrong location for the postpend"
        for pin in c3.pins[:c3_width]:
            assert pin in c3_pins, "a pin seems to have disappeared"

    def test_populate_new_port(self):
        parser = VerilogParser()
        
        test_data = [("test_name", 2, 0, sdn.Port.Direction.IN), ("\\escaped#$@_[213] ", 15,8, sdn.Port.Direction.OUT), ("some_name", 7,4,sdn.Port.Direction.INOUT)]

        for name, left, right, direction in test_data:
            port = sdn.Port()
            parser.populate_new_port(port,name,left,right,direction)
            assert port.name == name
            assert port.is_downto == (left >= right)
            assert port.direction == direction
            assert port.lower_index == min(left,right)

    def test_parse_port_declaration(self):
        parser = VerilogParser()
        count = 3
        names = ["i", "o", "io"]
        token_list = ["input", names[0], ";", "output", "[", "3", ":", "0", "]", names[1], ";", "inout", "wire", names[2], ";"]
        tokenizer = self.TestTokenizer(token_list)
        parser.tokenizer = tokenizer
        d = sdn.Definition()
        
        parser.current_definition = d

        for n in names:
            p = parser.create_or_update_port(n)
            c = parser.create_or_update_cable(n)
            c.wires[0].connect_pin(p.pins[0])

        for _ in range(count):
            parser.parse_port_declaration(dict())


    @unittest.expectedFailure
    def test_parse_port_declaration_failure(self):
        parser = VerilogParser()
        count = 3
        names = ["i", "o", "io"]
        token_list = ["input", names[0], ";", "output", "[", "3", ":", "0", "]", names[1], ";", "inout", "wire", names[2], ";"]
        tokenizer = self.TestTokenizer(token_list)
        parser.tokenizer = tokenizer
        d = sdn.Definition()
        
        parser.current_definition = d

        for n in names:
            parser.create_or_update_port(n)

        #the ports are in the definition but not connected this should fail

        for _ in range(count):
            parser.parse_port_declaration(properties = dict())

    def test_create_or_update_port_on_instance(self):
        parser = VerilogParser()
        parser.current_definition = sdn.Definition()
        parser.current_instance = parser.current_definition.create_child()
        parser.current_instance.reference = parser.blackbox_holder.get_blackbox("definition1")

        pins = parser.create_or_update_port_on_instance("port1", 1)

        assert parser.current_instance.reference.ports[0].name == "port1"
        assert len(parser.current_instance.reference.ports[0].pins) == 1
        assert len(parser.current_instance.pins) == 1
        assert len(pins) == 1

    ############################################
    ##assignment tests
    ############################################

    def test_create_new_assignment_instance(self):
        '''make sure the name, and width make sense
        also take advantage of the setup to make sure the definition returned is the same for the same width'''
        parser = VerilogParser()
        parser.netlist = sdn.Netlist()
        parser.current_definition = sdn.Definition()
        width = 4
        instance = parser.create_assignment_instance(width)
        assert len(instance.pins) == width * 2
        assert instance.name == "SDN_VERILOG_ASSIGNMENT_" + str(width) + "_" + str(0)
        assert instance.reference == parser.get_assignment_definition(width)

    def test_create_new_assignment_definition(self):
        '''make sure the names, width and acutal connectivity make sense'''
        parser = VerilogParser()
        parser.netlist = sdn.Netlist()
        parser.current_definition = sdn.Definition()
        width = 4
        definition = parser.get_assignment_definition(width)
        assert definition.name == "SDN_VERILOG_ASSIGNMENT_" + str(width)
        assert len(definition.ports) == 2
        assert len(definition.ports[0].pins) == width
        assert len(definition.ports[1].pins) == width
        assert len(definition.cables) == 1
        for i in range(width):
            assert definition.ports[0].pins[i] in definition.cables[0].wires[i].pins
            assert definition.ports[1].pins[i] in definition.cables[0].wires[i].pins


    def test_connect_assigned_wires(self):
        '''make sure the wires are actually connected to the instance and that the connectivity makes sense'''
        parser = VerilogParser()
        parser.netlist = sdn.Netlist()
        parser.current_definition = sdn.Definition()
        o_cable = parser.current_definition.create_cable(name = "c1")
        i_cable = parser.current_definition.create_cable(name = "c2")
        o_cable.create_wires(4)
        i_cable.create_wires(4)
        parser.connect_wires_for_assign(o_cable, 1, 0, i_cable, 3, 2)


    def test_names_of_instances_are_different(self):
        '''make sure the names of multiple instances of the same width are different'''
        parser = VerilogParser()
        parser.netlist = sdn.Netlist()
        parser.current_definition = sdn.Definition()
        width = 4
        inst1 = parser.create_assignment_instance(width)
        inst2 = parser.create_assignment_instance(width)
        assert inst1.name == "SDN_VERILOG_ASSIGNMENT_" + str(width) + "_" + str(0)
        assert inst2.name == "SDN_VERILOG_ASSIGNMENT_" + str(width) + "_" + str(1)

    def test_parse_assign(self):
        parser = VerilogParser()
        parser.netlist = sdn.Netlist()
        parser.current_definition = sdn.Definition()
        tokens = ["assign", "cable1", "=", "cable2", ";", "assign", "SR2", "[", "2", "]", "=", "\\<const0> ", ";"]
        tokenizer = self.TestTokenizer(tokens)
        parser.tokenizer = tokenizer
        c1, o_left, o_right, c2, i_left, i_right = parser.parse_assign()
        assert c1.name == "cable1"
        assert c2.name == "cable2"
        assert o_left == None
        assert o_right == None
        assert i_left == None
        assert i_right == None
        c1, o_left, o_right, c2, i_left, i_right = parser.parse_assign()
        assert c1.name == "SR2"
        assert c2.name == "\\<const0> "
        assert o_left == 2
        assert o_right == None
        assert i_left == None
        assert i_right == None

    ############################################
    ##Parse star parameters
    ############################################
    
    def test_parse_star_with_value(self):
        tokens = ['(', '*', 'key', '=', 'value', '*', ')']
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        
        stars = parser.parse_star_property()
        for k,v in stars.items():
            assert k == "key"
            assert v == "value"

    def test_parser_star_without_value(self):
        tokens = ['(', '*', 'key', '*', ')']
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        
        stars = parser.parse_star_property()
        for k,v in stars.items():
            assert k == "key"
            assert v is None

    def test_parser_star_list(self):
        '''example taken from a file that is not in our support files.
        the construct in question is referenced in xilinx documentation
        (* KEEP, DONT_TOUCH, BEL = "C6LUT" *)
        additionally:
        (*BEL="H6LUT",RLOC="X0Y0"*)
        and I presume that:
        (* KEEP, DONT_TOUCH *)
        would all be valid
        ''' 
        tokens = ["(", "*", "KEEP", ",", "DONT_TOUCH", ",", "BEL", "=", '"C6LUT"', "*", ")",\
            "(", "*", "BEL", "=", '"H6LUT"', ",", "RLOC", "=", '"X0Y0"', "*", ")",\
            "(", "*", "KEEP", ",", "DONT_TOUCH", "*", ")"]
        
        tokenizer = self.TestTokenizer(tokens)
        parser = VerilogParser()
        parser.tokenizer = tokenizer
        
        stars0 = parser.parse_star_property()
        stars1 = parser.parse_star_property()
        stars2 = parser.parse_star_property()

        assert "KEEP" in stars0
        assert stars0["KEEP"] == None
        assert "DONT_TOUCH" in stars0
        assert stars0["DONT_TOUCH"] == None
        assert "BEL" in stars0
        assert stars0["BEL"] == '"C6LUT"'

        assert "BEL" in stars1
        assert stars1["BEL"] == '"H6LUT"'
        assert "RLOC" in stars1
        assert stars1["RLOC"] == '"X0Y0"'

        assert "KEEP" in stars2
        assert stars2["KEEP"] == None
        assert "DONT_TOUCH" in stars2
        assert stars2["DONT_TOUCH"] == None
        


    ############################################
    ##test helpers
    ############################################

    def test_get_all_ports_from_wires(self):
        port1 = sdn.Port()
        port2 = sdn.Port()
        port1.create_pin()
        port2.create_pin()

        wire1 = sdn.Wire()
        wire2 = sdn.Wire()
        wire3 = sdn.Wire()

        wire1.connect_pin(port1.pins[0])
        wire2.connect_pin(port2.pins[0])

        groups = [[wire1, wire2, wire3], [wire1, wire2], [wire1], [wire3]]
        expected_results = [[port1, port2], [port1, port2], [port1], []]
        
        parser = VerilogParser()

        for i in range(len(groups)):
            g = groups[i]
            actual_results = parser.get_all_ports_from_wires(g)
            for r in actual_results:
                assert r in expected_results[i]
            for r in expected_results[i]:
                assert r in actual_results
        

    def test_get_wires_from_cable_helper(self):

        parser = VerilogParser()

        cable1 = sdn.Cable()
        cable1.create_wires(8)
        cable1.lower_index = 8

        cable2 = sdn.Cable()
        cable2.create_wires(8)
        cable2.lower_index = 0

        #add the cable.lower_index to all tests

        tests = [(7,0), (0, None), (0,0), (1,None), (2,4)]
        e11 = []
        e21 = []
        for i in reversed(range(0,8)):
            e11.append(cable1.wires[i])
            e21.append(cable2.wires[i])

        expected1 = [e11, [cable1.wires[0]], [cable1.wires[0]], [cable1.wires[1]], cable1.wires[2:5]]
        expected2 = [e21, [cable2.wires[0]], [cable2.wires[0]], [cable2.wires[1]], cable2.wires[2:5]]

        for i in range(len(tests)):
            left1 = tests[i][0] + cable1.lower_index
            if tests[i][1] != None:
                right1 = tests[i][1] + cable1.lower_index
            else:
                right1 = None
            left2 = tests[i][0] + cable2.lower_index
            if tests[i][1] != None:
                right2 = tests[i][1] + cable2.lower_index
            else:
                right2 = None
            wires1 = parser.get_wires_from_cable(cable1, left1, right1)
            wires2 = parser.get_wires_from_cable(cable2, left2, right2)

            for j in range(len(expected1[i])):
                w11 = wires1[j]
                w12 = expected1[i][j]
                assert w11 == w12, "the wires are not the same or not in the same order."
                w21 = wires2[j]
                w22 = expected2[i][j]
                assert w21 == w22, "the wires are not the same or not in the same order"



if __name__ == '__main__':
    unittest.main()
