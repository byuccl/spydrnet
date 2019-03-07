from spydrnet.parsers.edif.edif_tokens import *
from spydrnet.parsers.edif.edif_listener import EdifListener

import re

DEBUG = False

class EdifParser:
	def __init__(self):
		self.line_number = 0
		self.filename = r"C:\Users\keller\workplace\SpyDrNet\data\large_edif\osfbm.edf"
		self.token_generator = None
		
		self.listener = EdifListener()
		self.listener.parser = self

		self.identifier = None
		self.stringToken = None
		self.integerToken = None
	
	def run(self):
		self.parse()
		
	def parse(self):
		self.token_generator = self.generate_tokens()
		self.expect(LEFT_PAREN, self.get_next_token())
		self.listener.enter_edif()
		self.parse_header()
		self.parse_body()
		self.listener.exit_edif()
		self.expect(RIGHT_PAREN, next_token)
				
	def parse_header(self):
		self.expect(EDIF, self.get_next_token())
		self.parse_edifFileNameDef()
		self.parse_edifVersion()
		self.parse_edifLevel()
		self.parse_keywordMap()
	
	def parse_edifFileNameDef(self):
		self.parse_nameDef()
		
	def parse_edifVersion(self):
		self.listener.enter_edifVersion()

		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(EDIF_VERSION, self.get_next_token())
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()			
		self.expect(RIGHT_PAREN, self.get_next_token())

		self.listener.exit_edifVersion()
				
	def parse_keywordMap(self):
		self.listener.enter_keywordMap()

		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(KEYWORD_MAP, self.get_next_token())
		self.parse_keywordLevel()
		
		next_token = self.get_next_token()
		if not self.compare_token(RIGHT_PAREN, next_token):
			self.parse_comment()
			next_token = self.get_next_token()
		
		self.expect(RIGHT_PAREN, next_token)

		self.listener.exit_keywordMap()
		
	def parse_keywordLevel(self):
		self.listener.enter_keywordLevel()

		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(KEYWORD_LEVEL, self.get_next_token())
		self.parse_integerToken()
		self.expect(RIGHT_PAREN, self.get_next_token())

		self.listener.exit_keywordLevel()
	
	def parse_body(self):
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
				
			elif self.compare_token(EXTERNAL, next_token):
				self.parse_external()
				next_token = self.get_next_token()
				
			elif self.compare_token(LIBRARY, next_token):
				self.parse_library()
				next_token = self.get_next_token()
				
			elif self.compare_token(DESIGN, next_token):
				self.parse_design()
				next_token = self.get_next_token()

			elif self.compare_token(COMMENT, next_token):
				self.parse_comment()
				next_token = self.get_next_token()

			elif self.compare_token(USER_DATA, next_token):
				self.parse_userData()
				next_token = self.get_next_token()

			else:
				self.expect("|".join([STATUS, EXTERNAL, LIBRARY, DESIGN, COMMENT, USER_DATA]), next_token)

	def parse_status(self):
		self.listener.enter_status()

		next_token = self.get_next_token()
		while not self.compare_token(RIGHT_PAREN, next_token):
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

		self.listener.exit_status()
		
	def parse_written(self):
		self.listener.enter_written()

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
		
		self.listener.exit_written()
		
	def parse_timeStamp(self):
		self.listener.enter_timestamp()

		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(TIMESTAMP, self.get_next_token())
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()
		self.parse_integerToken()
		self.expect(RIGHT_PAREN, self.get_next_token())

		self.listener.exit_timestamp()
		
	def parse_author(self):
		self.parse_stringToken()
		self.expect(RIGHT_PAREN, self.get_next_token())
		
	def parse_program(self):
		self.listener.enter_program()

		self.parse_stringToken()
		
		next_token = self.get_next_token()
		if self.compare_token(LEFT_PAREN, next_token):
			self.parse_version()
			next_token = self.get_next_token()
		
		self.expect(RIGHT_PAREN, next_token)

		self.listener.exit_program()
		
	def parse_version(self):
		self.listener.enter_version()

		self.expect(VERSION, self.get_next_token())
		self.parse_stringToken()
		self.expect(RIGHT_PAREN, self.get_next_token())

		self.listener.exit_version()
		
	def parse_dataOrigin(self):
		self.parse_stringToken()
		
		next_token = self.get_next_token()
		if self.compare_token(LEFT_PAREN, next_token):
			self.parse_version()
		
		self.expect(RIGHT_PAREN, next_token)

	def parse_external(self):
		raise NotImplementedError()
		
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
		self.listener.enter_edifLevel()

		self.expect(LEFT_PAREN, self.get_next_token())
		self.expect(EDIF_LEVEL, self.get_next_token())
		self.parse_integerToken()
		self.expect(RIGHT_PAREN, self.get_next_token())

		self.listener.exit_edifLevel()

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
		raise NotImplementedError()
		
	def parse_comment(self):
		self.listener.enter_comment()

		next_token = self.get_next_token()
		while not self.compare_token(RIGHT_PAREN, next_token):
			self.expect_stringToken(next_token)
			self.listener.push_stringToken(next_token)
			next_token = self.get_next_token()
		self.expect(RIGHT_PAREN, next_token)

		self.listener.exit_comment()
		
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
		self.listener.push_integerToken(integerToken)
		
	def parse_nameDef(self):
		self.listener.enter_nameDef()
		next_token = self.get_next_token()
		if self.compare_token(LEFT_PAREN, next_token):
			self.expect(RENAME, self.get_next_token())
			self.parse_identifier()
			self.parse_stringToken()
			self.expect(RIGHT_PAREN, self.get_next_token())
		else:
			self.expect_identifier(next_token)
			self.listener.push_identifier(next_token)
		self.listener.exit_nameDef()
			
	def parse_identifier(self):
		identifier = self.get_next_token()
		self.expect_identifier(self.identifier)
		self.listener.push_identifier(identifier)
		
	def parse_stringToken(self):
		stringToken = self.get_next_token()
		self.expect_stringToken(stringToken)
		self.listener.push_stringToken(stringToken)
		
		
	def compare_token(self, expected_token, recieved_token):
		if expected_token != recieved_token:
			if expected_token != recieved_token.lower():
				return False
		return True
		
	def expect(self, expected_token, recieved_token):
		if expected_token != recieved_token:
			if expected_token != recieved_token.lower():
				raise RuntimeError("Parse error: Expecting {} on line {}, recieved {}".format(expected_token, self.line_number, recieved_token))
					
	def get_next_token(self):
		return next(self.token_generator)
						
if __name__ == '__main__':
	import cProfile
	edif_parser = EdifParser()
	edif_parser.run()
	#cProfile.run('edif_parser.run()')
