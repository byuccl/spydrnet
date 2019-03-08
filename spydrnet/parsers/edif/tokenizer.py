import re

class EdifTokenizer:
    @staticmethod
    def from_filename(filename):
        tokenizer = EdifTokenizer(filename)
        return tokenizer
    
    def __init__(self, filename):
        self.filename = filename
        self.generator = self.generate_tokens()
        self.token = None
        self.next_token = None

    def peek(self):
        if self.next_token:
            return self.next_token
        else:
            self.next_token = next(self.generator)
            return self.next_token

    def next(self):
        if self.next_token:
            self.token = self.next_token
            self.next_token = None
        else:
            self.token = next(self.generator)

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

    def expect(self, other):
        if not self.token_equals(other):
            raise RuntimeError("Parse error: Expecting {} on line {}, recieved {}".format(other, self.line_number, self.token))

    def peek_equals(self, other):
        peek_token = self.peek()
        return self.equals(peek_token, other)
    
    def token_equals(self, other):
        return self.equals(self.token, other)
    
    @staticmethod
    def equals(this, that):
        if this == that or this.lower() == that:
            return True
        return False

    def expect_valid_identifier(self):
        if self.is_valid_identifier() is False:
            raise RuntimeError("Parse error: Expecting EDIF identifier on line {}, recieved {}".format(self.line_number, self.token))

    def is_valid_identifier(self):
        if re.match(r"[a-zA-Z]|&\a*", self.token):
            return True 
        return False

    def expect_valid_integerToken(self):
        if self.is_valid_integerToken() is False:
            raise RuntimeError("Parse error: Expecting integerToken on line {}, recieved {}".format(self.line_number, self.token))

    def is_valid_integerToken(self):
        if re.match(r"[-+]?\d+", self.token):
            return True
        return False

    def expect_valid_stringToken(self):
        if self.is_valid_stringToken() is False:
            raise RuntimeError("Parse error: Expecting stringToken on line {}, recieved {}".format(self.line_number, self.token))

    def is_valid_stringToken(self):
        if re.match(r'"(?:[a-zA-Z]|(?:%[ \t\n\r]*(?:(?:[-+]?\d+[ \t\n\r]+)*(?:[-+]?\d+))*[ \t\n\r]*%)|[0-9]|[\!\#\$\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]|[ \t\n\r])*"', self.token):
            return True
        return False

if __name__ == "__main__":
    # filename = r"C:\Users\keller\workplace\SpyDrNet\data\large_edif\osfbm.edf"
    filename = r"C:\Users\akeller9\workspace\SpyDrNet\data\large_edif\osfbm.edf"
    tokenizer = EdifTokenizer.from_filename(filename)