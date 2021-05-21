import spydrnet.parsers.verilog.verilog_tokens as vt

class TokenFactory():
    def __init__(self):    
        self.buffer = ''
        #only one of these should ever be true at any time.
        self.single_line_comment = False
        self.multi_line_comment = False
        self.string = False
        self.escaped_identifier = False
        self.processor_directive = False
        self.last_character = "" #should not be relied on to always be the last character when tokens are ending
    
    def clear(self, character = ""):
        self.buffer = character

    def any_flag_set(self):
        return self.single_line_comment or self.multi_line_comment or self.string or self.escaped_identifier or self.processor_directive

    def set_flags(self):
        if len(self.buffer) <= 2 and not self.any_flag_set():
            
            if self.buffer == vt.OPEN_LINE_COMMENT:
                self.single_line_comment = True
        
            elif self.buffer == vt.OPEN_BLOCK_COMMENT:
                self.multi_line_comment = True
        
            elif self.buffer == '"':
                self.string = True
        
            elif self.buffer == "\\":
                self.escaped_identifier = True
            
            elif self.buffer == "`":
                self.processor_directive = True

    def add_character(self, character):
        #tries to add the character to the token.
        #if the token is complete it will return and start the next token
        #if the token is incomplete it will add it and return none
        token_out = None
        #first thing, see if we need to return a token
        if self.buffer in vt.SINGLE_CHARACTER_TOKENS:
            token_out = self.buffer
            self.clear()

        elif self.single_line_comment and character == vt.NEW_LINE:
            token_out = self.buffer
            self.clear()
            self.single_line_comment = False

        elif self.multi_line_comment and self.last_character == "*" and character == "/":
            token_out = self.buffer + character
            character = ""
            self.clear()
            self.multi_line_comment = False

        elif self.escaped_identifier and character in vt.WHITESPACE:
            token_out = self.buffer + " "
            self.clear()
            self.escaped_identifier = False

        elif self.string and character == '"':
            token_out = self.buffer + character
            character = ""
            self.clear()
            self.string = False

        elif self.processor_directive and character == vt.NEW_LINE:
            token_out = self.buffer
            self.clear()
            self.processor_directive = False

        elif character == vt.STAR and self.last_character == "/":
            pass #this will be a multi line comment but * is a breaker...

        elif character in vt.BREAKER_TOKENS and not self.any_flag_set() and len(self.buffer) != 0:
            token_out = self.buffer
            self.clear()

        elif character == vt.DOT and not self.any_flag_set() and len(self.buffer) != 0 and\
                not vt.is_numeric(self.buffer):
            token_out = self.buffer
            self.clear()

        
        if character not in vt.WHITESPACE:
            self.buffer = self.buffer + character
        elif self.single_line_comment or self.multi_line_comment or self.string or self.processor_directive:
            self.buffer = self.buffer + character
        self.last_character = character
        
        last_multi_line_comment = self.multi_line_comment
        self.set_flags()
        if self.multi_line_comment and not last_multi_line_comment:
            self.last_character = "" #these lines help to ensure that /*/ isn't precieved as a complete comment.


        return token_out

    def flush(self):
        token_out = self.buffer
        self.clear()
        if token_out == "":
            return None
        return token_out