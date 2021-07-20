import spydrnet as sdn


TAB = '\t'
NEW_LINE ='\n'
CARRIAGE_RETURN = '\r'
SPACE = ' '
FORM_FEED = '\f'

NUMBERS = {'0','1','2','3','4','5','6','7','8','9'}
LETTERS = {'a','b','c','d','e','f','g','h','i','j',\
    'k','l','m','n','o','p','q','r','s','t','u','v',\
    'w','x','y','z',\
    'A','B','C','D','E','F','G','H',\
    'I','J','K','L','M','N','O','P','Q','R','S','T',\
    'U','V','W','X','Y','Z'}

WHITESPACE = {SPACE, TAB, NEW_LINE, CARRIAGE_RETURN, FORM_FEED}

OPEN_PARENTHESIS = '('
CLOSE_PARENTHESIS = ')'
STAR = '*'
SEMI_COLON = ';'
MODULE = "module"
INPUT = "input"
OUTPUT = "output"
INOUT = "inout"
WIRE = "wire"
REG = "reg"
DOT = "."
OPEN_BRACKET = "["
CLOSE_BRACKET = "]"
OPEN_BRACE = "{"
CLOSE_BRACE = "}"
COLON = ":"
COMMA = ","
OCTOTHORP = "#"
END_MODULE = "endmodule"
PARAMETER = "parameter"
SINGLE_QUOTE = "'"
LOCAL_PARAM = "localparam"
ASSIGN = "assign"
EQUAL = "="
CELL_DEFINE = "`celldefine"
END_CELL_DEFINE = "`endcelldefine"
IFDEF = "`ifdef"
DEFINE = "`define"
ENDIF = "`endif"
ELSIF = '`elsif'
TIMESCALE = '`timescale'
OPEN_BLOCK_COMMENT = "/*"
CLOSE_BLOCK_COMMENT = "*/"
OPEN_LINE_COMMENT = "//"
PRIMITIVE = 'primitive'
END_PRIMITIVE = 'endprimitive'
FUNCTION = 'function'
END_FUNCTION = 'endfunction'
TASK = 'task'
END_TASK = 'endtask'
INTEGER = 'integer'
TRI0 = 'tri0'
TRI1 = 'tri1'
DEFPARAM = 'defparam'

#SET OF ALL THINGS THAT WILL END AN IDENTIFIER IF THEY ARE NOT ESCAPED.
#elif ch in {'(', ')', '.', ',', ';', '[', ']', ':', "{", "}", "*", "#", "`"}:
BREAKER_TOKENS = {SPACE, TAB, NEW_LINE, CARRIAGE_RETURN, FORM_FEED, OPEN_PARENTHESIS, CLOSE_PARENTHESIS,\
    COMMA, SEMI_COLON, OPEN_BRACKET, CLOSE_BRACKET, COLON, OPEN_BRACE, CLOSE_BRACE, STAR, OCTOTHORP,\
        EQUAL, "\\", "\"", "`"} #single quote should not be included here because of 1'b0 type of declarations (these should be one token)

SINGLE_CHARACTER_TOKENS = {OPEN_PARENTHESIS, CLOSE_PARENTHESIS, STAR, SEMI_COLON, DOT, OPEN_BRACKET,\
    CLOSE_BRACKET, OPEN_BRACE, CLOSE_BRACE, COLON, COMMA, COMMA, OCTOTHORP, SINGLE_QUOTE, EQUAL}

PORT_DIRECTIONS = {INPUT, OUTPUT, INOUT}

ALL_VERILOG_TOKENS = {
    TAB,\
    NEW_LINE,\
    CARRIAGE_RETURN,\
    SPACE,\
    FORM_FEED,\
    OPEN_PARENTHESIS,\
    CLOSE_PARENTHESIS,\
    STAR,\
    SEMI_COLON,\
    MODULE,\
    INPUT,\
    OUTPUT,\
    INOUT,\
    WIRE,\
    REG,\
    DOT,\
    OPEN_BRACKET,\
    CLOSE_BRACKET,\
    OPEN_BRACE,\
    CLOSE_BRACE,\
    COLON,\
    COMMA,\
    OCTOTHORP,\
    END_MODULE,\
    PARAMETER,\
    SINGLE_QUOTE,\
    LOCAL_PARAM,\
    ASSIGN,\
    EQUAL,\
    CELL_DEFINE,\
    END_CELL_DEFINE,\
    IFDEF,\
    ENDIF,\
    ELSIF,\
    OPEN_BLOCK_COMMENT,\
    CLOSE_BLOCK_COMMENT,\
    OPEN_LINE_COMMENT,\
    INTEGER,\
    TRI0,\
    TRI1,\
    DEFPARAM
}

def is_valid_identifier(token):
    if token == "":
        return False
    elif token[0] == '\\' and token[-1] == " ":
        for white in WHITESPACE: #there shouldn't be whitespace before the ending space
            if white in token[:-1]:
                return False
        return True
    else:
        if token[0] not in LETTERS and token[0] != "_":
            return False
        for c in token:
            if c not in LETTERS and c not in NUMBERS and c != "_":
                return False
        return True

def is_numeric(token):
    if token == "":
        return False
    for c in token:
        if c not in NUMBERS:
            return False
    return True

def string_to_port_direction(token):
    if token == INPUT:
        return sdn.Port.Direction.IN
    elif token == OUTPUT:
        return sdn.Port.Direction.OUT
    elif token == INOUT:
        return sdn.Port.Direction.INOUT
    else:
        return sdn.Port.Direction.UNDEFINED

