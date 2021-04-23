# Copyright 2020 please see the license
# Author Dallin Skouson

from functools import partial
import re
import zipfile
import io
import os


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
        self.to_next_whitespace = False

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
        # lets skip the comments
        run = True
        celldef = False
        while run:
            if self.next_token:
                self.token = self.next_token
                self.next_token = None
                #print("Tokenizer: next already here")
            else:
                self.token = next(self.generator)
                #print("Tokenizer: next not here")
            if self.token[:2] == "//":
                continue
            if not celldef:
                run = False
            if self.token == "`ifdef":
                run = True
                celldef = True
            if celldef and self.token == "`endif":
                celldef = False
            #print("looping", self.token)
        return self.token

    # def next_to_whitespace_depricated(self):
    #     if self.next_token:
    #         print("CAN'T PEEK BEFORE GETTING NEXT WHITESPACE")
    #     self.to_next_whitespace = True
    #     self.next()
    #     self.to_next_whitespace = False
    #     print("whitespace: ", self.token)
    #     return self.token

# def t_MODULE(t):
#     # r'[a-zA-Z]([a-zA-Z0-9]|_|\[[0-9]*\])'
#     r'module'
#     # t.lexer.begin('modulename')
#     return t

    def peek(self):
        #print("Tokenizer: peeked")
        if self.next_token:
            return self.next_token
        else:
            self.next_token = next(self.generator)
            return self.next_token

    def generate_tokens(self):
        try:
            self.line_number = 1
            in_quote = False
            in_ml_comment = False
            in_sl_comment = False
            comment_start = False
            comment_end = False
            escaped = False

            token_buffer = list()
            for buffer in iter(partial(self.input_stream.read, 32768), ""):
                for ch in buffer:
                    if ch == '\n':
                        self.line_number += 1
                    if comment_start:
                        if (ch == '*'):
                            in_ml_comment = True
                        elif(ch == '/'):
                            in_sl_comment = True
                        comment_start = False
                    if in_quote:
                        if ch in {"\n", "\r"}:
                            continue
                        token_buffer.append(ch)
                        if ch == '"':
                            in_quote = False
                            token = ''.join(token_buffer)
                            token_buffer.clear()
                            yield token
                    elif in_ml_comment:
                        if ch in {"\n", "\r"}:
                            continue
                        token_buffer.append(ch)
                        if ch == '*':
                            comment_end = True
                        elif comment_end:
                            if ch == '/':
                                in_ml_comment = False
                                token = ''.join(token_buffer)
                                token_buffer.clear()
                                yield token
                            else:
                                comment_end = False
                    elif in_sl_comment:
                        if ch in {"\n", "\r"}:
                            in_sl_comment = False
                            token = ''.join(token_buffer)
                            token_buffer.clear()
                            yield token
                        else:
                            token_buffer.append(ch)
                    elif ch == "\\" or escaped:
                        escaped = True
                        if ch not in {'\r', '\n', '\t', ' '}:
                            token_buffer.append(ch)
                            #print('appended ', ch)
                        else:
                            escaped = False
                            token = ''.join(token_buffer)
                            token_buffer.clear()
                            yield token
                    elif ch == '"':
                        in_quote = True
                        token_buffer.append(ch)
                    elif ch == '/':
                        comment_start = True
                        token_buffer.append(ch)
                    elif ch in {'(', ')', '.', ',', ';', '[', ']', ':', "{", "}", "*", "#"}:
                        if token_buffer:
                            token = ''.join(token_buffer)
                            token_buffer.clear()
                            yield token
                        yield ch
                    elif ch in {'\r', '\n', '\t', ' '}:
                        if token_buffer:
                            token = ''.join(token_buffer)
                            token_buffer.clear()
                            yield token
                        #if ch == '\n': self.line_number += 1
                    else:
                        token_buffer.append(ch)

            if token_buffer:
                token = ''.join(token_buffer)
                token_buffer.clear()
                yield token
        finally:
            self.input_stream.close()

    def close(self):
        if self.input_stream:
            self.input_stream.close()

    def expect(self, other):
        if not self.token_equals(other):
            raise RuntimeError("Parse error: Expecting {} on line {}, recieved {}".format(
                other, self.line_number, self.token))

    def peek_equals(self, other):
        peek_token = self.peek()
        return self.equals(peek_token, other)

    def token_equals(self, other):
        return self.equals(self.token, other)

    @staticmethod
    def equals(this, that):
        if this == that:
            return True
        else:
            lowercase_this = this.lower()
            if lowercase_this == that:
                return True
            elif lowercase_this == that.lower():
                return True
        return False

    def is_comment(self, token):
        if token[0:2] == "//" or token[0:2] == "/*":
            return True
        return False

    # def is_timescale_directive(self, token):
    #     if token[0:10] == '`timescale':
    #         return True
    #     return False

    # def is_celldefine_directive(self, token):
    #     if token[0:11] == '`celldefine':
    #         return True
    #     return False

    def is_module(self, token):
        if token == 'module':
            return True
        return False

    def expect_valid_identifier(self):
        if self.is_valid_identifier() is False:
            raise RuntimeError("Parse error: Expecting Verilog identifier on line {}, recieved {}".format(
                self.line_number, self.token))

    def is_valid_identifier(self):
        # TODO deal with \ identifiers
        if re.match(r"[a-zA-Z]|&\a*", self.token) and len(self.token) <= 256:
            return True
        return False

    def expect_valid_integerToken(self):
        if self.is_valid_integerToken() is False:
            raise RuntimeError("Parse error: Expecting integerToken on line {}, recieved {}".format(
                self.line_number, self.token))

    def is_valid_integerToken(self):
        if re.match(r"[-+]?\d+", self.token):
            return True
        return False

    def expect_valid_stringToken(self):
        if self.is_valid_stringToken() is False:
            raise RuntimeError("Parse error: Expecting stringToken on line {}, recieved {}".format(
                self.line_number, self.token))

    def is_valid_stringToken(self):
        if re.match(r'"(?:[a-zA-Z]|(?:%[ \t\n\r]*(?:(?:[-+]?\d+[ \t\n\r]+)*(?:[-+]?\d+))*[ \t\n\r]*%)|[0-9]|[\!\#\$\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]|[ \t\n\r])*"', self.token):
            return True
        return False


if __name__ == "__main__":
    # filename = r"C:\Users\keller\workplace\SpyDrNet\data\large_edif\osfbm.edf"
    import cProfile

    def run():
        filename = r"/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/4bitadder.v"
        tokenizer = VerilogTokenizer.from_filename(filename)
        count = 0
        for token in tokenizer.generator:
            if count < 100:
                if not tokenizer.is_comment(token):
                    print(token)
            count += 1
        print(count)
    cProfile.run("run()")