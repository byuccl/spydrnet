import re

AUTHOR = 'author'
BEHAVIOR = 'behavior'
CELL = 'cell'
CELL_TYPE = 'celltype'
COMMENT = 'comment'
DATA_ORIGIN = 'dataorigin'
DESIGN = 'design'
DOCUMENT = 'document'
EDIF = 'edif'
EDIF_VERSION = 'edifversion'
EDIF_LEVEL = 'ediflevel'
EXTERNAL = 'external'
GENERIC = 'generic'
GRAPHIC = 'graphic'
KEYWORD_MAP = 'keywordmap'
KEYWORD_LEVEL = 'keywordlevel'
LEFT_PAREN = '('
LIBRARY = 'library'
LOGICMODEL = 'logicmodel'
MASKLAYOUT = 'masklayout'
NETLIST = 'netlist'
PCBLAYOUT = 'netlist'
PROGRAM = 'program'
PROPERTY = 'property'
NUMBER_DEFINITION = 'numberdefinition'
RENAME = 'rename'
RIGHT_PAREN = ')'
RIPPER = 'ripper'
SCHEMATIC = 'schematic'
STATUS = 'status'
STRANGER = 'stranger'
SYMBOLIC = 'symbolic'
TECHNOLOGY = 'technology'
TIE = 'tie'
TIMESTAMP = 'timestamp'
USER_DATA = 'userdata'
VERSION = 'version'
VIEW = 'view'
VIEW_MAP = 'viewmap'
VIEW_TYPE = 'viewtype'
WRITTEN = 'written'

DEBUG = False

