import ply.yacc as yacc
import spydrnet as sdn
from parsers.verilog.tokenizer import tokens

direction = sdn.UNDEFINED
lock = False
undefined = dict()
defined = dict()
instance_absolute = None

#TODO Fix port direction, currently not getting direction if direction not declared when interface defined

def p_netlist(p):
    'nestlist : finalDefinition'
    netlist = sdn.Netlist()
    library = netlist.create_library()
    library.add_definition(p[1])
    p[0] = netlist

# def p_test(p):
#     'netlist : netlist'
#     p[0] = p[1]

def p_final_definition(p):
    'finalDefinition : MODULE definition ENDMODULE'
    # definition = sdn.Definition()
    # definition['verilog.identifier'] = p[2]
    direction = sdn.UNDEFINED
    p[0] = p[2]

def p_definition_start(p):
    'definition : SIMPLE_IDENTIFIER portList'
    definition = sdn.Definition()
    definition['Verilog.identifier'] = p[1]
    for x in range(len(p[2])):
        definition.add_port(p[2][x])
    p[0] = definition

def p_definition_add_element(p):
    'definition : definition element'
    if (isinstance(p[2], sdn.Cable)):
        p[1].add_cable(p[2])
    p[0] = p[1]

def p_portList_final(p):
    'portList : LEFT_PAREN portList RIGHT_PAREN SEMICOLON'
    p[0] = p[2]

def p_portList(p):
    'portList :  portList COMMA port'
    p[1].append(p[3])
    p[0] = p[1]

def p_portList_first(p):
    'portList : port'
    ports = list()
    ports.append(p[1])
    p[0] = ports

def p_port_input(p):
    'port : INPUT SIMPLE_IDENTIFIER'
    if p.parser.lock:
        p_error(p)
    port = sdn.Port()
    port['Verilog.identifier'] = p[2]
    port.create_pin()
    direction = sdn.IN
    p.parser.direction = direction
    port.direction = direction
    p[0] = port

def p_port_inout(p):
    'port : INOUT SIMPLE_IDENTIFIER'
    if p.parser.lock:
        p_error(p)
    port = sdn.Port()
    port['Verilog.identifier'] = p[2]
    port.create_pin()
    direction = sdn.INOUT
    port.direction = direction
    p[0] = port

def p_port_output(p):
    'port : OUTPUT SIMPLE_IDENTIFIER'
    if p.parser.lock:
        p_error(p)
    port = sdn.Port()
    port['Verilog.identifier'] = p[2]
    port.create_pin()
    direction = sdn.OUT
    port.direction = direction
    p[0] = port

def p_port_input_range(p):
    'port : INPUT range SIMPLE_IDENTIFIER'
    if p.parser.lock:
        p_error(p)
    port = sdn.Port()
    port['Verilog.identifier'] = p[3]
    port.create_pins(int(p[2][0]) + 1)
    direction = sdn.IN
    port.direction = direction
    p[0] = port

def p_port_inout_range(p):
    'port : INOUT range SIMPLE_IDENTIFIER'
    if p.parser.lock:
        p_error(p)
    port = sdn.Port()
    port['Verilog.identifier'] = p[3]
    direction = sdn.INOUT
    port.direction = direction
    p[0] = port

def p_port_output_range(p):
    'port : OUTPUT range SIMPLE_IDENTIFIER'
    if p.parser.lock:
        p_error(p)
    port = sdn.Port()
    port['Verilog.identifier'] = p[3]
    direction = sdn.OUT
    port.direction = direction
    p[0] = port

def p_port(p):
    'port : SIMPLE_IDENTIFIER'
    port = sdn.Port()
    port['Verilog.identifier'] = p[1]
    if (p.parser.direction is sdn.UNDEFINED):
        undefined['Verilog.identifier'] = port
        p.parser.lock = True
    else:
        port.direction = p.parser.direction
    p[0] = port


def p_range(p):
    'range : LEFT_BRACKET NUMBER COLON NUMBER RIGHT_BRACKET'
    range = tuple((int(p[2]), int(p[4])))
    p[0] = range


def p_index(p):
    'index : LEFT_BRACKET NUMBER RIGHT_BRACKET'
    p[0] = int(p[2])


def p_connections_list(p):
    'connections : connections COMMA DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER RIGHT_PAREN'
    if not p.parser.instance_absolute:
        p_error(p)
    p[1].append((p[4], p[6]))
    p[0] = p[1]

def p_connections_list_positional(p):
    'connections : connections COMMA SIMPLE_IDENTIFIER'
    if p.parser.instance_absolute:
        p_error(p)
    p[1].append(p[3])
    p[0] = p[1]

def p_connections_list_subset(p):
    '''connections : connections COMMA DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER  index RIGHT_PAREN
                   | connections COMMA DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER  range RIGHT_PAREN'''
    if not p.parser.instance_absolute:
        p_error(p)
    p[1].append((p[4], p[6], p[7]))
    p[0] = p[1]

def p_connections_list_subset_positional(p):
    '''connections : connections COMMA SIMPLE_IDENTIFIER index
                   | connections COMMA SIMPLE_IDENTIFIER  range'''
    if p.parser.instance_absolute:
        p_error(p)
    p[1].append((p[3], p[4]))
    p[0] = p[1]


def p_connections_first(p):
    'connections : DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER RIGHT_PAREN'
    p.parser.instance_absolute = True
    connections = list()
    connections.append((p[2], p[4]))
    p[0] = connections

def p_connections_first_positional(p):
    'connections : SIMPLE_IDENTIFIER'
    p.parser.instance_absolute = False
    connections = list()
    connections.append(p[1])
    p[0] = connections

def p_connections_first_subset(p):
    '''connections : DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER index RIGHT_PAREN
                   | DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER range RIGHT_PAREN'''
    p.parser.instance_absolute = True
    connections = list()
    connections.append((p[2], p[4], p[5]))
    p[0] = connections

def p_connections_first_subset_positional(p):
    '''connections : SIMPLE_IDENTIFIER index
                   | SIMPLE_IDENTIFIER range '''
    p.parser.instance_absolute = False
    connections = list()
    connections.append((p[1], p[2]))
    p[0] = connections


def p_instance(p):
    'instance : SIMPLE_IDENTIFIER SIMPLE_IDENTIFIER LEFT_PAREN connections RIGHT_PAREN SEMICOLON'
    instance = sdn.Instance
    # After getting all the info reset tracker
    p.parser.instance_absolute = None
    p[0] = instance


def p_element(p):
    '''element : wire
               | instance '''
    p[0] = p[1]


def p_wire_with_range(p):
    'wire : WIRE range SIMPLE_IDENTIFIER SEMICOLON'
    cable = sdn.Cable()
    length = p[2][0] - p[2][1] + 1
    cable.create_wires(length)
    cable['Verilog.identifier'] = p[3]
    print()
    p[0] = cable


def p_wire(p):
    'wire : WIRE SIMPLE_IDENTIFIER SEMICOLON'
    cable = sdn.Cable()
    cable.create_wire()
    cable['Verilog.identifier'] = p[2]
    print()
    p[0] = cable


def p_error(p):
    print("Syntax error on line %d near " %(p.lexer.lineno))
    exit(-1)

# def p_empty(p):
#     'empty :'
#     pass

parser = yacc.yacc()

if __name__ == '__main__':
    f = open('test.v', 'r')
    s = f.read()
    parser.direction = sdn.UNDEFINED
    parser.instance_absolute = None
    parser.lock = False
    result = parser.parse(s)
    print(result)