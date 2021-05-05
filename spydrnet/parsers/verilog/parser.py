#Copyright 2021 Dallin Skouson, BYU CCL
#please see the BYU CCl SpyDrNet license file for terms of usage.


from spydrnet.parsers.verilog.tokenizer import VerilogTokenizer
import spydrnet.parsers.verilog.verilog_tokens as vt
from spydrnet.ir import Netlist, Library, Definition, Port, Cable, Instance, OuterPin
from spydrnet.plugins import namespace_manager
import spydrnet as sdn

from functools import reduce
import re


class VerilogParser:
    '''
    Parse verilog files into spydrnet.

    Higher level functions will always peek when deciding what lower level function to call.
    within your own function call next instead to keep the flow moving.

    the first token to expect in a function will be the token that starts that construct.
    '''

    '''some notes:

    port aliasing: .my_in_port({bit1, bit2, bit3, bit4})
    Port aliasing happens in some Xlinix generated netlists
    the port name for example my_in_port is used by all refernces outside the module
    the names bit1, bit2, bit3, bit4 are used interally including for declaring the definition
    So how do I know that the concatenated cables line up with the port?
    I plan to have other port creation methods create a cable with the same name as the port (to allow for mapping to instances directly)
    in the case of an alias the cable name will just be different than the port name.
    options not chosen: have the ports and the cables be assigned

    pass
    todo: need to setup a way to let the ports lower index be floating until it's defined later. when a blackbox is instantiated
    that has a port that is perhaps not 0 lower indexed then the current system may do something wrong when the port is given its proper
    lower index. for now, it is required that all ports lower indicies are 0 

    assignments can be kept in an assignment dictionary that will map a name to a group of wires like a cable. 
    This will take the shape of a class that is name with a group of wires. kindof like a cable but the wires will
    all need to belong to another cable. this is used uniquely for lookups and will not remain in the
    intermediate representation

    on compose assignments can be generated when there would otherwise be a concatenation operator in a port map
    
    '''

    #########################################################
    ##helper classes
    #########################################################

    


    class AssignmentManager:

        class AssignmentCable:

            '''
            assignments are basically a name mapped to some wires.
            '''

            def __init__(self, wires = [], lower_index = 0):
                self.wires = wires
                self.lower_index = wires

            def get_wires(self, left, right):
                '''
                get the wires out of the wires list that correspond to the left and right
                indicies.
                '''
                index = None
                if left is not None and right is not None:
                    l = left - self.lower_index
                    r = right - self.lower_index + 1
                    return self.wires[l:r]
                elif right is not None:
                    index = right
                elif left is not None:
                    index = left
                else:
                    return self.wires
                return [self.wires[index]]
        
        def __init__(self):
            self.assignment_dict = dict()
        
        def is_assigned(self, name):
            return name in self.assignment_dict
        
        def create_assign(self, name, wires, lower_index):
            aca = self.AssignmentCable(wires, lower_index)
            self.assignment_dict[name] = aca

        def get_wires(self, name, left, right):
            self.assignment_dict[name].get_wires(left, right)

    class CableSuggestionHolder:

        def __init__(self):
            self.defined = set()

        def clear(self):
            self.defined = set()

        def define_cable(self, cable):
            self.defined.add(cable)

        def is_defined(self, cable):
            return cable in self.defined


    class BlackboxHolder:
        
        def __init__(self):
            self.name_lookup = dict()
            self.defined = set()
        
        def get_blackbox(self, name):
            '''creates or returns the black box based on the name'''
            if name in self.name_lookup:
                return self.name_lookup[name]
            else:
                definition = sdn.Definition()
                definition.name = name
                self.name_lookup[name] = definition
                return definition

        def define(self, name):
            '''adds the name to the defined set'''
            self.defined.add(self.name_lookup[name])

        def get_undefined_blackboxes(self):
            '''return an iterable of all undefined blackboxes'''
            undef = set()
            for v in self.name_lookup.values():
                if v not in self.defined:
                    undef.add(v)
            return undef

    # class PortSuggestionHolder:

    #     def __init__(self):
    #         self.port_suggested = set()
    #         self.port_defined = set()
        
    #     def is_defined(self, port):
    #         return port in self.port_defined

    #     def suggest_port(self, port):
    #         if port not in self.port_defined:
    #             self.port_suggested.add(port)
        
    #     def is_suggested(self, port):
    #         return port in self.port_suggested

    #     def define_port(self, port):
    #         self.port_defined.add(port)
    #         if port in self.port_suggested:
    #             self.port_suggested.remove(port)
            

    #######################################################
    ##setup functions
    #######################################################
    @staticmethod
    def from_filename(filename):
        parser = VerilogParser()
        parser.filename = filename
        return parser

    @staticmethod
    def from_file_handle(file_handle):
        parser = VerilogParser()
        parser.filename = file_handle
        return parser

    def __init__(self):
        self.filename = None
        self.tokenizer = None

        self.netlist = None
        self.current_library = None
        self.current_definition = None
        self.current_instance = None

        self.primitives = None
        self.work = None

        self.blackbox_holder = self.BlackboxHolder()
        self.assignment_manager = self.AssignmentManager()
        #self.port_suggestion_holder = self.PortSuggestionHolder()
          
    def parse(self):
        ''' parse a verilog netlist represented by verilog file

            verilog_file can be a filename or stream
        '''
        self.initialize_tokenizer()
        ns_default = namespace_manager.default
        namespace_manager.default = "DEFAULT"
        self.parse_verilog()
        namespace_manager.default = ns_default
        self.tokenizer.__del__()
        return self.netlist

    def initialize_tokenizer(self):
        self.tokenizer = VerilogTokenizer(self.filename)

    def peek_token(self):
        token = self.peek_token_remove_comments()
        if token[0] == '`':
            t_split = token.split(maxsplit=1)
            if len(t_split)> 1 and t_split[0] in [vt.IFDEF]:
                while t_split[0] != vt.ENDIF:
                    token = self.next_token_remove_comments()
                    t_split = token.split(maxsplit=1)
                token = self.peek_token_remove_comments()
            if len(t_split) > 1 and t_split[0] == vt.DEFINE:
                assert False, self.error_string("define not supported", "assumes all macros are undefined", vt.DEFINE)
        return token

    def next_token(self):
        token = self.next_token_remove_comments()
        if token[0] == '`':
            t_split = token.split(maxsplit=1)
            if len(t_split)> 1 and t_split[0] in [vt.IFDEF]:
                while t_split[0] != vt.ENDIF:
                    token = self.next_token_remove_comments()
                    t_split = token.split(maxsplit=1)
                token = self.next_token_remove_comments()
            if len(t_split) > 1 and t_split[0] == vt.DEFINE:
                assert False, self.error_string("define not supported", "assumes all macros are undefined", vt.DEFINE)
        return token

    def peek_token_remove_comments(self):
        '''peeks from the tokenizer this wrapper function exists to skip comment tokens'''
        token = self.tokenizer.peek()
        while len(token) >= 2 and token[0] == "/" and (token[1] == "/" or token[1] == "*"):
            #this is a comment token skip it
            self.tokenizer.next()
            token = self.tokenizer.peek()
        return token

    def next_token_remove_comments(self):
        '''peeks from the tokenizer this wrapper function exists to skip comment tokens'''
        token = self.tokenizer.next()
        while len(token) >= 2 and (token[0:1] == vt.OPEN_LINE_COMMENT or token[0:1] == vt.OPEN_BLOCK_COMMENT):
            #this is a comment token, skip it
            token = self.tokenizer.next()
        return token
        # token = self.peek_token()
        # self.tokenizer.next()
        # return token

    #######################################################
    ##parsing functions
    #######################################################

    def parse_verilog(self):
        self.netlist = sdn.Netlist()
        self.work = self.netlist.create_library("work")
        self.primitives = self.netlist.create_library("SDN.verilog_primitives")
        self.current_library = self.work

        preprocessor_defines = set()
        star_properties = dict()
        time_scale = None
        primitive_cell = False

        while self.tokenizer.has_next():
            token = self.peek_token()
            if token.split(maxsplit = 1)[0] == vt.CELL_DEFINE:
                primitive_cell = True
                self.current_library = self.primitives
                #token = token.split(maxsplit = 1)[1]
                token = self.next_token()
            elif token.split(maxsplit = 1)[0] == vt.END_CELL_DEFINE:
                primitive_cell = False
                self.current_library = self.work
                #token = token.split(maxsplit = 1)[1]
                token = self.next_token()

            elif token == vt.MODULE:
                if primitive_cell:
                    self.parse_primitive()
                else:
                    self.parse_module()
                #go ahead and set the extra metadata that we collected to this point
                if time_scale is not None:
                    self.current_definition["Verilog.TimeScale"] = time_scale
                if len(star_properties.keys()) > 0:
                    self.current_definition["Verilog.StarProperties"] = star_properties
                    star_properties = dict()
            
            elif token == vt.PRIMITIVE:
                self.parse_primitive()
                if time_scale is not None:
                    self.current_definition["Verilog.TimeScale"] = time_scale
                if len(star_properties.keys()) > 0:
                    self.current_definition["Verilog.StarProperties"] = star_properties
                    star_properties = dict()
            
            elif token == vt.DEFINE:
                assert False, "Currently `define is not supported"
            elif token == vt.IFDEF:
                token = self.next_token()
                token = self.next_token()
                if token not in preprocessor_defines:
                    while token != vt.ENDIF:
                        token = self.next_token()
            elif token == vt.OPEN_PARENTHESIS:
                k,v = self.parse_star_property()
                star_properties[k] = v
                
            elif token.split(maxsplit = 1)[0] == vt.TIMESCALE:
                token = self.next_token()
                time_scale = token.split(maxsplit = 1)[1]
            else:
                pass       
                assert False, self.error_string("something at the top level of the file", "got unexpected token", token)
        
        self.add_blackbox_definitions()

        return self.netlist

    def add_blackbox_definitions(self):
        self.current_library = self.primitives
        for d in self.blackbox_holder.get_undefined_blackboxes():
            d["VERILOG.primitive"] = True
            self.current_library.add_definition(d)

    def parse_primitive(self):
        '''simply skips the whole definition:'''
        token = self.next_token()
        if token == vt.MODULE:
            while token != vt.END_MODULE:
                token = self.next_token()

        elif token == vt.PRIMITIVE:
            while token != vt.END_PRIMITIVE:
                token = self.next_token()
        #to use these definitions uncomment the following
        # '''similar to parse module but it will only look for the inputs and outputs to get an idea of how those things look'''

        # token = self.next_token()
        # assert token == vt.MODULE or token == vt.PRIMITIVE, self.error_string(vt.MODULE, "to begin module statement", token)
        # token = self.next_token()
        # assert vt.is_valid_identifier(token), self.error_string("identifier", "not a valid module name", token)
        # name = token

        # definition = self.blackbox_holder.get_blackbox(name)
        # self.blackbox_holder.define(name)
        # self.current_library.add_definition(definition)
        # self.current_definition = definition

        # #uses the same header parser because the primitives and regular cells have the same header.
        # self.parse_module_header()


        # self.parse_primitive_body()



    def parse_primitive_body(self):
        ''' just look for port information'''
        
        token = self.peek_token()

        while token != vt.END_MODULE and token != vt.END_PRIMITIVE:
            token = self.peek_token()
            if token == vt.FUNCTION:
                while token != vt.END_FUNCTION:
                    token = self.next_token()
            if token in vt.PORT_DIRECTIONS:
                self.parse_port_declaration(dict())
            else:
                token = self.next_token()

    def parse_module(self):
        
        token = self.next_token()
        assert token == vt.MODULE, self.error_string(vt.MODULE, "to begin module statement", token)
        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("identifier", "not a valid module name", token)
        name = token

        definition = self.blackbox_holder.get_blackbox(name)
        self.blackbox_holder.define(name)
        self.current_library.add_definition(definition)
        self.current_definition = definition
        if self.netlist.top_instance is None:
            self.netlist.top_instance = sdn.Instance()
            self.netlist.top_instance.reference = definition

        self.parse_module_header()

        self.parse_module_body()

    
    def parse_module_header(self):
        '''parse a module header and add the parameter dictionary and port list to the current_definition'''
        token = self.peek_token()
        if token == "#":
            self.parse_module_header_parameters()

        token = self.peek_token()
        assert token == "(", self.error_string("(", "for port mapping", token)

        self.parse_module_header_ports()

        token = self.next_token()
        assert token == vt.SEMI_COLON, self.error_string(vt.SEMI_COLON, "to end the module header section", token)


    def parse_module_header_parameters(self):
        '''parse a parameter block in a module header, add all parameters to the current definition'''
        token = self.next_token()
        assert token == vt.OCTOTHORP, self.error_string(vt.OCTOTHORP, "to begin parameter map", token)
        token = self.next_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "to begin parameter map", token)

        token = self.next_token()

        parameter_dictionary = dict()

        while token != ")":
            assert token == vt.PARAMETER, self.error_string(vt.PARAMETER, "parameter declaration", token) #this is happening twice for all but the first one.. could simplify

            key = ""
            token = self.peek_token()
            if token == vt.OPEN_BRACKET:
                left, right = self.parse_brackets()
                if right != None:
                    key = "[" + str(left) + ":" + str(right) + "] "
                else:
                    key = "[" + str(left) + "] "

            token = self.next_token()
            assert vt.is_valid_identifier(token), self.error_string('identifer', "in parameter list", token)
            key += token

            token = self.next_token()
            assert token == "="

            token = self.next_token()
            #not really sure what to assert here.
            value = token

            parameter_dictionary[key] = value
            token = self.next_token()
            if token == vt.COMMA: #just keep going
                token = self.next_token()
                assert token == vt.PARAMETER, self.error_string(vt.PARAMETER, "after comma in parameter map", token)
            else:
                assert token == vt.CLOSE_PARENTHESIS, self.error_string(vt.CLOSE_PARENTHESIS, "to end parameter declarations", token)

        self.set_definition_parameters(self.current_definition, parameter_dictionary)


    def parse_module_header_ports(self):
        '''parse port declarations in the module header and add them to the definition'''
        token = self.next_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "to begin port declarations", token)

        token = self.peek_token()

        port_list = []

        while token != ")":
            #the first token could be a name or input output or inout
            if token == ".":
                self.parse_module_header_port_alias()
            else:
                self.parse_module_header_port()
            token = self.next_token()
            if token != vt.CLOSE_PARENTHESIS:
                assert token == vt.COMMA, self.error_string(vt.COMMA, "to separate port declarations", token)
                token = self.peek_token()
        
    def parse_module_header_port_alias(self):
        '''parse the port alias portion of the module header
        this parses the port alias section so that the port name is only a port and the mapped wires are the cables names that connect to that port.

        this requires that the cables names be kept in a dictionary to allow for setting the direction when the direction is given to the internal port names.

        example syntax
        .canale({\\canale[3] ,\\canale[2] ,\\canale[1] ,\\canale[0] }),'''

        token = self.next_token()
        assert token == vt.DOT, self.error_string(vt.DOT, "for port aliasing", token)
        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("identifier", "for port in port aliasing", token)
        name = token
        
        token = self.next_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "parethesis to enclose port aliasing", token)

        wires = self.parse_cable_concatenation()

        token = self.next_token()
        assert token == vt.CLOSE_PARENTHESIS, self.error_string(vt.CLOSE_PARENTHESIS, "parethesis to end port aliasing construct", token)

        port = self.create_or_update_port(name, left_index = len(wires)-1, right_index = 0)
        
        #connect the wires to the pins

        assert len(port.pins) == len(wires), "Internal Error: the pins in a created port and the number of wires the aliased cable do not match up"

        for i in range(len(port.pins)):
            wires[i].connect_pin(port.pins[i])
            #self.port_alias_manager.add_wire(wires[i], port.pins[i])

    
    def parse_cable_concatenation(self):
        '''parse a concatenation structure of cables, create the cables mentioned, and deal with indicies
        return a list of ordered wires that represents the cable concatenation
        example syntax
        {wire1, wire2, wire3, wire4}'''
        token = self.next_token()
        assert token == vt.OPEN_BRACE, self.error_string(vt.OPEN_BRACE, "to start cable concatenation", token)
        token = self.peek_token()
        wires = []
        while token != vt.CLOSE_BRACE:
            cable, left, right = self.parse_variable_instantiation()
            wires_temp = self.get_wires_from_cable(cable, left, right)
            for w in wires_temp:
                wires.append(w)
            token = self.next_token()
            if token != vt.COMMA:
                assert token == vt.CLOSE_BRACE, self.error_string(vt.CLOSE_BRACE, "to end cable concatenation", token)
            
        return wires

    def parse_module_header_port(self):
        '''parse the port declaration in the module header'''
        token = self.peek_token()
        direction = None
        if token in vt.PORT_DIRECTIONS:
            token = self.next_token()
            direction = vt.string_to_port_direction(token)
            token = self.peek_token()
        
        left = None
        right = None
        if token == vt.OPEN_BRACKET:
            left, right = self.parse_brackets()
        
        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("identifier", "for port declaration", token)
        name = token
        port = self.create_or_update_port(name,left_index = left, right_index = right, direction = direction)
        cable = self.create_or_update_cable(name, left_index = left, right_index = right)
        
        #wire together the cables and the port
        assert len(port.pins) == len(cable.wires), "Internal Error: the pins in a created port and the number of wires in it's cable do not match up"
        for i in range(len(port.pins)):
            cable.wires[i].connect_pin(port.pins[i])

    def parse_module_body(self):
        '''
        parse through a module body

        module bodies consist of port declarations,
        wire and reg declarations
        and instantiations

        expects port declarations to start with the direction and then include the cable type if provided
        '''
        direction_tokens = [vt.INPUT, vt.OUTPUT, vt.INOUT]
        variable_tokens = [vt.WIRE, vt.REG]
        token = self.peek_token()
        params = dict()
        while token != vt.END_MODULE:
            if token in direction_tokens:
                self.parse_port_declaration(params)
                params = dict()
            elif token in variable_tokens:
                self.parse_cable_declaration(params)
                params = dict()
            elif vt.is_valid_identifier(token):
                self.parse_instantiation(params)
                params = dict()
            elif token == vt.OPEN_PARENTHESIS:
                k,v = self.parse_star_property()
                params[k] = v
            else:
                assert False, self.error_string("direction, reg, wire, star_properties, or instance identifier", "in module body", token)

            token = self.peek_token()
        
        token = self.next_token()
        assert token == vt.END_MODULE, self.error_string(vt.END_MODULE, "to end the module body", token)

    def parse_port_declaration(self, properties):
        '''parse the port declaration post port list.'''
        token = self.next_token()
        assert token in vt.PORT_DIRECTIONS, self.error_string("direction keyword", "to define port", token)
        direction = vt.string_to_port_direction(token)
        
        token = self.peek_token()
        if token in [vt.REG, vt.WIRE]:
            var_type = token
            token = self.next_token()
        else:
            var_type = None

        token = self.peek_token()
        if token == vt.OPEN_BRACKET:
            left, right = self.parse_brackets()
        else:
            left = None
            right = None
        
        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("port identifier", "identify port", token)
        names = []
        names.append(token)

        token = self.next_token()
        while token == vt.COMMA:
            token = self.next_token()
            names.append(token)
            token = self.next_token()

        assert token == vt.SEMI_COLON, self.error_string(vt.SEMI_COLON, "to end port declaration", token)

        for name in names:    
            cable = self.create_or_update_cable(name, left_index = left, right_index = right, var_type = var_type)

            port_list = self.get_all_ports_from_wires(self.get_wires_from_cable(cable, left, right))
            
            assert len(port_list) > 0, self.error_string("port name defined in the module header", "to declare a port", cable.name)

            for p in port_list:
                port = self.create_or_update_port(p.name, left_index = left, right_index = right, direction = direction)
                port["Verilog.StarProperties"] = properties

    def parse_cable_declaration(self, properties):
        token = self.next_token()
        assert token in [vt.REG, vt.WIRE], self.error_string("reg or wire", "for cable declaration", token)
        var_type = token

        token = self.peek_token()
        if token == vt.OPEN_BRACKET:
            left, right = self.parse_brackets()
        else:
            left = None
            right = None

        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("valid cable identifier", "identify the cable", token)
        name = token

        cable = self.create_or_update_cable(name, left_index = left, right_index = right, var_type = var_type)
        cable["Verilog.StarProperties"] = properties

        token = self.next_token()
        assert token == vt.SEMI_COLON, self.error_string(vt.SEMI_COLON, "to end cable declaration", token)

    def parse_instantiation(self, properties):
        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("module identifier", "for instantiation", token)
        def_name = token

        parameter_dict = dict()
        token = self.peek_token()
        if token == vt.OCTOTHORP:
            parameter_dict = self.parse_parameter_mapping()

        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("instance name", "for instantiation", token)
        name = token

        token = self.peek_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "to start port to cable mapping", token)

        instance = self.current_definition.create_child()
        self.current_instance = instance

        instance.name = name
        instance.reference = self.blackbox_holder.get_blackbox(def_name)
        instance["Verilog.StarProperties"] = properties

        self.parse_port_mapping()

        self.set_instance_parameters(instance, parameter_dict)

        token = self.next_token()
        assert token == vt.SEMI_COLON, self.error_string(vt.SEMI_COLON, "to end instatiation", token)
        
    def parse_parameter_mapping(self):
        params = dict()
        token = self.next_token()
        assert token == vt.OCTOTHORP, self.error_string(vt.OCTOTHORP, "to begin parameter mapping", token)

        token = self.next_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "after # to begin parameter mapping", token)

        while token != vt.CLOSE_PARENTHESIS:
            k,v = self.parse_parameter_map_single()
            params[k] = v
            token = self.next_token()
            assert token in [vt.CLOSE_PARENTHESIS, vt.COMMA], self.error_string(vt.COMMA + " or " + vt.CLOSE_PARENTHESIS, "to separate parameters or end parameter mapping", token)

        assert token == vt.CLOSE_PARENTHESIS, self.error_string(vt.CLOSE_PARENTHESIS, "to terminate ", result)

        return params

    def parse_parameter_map_single(self):
        #syntax looks like .identifier(value)
        token = self.next_token()
        assert token == vt.DOT, self.error_string(vt.DOT, "to begin parameter mapping", token)
        
        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("valid parameter identifier", "in parameter mapping", token)
        k = token

        token = self.next_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "after identifier in parameter mapping", token)
        
        token = self.next_token()
        v = token

        token = self.next_token()
        assert token == vt.CLOSE_PARENTHESIS, self.error_string(vt.CLOSE_PARENTHESIS, "to close the parameter mapping value", token)

        return k, v

    def parse_port_mapping(self):
        token = self.next_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "to start the port mapping", token)

        while token != vt.CLOSE_PARENTHESIS:
            self.parse_port_map_single()
            token = self.next_token()
            assert token in [vt.COMMA, vt.CLOSE_PARENTHESIS], self.error_string(vt.COMMA + " or " + vt.CLOSE_PARENTHESIS, "between port mapping elements or to end the port mapping", token)

    def parse_port_map_single(self):
        '''acutally does the mapping of the pins'''
        token = self.next_token()
        assert token == vt.DOT, self.error_string(vt.DOT, "to start a port mapping instance", token)

        token = self.next_token()
        assert vt.is_valid_identifier(token), self.error_string("valid port identifier", "for port in instantiation port map", token)
        port_name = token

        token = self.next_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "to encapsulate cable name in port mapping", token)

        token = self.peek_token()
        # cable = None
        # left = None
        # right = None
        if token != vt.CLOSE_PARENTHESIS:
            # assert vt.is_valid_identifier(token), self.error_string("valid cable identifier", "cable name to map in port mapping", token)
            # cable_name = token
            # token = self.peek_token()
            # left = None
            # right = None
            # if token == vt.OPEN_BRACKET:
            #     left, right = self.parse_brackets()
            # cable = self.create_or_update_cable(cable_name, left_index = left, right_index = right)
            # token = self.next_token()

            # wires = self.get_wires_from_cable(cable, left, right)
            

            if token == vt.OPEN_BRACE:
                wires = self.parse_cable_concatenation()
            else:
                cable, left, right = self.parse_variable_instantiation()
                wires = self.get_wires_from_cable(cable, left, right)

            pins = self.create_or_update_port_on_instance(port_name, len(wires))


            assert len(pins) >= len(wires), self.error_string("pins length to match or exceed cable.wires length", "INTERNAL ERROR", str(len(pins)) + "!=" + str(len(wires)))

            #there can be unconnected pins at the end of the port.
            for i in range(len(wires)):
                wires[i].connect_pin(pins[i])
            
            token = self.next_token()

        else:
            #the port is intentionally left unconnected.
            self.create_or_update_port_on_instance(port_name, 1)

        assert token == vt.CLOSE_PARENTHESIS, self.error_string(vt.CLOSE_PARENTHESIS, "to end cable name in port mapping", token)

    # def parse_variable_declaration(self):
    #     direction_tokens = [vt.INPUT, vt.OUTPUT, vt.INOUT]
    #     type_tokens = [vt.REG, vt.WIRE]
    #     token = self.next_token()
    #     name = None
    #     direction = None
    #     var_type = None
    #     left = None
    #     right = None

    #     if token in direction_tokens:
    #         direction = self.convert_string_to_port_direction(token)
    #     elif token in type_tokens:
    #         var_type = token
    #     else:
    #         assert False, self.error_string("port direction or wire or reg", "to start variable declaration", token)

    #     token = self.peek_token()

    #     if token in direction_tokens:
    #         direction = self.convert_string_to_port_direction(token)
    #         self.next_token() #consume the peeked token
    #     elif token in type_tokens:
    #         var_type = token
    #         self.next_token() #consume the peeked token

    #     token = self.peek_token()

    #     if token == vt.OPEN_BRACKET:
    #         left, right = self.parse_brackets()

    #     token = self.next_token()
    #     name = token

    #     token = self.next_token()
    #     assert token in [vt.COMMA, vt.SEMI_COLON, vt.CLOSE_PARENTHESIS],\
    #         self.error_string("; , or )", "to terminate variable declaration", token)

    #     cable = self.create_or_update_cable(name, left_index = left, right_index = right, var_type = var_type)
    #     if direction is not None:
    #         port = self.create_or_update_port(name, left_index = left, right_index = right, direction = direction)
    #     else:
    #         port = None
        
    #     return cable, port
            
    
    def parse_assign(self):
        token = self.next_token()
        assert token == vt.ASSIGN, self.error_string("assign", "to begin assignment statment", token)
        l_cable, l_left, l_right = self.parse_variable_instantiation()
        token = self.next_token()
        assert token == vt.EQUAL, self.error_string("=", "in assigment statment", token)
        r_cable, r_left, r_right = self.parse_variable_instantiation()
        token = self.next_token()
        assert token == vt.SEMI_COLON, self.error_string(";", "to terminate assign statement", token)

        return l_cable, l_left, l_right, r_cable, r_left, r_right

    
    def parse_variable_instantiation(self):
        name = self.next_token()
        token = self.peek_token()
        left = None
        right = None
        if token == vt.OPEN_BRACKET:
            left, right = self.parse_brackets()

        cable = self.create_or_update_cable(name, left_index = left, right_index = right)
        
        return cable, left, right


    def parse_brackets(self):
        '''returns 2 integer values or 1 integer value and none'''
        token = self.next_token()
        assert token == vt.OPEN_BRACKET, self.error_string("[","to begin array slice", token)
        token = self.next_token()
        assert self.is_numeric(token), self.error_string("number", "after [", token)
        left = int(token)
        token = self.next_token()
        if token == "]":
            return left, None
        else:
            assert(token == vt.COLON), self.error_string("] or :", "in array slice", token)
            token = self.next_token()
            assert(self.is_numeric(token)), self.error_string("number", "after : in array slice", token)
            right = int(token)
            token = self.next_token()
            assert token == vt.CLOSE_BRACKET, self.error_string("]", "to terminate array slice", token)
            return left, right

    def parse_star_property(self):
        token = self.next_token()
        assert token == vt.OPEN_PARENTHESIS, self.error_string(vt.OPEN_PARENTHESIS, "to begin star property", token)
        token = self.next_token()
        assert token == vt.STAR, self.error_string(vt.STAR, "to begin star property", token)
        token = self.next_token()
        assert vt.is_valid_identifier(token)
        key = token
        token = self.next_token()
        assert token == vt.EQUAL, self.error_string(vt.EQUAL, "to set a star parameter", token)
        token = self.next_token()
        value = ""
        while token != vt.STAR:
            value += token
            token = self.next_token()
        assert token == vt.STAR, self.error_string(vt.STAR, "to start the ending of a star property", token)
        token = self.next_token()
        assert token == vt.CLOSE_PARENTHESIS, self.error_string(vt.CLOSE_PARENTHESIS, "to end the star property", token)
        return key, value
    
    #######################################################
    ##assignment helpers
    #######################################################

    def connect_wires(self, l_cable, l_left, l_right, r_cable, r_left, r_right):
        '''connect the wires in r_left to the wires in l_left'''
        pass

    #######################################################
    ##helper functions
    #######################################################

    def set_instance_parameters(self, instance, params):
        for k, v in params.items():
            self.set_single_parameter(instance.reference, k, None)
            self.set_single_parameter(instance, k, v)
        
    def set_definition_parameters(self, definition, params):
        for k,v in params.items():
            self.set_single_parameter(definition, k, v)
    
    def set_single_parameter(self, var, k, v):
        if "Verilog.Parameters" not in var:
            var["Verilog.Parameters"] = dict()

        if k not in var["Verilog.Parameters"] or var["Verilog.Parameters"][k] is None:
            var["Verilog.Parameters"][k] = v

    def get_all_ports_from_wires(self, wires):
        '''gets all ports associated with a set of wires'''
        ports = set()
        for w in wires:
            for p in w.pins:
                if isinstance(p, sdn.InnerPin):
                    ports.add(p.port)
        return ports

    def get_wires_from_cable(self, cable, left, right):
        wires = []
        cable_wires = cable.wires

        if left != None and right != None:
            left = left - cable.lower_index
            right = right - cable.lower_index
            temp_wires = cable.wires[min(left,right): max(left,right) + 1]
            if left > right:
                temp_wires = reversed(temp_wires)

            for w in temp_wires:
                wires.append(w)
        
        elif left != None or right != None:
            if left != None:
                index = left - cable.lower_index
            else:
                index = right - cable.lower_index
            wires.append(cable.wires[index])

        else:
            for w in cable.wires:
                wires.append(w)
        
        return wires

    def convert_string_to_port_direction(self, token):
        if token == vt.INPUT:
            return sdn.Port.Direction.IN
        if token == vt.INOUT:
            return sdn.Port.Direction.INOUT
        if token == vt.OUTPUT:
            return sdn.Port.Direction.OUT
        else:
            return sdn.Port.Direction.UNDEFINED

    def create_or_update_cable(self, name, left_index = None, right_index = None, var_type = None):
        cable_generator = self.current_definition.get_cables(name)
        cable = next(cable_generator, None)
        if cable == None:
            cable = self.current_definition.create_cable()
            self.populate_new_cable(cable,name,left_index, right_index, var_type)
            return cable

        assert cable.name == name

        #figure out what we need to do with the indicies

        cable_lower = cable.lower_index
        cable_upper = cable.lower_index + len(cable.wires) - 1 #-1 so that it is the same number if the width is 1
        
        if left_index is not None and right_index is not None:
            in_lower = min(left_index, right_index)
            in_upper = max(left_index, right_index)
        elif left_index is not None:
            in_lower = left_index
            in_upper = left_index
        elif right_index is not None:
            in_upper = right_index
            in_lower = right_index
        else:
            in_upper = None
            in_lower = None

        if in_upper is not None and in_lower is not None:

            if in_lower < cable_lower:
                prepend = cable_lower - in_lower
                self.prepend_wires(cable, prepend)
            if in_upper > cable_upper:
                postpend = in_upper - cable_upper
                self.postpend_wires(cable,postpend)
        
        if var_type:
            cable["Verilog.CableType"] = var_type

        return cable

    # def create_or_get_definition(self, name):
    #     dictionary_generator = self.netlist.get_definitions(name)
    #     definition = next(cable_generator, None)
    #     if definition == None:
    #         definition = self.current_library.create_definition()
    #         definition.name = name

    #     return definition

    def populate_new_cable(self, cable, name, left_index, right_index, var_type):
        cable.name = name
        if left_index is not None and right_index is not None:
            cable.is_downto = right_index < left_index
            cable.create_wires(max(left_index,right_index) - min(left_index,right_index) + 1)
            cable.lower_index = min(left_index, right_index)
        elif left_index is not None:
            cable.lower_index = left_index
            cable.create_wire()
        elif right_index is not None:
            cable.lower_index = right_index
            cable.create_wire()
        else:
            cable.lower_index = 0
            cable.create_wire()

        if var_type:
            cable["Verilog.CableType"] = var_type

        return cable

    def prepend_wires(self, cable, count):
        orig_count = len(cable.wires)
        cable.create_wires(count)
        cable.wires = cable.wires[orig_count:] + cable.wires[:orig_count]
        cable.lower_index = cable.lower_index - count

    def postpend_wires(self, cable, count):
        cable.create_wires(count)

    def create_or_update_port_on_instance(self, name, width):
        '''returns the set of pins associated with the port on the instance'''
        pins = []
        port = self.create_or_update_port(name, left_index = width -1, right_index = 0, definition = self.current_instance.reference)
        for pin in self.current_instance.pins:
            if pin.inner_pin in port.pins:
                pins.append(pin)
        return pins

    def create_or_update_port(self, name, left_index = None, right_index = None, direction = None, definition = None):
        if definition == None:
            definition = self.current_definition

        port_generator = definition.get_ports(name)
        port = next(port_generator, None)
        if port == None:
            port = definition.create_port()
            self.populate_new_port(port,name,left_index, right_index, direction)
            return port

        assert port.name == name

        #figure out what we need to do with the indicies

        port_lower = port.lower_index
        port_upper = port.lower_index + len(port.pins) - 1 #-1 so that it is the same number if the width is 1
         
        if left_index is not None and right_index is not None:
            in_lower = min(left_index, right_index)
            in_upper = max(left_index, right_index)
        elif left_index is not None:
            in_lower = left_index
            in_upper = left_index
        elif right_index is not None:
            in_upper = right_index
            in_lower = right_index
        else:
            in_upper = None
            in_lower = None

        if in_upper is not None and in_lower is not None:

            if in_lower < port_lower:
                prepend = port_lower - in_lower
                self.prepend_pins(port, prepend)
            if in_upper > port_upper:
                postpend = in_upper - port_upper
                self.postpend_pins(port,postpend)
        
        if direction is not None:
            port.direction = direction

        return port


    def populate_new_port(self, port, name, left_index, right_index, direction):
        port.name = name
        if left_index is not None and right_index is not None:
            port.is_downto = right_index < left_index
            port.create_pins(max(left_index,right_index) - min(left_index,right_index) + 1)
            port.lower_index = min(left_index, right_index)
        elif left_index is not None:
            port.lower_index = left_index
            port.create_pin()
        elif right_index is not None:
            port.lower_index = right_index
            port.create_pin()
        else:
            port.lower_index = 0
            port.create_pin()
        
        if direction is not None:
            port.direction = direction

        return port

    def prepend_pins(self, port, count):
        orig_count = len(port.pins)
        port.create_pins(count)
        port.pins = port.pins[orig_count:] + port.pins[:orig_count]
        port.lower_index = port.lower_index - count

    def postpend_pins(self, port, count):
        port.create_pins(count)

    def is_numeric(self,token):
        first = True
        for c in token:
            if first:
                first = False
                if c == "-":
                    continue
            if c not in vt.NUMBERS:
                return False
        return True

    def is_alphanumeric(self, token):
        for c in token:
            if c not in vt.NUMBERS and c not in vt.LETTERS:
                return False
        return True

    def error_string(self, expected, why, result):
        '''put in the expectation and then the reason or location and the actual result'''
        return "expected " + str(expected) + " " + why + " but got " + str(result) + " Line: " + str(self.tokenizer.line_number)

    