class EdifParser:

	def __init__(self):
		self.line_number = 0
		self.filename = "C:\\Users\\akeller9\\workspace\\SpyDrNet\\data\\large_edif\\osfbm.edf"
		self.token_generator = None
		
		self.identifier = None
		self.stringToken = None
		self.integerToken = None
	
	def run(self):
		self.parse()
		
	def parse(self):
		self.token_generator = self.generate_tokens()
		self.expect(LEFT_PAREN, self.get_next_token())
		self.parse_header()
		
		has_status = False
		next_token = self.get_next_token()
		while self.compare_token(LEFT_PAREN, next_token):
			next_token = self.get_next_token()
			if self.compare_token(STATUS, next_token):
				if has_status:
					raise RuntimeError("Parse error: Multiple occurances of status, line {}".format(self.line_number))
				else:
					has_status = True
					self.parse_status()
				next_token = self.get_next_token()
				
			elif self.compare_token(EXTERNAL, next_token):
				
				next_token = self.get_next_token()
				
			elif self.compare_token(LIBRARY, next_token):
				self.parse_library()
				next_token = self.get_next_token()
				
			elif self.compare_token(DESIGN, next_token):
				
				next_token = self.get_next_token()
			elif self.compare_token(COMMENT, next_token):
				
				next_token = self.get_next_token()
			elif self.compare_token(USER_DATA, next_token):
				
				next_token = self.get_next_token()
			else:
				self.expect("|".join([STATUS, EXTERNAL, LIBRARY, DESIGN, COMMENT, USER_DATA]), next_token)
		
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_header(self):
		self.expect(EDIF, self.get_next_token())
		self.parse_edifFileNameDef()
		self.parse_edifVersion()
		self.parse_edifLevel()
		self.parse_keywordMap()
	
	def parse_edifFileNameDef(self):
		self.parse_nameDef()
		if DEBUG:
			print(EDIF, self.identifier)
		
	def parse_edifVersion(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(EDIF_VERSION, self.get_next_token())
		
		self.parse_integerToken()
		version_digit_0 = self.integerToken
		self.parse_integerToken()
		version_digit_1 = self.integerToken
		self.parse_integerToken()
		version_digit_2 = self.integerToken
		
		if version_digit_0 != 2 or version_digit_1 != 0 or version_digit_2 != 0:
			raise RuntimeError("Parse error: Only EDIF Version 2 0 0 is supported, EDIF Version is {} {} {} on line {}".format(version_digit_0, version_digit_1, version_digit_2, self.line_number))
			
		self.expect(RIGHT_PAREN, self.get_next_token())
				
	def parse_keywordMap(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(KEYWORD_MAP, self.get_next_token())
		self.parse_keywordLevel()
		
		next_token = self.get_next_token()
		if self.compare_token(LEFT_PAREN, next_token):
			self.parse_comment()
			next_token = self.get_next_token()
		
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_keywordLevel(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(KEYWORD_LEVEL, self.get_next_token())
		self.parse_integerToken()
		self.expect(RIGHT_PAREN, self.get_next_token())
		
	def parse_status(self):
		next_token = self.get_next_token()
		while self.compare_token(LEFT_PAREN, next_token):
			next_token = self.get_next_token()
			if self.compare_token(WRITTEN, next_token):
				self.parse_written()
				next_token = self.get_next_token()
			elif self.compare_token(COMMENT, next_token):
				next_token = self.get_next_token()
			elif self.compare_token(USER_DATA, next_token):
				next_token = self.get_next_token()
			else:
				self.expect("|".join([WRITTEN|COMMENT|USER_DATA]), next_token)
			
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_written(self):
		self.parse_timeStamp()
		
		next_token = self.get_next_token()
		while self.compare_token(LEFT_PAREN, next_token):
			has_author = False
			has_program = False
			has_data_origin = False
			next_token = self.get_next_token()
			if self.compare_token(AUTHOR, next_token):
				self.parse_author()
				next_token = self.get_next_token()
			elif self.compare_token(PROGRAM, next_token):
				self.parse_program()
				next_token = self.get_next_token()
			elif self.compare_token(DATA_ORIGIN, next_token):
				self.parse_dataOrigin()
				next_token = self.get_next_token()
			elif self.compare_token(PROPERTY, next_token):
				self.parse_property()
				next_token = self.get_next_token()
			elif self.compare_token(COMMENT, next_token):
				self.parse_comment()
				next_token = self.get_next_token()
			elif self.compare_token(USER_DATA, next_token):
				next_token = self.get_next_token()
			else:
				expected_tokens = list()
				if not has_author:
					expected_tokens.append(AUTHOR)
				if not has_program:
					expected_tokens.append(PROGRAM)
				if not has_data_origin:
					expected_tokens.append(DATA_ORIGIN)
				expected_tokens.append(PROPERTY)
				expected_tokens.append(COMMENT)
				expected_tokens.append(USER_DATA)
				self.expect("|".join(expected_tokens), next_token)
			
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_timeStamp(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(TIMESTAMP, self.get_next_token())
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()
		self.expect(RIGHT_PAREN, self.get_next_token())
		
	def parse_author(self):
		self.parse_stringToken()
		self.expect(RIGHT_PAREN, self.get_next_token())
		
	def parse_program(self):
		self.parse_stringToken()
		
		next_token = self.get_next_token()
		if self.compare_token(LEFT_PAREN, next_token):
			self.parse_version()
			next_token = self.get_next_token()
		
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_version(self):
		self.expect(VERSION, self.get_next_token())
		self.parse_stringToken()
		self.expect(RIGHT_PAREN, self.get_next_token())
		
	def parse_dataOrigin(self):
		self.parse_stringToken()
		
		next_token = self.get_next_token()
		if self.compare_token(LEFT_PAREN, next_token):
			self.parse_version()
		
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_library(self):
		self.parse_nameDef()
		self.parse_edifLevel()
		self.parse_technology()
		
		has_status = False
		next_token = self.get_next_token()
		while not self.compare_token(RIGHT_PAREN, next_token):
			next_token = self.get_next_token()
			if self.compare_token(STATUS, next_token):
				if has_status:
					raise RuntimeError("Parse error: Multiple occurances of status, line {}".format(self.line_number))
				else:
					has_status = True
					self.parse_status()
				next_token = self.get_next_token()
			elif self.compare_token(CELL, next_token):
				self.parse_cell()
				next_token = self.get_next_token()
			elif self.compare_token(COMMENT, next_token):
				self.parse_comment()
				next_token = self.get_next_token()
			elif self.compare_token(USER_DATA, next_token):
				next_token = self.get_next_token()
			else:
				expect_tokens = list()
				if not has_status:
					expect_tokens.append(STATUS)
				expect_tokens.append(CELL)
				expect_tokens.append(COMMENT)
				expect_tokens.append(USER_DATA)
				self.expect("|".join(expect_tokens), next_token)
			
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_edifLevel(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(EDIF_LEVEL, self.get_next_token())
		self.parse_integerToken()
		self.expect(RIGHT_PAREN, self.get_next_token())

	def parse_technology(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(TECHNOLOGY, self.get_next_token())
		self.parse_numberDefinition()
		
		has_simulationInfo = False
		has_physicalDesignRule = False
		next_token = self.get_next_token()
		while self.compare_token(LEFT_PAREN, next_token):
			next_token = self.get_next_token()
		
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_numberDefinition(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(NUMBER_DEFINITION, self.get_next_token())
		
		next_token = self.get_next_token()
		while self.compare_token(LEFT_PAREN, next_token):
			next_token = self.get_next_token()
		
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_cell(self):
		self.parse_nameDef()
		self.parse_cellType()
		
		has_status = False
		has_viewMap = False
		next_token = self.get_next_token()
		while not self.compare_token(RIGHT_PAREN, next_token):
			next_token = self.get_next_token()
			print("MADE IT")
			if self.compare_token(STATUS, next_token):
				if has_status:
					raise RuntimeError("Parse error: Multiple occurances of status, line {}".format(self.line_number))
				else:
					has_status = True
					self.parse_status()
				next_token = self.get_next_token()
			elif self.compare_token(VIEW, next_token):
				self.parse_view()
				next_token = self.get_next_token()
			elif self.compare_token(VIEW_MAP, next_token):
				if has_viewMap:
					raise RuntimeError("Parse error: Multiple occurances of viewmap, line {}".format(self.line_number))
				else:
					has_status = True
				next_token = self.get_next_token()
			elif self.compare_token(PROPERTY, next_token):
				self.parse_property()
				next_token = self.get_next_token()
			elif self.compare_token(COMMENT, next_token):
				self.parse_comment()
				next_token = self.get_next_token()
			elif self.compare_token(USER_DATA, next_token):
				next_token = self.get_next_token()
			else:
				expect_tokens = list()
				if not has_status:
					expect_tokens.append(STATUS)
				if not has_viewMap:
					expect_tokens.append(VIEW_MAP)
				expect_tokens.append(CELL)
				expect_tokens.append(COMMENT)
				expect_tokens.append(USER_DATA)
				self.expect("|".join(expect_tokens), next_token)
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_cellType(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(CELL_TYPE, self.get_next_token())
		
		next_token = self.get_next_token()
		if not self.compare_token(GENERIC, next_token) and not self.compare_token(TIE, next_token) and not self.compare_token(RIPPER, next_token):
			self.expect('|'.join([GENERIC, TIE, RIPPER]), next_token)
			
		self.expect(RIGHT_PAREN, self.get_next_token())
		
	def parse_view(self):
		self.parse_nameDef()
		self.parse_viewType()
		self.parse_interface()
		
	def parse_viewType(self):
		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(VIEW_TYPE, self.get_next_token())
		
		next_token = self.get_next_token()
		if not self.compare_token(BEHAVIOR, next_token) and \
		   not self.compare_token(DOCUMENT, next_token) and \
		   not self.compare_token(GRAPHIC, next_token) and \
		   not self.compare_token(LOGICMODEL, next_token) and \
		   not self.compare_token(MASKLAYOUT, next_token) and \
		   not self.compare_token(NETLIST, next_token) and \
		   not self.compare_token(PCBLAYOUT, next_token) and \
		   not self.compare_token(SCHEMATIC, next_token) and \
		   not self.compare_token(STRANGER, next_token) and \
		   not self.compare_token(SYMBOLIC, next_token):
			self.expect('|'.join([BEHAVIOR, DOCUMENT, GRAPHIC, LOGICMODEL, MASKLAYOUT, NETLIST, PCBLAYOUT, SCHEMATIC, STRANGER, SYMBOLIC]), next_token)
		
		self.expect(RIGHT_PAREN, self.get_next_token())
		
	def parse_interface(self):
		
	def parse_comment(self):
		next_token = self.get_next_token()
		while not self.compare_token(RIGHT_PAREN, next_token):
			self.expect_stringToken(next_token)
			self.stringToken = next_token
			next_token = self.get_next_token()
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_property(self):
		self.parse_nameDef()
		self.parse_typedValue()
		
		has_owner = False
		has_unit = False
		next_token = self.get_next_token()
		while self.compare_token(LEFT_PAREN, next_token):
			next_token = self.get_next_token()
			if self.compare_token(OWNER, next_token):
				next_token = self.get_next_token()
			elif self.compare_token(UNIT, next_token):
				next_token = self.get_next_token()
			elif self.compare_token(PROPERTY, next_token):
				next_token = self.get_next_token()
			elif self.compare_token(COMMENT, next_token):
				next_token = self.get_next_token()
			else:
				expected_tokens = list()
				if not has_owner:
					expected_tokens.append(OWNER)
				if not has_unit:
					expected_tokens.append(UNIT)
				expected_tokens.append(PROPERTY)
				expected_tokens.append(COMMENT)
				self.expect("|".join(expected_tokens), next_token)
		
		self.expect(RIGHT_PAREN, next_token)
		
	def parse_integerToken(self):
		integerToken = self.get_next_token()
		self.expect_integerToken(integerToken)
		self.integerToken = int(integerToken)
		
	def parse_nameDef(self):
		next_token = self.get_next_token()
		if self.compare_token(LEFT_PAREN, next_token):
			self.expect(RENAME, self.get_next_token())
			self.parse_identifier()
			self.parse_stringToken()
			self.expect(RIGHT_PAREN, self.get_next_token())
		else:
			self.expect_identifier(next_token)
			self.identifier = next_token
			self.external_identifier = None
			
	def parse_identifier(self):
		identifier = self.get_next_token()
		self.expect_identifier(self.identifier)
		self.identifier = identifier
		
	def parse_stringToken(self):
		stringToken = self.get_next_token()
		self.expect_stringToken(stringToken)
		self.stringToken = stringToken[1:-1]
		
		
	def compare_token(self, expected_token, recieved_token):
		if expected_token != recieved_token:
			if expected_token != recieved_token.lower():
				return False
		return True
		
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
	
	def get_next_token(self):
		return next(self.token_generator)
		
	def generate_tokens(self):
		with open(self.filename, 'r') as fi:
			self.line_number = 1
			in_quote = False
			in_token = False
			token = list()
			while True:
				buffer = fi.read(8192)
				if not buffer:
					break
				for ch in buffer:
					if ch == '\n':
						self.line_number += 1
						
					if in_quote:
						if ch == '"':
							in_quote = False
							token.append('"')
							yield ''.join(token)
						elif ch != '\n' and ch != '\r':
							token.append(ch)
							
					elif ch == '"':
						in_quote = True
						token.clear()
						token.append(ch)
						
					elif ch == '(':
						yield ch
						
					elif ch == ')':
						if in_token == True:
							in_token = False
							yield ''.join(token)
						
						yield ch
						
					elif ch == '\t' or ch == '\n' or ch == '\r' or ch == ' ':
						if in_token == True:
							in_token = False
							yield ''.join(token)
							
					else:
						if in_token == False:
							in_token = True
							token.clear()
							
						token.append(ch)
						
if __name__ == '__main__':
	import cProfile
	edif_parser = EdifParser()
	edif_parser.run()
	#cProfile.run('edif_parser.run()')
