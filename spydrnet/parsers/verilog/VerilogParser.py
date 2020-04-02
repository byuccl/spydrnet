import ply.yacc as yacc
import spydrnet as sdn
# from parsers.verilog.tokenizer import tokens
from spydrnet.parsers.verilog.tokenizer import tokens

direction = sdn.UNDEFINED
lock = False
undefined = dict()
defined = dict()
instance_absolute = None


# TODO Fix port direction, currently not getting direction if direction not declared when interface defined

class verilogParser():
    tokens = tokens

    def __init__(self):
        parser = yacc.yacc(module=self)
        parser.instance_absolute = None
        parser.lock = False
        self.direction = sdn.UNDEFINED
        self.defined = dict()
        self.undefined = dict()
        self.parser = parser

    def parse(self, s):
        return self.parser.parse(s)

    def p_netlist_start(self, p):
        'netlist : finalDefinition'
        netlist = sdn.Netlist()
        library = netlist.create_library()
        library.add_definition(p[1])
        p[0] = netlist

    def p_netlist(self, p):
        'netlist : netlist finalDefinition'
        library = p[1].libraries[0]
        library.add_definition(p[2])
        p[0] = p[1]

    # def p_test(self, p):
    #     'netlist : netlist'
    #     p[0] = p[1]

    def p_final_definition(self, p):
        'finalDefinition : MODULE definition ENDMODULE'
        # definition = sdn.Definition()
        # definition['verilog.identifier'] = p[2]
        #self.defined[p[2]['Verilog.identifier']] = p[2]
        self.defined[p[2].name] = p[2]
        if self.undefined.get(p[2].name) != None:
            self.define_instance(p[2]);
            print("I can finally finish creating some instances")
        else:
            pass
            # definition = p[2]
            # cable = list(definition.get_cables('a'))
            # print()
        direction = sdn.UNDEFINED
        p[0] = p[2]

    def define_instance2(self, definition, instance, connection):
        connectionInfo = connection
        parent = instance.parent
        instance.reference = definition
        instance['Verilog.identifier'] = connectionInfo.instanceName
        instance.name = connectionInfo.instanceName
        if isinstance(connectionInfo.connections, list):
            port_counter = 0
            for i in range(len(connectionInfo.connections)):
                connection = connectionInfo.connections[i]
                increment = True
                if isinstance(connectionInfo.range[i], tuple):
                    if (connectionInfo.range[i][1] > connectionInfo.range[i][0]):
                        increment = False
                    wire_counter = connectionInfo.range[i][1]
                    last = connectionInfo.range[i][0]
                elif isinstance(connectionInfo.range[i], int):
                    wire_counter = connectionInfo.range[i]
                    last = connectionInfo.range[i]
                else:
                    wire_counter = 0
                    last = None
                cable = next(parent.get_cables(connection))
                port = definition.ports[port_counter]
                # TODO make sure port have enough pins for each wire in cable?
                for pin in port.pins:
                    wire = cable.wires[wire_counter]
                    outerPin = instance.pins[pin]
                    wire.connect_pin(outerPin)

                    if increment:
                        wire_counter += 1
                        if last is not None and wire_counter > last:
                            break
                    else:
                        wire_counter -= 1
                        if last is not None and wire_counter < last:
                            break
                port_counter += 1
                for test in cable:
                    pass
        # else:
        #     for connection in connectionInfo.connections:
        #         pass
        pass

    def define_instance(self, definition):
        connections = self.undefined[definition['Verilog.identifier']]
        for connectionInfo in connections:
            instance = connectionInfo.instance
            parent = instance.parent
            instance.reference = definition
            instance['Verilog.identifier'] = connectionInfo.instanceName
            instance.name = connectionInfo.instanceName
            if isinstance(connectionInfo.connections, list):
                port_counter = 0
                for i in range(len(connectionInfo.connections)):
                    connection = connectionInfo.connections[i]
                    increment = True
                    if isinstance(connectionInfo.range[i], tuple):
                        if(connectionInfo.range[i][1] > connectionInfo.range[i][0]):
                            increment = False
                        wire_counter = connectionInfo.range[i][1]
                        last = connectionInfo.range[i][0]
                    elif isinstance(connectionInfo.range[i], int):
                        wire_counter = connectionInfo.range[i]
                        last = connectionInfo.range[i]
                    else:
                        wire_counter = 0
                        last = None
                    cable = next(parent.get_cables(connection))
                    port = definition.ports[port_counter]
                    #TODO make sure port have enough pins for each wire in cable?
                    for pin in port.pins:
                        wire = cable.wires[wire_counter]
                        outerPin = instance.pins[pin]
                        wire.connect_pin(outerPin)

                        if increment:
                            wire_counter += 1
                            if last is not None and wire_counter > last:
                                break
                        else:
                            wire_counter -= 1
                            if last is not None and wire_counter < last:
                                break
                    port_counter += 1
                    for test in cable:
                        pass
            else:
                for connection in connectionInfo.connections:
                    pass
            pass

    def p_definition_start(self, p):
        'definition : SIMPLE_IDENTIFIER portList'
        definition = sdn.Definition()
        definition['Verilog.identifier'] = p[1]
        definition.name = p[1]

        ports = p[2]
        for x in range(len(ports)):
            definition.add_port(ports[x])
            cable = sdn.Cable()
            test = ports[x].name
            cable.create_wires(len(ports[x].pins))
            cable.name = ports[x].name
            for ii in range(len(ports[x].pins)):
                cable.wires[ii].connect_pin(ports[x].pins[ii])
            definition.add_cable(cable)
        p[0] = definition

    def p_definition_add_element(self, p):
        'definition : definition element'
        if (isinstance(p[2], sdn.Cable)):
            p[1].add_cable(p[2])
        elif isinstance(p[2], sdn.Port):
            name = p[2].name
            try:
                port = next(p[1].get_ports(name))
            except Exception as e:
                port = p[2]
                p[1].add_port(p[2])
            cable = p[1].create_cable()
            cable.name = p[2].name
            for pin in p[2].pins:
                wire = cable.create_wire()
                wire.connect_pin(pin)
            print()
        else:
            p[1].add_child(p[2])
            if(self.name in self.defined):
                self.define_instance2(self.defined[self.name], p[2], self.test)
        p[0] = p[1]

    def p_portList_final(self, p):
        'portList : LEFT_PAREN portList RIGHT_PAREN SEMICOLON'
        p[0] = p[2]

    def p_portList(self, p):
        'portList :  portList COMMA port'
        p[1].append(p[3])
        p[0] = p[1]

    def p_portList_first(self, p):
        'portList : port'
        ports = list()
        ports.append(p[1])
        p[0] = ports

    def p_port_input(self, p):
        'port : INPUT SIMPLE_IDENTIFIER'
        if p.parser.lock:
            self.p_error(p)
        port = sdn.Port()
        port.name = p[2]
        port.create_pin()
        direction = sdn.IN
        self.direction = direction
        port.direction = direction
        p[0] = port

    def p_port_inout(self, p):
        'port : INOUT SIMPLE_IDENTIFIER'
        if p.parser.lock:
            self.p_error(self, p)
        port = sdn.Port()
        port.name = p[2]
        port.create_pin()
        self.direction = sdn.INOUT
        port.direction = self.direction
        p[0] = port

    def p_port_output(self, p):
        'port : OUTPUT SIMPLE_IDENTIFIER'
        if p.parser.lock:
            self.p_error(p)
        port = sdn.Port()
        port.name = p[2]
        port.create_pin()
        self.direction = sdn.OUT
        port.direction = self.direction
        p[0] = port

    def p_port_input_range(self, p):
        'port : INPUT range SIMPLE_IDENTIFIER'
        if p.parser.lock:
            self.p_error(p)
        port = sdn.Port()
        port.name = p[3]
        port.create_pins(int(p[2][0]) + 1)
        self.direction = sdn.IN
        port.direction = self.direction
        p[0] = port

    def p_port_inout_range(self, p):
        'port : INOUT range SIMPLE_IDENTIFIER'
        if p.parser.lock:
            self.p_error(p)
        port = sdn.Port()
        port.name = p[3]
        self.direction = sdn.INOUT
        port.direction = self.direction
        p[0] = port

    def p_port_output_range(self, p):
        'port : OUTPUT range SIMPLE_IDENTIFIER'
        if p.parser.lock:
            self.p_error(p)
        port = sdn.Port()
        port.name = p[3]
        self.direction = sdn.OUT
        port.direction = self.direction
        p[0] = port

    def p_port(self, p):
        'port : SIMPLE_IDENTIFIER'
        port = sdn.Port()
        port.name = p[1]
        if (self.direction is sdn.UNDEFINED):
            undefined['Verilog.identifier'] = port
            #p.parser.lock = True
        else:
            port.direction = self.direction
        port.create_pin()
        p[0] = port

    def p_port_range(self, p):
        'port : range SIMPLE_IDENTIFIER'
        port = sdn.Port()
        port.name = p[2]
        if (self.direction is sdn.UNDEFINED):
            undefined['Verilog.identifier'] = port
            #p.parser.lock = True
        else:
            port.direction = self.direction
        port.create_pins(int(p[1][0]) + 1)
        p[0] = port



    def p_range(self, p):
        'range : LEFT_BRACKET NUMBER COLON NUMBER RIGHT_BRACKET'
        range = tuple((int(p[2]), int(p[4])))
        p[0] = range

    def p_index(self, p):
        'index : LEFT_BRACKET NUMBER RIGHT_BRACKET'
        p[0] = int(p[2])

    def p_connections_list(self, p):
        'connections : connections COMMA DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER RIGHT_PAREN'
        if not p.parser.instance_absolute:
            self.p_error(self, p)
        p[1].connections[p[4]] = p[6]
        p[1].range.append(None)
        # p[1].append((p[4], p[6]))
        p[0] = p[1]

    def p_connections_list_positional(self, p):
        'connections : connections COMMA SIMPLE_IDENTIFIER'
        if p.parser.instance_absolute:
            self.p_error(p)
        # p[1].append(p[3])
        p[1].connections.append(p[3])
        p[1].range.append(None)
        p[0] = p[1]

    def p_connections_list_subset(self, p):
        '''connections : connections COMMA DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER  index RIGHT_PAREN
                       | connections COMMA DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER  range RIGHT_PAREN'''
        if not p.parser.instance_absolute:
            self.p_error(self, p)
        p[1].connections[p[4]] = p[6]
        p[1].range.append(p[7])
        p[0] = p[1]

    def p_connections_list_subset_positional(self, p):
        '''connections : connections COMMA SIMPLE_IDENTIFIER index
                       | connections COMMA SIMPLE_IDENTIFIER  range'''
        if p.parser.instance_absolute:
            self.p_error(self, p)
        p[1].connections.append(p[3])
        p[1].range.append(p[4])
        p[0] = p[1]

    def p_connections_first(self, p):
        'connections : DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER RIGHT_PAREN'
        p.parser.instance_absolute = True
        # connections = list()
        # connections.append((p[2], p[4]))
        connections = Connections()
        connections.connections = dict()
        connections.connections[p[2]] = p[4]
        connections.range.append(None)
        p[0] = connections

    def p_connections_first_positional(self, p):
        'connections : SIMPLE_IDENTIFIER'
        p.parser.instance_absolute = False
        # connections = list()
        # connections.append(p[1])
        connections = Connections()
        connections.connections = list()
        connections.connections.append(p[1])
        connections.range.append(None)
        p[0] = connections

    def p_connections_first_subset(self, p):
        '''connections : DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER index RIGHT_PAREN
                       | DOT SIMPLE_IDENTIFIER LEFT_PAREN SIMPLE_IDENTIFIER range RIGHT_PAREN'''
        p.parser.instance_absolute = True
        connections = Connections()
        connections.connections = dict()
        connections.connections[p[2]] = p[4]
        connections.range.append(p[5])
        p[0] = connections

    def p_connections_first_subset_positional(self, p):
        '''connections : SIMPLE_IDENTIFIER index
                       | SIMPLE_IDENTIFIER range '''
        p.parser.instance_absolute = False
        connections = Connections()
        connections.connections = list()
        connections.connections.append(p[1])
        connections.range.append(p[2])
        p[0] = connections

    def p_instance(self, p):
        'instance : SIMPLE_IDENTIFIER SIMPLE_IDENTIFIER LEFT_PAREN connections RIGHT_PAREN SEMICOLON'
        instance = sdn.Instance()
        # After getting all the info reset tracker
        p.parser.instance_absolute = None
        p[4].instanceName = p[2]
        if p[1] in self.defined:
            print("It has been defined so I can fully create the instance")
            test = p[1]
            # self.define_instance2(self.defined[p[1]], instance, p[4])
            self.test = p[4]
            self.name = p[1]
        else:
            print("The instance does not have a definition yet")
            if p[1] not in self.undefined:
                self.undefined[p[1]] = list()
            p[4].defName = p[1]
            p[4].instance = instance
            self.undefined[p[1]].append(p[4])
        p[0] = instance

    def p_element(self, p):
        '''element : wire
                   | instance
                   | port SEMICOLON'''
        p[0] = p[1]

    def p_wire_with_range(self, p):
        'wire : WIRE range SIMPLE_IDENTIFIER SEMICOLON'
        cable = sdn.Cable()
        length = p[2][0] - p[2][1] + 1
        cable.create_wires(length)
        cable.name = p[3]
        p[0] = cable

    def p_wire(self, p):
        'wire : WIRE SIMPLE_IDENTIFIER SEMICOLON'
        cable = sdn.Cable()
        cable.create_wire()
        cable.name = p[2]
        p[0] = cable

    def p_error(self, p):
        print("Syntax error on line %d near " % (p.lexer.lineno))
        exit(-1)

    # def p_empty(self, p):
    #     'empty :'
    #     pass

class Connections():

    def __init__(self):
        self.defName = None
        self.instanceName = None
        self.connections = None
        self.range = list()


if __name__ == '__main__':
    f = open('test.v', 'r')
    s = f.read()
    parser = verilogParser()
    result = parser.parse(s)
    print(result)