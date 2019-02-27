import re
from collections import deque
import pprint

fi = None
edif_file = "temp.edf"

tokens = deque([])



def read_edif():
    global edif_file
    global json_structure
    open_edif_file(edif_file)
    tokenize_edif()
    close_edif_file()
    parse_edif()
    pp = pprint.PrettyPrinter()
    pp.pprint(json_structure)



def open_edif_file(filename):
    global fi
    fi = open(filename)

def close_edif_file():
    global fi
    fi.close()

class token():
    text = ""
    line = 0
    #values are:
    #string
    #word
    #open parenthesis
    #close parenthesis
    kind = ""
    def __init__(self, text, line):
        #self.text = text
        self.line = line
        if(text[0] == '"'):
            self.text = text.strip('"')
            self.kind = "string"
        elif(text == ')'):
            self.text = text
            self.kind = ")"
        elif(text == '('):
            self.text = text
            self.kind = "("
        else:
            self.text = text
            self.kind = "word"
        #right now we don't check for keywords yet


def tokenize_edif():
    global tokens
    global fi

    token_regex = r'".+?"|[a-zA-Z0-9_]+|[)]|[(]'
    line_number = 0
    for line in fi:
        line_number = line_number +1
        line_tokens = re.findall(token_regex, line)

        for text in line_tokens:
            tokens.append(token(text,line_number))
    #tokens = deque(tokens)

json_structure = dict()
uid_counter = 0
edif_level = 0
last_edif_level = 0
t = None

def parse_edif():
    global tokens
    global json_structure
    global edif_level
    global t
    
    print("parsing edif header...", end = " ")
    json_structure["uid"] = get_uid()
    t = next()
    validate(t.kind, ["("], t)
    edif_level = edif_level + 1
    t = next()
    validate(t.text, ["edif"], t)
    json_structure["name"] = parse_name()
    validate(t.kind, ["("], t)
    metadata = parse_metadata("library")
    json_structure["metadata"] = metadata
    print("done")
    print("parsing edif Libraries...", end = " ")
    libraries = []
    libraries.append(parse_library(json_structure["uid"]))
    json_structure["libraries"] = libraries
    print("done")


def next():
    global edif_level
    global last_edif_level
    last_edif_level = edif_level
    next_t = tokens.popleft()
    if(next_t.kind == "("):
        edif_level = edif_level + 1
    elif(next_t.kind == ")"):
        edif_level = edif_level -1
    #print("\t{}".format(next_t.text))
    return next_t

def validate(real, expected , my_token):
    #debug print
    #print("real {} expected{}".format(my_token.text, expected))
    if(not(real in expected)):
        parse_error(real,expected,my_token)

def parse_error(real, expected, my_token):
    print("parse error on line {}".format(my_token.line))
    print('token not understood in context "{}"'.format(my_token.text))
    print('expected {} recieved {}'.format(expected, real))
    raise SyntaxError('edif syntax error::see print statements')


def get_uid():
    global uid_counter
    temp = uid_counter
    uid_counter = uid_counter +1
    return temp

def parse_name():
    global t
    name = ""
    t = next()
    while t.kind != "(" and t.kind != ")":
        validate(t.kind, ["string", "word"], t)
        name += t.text + " "
        t = next()
    name = name.strip(" ")
    #name is the name of the edif
    #TODO take care of the old name deal.
    return name

def parse_metadata(stop_word):
    global t
    metadata = dict()
    t = next()
    validate(t.kind, ["word"], t)
    while t.text.lower() != stop_word.lower():
        #print(t.text)
        key = t.text
        t = next()
        validate(t.kind, ["word", "string", "("], t)
        value = parse_value_list()
        t = next()
        if(t.kind == ")"):
            metadata[key] = value
            break
        validate(t.kind, ["("], t)
        t = next()
        validate(t.kind, ["word"], t)
        metadata[key] = value
    return metadata

def parse_value_list():
    global t
    value_list = []
    while(t.kind != ")"):
        value_list.append(parse_value())
        t = next()
    if(len(value_list) == 0):
        return ""
    if(len(value_list) == 1):
        return value_list[0]
    else:
        return value_list

def parse_value():
    global t
    if(t.kind == "("):
        #the value is a dictionary
        return parse_dictionary()
    else:
        return t.text

def parse_dictionary():
    global t
    t = next()
    validate(t.kind, ["word", "string"], t)
    key = t.text
    t = next()
    value = parse_value_list()
    out = dict()
    out[key] = value
    return out

def parse_library(parent_uid):
    global t
    library = dict()
    uid = get_uid()
    library["uid"] = uid
    library["parent_uid"] = parent_uid
    validate(t.text.lower(), ["library"], t)
    library["name"] = parse_name()
    validate(t.kind, ["("], t)
    metadata = parse_metadata("cell")
    library["metadata"] = metadata
    cells = []
    while t.text.lower() == "cell":#we are getting a cell
        cells.append(parse_definition(uid))
        validate(t.kind, [")"], t)
        t = next()
        validate(t.kind, [")", "("], t)
        t = next()
    library["definitions"] = cells
    return library

def parse_definition(parent_uid):
    global t
    cell = dict()
    uid = get_uid()
    cell["uid"] = uid
    cell["parent_uid"] = parent_uid
    validate(t.text.lower(), ["cell"], t)
    cell["name"] = parse_name()
    validate(t.kind, ["("], t)
    metadata = parse_metadata("view")
    validate(t.text, ["view"], t)
    metadata["view"] = parse_name()
    validate(t.kind, ["("], t)
    view_meta = parse_metadata("interface")
    metadata["view_metadata"] = view_meta
    cell["metadata"] = metadata

read_edif()