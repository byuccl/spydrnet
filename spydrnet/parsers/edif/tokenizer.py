import re

class EdifTokenizer:
    @staticmethod
    def from_filename(filename):
        tokenizer = EdifTokenizer(filename)
        return tokenizer
    
    def __init__(self, filename):
        self.filename = filename
        self.generator = self.generate_tokens()
        # self.lookahead_buffer = None # LookaheadBuffer()

    def next_token(self):
        return Token(next(self.generator))

    # def lookahead(self, distance = 0):
    #     lookahead_count = self.lookahead_buffer.get_count()
    #     if lookahead_count < distance + 1:
    #         for _ in range(distance - lookahead_count + 1):
    #             self.lookahead_buffer.add(next(self.generator))

    #     return self.lookahead_buffer.lookahead(distance)

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

class Token:
    def __init__(self, value, line_number):
        self.value = value
        self.line_number = line_number

    def expect(self, other):
        if self.equals(other):
            raise RuntimeError("Parse error: Expecting {} on line {}, recieved {}".format(self.value, self.line_number, other))

    def equals(self, other):
        if isinstance(other, Token):
            other_value = other.value
        else:
            other_value = other
        
        if isinstance(other_value, str):
            if self.value == other_value:
                return True
            
            lowercase_token = self.value.lower()
            if lowercase_token == other_value:
                return True

            if lowercase_token == other.lower():
                return True
            
        return False

    def expect_valid_identifier(self):
        if self.is_valid_identifier() is False:
            raise RuntimeError("Parse error: Expecting EDIF identifier on line {}, recieved {}".format(self.line_number, self.value))

    def is_valid_identifier(self):
        if re.match(r"[a-zA-Z]|&\a*", self.value):
            return True 
        return False

    def expect_valid_integerToken(self):
        if self.is_valid_integerToken() is False:
            raise RuntimeError("Parse error: Expecting integerToken on line {}, recieved {}".format(self.line_number, self.value))

    def is_valid_integerToken(self):
        if re.match(r"[-+]?\d+", self.value):
            return True
        return False

    def expect_valid_stringToken(self):
        if self.is_valid_stringToken() is False:
            raise RuntimeError("Parse error: Expecting integerToken on line {}, recieved {}".format(self.line_number, self.value))

    def is_valid_stringToken(self):
        if re.match(r'"(?:[a-zA-Z]|(?:%[ \t\n\r]*(?:(?:[-+]?\d+[ \t\n\r]+)*(?:[-+]?\d+))*[ \t\n\r]*%)|[0-9]|[\!\#\$\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?\@\[\\\]\^\_\`\{\|\}\~]|[ \t\n\r])*"', self.value):
            return True
        return False

class LookaheadBuffer:
    def __init__(self, size = 10):
        self.size = size
        self.out_index = 0
        self.in_index = 0
        self.buffer = [None]*10
        self.is_empty = True

    def add(self, item):
        if self.is_empty:
            self.is_empty = False
        else:
            assert(self.in_index != self.out_index)
        self.buffer[self.in_index] = item
        self.in_index = (self.in_index + 1) % self.size

    def remove(self):
        assert(not self.is_empty)
        item = self.buffer[self.out_index]
        self.out_index = (self.out_index + 1) % self.size
        if self.out_index == self.in_index:
            self.is_empty = True
        return item

    def get_count(self):
        if self.is_empty:
            return 0
        if self.in_index == self.out_index:
            return self.size
        return (self.in_index - self.out_index) % self.size

    def lookahead(self, distance = 0):
        return self.buffer[(self.out_index + distance) % self.size]

if __name__ == "__main__":
    filename = r"C:\Users\keller\workplace\SpyDrNet\data\large_edif\osfbm.edf"
    tokenizer = EdifTokenizer.from_filename(filename)

    for i in range(10):
        print("lookahead", i, "token", tokenizer.lookahead(i))

    for _ in range(10):
        print("next token", tokenizer.next_token())

    for i in range(10):
        print("lookahead", i, "token", tokenizer.lookahead(i))

    for _ in range(10):
        print("next token", tokenizer.next_token())

    for _ in range(10):
        print("next token", tokenizer.next_token())

    for i in range(7):
        print("lookahead", i, "token", tokenizer.lookahead(i))

    for _ in range(10):
        print("next token", tokenizer.next_token())

    for i in range(7):
        print("lookahead", i, "token", tokenizer.lookahead(i))

    for _ in range(10):
        print("next token", tokenizer.next_token())

    for i in range(11):
        print("lookahead", i, "token", tokenizer.lookahead(i))