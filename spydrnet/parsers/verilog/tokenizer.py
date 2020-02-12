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
    'DIGIT',
    'HEXDIGIT',
    'SINGLEQUOTE'
    # 'CONSTENT',
    # 'STRING'
    # 'PORT',
    # 'PRIMITIVE',
    # 'ENDPRIMITIVE',
    # 'MODULE_NAME',
    # 'COMMENT',
    # 'MULTILINECOMMENT',
    # 'SOMETHING',
    # 'NAME',
    # 'EQUALS',
    # 'NUMBER',
    # 'PORT_NAME',
)


# states = (
#     ('modulename', 'inclusive'),
#     ('portname', 'inclusive'),
#
# )

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
t_DIGIT = r'[0-9]'
t_HEXDIGIT = r'[a-fA-F]'
t_SINGLEQUOTE = r'\''


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


def t_error(t):
    print("Illegal character '%s' on line %d" % (t.value[0], t.lexer.lineno))
    # outfile.write("Illegal character '%s' on line %d\n" % (t.value[0], t._lexer.lineno))
    t.lexer.skip(1)
    # count.increment_count()

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


class verilogTokenizer():

    def __init__(self, file=None):
        if file is None:
            raise Exception('Tokenizer requires a file')
        self._lexer = lex.lex()
        file = open(file, 'r')
        self._lexer.input(file.read())
        file.close()
        self._next_token = self._lexer.next()

    def next(self):
        current_token = self._next_token
        try:
            self._next_token = self._lexer.next()
        except StopIteration:
            self._next_token = None
        return current_token

    def peek(self):
        return self._next_token


if __name__ == '__main__':
    tokenizer = verilogTokenizer('test.v')
    while True:
        tok = tokenizer.next()
        if not tok:
            break
        print(tok)