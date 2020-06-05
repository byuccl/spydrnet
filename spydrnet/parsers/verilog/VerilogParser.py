
#parser strategy
#we will use the namespace manager to figure out if the object already exists. if it does we will just add to it/modify it
#on first mention we will create all objects mentioned and put them in the corresponding objects.
#on any future mention we will look up the object and change it to match the specifications of the mention

#throw away comments
#3 basic components definition, instance, nets,
#there are also ports and whatnot.

#so here is the idea. Where we ge to the first definition create a definition and a library named work
#we will also need a primative library
#primatives only have ports on the definition

'''
basic verilog file structure from vivado:

    (optional) Comments
    (optional) `timescale 1 ps / 1 ps
    (optional) `celldefine
    (optional) (* words *)
    module header
    module body

    repeat the above

the module header consists of:

    module module_name
    (optional) #(parameters)
    (input/output list);

the input/output list:

    

the module body:

    consists of the wire/register/parameter list
    intermixed with instantiations

The wire/register/parameter list
    
    localparam statments
    input statements
    output statements
    inout statements
    wire statements
    register statements
    assign statements
    
an instantiation looks like

    any number of (* ... *) comments
    name of the module
    #(parameters)
    instance_name (can contain [])
    port mapping
'''

from spydrnet.parsers.verilog.tokenizer import VerilogTokenizer
from spydrnet.parsers.verilog.verilog_tokens import *
from spydrnet.ir import Netlist, Library, Definition, Port, Cable, Instance
from spydrnet.plugins import namespace_manager

from functools import reduce
import re


