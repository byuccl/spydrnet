# Copyright 2021 please see the license
# Author Dallin Skouson

from functools import partial
import re
import zipfile
import io
import os
import spydrnet.parsers.verilog.verilog_tokens as vt
from spydrnet.parsers.verilog.verilog_token_factory import TokenFactory


class VerilogTokenizer:
    @staticmethod
    def from_stream(stream):
        tokenizer = VerilogTokenizer(stream)
        return tokenizer

    @staticmethod
    def from_string(string):
        string_stream = io.StringIO(string)
        tokenizer = VerilogTokenizer(string_stream)
        return tokenizer

    @staticmethod
    def from_filename(filename):
        tokenizer = VerilogTokenizer(filename)
        return tokenizer

    def __init__(self, input_source):
        self.token = None
        self.next_token = None
        self.line_number = 0

        if isinstance(input_source, str):
            if zipfile.is_zipfile(input_source):
                zip = zipfile.ZipFile(input_source)
                filename = os.path.basename(input_source)
                filename = filename[:filename.rindex(".")]
                stream = zip.open(filename)
                stream = io.TextIOWrapper(stream)
                self.input_stream = stream
            else:
                self.input_stream = open(input_source, 'r')
        else:
            if isinstance(input_source, io.TextIOBase) is False:
                self.input_stream = io.TextIOWrapper(input_source)
            else:
                self.input_stream = input_source

        self.generator = self.generate_tokens()

    def __del__(self):
        if hasattr(self, "input_stream"):
            self.close()

    def has_next(self):
        try:
            self.peek()
            return True
        except StopIteration:
            return False

    def next(self):
        if self.next_token is not None:
            self.token = self.next_token
            self.next_token = None
        else:
            self.token = next(self.generator)
        return self.token

    def peek(self):
        if self.next_token is not None:
            return self.next_token
        else:
            token = next(self.generator)
            while len(token) >= 2 and (token[0:2] == vt.OPEN_LINE_COMMENT
                                       or token[0:2] == vt.OPEN_BLOCK_COMMENT):
                token = next(self.generator)
            self.next_token = token
            return self.next_token

    def generate_tokens(self):
        '''give independent tokens from the token factory'''

        try:
            self.line_number = 1
            tf = TokenFactory()
            for buffer in iter(partial(self.input_stream.read, 32768), ""):
                for ch in buffer:
                    if ch == vt.NEW_LINE:
                        self.line_number += 1
                    result = tf.add_character(ch)
                    if result is not None:
                        yield result
        finally:
            self.input_stream.close()

        # if the input doesn't end in white space there will be one token left in the token factory try and get it.

        result = tf.flush()
        if result != None:
            yield result

    def close(self):
        if self.input_stream:
            self.input_stream.close()
