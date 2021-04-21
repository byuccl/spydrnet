import unittest

from spydrnet.parsers.verilog.tokenizer import *
import spydrnet as sdn


class TestVerilogTokenizer(unittest.TestCase):
    pass

    def test_against_4bit_adder(self):
        directory = os.path.join(sdn.base_dir, "support_files", "verilog_netlists", "4bitadder.v.zip")
        tokenizer = VerilogTokenizer.from_filename(directory)
        while(tokenizer.has_next()):
            #print(tokenizer.next())
            tokenizer.next()

    def test_basic(self):
        string = "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20"
        for i in range(2):
            tokenizer = VerilogTokenizer.from_string(string)
            assert(tokenizer.has_next())
            assert(tokenizer.next() == "1")
            assert(tokenizer.peek() == "2")
            assert(tokenizer.next() == "2")
            for i in range(10):
                tokenizer.next()
            assert(tokenizer.peek() == "13")
            assert(tokenizer.next() == "13")
            for i in range(5):
                tokenizer.next()
            assert(tokenizer.next() == "19")
            assert(tokenizer.has_next())
            assert(tokenizer.next() == "20")
            assert(not tokenizer.has_next())
            string += "\n"


