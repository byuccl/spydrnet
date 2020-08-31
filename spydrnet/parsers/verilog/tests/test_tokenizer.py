import unittest

from spydrnet.parsers.verilog.tokenizer import *


class TestVerilogTokenizer(unittest.TestCase):

# <<<<<<< HEAD
    # def test_empty_string(self):
    #     tokenizer = VerilogTokenizer.from_string("")
    #     self.assertRaises(StopIteration, tokenizer.next)

    # def test_module_with_whitespace(self):
    #     tokenizer = VerilogTokenizer.from_string(" \t\nmodule \n\t endmodule\n \t")
    #     token = tokenizer.next()
    #     self.assertEqual("module", token.value)
    #     token = tokenizer.next()
    #     self.assertEqual("endmodule", token.value)
    #     token = tokenizer.next()
    #     self.assertEqual(None, token)
    #     self.assertRaises(StopIteration, tokenizer.next)

    # def test_peek(self):
    #     tokenizer = VerilogTokenizer.from_string('module endmodule')
    #     self.assertEqual(tokenizer.peek().value, 'module')
    #     tokenizer.next()
    #     self.assertEqual(tokenizer.peek().value, 'endmodule')
    #     tokenizer.next()
    #     self.assertTrue(tokenizer.peek() is None)

    # def test_line_numbering(self):
    #     tokenizer = VerilogTokenizer.from_string('module\n\n\ninput\n\n\n\n\noutput\n\nwire\n\n\nendmodule')
    #     self.assertEqual(tokenizer.next().lineno, 1)
    #     self.assertEqual(tokenizer.next().lineno, 4)
    #     self.assertEqual(tokenizer.next().lineno, 9)
    #     self.assertEqual(tokenizer.next().lineno, 11)
    #     self.assertEqual(tokenizer.next().lineno, 14)

    # def test_single_line_comment(self):
    #     tokenizer = VerilogTokenizer.from_string('module\n//This is a comment\nendmoudle')
    #     self.assertEqual(tokenizer.next().value, 'module')
    #     self.assertEqual(tokenizer.next().value, 'endmoudle')

    # def test_block_comment(self):
    #     tokenizer = VerilogTokenizer.from_string('module\n/*This is a\nblock comment*/\nendmoudle')
    #     self.assertEqual(tokenizer.next().value, 'module')
    #     self.assertEqual(tokenizer.next().value, 'endmoudle')

    # def test_embedded_block_comment(self):
    #     tokenizer = VerilogTokenizer.from_string('module/*This is an embedded block comment*/endmoudle')
    #     self.assertEqual(tokenizer.next().value, 'module')
    #     self.assertEqual(tokenizer.next().value, 'endmoudle')

    # def test_binary_number(self):
    #     tokenizer = VerilogTokenizer.from_string('4\'b1010\n16\'b1010001111110001')
    #     self.assertEqual(tokenizer.next().value, '4\'b1010')
    #     self.assertEqual(tokenizer.next().value, '16\'b1010001111110001')

    # def test_hex_number(self):
    #     tokenizer = VerilogTokenizer.from_string('4\'h1\n24\'habcdef\n24\'hABCDEF\n24\'hAbCdEf')
    #     self.assertEqual(tokenizer.next().value, '4\'h1')
    #     self.assertEqual(tokenizer.next().value, '24\'habcdef')
    #     self.assertEqual(tokenizer.next().value, '24\'hABCDEF')
    #     self.assertEqual(tokenizer.next().value, '24\'hAbCdEf')

    # def test_decimal_number(self):
    #     tokenizer = VerilogTokenizer.from_string('4\'d5\n16\'d765')
    #     self.assertEqual(tokenizer.next().value, '4\'d5')
    #     self.assertEqual(tokenizer.next().value, '16\'d765')

    # def test_number(self):
    #     tokenizer = VerilogTokenizer.from_string('56\n27\n789456123')
    #     self.assertEqual(tokenizer.next().value, '56')
    #     self.assertEqual(tokenizer.next().value, '27')
    #     self.assertEqual(tokenizer.next().value, '789456123')

    # def test_string(self):
    #     tokenizer = VerilogTokenizer.from_string('"This is a correct string"')
    #     self.assertEqual(tokenizer.next().type, 'STRING')
    #     tokenizer = VerilogTokenizer.from_string('"This is a \nillegal string"')
    #     self.assertRaises(UnsupportedTokenException, tokenizer.next)
    def test_against_4bit_adder(self):
        tokenizer = VerilogTokenizer.from_filename("./spydrnet/support_files/verilog_netlists/4bitadder.v")
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

