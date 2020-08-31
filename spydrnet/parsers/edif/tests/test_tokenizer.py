import unittest
import os
import io
import zipfile
import tempfile

from spydrnet.parsers.edif.tokenizer import EdifTokenizer
from spydrnet import base_dir

class TestEdifTokenizer(unittest.TestCase):
    def test_no_constructor_of_zero_argument(self):
        self.assertRaises(TypeError, EdifTokenizer)

    def test_stream(self):
        dir_of_edif_netlists = os.path.join(base_dir, "support_files", "EDIF_netlists")
        test_file = os.path.join(dir_of_edif_netlists, "n_bit_counter.edf.zip")
        zip = zipfile.ZipFile(test_file)
        file_name = os.path.basename(test_file)
        file_name = file_name[:file_name.rindex(".")]
        stream = zip.open(file_name)
        stream = io.TextIOWrapper(stream)
        tokenizer = EdifTokenizer.from_stream(stream)
        next_token = tokenizer.next()
        self.assertEqual("(", next_token)

    def test_open_zip_file(self):
        dir_of_edif_netlists = os.path.join(base_dir, "support_files", "EDIF_netlists")
        test_file = os.path.join(dir_of_edif_netlists, "n_bit_counter.edf.zip")
        tokenizer = EdifTokenizer.from_filename(test_file)
        next_token = tokenizer.next()
        self.assertEqual("(", next_token)

    def test_open_file(self):
        dir_of_edif_netlists = os.path.join(base_dir, "support_files", "EDIF_netlists")
        test_file = os.path.join(dir_of_edif_netlists, "n_bit_counter.edf.zip")
        file_name = os.path.basename(test_file)
        file_name = file_name[:file_name.rindex(".")]
        zip = zipfile.ZipFile(test_file)
        with tempfile.TemporaryDirectory() as tempdir:
            zip.extract(file_name, tempdir)
            extract_path = os.path.join(tempdir, file_name)
            tokenizer = EdifTokenizer.from_filename(extract_path)
            next_token = tokenizer.next()
            self.assertEqual("(", next_token)
            tokenizer.close()

    def test_empty_string(self):
        tokenizer = EdifTokenizer.from_string("")
        self.assertRaises(StopIteration, tokenizer.next)

    def test_has_next_false(self):
        tokenizer = EdifTokenizer.from_string("")
        self.assertFalse(tokenizer.has_next())

    def test_has_next_true(self):
        tokenizer = EdifTokenizer.from_string("(")
        self.assertTrue(tokenizer.has_next())

    def test_paren_with_whitespace(self):
        tokenizer = EdifTokenizer.from_string(" \t\n\r( \r\n\t )\n\r \t")
        self.assertEqual("(", tokenizer.next())
        self.assertEqual(2, tokenizer.line_number)
        self.assertEqual(")", tokenizer.next())
        self.assertEqual(3, tokenizer.line_number)
        self.assertRaises(StopIteration, tokenizer.next)

    def test_string_token(self):
        test_string = "\"This is a test string in EDIF\""
        tokenizer = EdifTokenizer.from_string(test_string)
        next_token = tokenizer.next()
        self.assertEqual(test_string, next_token)
        self.assertRaises(StopIteration, tokenizer.next)

    def test_multiline_string(self):
        test_string = "\"This is a test string in EDIF\n with a new line in it.\""
        tokenizer = EdifTokenizer.from_string(test_string)
        next_token = tokenizer.next()
        self.assertEqual(test_string.replace("\n", ""), next_token)
        self.assertRaises(StopIteration, tokenizer.next)
    
    def test_peek_and_token_equals(self):
        test_id = "VALID_EDIF_ID"
        tokenizer = EdifTokenizer.from_string(test_id)
        self.assertTrue(tokenizer.has_next())
        self.assertFalse(tokenizer.peek_equals("DIFFERENT_TOKEN"))
        self.assertTrue(tokenizer.peek_equals("valid_edif_id"))
        self.assertTrue(tokenizer.peek_equals("vAlId_eDIf_ID"))
        self.assertTrue(tokenizer.peek_equals(test_id))
        tokenizer.next()
        self.assertFalse(tokenizer.token_equals("DIFFERENT_TOKEN"))
        self.assertTrue(tokenizer.token_equals("valid_edif_id"))
        self.assertTrue(tokenizer.token_equals("vAlId_eDIf_ID"))
        self.assertTrue(tokenizer.token_equals(test_id))


class TestTokenTypes(unittest.TestCase):

    def test_edif_identifier(self):
        valid_ids = "&test a a9 a_ Alpha_Numeric_0123456789 &"
        tokenizer = EdifTokenizer.from_string(valid_ids)
        while tokenizer.has_next():
            tokenizer.next()
            self.assertTrue(tokenizer.is_valid_identifier(), tokenizer.token)

        invalid_ids = "_ _idenitier_ 9alkjf too_long" + "0"*(256 - 7)
        tokenizer = EdifTokenizer.from_string(invalid_ids)
        while tokenizer.has_next():
            tokenizer.next()
            self.assertFalse(tokenizer.is_valid_identifier(), tokenizer.token)

        #TODO Special characters are weird. We should check them out.