class VerilogParser:

    @staticmethod
    def from_filename(filename):
        parser = VerilogParser()
        parser.filename = filename
        return parser

    @staticmethod
    def from_file_handle(file_handle):
        parser = VerilogParser()
        parser.file_handle = file_handle
        return parser
    

    def __init__(self):
        self.filename = None
        self.file_handle = None
        self.elements = list()
        self.tokenizer = None
        self.netlist = None


    def parse(self):
        self.initialize_tokenizer()
        ns_default = namespace_manager.default
        namespace_manager.default = "VERILOG"
        self.netlist = self.parse_verilog()
        namespace_manager.default = ns_default
        self.tokenizer.__del__()


    # def parse(self):
    #     self.initialize_tokenizer()
    #     ns_default = namespace_manager.default
    #     namespace_manager.default = "VERILOG"
    #     self.netlist = self.parse_construct(self.parse_edif)
    #     namespace_manager.default = ns_default
    #     self.tokenizer.__del__()

    def initialize_tokenizer(self):
        if self.filename:
            self.tokenizer = VerilogTokenizer.from_filename(self.filename)
        elif self.file_handle:
            self.tokenizer = VerilogTokenizer.from_stream(self.file_handle)

    def parse_verilog(self):
        #tokenizer will skip the comments, this can be changed in the future to improve the results.
        library = Library()
        definition = Definition()
        token = self.tokenizer.next()
        while token:
            if token == '`':
                #backtick directive
                k,v = self.parse_back_tick()
                definition[k] = v #this line can overwrite because in verilog they override.
                #TODO fix this so it has it's own backtick namespace

            if token == "(":
                token = self.tokenizer.next()
                assert token == "*", "unexpected ( without a * character"
                k,v = self.parse_star_parameters()
                definition[k] = v #TODO make this somehow different than above to more easily compose.

            if token == "module":
                self.parse_module(definition, library)
                #TODO lookup to see if the definition already exists, if so modify the existing one to match instead
                library.add_definition(definition)
                definition = Definition()
            token = self.tokenizer.next()
        netlist = Netlist()
        netlist.add_library(library)

    def parse_back_tick(self):
        start_line = self.tokenizer.line_number
        key = self.tokenizer.next()
        value = ""
        while self.tokenizer.line_number == start_line:
            value += self.tokenizer.next()
        return key, value

    def parse_star_parameters(self):
        key = self.tokenizer.next()
        assert self.tokenizer.next() == "=", "expected a = character in the key value directive"
        value = self.tokenizer.next()
        return key, value

    def parse_module(self, definition, library):
        self.parse_module_header(definition)
        self.parse_module_body(definition, library)


    def parse_module_header(self, definition):
        definition.name = self.tokenizer.next()
        token = self.tokenizer.next()
        if token == "#":
            self.parse_parameter_list(definition)
        elif token == "(":
            token = self.tokenizer.next()
            while token != ")":
                port = Port()
                if token == "input" or token == "output" or token == "inout":
                    port.direction = token
                    token = self.tokenizer.next()
                port.name = token
                token = self.tokenizer.next()
                definition.add_port(port)
        token = self.tokenizer.next()
        assert token == ";", "expected ; to finish the port list"
        # port = Port()
        # while token != ")":
        #     port.name = token = self.tokenizer.next()
        #     token = self.tokenizer.next()

    def parse_parameter_list(self, definition):
        token = self.tokenizer.next()
        assert token == "(", "expected a ( following the # for the parameter definitions"
        while token != ")":
            token = self.tokenizer.next()
            assert token == "parameter", "expected a parameter in the parameter list"
            key = self.tokenizer.next()
            token = self.tokenizer.next()
            assert token == "=", "expected a = in the key value pair for the parameter"
            value = self.tokenizer.next()
            if key not in definition:
                definition[key] = value
            #else the key has been set by the instantiation perhaps.
            token = self.tokenizer.next()

    def parse_module_body(self, definition):
        self.parse_wire_list(definition)
        self.parse_instantiations(definition, library)

    def parse_wire_list(self, definition):
        keywords = set(["input", "output", "inout", "wire", "reg"]) #this is the list of words that could begin a wire list line
        portwords =set(["input", "output", "inout"])
        token = self.tokenizer.peek()
        while token in keywords:
            self.tokenizer.next()
            name, left, right = self.parse_wire()
            #check and see what a name lookup on the name yeids for the ports
            #go ahead and modify it if it exists.
            port = definition.get_ports(name)
            if port: #name lookup yields results on ports 
                port.is_downto = left > right
                port.lower_index = min(left, right)
                port.is_scalar = (left == right and right == 0)
                if token in portwords:
                    port.direction = token
            else:
                cable = Cable()
                cable.name = name
                cable.is_downto = left > right
                cable.lower_index = min(left, right)
                cable.is_scalar = (left == right and right == 0)
                definition.add_cable(cable)
            assert self.tokenizer.next() == ";"
            token = self.tokenizer.peek()

    def parse_wire(self):
        #the next token will be either [ or a letter
        #if [ then the next is the left then : then right
        #if a letter then it will just be 0 downto 0
        token = self.tokenizer.next()
        left = 0
        right = 0
        if token == "[":
            right = int(self.tokenizer.next())
            assert self.tokenizer.next() == ":", "expected a colon"
            left = int(self.tokenizer.next())
            assert self.tokenizer.next() == "]", "expected an end bracket"
        name = self.parse_name()
        return name, left, right

    def parse_name(self):
        name = ""
        token = self.tokenizer.next()
        if token == "\\":
            name = token + self.tokenizer.next()
        name += self.tokenizer.next()
        return name

    def parse_instantiations(self, definition, library):
        token = self.tokenizer.next()
        while token != "endmodule":
            def_name = token
            instance = Instance()
            lib_def = library.get_definition(def_name)
            if lib_def: #the definition exists
                ref_def = lib_def
            else:
                ref_def = Definition()
                ref_def.name = def_name
                library.add_definition(definition)
            instance.reference = ref_def
            token = self.tokenizer.next()
            if token == "#":
                token = self.tokenizer.next()
                pass # we have a parameter list parse it
            
            inst_name = self.parse_name()
            instance.name = inst_name
            self.parse_port_map(definition, instance)
            
    def parse_port_map(self, definition, instance):
        ref_def = instance.reference
        #extract/create the port that will be wired up to I guess assume the width is the same as the wire?
        port = Port()
        #extract the cable that will connect to the pins in the port
        cable = Cable()
        #put the port, cable, and instance into a definition to be attached later.
