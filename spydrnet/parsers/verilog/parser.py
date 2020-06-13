
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
from spydrnet.ir import Netlist, Library, Definition, Port, Cable, Instance, OuterPin
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
        params = dict()
        token = self.tokenizer.next()
        while token:
            if token == '`':
                k,v = self.parse_back_tick()
                k = "VERILOG.backtick." + k
                params[k] = v
            
            if token === "(":
                token = self.tokenizer.next()
                assert token == "*", "unexpected ( with out a *
                k,v = self.parse_star_parameters()
                k = "VERILOG.star." + k
                params[k] = v
            
            if token == "module":
                definition = self.parse_module(params, params)
                

    # def parse_verilog(self):
    #     #tokenizer will skip the comments, this can be changed in the future to improve the results.
    #     library = Library()
    #     params = dict()
    #     token = self.tokenizer.next()
    #     while token:
    #         if token == '`':
    #             #backtick directive
    #             k,v = self.parse_back_tick()
    #             k = "VERILOG.backtick." + k
    #             params[k] = v #this line can overwrite because in verilog they override.
    #             #TODO fix this so it has it's own backtick namespace

    #         if token == "(":
    #             token = self.tokenizer.next()
    #             assert token == "*", "unexpected ( without a * character"
    #             k,v = self.parse_star_parameters()
    #             k = "VERILOG.star." + k
    #             params[k] = v #TODO make this somehow different than above to more easily compose.

    #         if token == "module":
    #             definition = self.parse_module(params, params)
    #             #TODO lookup to see if the definition already exists, if so modify the existing one to match instead
    #             library.add_definition(definition)
    #             definition = Definition()
    #         token = self.tokenizer.next()
    #     netlist = Netlist()
    #     netlist.add_library(library)
    #     return

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
        definition = Definition()
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

    def _get_create_library(self, netlist, library_name = None):
        if library_name:
            lib = netlist.get_library(library_name)
            if not lib:
                lib = netlist.create_library()
                lib.name = library_name
        else:
            lib = netlist.get_library("spydrnet_temporary")
            if not lib:
                lib = netlist.create_library()
                lib.name = "spydrnet_temporary"
        return lib

    def _get_create_definition(self, netlist, definition_name, library = None):
        if library is not None:
            d = library.get_definition(definition_name)
            if d is None:
                d = library.create_definition()
                d.name = definition_name
            return d
        else:
            self._get_create_library(self)
            

    def _update_instance(self, netlist, definition, name, reference = None, properties = dict()):
        #pass in a definition in which to contain the instance as a child
        #pass in the name of the instance to create/find
        #pass in the reference of the instance to create/find
        #can also pass in a dictionary of properties to add to the instance.
        #return the instance that was created or found
        inst = definition.get_children(name)
        if not inst:
            inst = definition.create_child()
            inst.name = name
        if reference is not None:
            ref = netlist.get_definition(reference)
            if not ref:
                lib = self._get_create_library(netlist)
                ref = lib.create_definition()
                ref.name = reference
            inst.reference = ref
        for k,v in properties.items():
            inst[k] = v
        return inst

    def _update_definition(self, netlist, name, library = None, properties = dict()):
        lib = self._get_create_library(netlist, library)
        d = netlist.get_definition(name)
        if not d:
            d = lib.create_definition()
            d.name = name

        if library is not None:
            if d.library.name != library:
                d.library.remove_definition(d)
                lib.add_definition(d)
        
        for k,v in properties.items():
            d[k] = v

        return d
            

    def _update_port(self, definition, name, width = None,
                direction = None, lower_index = None, is_downto = None, properties = dict()):
        port = definition.get_port(name)
        cable = definition.get_cable(name)
        if not port:
            port = definition.create_port()
            port.name = name
            cable = definition.create_cable()
            cable.name = name
            

        
        if width is not None:
            port.width = width
            cable.width = width
        if direction is not None:
            port.direction = direction
            cable.direction = direction
        if lower_index is not None:
            port.lower_index = lower_index
            cable.lower_index = lower_index
        if is_downto is not None:
            port.is_downto = is_downto
            cable.is_downto = is_downto

        for k,v in properties.items():
            port[k] = v
            cable[k] = v

        for i in range(len(port.pins)):
            cable.wires[i].connect_pin(port.pins[i])

        return port

    def _get_create_cable(self, definition, name, width = 0):
        cable = definition.get_cable(name)
        if not cable:
            cable = definition.create_cable()
            cable.name = name
        cable.width = width


    def _connect_ports(self, parent, instance,
                        port_name, cable_name, range_index_low = 0, range_index_high = 0):
        #this method will conenct and wire up all the ports.
        #make sure the definition has all apropriate ports. create them if not
        port_width = range_index_high - range_index_low + 1
        port = self._update_port(instance.reference, port_name, width = port_width)
        cable = parent._get_create_cable(parent, cable_name)
        #for i_pin in port.pins:
        #    o_pin = OuterPin.from_instance_and_inner_pin(instance, i_pin)
        for i in range(max(port_width)):
            cable.wires[i + range_index_low] = port.pins[i] 