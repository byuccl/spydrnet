import ply.lex as lex

tokens = (
    'MODULE',
    'ENDMODULE',
    'INPUT',
    'OUTPUT',
    'INOUT',
    'WIRE',
    'COMMA',
    'COLON',
    'SEMICOLON',
    'LEFT_PAREN',
    'RIGHT_PAREN',
    'SIMPLE_IDENTIFIER',
    'LEFT_BRACKET',
    'RIGHT_BRACKET',
    'POUND',
    'DOT',
    # 'DIGIT',
    # 'HEXDIGIT',
    'NUMBER',
    'BINARY_NUMBER',
    'DECIMAL_NUMBER',
    'HEX_NUMBER',
    # 'SINGLEQUOTE',
    'BLOCK_START',
    'BLOCK_END',
    # 'CONSTENT',
    'STRING',
    # 'PORT',
    'PRIMITIVE',
    'ENDPRIMITIVE',
    # 'MODULE_NAME',
    'COMMENT',
    # 'MULTILINECOMMENT',
    # 'SOMETHING',
    # 'NAME',
    # 'EQUALS',
    # 'NUMBER',
    # 'PORT_NAME',
)


states = (
    ('blockComment', 'exclusive'),
#     ('modulename', 'inclusive'),
#     ('portname', 'inclusive'),
#
)

t_SIMPLE_IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_$]*'
t_LEFT_PAREN = r'\('
t_RIGHT_PAREN = r'\)'
t_SEMICOLON = r';'
t_COMMA = r','
t_POUND = r'\#'
t_DOT = r'\.'
t_COLON = r':'
t_LEFT_BRACKET = r'\['
t_RIGHT_BRACKET = r'\]'
# t_DIGIT = r'[0-9]'
# t_HEXDIGIT = r'[a-fA-F]'
# t_SINGLEQUOTE = r'\''
t_NUMBER = r'[0-9]+'
t_STRING = r'".*"'


def t_BINARY_NUMBER(t):
    r'[0-9]+\'b[0-1]+'
    return t


def t_DECIMAL_NUMBER(t):
    r'[0-9]+\'d[0-9]+'
    return t


def t_HEX_NUMBER(t):
    r'[0-9]+\'h[0-9a-fA-F]+'
    return t


def t_PRIMITIVE(t):
    r'primitive'
    return t


def t_ENDPRIMITIVE(t):
    r'endprimitive'
    return t


def t_comment(t):
    r'//.*'


def t_blockComment_comment(t):
    r'[a-zA-Z0-9]+(?<!\*/)'


def t_BLOCK_START(t):
    r'/\*'
    t.lexer.begin('blockComment')

def t_blockComment_BLOCK_END(t):
    r'\*/'
    t.lexer.begin('INITIAL')

def t_WIRE(t):
    r'wire'
    return t


def t_INOUT(t):
    r'inout'
    return t


def t_INPUT(t):
    r'input'
    return t


def t_OUTPUT(t):
    r'output'
    return t


def t_MODULE(t):
    # r'[a-zA-Z]([a-zA-Z0-9]|_|\[[0-9]*\])'
    r'module'
    # t.lexer.begin('modulename')
    return t

def t_ENDMODULE(t):
    # r'[a-zA-Z]([a-zA-Z0-9]|_|\[[0-9]*\])'
    r'endmodule'
    # t.lexer.begin('modulename')
    return t
#
#
# def t_portname_PORT_NAME(t):
#     r'[a-zA-Z]([a-zA-Z]|_|[0-9])*'
#     return t
#
#
# def t_modulename_MODULE_NAME(t):
#     r'[a-zA-Z]([a-zA-Z]|_|[0-9])*'
#     t.lexer.begin('INITIAL')
#     return t
#
#
# def t_LEFT_PAREN(t):
#     r'\('
#     t.lexer.begin('portname')
#     t.lexer.level += 1
#     return t
#
#
# def t_RIGHT_PAREN(t):
#     r'\)'
#     if t.lexer.level == 1:
#         t.lexer.begin('INITIAL')
#     t.lexer.level -= 1
#     return t


def t_ANY_error(t):
    for x in range(len(t.value)):
        if(t.value[x].isspace()):
            t.value = t.value[:x]
            break
    raise UnsupportedTokenException(t)


def t_ANY_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ANY_ignore = ' \t'


class UnsupportedTokenException(Exception):

    def __init__(self, *args):
        self.badToken = args[0]

    def __str__(self):
        return 'Got a bad token "{0}" on line number {1}'.format(self.badToken.value, self.badToken.lineno)


class verilogTokenizer():

    @staticmethod
    def from_string(string):
        tokenizer = verilogTokenizer(string)
        return tokenizer

    @staticmethod
    def from_file(file):
        file = open(file, 'r')
        string = file.read()
        file.close()
        tokenizer = verilogTokenizer(string)
        return tokenizer

    def __init__(self, string):
        self._lexer = lex.lex()
        self._lexer.input(string)
        try:
            self._next_token = self._lexer.next()
        except Exception as error:
            self.error = error
        self._stopitteration = False

    def next(self):
        if hasattr(self, 'error'):
            raise self.error
        current_token = self._next_token
        if self._stopitteration:
            raise StopIteration
        if current_token is None:
            self._stopitteration = True
        try:
            self._next_token = self._lexer.next()
        except StopIteration:
            self._next_token = None
        return current_token

    def peek(self):
        return self._next_token


if __name__ == '__main__':
    # tokenizer = verilogTokenizer.from_file('test.v')
    tokenizer = verilogTokenizer.from_string('4\'b1010\n16\'b1010001111110001')
    while True:
        tok = tokenizer.next()
        if not tok:
            break
        print(tok)