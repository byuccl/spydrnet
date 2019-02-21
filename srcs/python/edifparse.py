import re
from collections import deque

fi = None
edif_file = "fake.edf"

tokens = deque([])



def read_edif():
    global edif_file
    global json_structure
    open_edif_file(edif_file)
    tokenize_edif()
    close_edif_file()
    parse_edif()
    print(json_structure)



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
    #key
    #word
    #open_parenthesis
    #close_parenthesis
    kind = ""
    def __init__(self, text, line):
        self.text = text
        self.line = line
        if(text[0] == '"'):
            self.kind = "string"
        elif(text == ')'):
            self.kind = ")"
        elif(text == '('):
            self.kind = "("
        else:
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
    metadata = dict()
    while t.text != "Library":
        #print("looping")
        p = make_pair()
        metadata[p[0]] = p[1]
        t = next()


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

def make_pair():
    global t
    val = None
    key = None
    val_out = deque([])
    validate(t.kind, ["("],t)
    t = next()
    validate(t.kind, ["string", "word"], t)
    key = t.text
    t = next()
    validate(t.kind, ["string", "word", "("], t)
    while(True):
        if(t.kind == "("):
            temp = make_pair()
            val = dict()
            val[temp[0]] = temp[1]
        elif(t.kind == ")"):
            break
        else:
            val = t.text
        val_out.append(val)
        t = next()
    #print(key, val_out)
    return key,val_out



read_edif()