# if __name__ == '__main__':
#     unittest.main()
# =======
#     def test_empty_string(self):
#         tokenizer = verilogTokenizer.from_string("")
#         self.assertRaises(StopIteration, tokenizer.next)

#     def test_module_with_whitespace(self):
#         tokenizer = verilogTokenizer.from_string(" \t\nmodule \n\t endmodule\n \t")
#         token = tokenizer.next()
#         self.assertEqual("module", token.value)
#         token = tokenizer.next()
#         self.assertEqual("endmodule", token.value)
#         token = tokenizer.next()
#         self.assertEqual(None, token)
#         self.assertRaises(StopIteration, tokenizer.next)

#     def test_peek(self):
#         tokenizer = verilogTokenizer.from_string('module endmodule')
#         self.assertEqual(tokenizer.peek().value, 'module')
#         tokenizer.next()
#         self.assertEqual(tokenizer.peek().value, 'endmodule')
#         tokenizer.next()
#         self.assertTrue(tokenizer.peek() is None)

#     def test_line_numbering(self):
#         tokenizer = verilogTokenizer.from_string('module\n\n\ninput\n\n\n\n\noutput\n\nwire\n\n\nendmodule')
#         self.assertEqual(tokenizer.next().lineno, 1)
#         self.assertEqual(tokenizer.next().lineno, 4)
#         self.assertEqual(tokenizer.next().lineno, 9)
#         self.assertEqual(tokenizer.next().lineno, 11)
#         self.assertEqual(tokenizer.next().lineno, 14)

#     def test_single_line_comment(self):
#         tokenizer = verilogTokenizer.from_string('module\n//This is a comment\nendmoudle')
#         self.assertEqual(tokenizer.next().value, 'module')
#         self.assertEqual(tokenizer.next().value, 'endmoudle')

#     def test_block_comment(self):
#         tokenizer = verilogTokenizer.from_string('module\n/*This is a\nblock comment*/\nendmoudle')
#         self.assertEqual(tokenizer.next().value, 'module')
#         self.assertEqual(tokenizer.next().value, 'endmoudle')

#     def test_embedded_block_comment(self):
#         tokenizer = verilogTokenizer.from_string('module/*This is an embedded block comment*/endmoudle')
#         self.assertEqual(tokenizer.next().value, 'module')
#         self.assertEqual(tokenizer.next().value, 'endmoudle')

#     def test_binary_number(self):
#         tokenizer = verilogTokenizer.from_string('4\'b1010\n16\'b1010001111110001')
#         self.assertEqual(tokenizer.next().value, '4\'b1010')
#         self.assertEqual(tokenizer.next().value, '16\'b1010001111110001')

#     def test_hex_number(self):
#         tokenizer = verilogTokenizer.from_string('4\'h1\n24\'habcdef\n24\'hABCDEF\n24\'hAbCdEf')
#         self.assertEqual(tokenizer.next().value, '4\'h1')
#         self.assertEqual(tokenizer.next().value, '24\'habcdef')
#         self.assertEqual(tokenizer.next().value, '24\'hABCDEF')
#         self.assertEqual(tokenizer.next().value, '24\'hAbCdEf')

#     def test_decimal_number(self):
#         tokenizer = verilogTokenizer.from_string('4\'d5\n16\'d765')
#         self.assertEqual(tokenizer.next().value, '4\'d5')
#         self.assertEqual(tokenizer.next().value, '16\'d765')

#     def test_number(self):
#         tokenizer = verilogTokenizer.from_string('56\n27\n789456123')
#         self.assertEqual(tokenizer.next().value, '56')
#         self.assertEqual(tokenizer.next().value, '27')
#         self.assertEqual(tokenizer.next().value, '789456123')

#     def test_string(self):
#         tokenizer = verilogTokenizer.from_string('"This is a correct string"')
#         self.assertEqual(tokenizer.next().type, 'STRING')
#         tokenizer = verilogTokenizer.from_string('"This is a \nillegal string"')
#         self.assertRaises(UnsupportedTokenException, tokenizer.next)
# >>>>>>> master
