
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
        self.primitive_cell = False


    def parse(self):
        self.initialize_tokenizer()
        ns_default = namespace_manager.default
        namespace_manager.default = "DEFAULT"
        self.netlist = self.parse_verilog()
        namespace_manager.default = ns_default
        self.tokenizer.__del__()
        return self.netlist


    def initialize_tokenizer(self):
        if self.filename:
            self.tokenizer = VerilogTokenizer.from_filename(self.filename)
        elif self.file_handle:
            self.tokenizer = VerilogTokenizer.from_stream(self.file_handle)


    def parse_verilog(self):
        params = dict()
        
        token = self.tokenizer.next()
        line_num = self.tokenizer.line_number
        netlist = Netlist()
        self.primitive_cell = False
        while token:

            if token == '`celldefine':
                self.primitive_cell = True
            elif self.primitive_cell and token == "`endcelldefine":
                self.primitive_cell = False
                
            
            elif token == "(":
                token = self.tokenizer.next()
                assert token == "*", "unexpected ( with out a *" + " " + str(self.tokenizer.line_number)
                k,v = self.parse_star_parameters()
                k = "VERILOG.star." + k
                params[k] = v
            
            elif token == "module":
                definition = self.parse_module(params, netlist)
                if netlist.top_instance is None:
                    instance = Instance()
                    instance.name = definition.name
                    instance.reference = definition
                    netlist.top_instance = instance
            
            elif token[:2] == "//":
                pass #comment

            elif token == "primitive":
                while token != "endprimitive":
                    token = self.tokenizer.next() 

            else:
                pass #unsorted token

            if self.tokenizer.has_next():
                token = self.tokenizer.next()
                line_num = self.tokenizer.line_number
            else:
                token = None
        return netlist
                


    def parse_star_parameters(self):
        key = self.tokenizer.next()
        assert self.tokenizer.next() == "=", "expected a = character in the key value directive"+ " " + str(self.tokenizer.line_number)
        value = self.tokenizer.next()
        assert self.tokenizer.next() == "*", "expected * to end star params"+ " " + str(self.tokenizer.line_number)
        assert self.tokenizer.next() == ")", "expected ) to end the star params"+ " " + str(self.tokenizer.line_number)
        return key, value

    def parse_module(self, params, netlist):
        
        definition = self.parse_module_header(netlist)
        for k,v in params.items():
            definition[k] = v
        if self.primitive_cell:
            self.parse_primitive_cell_body(definition)
        else:
            self.parse_module_body(definition, netlist)
        return definition

    def parse_primitive_cell_body(self, definition):
        token = self.tokenizer.next()
        keywords = set(["input", "output", "inout"])
        while token != "endmodule" and token != "endprimative":
            if token in keywords:
                name, left, right = self.parse_wire()
                port = self._update_port(definition, name, (max(left,right) - min(left,right)), None, min(left,right), left > right)
            elif token == "function":
                while token != "endfunction":
                    token = self.tokenizer.next()
            token = self.tokenizer.next()
            
        pass

    def parse_module_header(self, netlist):
        name = self.tokenizer.next()
        definition = self._get_create_definition(netlist, name)
        token = self.tokenizer.next()
        if token == "#":
            self.parse_parameter_list(definition)
            token = self.tokenizer.next()
        if token == "(":
            token = self.tokenizer.next()
            while True:
                d = None
                if token == "input" or token == "output" or token == "inout":
                    d = token
                    token = self.tokenizer.next()
                name = token
                self._update_port(definition, name, direction=d)
                token = self.tokenizer.next()
                if token == ")":
                    break
                assert token == ",", "expected a , separater in the port list"+ " " + str(self.tokenizer.line_number)
                token = self.tokenizer.next()
        token = self.tokenizer.next()
        assert token == ";", "expected ; to finish the port list"+ " " + str(self.tokenizer.line_number)
        return definition


    def parse_parameter_list(self, definition):
        token = self.tokenizer.next()
        assert token == "(", "expected a ( following the # for the parameter definitions"+ " " + str(self.tokenizer.line_number)
        while token != ")":
            token = self.tokenizer.next()
            assert token == "parameter", "expected a parameter in the parameter list"+ " " + str(self.tokenizer.line_number)
            token = self.tokenizer.next()
            if token == "[":
                key = ""
                while token != "=":
                    key += token
                    token = self.tokenizer.next()
            else:
                key = token
                token = self.tokenizer.next()
                assert token == "=", "expected a = in the key value pair for the parameter"+ " " + str(self.tokenizer.line_number)
            value = self.tokenizer.next()
            if key not in definition:
                definition[key] = value
            token = self.tokenizer.next()

    def parse_module_body(self, definition, netlist):
        self.parse_wire_list(definition)
        self.parse_instantiations(definition, netlist)

    def parse_wire_list(self, definition):
        keywords = set(["input", "output", "inout", "wire", "reg"]) #this is the list of words that could begin a wire list line
        portwords =set(["input", "output", "inout"])
        while True:
            token = self.tokenizer.peek()
            if token not in keywords:
                break
            token = self.tokenizer.next()
            name, left, right = self.parse_wire()
            #check and see what a name lookup on the name yeids for the ports
            #go ahead and modify it if it exists.
            if token in portwords:
                port = self._update_port(definition, name, width = (max(left,right) - min(left,right)), direction = token, lower_index = min(left,right), is_downto = left > right)
            else:
                cable = self._update_cable(definition, name, width = (max(left,right) - min(left,right)), lower_index = min(left,right), is_downto = left > right)
            

    def parse_wire(self):
        #the next token will be either [ or a letter
        #if [ then the next is the left then : then right
        #if a letter then it will just be 0 downto 0
        token = self.tokenizer.next()
        left = 0
        right = 0
        if token == "[":
            right = int(self.tokenizer.next())
            assert self.tokenizer.next() == ":", "expected a colon"+ " " + str(self.tokenizer.line_number)
            left = int(self.tokenizer.next())
            assert self.tokenizer.next() == "]", "expected an end bracket"+ " " + str(self.tokenizer.line_number)
            token = self.tokenizer.next()
        name = token
        token = self.tokenizer.next()
        assert token == ";", "expected ;" + " " + str(self.tokenizer.line_number)
        return name, left, right

    def parse_instantiations(self, definition, netlist):
        token = self.tokenizer.next()
        params = dict()
        while token != "endmodule":
            def_name = token
            if token == ";":
                pass
            elif token == "(":
                token = self.tokenizer.next()
                assert token == "*", "unexpected ( with out a *"+ " " + str(self.tokenizer.line_number)
                k,v = self.parse_star_parameters()
                params[k] = v
            else:
                instance = self.parse_single_instance(netlist, definition, def_name)
                params = dict()
            token = self.tokenizer.next()
            

    def parse_single_instance(self, netlist, parent, reference_name):
        
        ref_def = self._get_create_definition(netlist, reference_name)
        instance = parent.create_child()
        token = self.tokenizer.next()
        
        if token == "#":
            param = self.parse_instance_parameter_list()
            token = self.tokenizer.next()

        name = token
        instance.name = name

        instance.reference = ref_def

        self.parse_port_map(instance)

        return instance
        

    def parse_instance_parameter_list(self):
        params = dict()
        token = self.tokenizer.next()
        assert token == "(", "expected list of attributes to map after #"+ " " + str(self.tokenizer.line_number)
        token = self.tokenizer.next()
        while True:
            if token == ".":
                pass
            elif token == ",":
                pass
            elif token == "*":
                print(".* mapping is unsupported")
            elif token == ")":
                break
            else:
                key = token
                token = self.tokenizer.next()
                assert token == "(", "expected a ( in parameter mapping " + str(self.tokenizer.line_number)
                value = ""
                token = self.tokenizer.next()
                while token != ")":
                    value += token
                    token = self.tokenizer.next()
                params[key] = value
            token = self.tokenizer.next()    
        return params
    
    def parse_port_map(self, instance):
        #extract/create the port that will be wired up to I guess assume the width is the same as the wire?
        token = self.tokenizer.next()
        assert token == "(", "expected ( for port mapping " + str(self.tokenizer.line_number)
        token = self.tokenizer.next()
        port_map = dict()
        while True:
            if token == ")":
                break
            elif token == "." or token == ",":
                pass
            else:
                port_name = token
                assert self.tokenizer.next() == "(", "port needs to be followed by (cable) " + str(self.tokenizer.line_number)
                cable_name = self.tokenizer.next()
                token = self.tokenizer.next()
                if token == "[": #this will be a slice. for now just put it in the value
                    cable_name += token
                    while token != "]":
                        token = self.tokenizer.next()
                        cable_name += token
                    token = self.tokenizer.next()
                assert token == ")", "port list needs to be ended with a ) " + str(self.tokenizer.line_number)
                port_map[port_name] = cable_name
            token = self.tokenizer.next()

    def _get_create_library(self, netlist, library_name = None):
        if library_name:
            lib_list = netlist.get_libraries(library_name)
            lib = next(lib_list, None)
            if not lib:
                lib = netlist.create_library()
                lib.name = library_name
        else:
            lib_list = netlist.get_libraries("work")
            lib = next(lib_list, None)
            if not lib:
                lib = netlist.create_library()
                lib.name = "work"
        return lib

    def _get_create_definition(self, netlist, definition_name, library = None):
        if library is not None:
            d = next(library.get_definitions(definition_name),None)
            if d is None:
                d = library.create_definition()
                d.name = definition_name
            return d
        else:
            library = self._get_create_library(netlist)
            d = next(library.get_definitions(definition_name),None)
            if d is None:
                d = library.create_definition()
                d.name = definition_name
            return d

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
            ref = netlist.get_definitions(reference)
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
        d_list = netlist.get_definitions(name)
        d = next(d_list, None)
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
        port_list = definition.get_ports(name)
        cable_list = definition.get_cables(name)
        
        port = next(port_list, None)
        cable = next(cable_list, None)

        if port is None:
            port = definition.create_port()
            port.name = name

        if cable is None:
            cable = definition.create_cable()
            cable.name = name
            
        if width is not None:
            current_p_width = len(port.pins)
            current_c_width = len(cable.wires)

            if width < current_p_width or width < current_c_width:
                print("updating port width does not support reducing size. a port or wire might be declared twice?")
                raise NotImplementedError
            wp = width - current_p_width
            wc = width - current_c_width

            port.create_pins(wp)
            cable.create_wires(wc)

        if direction is not None:
            port.direction = direction
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

    def _update_cable(self, definition, name, width = None,
                direction = None, lower_index = None, is_downto = None, properties = dict()):
        cable_list = definition.get_cables(name)
        
        cable = next(cable_list, None)
        
        if cable is None:
            cable = definition.create_cable()
            cable.name = name
            
        if width is not None:
            current_width = len(cable.wires)
            cable.create_wires(width)
            if width < current_width:
                print("updating port width does not support reducing size. a port or wire might be declared twice with different lengths?")
                raise NotImplementedError
    
        if lower_index is not None:
            cable.lower_index = lower_index
        if is_downto is not None:
            cable.is_downto = is_downto

        for k,v in properties.items():
            cable[k] = v

        return cable
