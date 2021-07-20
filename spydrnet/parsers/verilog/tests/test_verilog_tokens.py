import unittest

import spydrnet.parsers.verilog.verilog_tokens as vt
import spydrnet as sdn


class TestVerilogTokens(unittest.TestCase):


    def test_valid_identifier(self):
        identifiers = ["valid", "_valid", "\\^[0]should_be_valid ", "_1293i123"]
        for i in identifiers:
            assert vt.is_valid_identifier(i)

    def test_invalid_identifier(self):
        identifiers = ["not valid", "6invalid" "^[0]no_escape...", "\\space in escaped ", "", "!"]
        for i in identifiers:
            assert not vt.is_valid_identifier(i)

    def test_valid_number(self):
        numbers = ["123465789", "000000123", "0"]
        for n in numbers:
            assert vt.is_numeric(n)

    def test_invalid_number(self):
        #we could change this so that a decimal point is still a valid number if needed.
        numbers = ["123123.12903", "\\*#@(&$#@*$", "123 3901", ""]
        for n in numbers:
            assert not vt.is_numeric(n)

    def test_convert_string_to_direction(self):
        strings = ["input", "output", "inout", "unknown"]
        values = [sdn.Port.Direction.IN, sdn.Port.Direction.OUT, sdn.Port.Direction.INOUT, sdn.Port.Direction.UNDEFINED]
        for i in range(len(strings)):
            assert vt.string_to_port_direction(strings[i]) == values[i]