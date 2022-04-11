import io
import re
import zipfile
import io
import os
from spydrnet.parsers.eblif.eblif_tokens import BACKSLASH

class Tokenizer:
    @staticmethod
    def from_stream(stream):
        tokenizer = Tokenizer(stream)
        return tokenizer

    @staticmethod
    def from_string(string):
        string_stream = io.StringIO(string)
        tokenizer = Tokenizer(string_stream)
        return tokenizer

    @staticmethod
    def from_filename(filename):
        tokenizer = Tokenizer(filename)
        return tokenizer

    def __init__(self,input_source):
        # self.file = file
        self.token = None
        self.next_token = None
        self.line_number = 0
        self.current_line_tokens = list()
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
    
    def generate_tokens(self):
        # with open(file) as file:   
        for line in self.input_stream: 
            self.current_line_tokens.clear()     
            for word in line.split():
                self.current_line_tokens.append(word)
                yield word
            self.line_number+=1
            yield "\n"

    def has_next(self):
        try:
            self.peek()
            return True
        except StopIteration:
            return False

    def next(self):
        if self.next_token:
            self.token = self.next_token
            self.next_token = None
        else:
            self.token = next(self.generator)
        # print(self.token)
        if (self.token is BACKSLASH):
            # print("BACKSLASH!!!!")
            # print("Token is " + self.token)
            self.next()
            # print("Token is " + self.token)
            self.next()
            # print("Token is " + self.token)
        return self.token

    def peek(self):
        if self.next_token:
            return self.next_token
        else:
            self.next_token = next(self.generator)
            return self.next_token

    def expect(self, other):
        if not self.token_equals(other):
            raise RuntimeError(
                "Parse error: Expecting {} on line {}, recieved {}".format(
                    other, self.line_number, self.token
                )
            )

    def token_equals(self, other):
        return self.equals(self.token, other)

    def equals(self, this, that):
        if this == that:
            return True
        else:
            lowercase_this = this.lower()
            if lowercase_this == that:
                return True
            elif lowercase_this == that.lower():
                return True
        return False