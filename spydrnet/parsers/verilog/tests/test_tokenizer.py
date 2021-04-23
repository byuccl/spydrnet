import unittest

from spydrnet.parsers.verilog.tokenizer import *
import spydrnet as sdn


class TestVerilogTokenizer(unittest.TestCase):


    def test_against_4bit_adder(self):
        directory = os.path.join(sdn.base_dir, "support_files", "verilog_netlists", "4bitadder.v.zip")
        tokenizer = VerilogTokenizer.from_filename(directory)
        while(tokenizer.has_next()):
            #print(tokenizer.next())
            tokenizer.next()

    def test_spaces(self):
        tokenizer = VerilogTokenizer.from_string("wire temp = 1'b1; if something == some2")
        while(tokenizer.has_next()):
            #print(tokenizer.next())
            tokenizer.next()
        tokenizer = VerilogTokenizer.from_string("wire temp=1'b1 ;if something==some2")
        while(tokenizer.has_next()):
            #print(tokenizer.next())
            tokenizer.next()