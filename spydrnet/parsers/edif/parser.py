from spydrnet.parsers.edif.tokenizer import EdifTokenizer
from spydrnet.ir import *
from spydrnet.parsers.edif.edif_tokens import *

class EdifParser:
    @staticmethod
    def from_filename(filename):
        parser = EdifParser()
        parser.filename = filename
        return parser

    def __init__(self):
        self.filename = None
        self.elements = list()
        self.data = list()
        self.parse_stack = list()
    
    def parse(self):
        self.tokenizer = EdifTokenizer.from_filename(self.filename)
        self.token_generator = self.tokenizer.generate_tokens()

        self.parse_edif()

    def parse_edif(self):
        self.expect(LEFT_PAREN, next(self.token_generator))
        self.expect(EDIF, next(self.token_generator))
        self.elements.append(Environment())
        self.parse_nameDef()

    def parse_nameDef(self):
        next_token = next(self.token_generator) 
        if next_token == LEFT_PAREN:
            self.expect(RENAME, next(self.token_genterator))
            edif_identifier = next(self.token_generator)
            edif_external_identifier = next(self.token_generator)
            self.expect_stringToken(edif_external_identifier)
            self.elements[-1].set_entry("")
        else:
            edif_identifier = next_token
            self.expect_identifier(edif_identifier)
        
    def experimental(self):
        first_token = next(token_generator)
        self.expect(LEFT_PAREN, first_token)
        self.parse_stack.append(self.data)
        
        for token in token_generator:
            if token == LEFT_PAREN:
                next_level = list()
                self.parse_stack[-1].append(next_level)
                self.parse_stack.append(next_level)
            elif token == RIGHT_PAREN:
                self.parse_stack.pop()
            else:
                self.parse_stack[-1].append(token)
        assert (not self.parse_stack)

    def expect(self, expected_token, recieved_token):
        if expected_token != recieved_token:
            if expected_token != recieved_token.lower():
                raise RuntimeError("Parse error: Expecting {} on line {}, recieved {}".format(expected_token, self.line_number, recieved_token))

	def expect_identifier(self, token):
		if not re.match(r"[a-zA-Z]|&\a*", token):
			raise RuntimeError("Parse error: Expecting EDIF identifier on line {}, recieved {}".format(self.line_number, token))
			
	def expect_integerToken(self, token):
		if not re.match(r"[-+]?\d+", token):
			raise RuntimeError("Parse error: Expecting integerToken on line {}, recieved {}".format(self.line_number, token))
			
	def expect_stringToken(self, token):
		if not re.match(r'"(?:[a-zA-Z]|(?:%[ \t\n\r]*(?:(?:[-+]?\d+[ \t\n\r]+)*(?:[-+]?\d+))*[ \t\n\r]*%)|[0-9]|[\!\#\$\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]|[ \t\n\r])*"', token):
			raise RuntimeError("Parse error: Expecting stringToken on line {}, recieved {}".format(self.line_number, token))


if __name__ == "__main__":
    filename = r"C:\Users\keller\workplace\SpyDrNet\data\large_edif\osfbm.edf"
    parser = EdifParser.from_filename(filename)
    import cProfile
    cProfile.run('parser.parse()')