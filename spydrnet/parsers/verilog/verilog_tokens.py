
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
IFDEF = "`ifdef"
ENDIF = '`endif'
ELSIF = '`elsif'
TIMESCALE = '`timescale'
OPEN_BLOCK_COMMENT = "/*"
CLOSE_BLOCK_COMMENT = "*/"
OPEN_LINE_COMMENT = "//"

#SET OF ALL THINGS THAT WILL END AN IDENTIFIER IF THEY ARE NOT ESCAPED.
#elif ch in {'(', ')', '.', ',', ';', '[', ']', ':', "{", "}", "*", "#", "`", "'", }:
BREAKER_TOKENS = {SPACE, TAB, NEW_LINE, CARRIAGE_RETURN, FORM_FEED, OPEN_PARENTHESIS, CLOSE_PARENTHESIS, DOT,\
    COMMA, SEMI_COLON, OPEN_BRACKET, CLOSE_BRACKET, COLON, OPEN_BRACE, CLOSE_BRACE, STAR, OCTOTHORP,\
        SINGLE_QUOTE, EQUAL, "\\", "\"", "`"}

SINGLE_CHARACTER_TOKENS = {OPEN_PARENTHESIS, CLOSE_PARENTHESIS, STAR, SEMI_COLON, DOT, OPEN_BRACKET,\
    CLOSE_BRACKET, OPEN_BRACE, CLOSE_BRACE, COLON, COMMA, COMMA, OCTOTHORP, SINGLE_QUOTE, EQUAL}

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
    IFDEF,\
    ENDIF,\
    ELSIF,\
    OPEN_BLOCK_COMMENT,\
    CLOSE_BLOCK_COMMENT,\
    OPEN_LINE_COMMENT,\
}