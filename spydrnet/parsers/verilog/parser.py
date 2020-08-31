
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
        self.direction_string_map = dict()
        self.direction_string_map["input"] = Port.Direction.IN
        self.direction_string_map["output"] = Port.Direction.OUT
        self.direction_string_map["inout"] = Port.Direction.INOUT
        self.direction_string_map[None] = None
        
        self.instance_to_port_map = dict()


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
        top_next = False
        while token:

            if token == '`celldefine':
                self.primitive_cell = True
            elif self.primitive_cell and token == "`endcelldefine":
                self.primitive_cell = False
                
            
            elif token == "(":
                token = self.tokenizer.next()
                assert token == "*", "unexpected ( with out a *" + " " + str(self.tokenizer.line_number)
                k,v = self.parse_star_parameters()
                if k == "STRUCTURAL_NETLIST":
                    top_next = True
                k = "VERILOG.star." + k
                params[k] = v
            
            elif token == "module":
                definition = self.parse_module(params, netlist)
                #if netlist.top_instance is None:
                if top_next == True:
                    instance = Instance()
                    instance.name = definition.name
                    instance.reference = definition
                    netlist.top_instance = instance
                    top_next = False
            
            elif token[:2] == "//":
                pass #comment

            elif token == "primitive":
                while token != "endprimitive":
                    token = self.tokenizer.next() 

            else:
                #print("unsorted token", token)
                pass #unsorted token

            if self.tokenizer.has_next():
                token = self.tokenizer.next()
                line_num = self.tokenizer.line_number
            else:
                token = None

        for instance, port_map in self.instance_to_port_map.items():
            port_pin_map = dict()
            for port in instance.reference.ports:
                port_pin_map[port] = []
            for pin in instance.pins:
                port_pin_map[pin.inner_pin.port].append(pin)
            definition = instance.parent
            
            for port_name, cable_list in port_map.items():

                index_offset = 0
                for cable_name in cable_list:
                    low = None
                    high = None
                    index_offset_initial = index_offset
                    if cable_name[len(cable_name)-1] == "]" and (cable_name[0] != "\\" or len(cable_name.split(" ")) > 1):
                        cable_name_real, index = cable_name.split(" ")
                        indicies = index[1:len(index)-1].split(":")
                        if len(indicies) == 1:
                            low = int(indicies[0])
                            high = None
                        else:
                            low = min(int(indicies[0]), int(indicies[1]))
                            high = max(int(indicies[0]), int(indicies[1]))
                    else:
                        cable_name_real = cable_name
                    cable_def_list = definition.get_cables(cable_name_real)
                    cable = next(cable_def_list)
                    port_list = instance.reference.get_ports(port_name)
                    # print(port_name)
                    port = next(port_list)
                    # if len(cable_list) > 1:
                    #     import pdb; pdb.set_trace()
                    if low == None and high == None:
                        if len(cable.wires) == len(port_pin_map[port]):
                            for i in range(len(cable.wires)):
                                cable.wires[i].connect_pin(port_pin_map[port][i+index_offset_initial])
                                index_offset += 1
                        else:
                            for i in range(min(len(port_pin_map[port]), len(cable.wires))):
                                cable.wires[i].connect_pin(port_pin_map[port][i + index_offset_initial])
                                index_offset += 1
                    else:
                        if high == None:
                            cable.wires[low-cable.lower_index].connect_pin(port_pin_map[port][0 + index_offset_initial])
                            index_offset += 1
                        else:
                            for i in range(low,high):
                                cable.wires[i-cable.lower_index].connect_pin(port_pin_map[port][i-low + index_offset_initial])
                                index_offset += 1
        return netlist
                


    def parse_star_parameters(self):
        key = self.tokenizer.next()
        token = self.tokenizer.next()
        if token == "*":
            assert self.tokenizer.next() == ")", "expected ) to end the star params"+ " " + str(self.tokenizer.line_number)    
            return key, None
        assert token == "=", "expected a = character in the key value directive got: "+token+ " line " + str(self.tokenizer.line_number)
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
        definition["VERILOG.primative"] = True
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


    def parse_module_header(self, netlist):
        name = self.tokenizer.next()
        definition = self._get_create_definition(netlist, name)
        token = self.tokenizer.next()
        if token == "#":
            self.parse_parameter_list(definition)
            token = self.tokenizer.next()
        if token == "(":
            
            while True:
                verilog_rename = None
                name_list = []
                token = self.tokenizer.next()
                if token == ")":
                    break
                if token == ".":
                    verilog_rename = self.tokenizer.next()
                    token = self.tokenizer.next()
                    assert token == "(", "expected ( to create a port alias got " + token + " line " + str(self.tokenizer.line_number)
                    token = self.tokenizer.next()
                    if token == "{":
                        while token != "}":
                            name = self.tokenizer.next()
                            token = self.tokenizer.next()
                            if token == "[":
                                name += " "
                                while token != "," and token != "}":
                                    name += token
                                    token = self.tokenizer.next()
                            name_list.append(name)
                            assert token == "," or token == "}", "syntax error expect , or } got " + token + " line " + str(self.tokenizer.line_number)
                            
                    temp = self.tokenizer.next()
                    assert temp == ")", "expected ) to finish alias got " + temp + " line " + str(self.tokenizer.line_number)
                d = None
                if token == "input" or token == "output" or token == "inout":
                    d = token
                    token = self.tokenizer.next()
                left = 0
                right = 0
                if token == "[":
                    left = int(self.tokenizer.next())
                    token = self.tokenizer.next()
                    assert token == ":", "expected a : to separate the numbers in a port width  got " + str(token) + " line " + self.tokenizer.line_number
                    right = int(self.tokenizer.next())
                    token = self.tokenizer.next()
                    assert token == "]", "expected ] to end the port length definition got " + str(token) + " line " + self.tokenizer.line_number
                    token = self.tokenizer.next()
                if verilog_rename is None:
                    name = token
                    port = self._update_port(definition, name, width = (max(left,right) - min(left,right)), direction=d, lower_index = min(left,right), is_downto = left > right)
                else:
                    i = 0
                    outer_port = self._update_port(definition, verilog_rename, width = i, direction=d, lower_index = 0, is_downto = True)
                    for name in name_list:
                        name_split = name.split(" ")
                        name = name_split[0]
                        index = None
                        if len(name_split) > 1:
                            index = name_split[1]
                        port = self._update_port(definition, name, width = (max(left,right) - min(left,right)), direction=d, lower_index = min(left,right), is_downto = left > right)
                        port["VERILOG.port_rename_member"] = "true"
                        if index is not None:
                            outer_port["VERILOG.port_rename."+str(i)] = name + " " + index
                        else:
                            outer_port["VERILOG.port_rename."+str(i)] = name
                        i += 1
                    outer_port = self._update_port(definition, verilog_rename, width = i, direction=d, lower_index = 0, is_downto = True)
                    
                token = self.tokenizer.next()
                if token == ")":
                    break
                assert token == ",", "expected a , separater in the port list got "+ token+ " line " + str(self.tokenizer.line_number)
                    

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
            key = ""
            if token == "integer":
                key += "integer "
                token = self.tokenizer.next()
            if token == "[":
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
        keywords = set(["input", "output", "inout", "wire", "reg", "assign"]) #this is the list of words that could begin a wire list line
        portwords =set(["input", "output", "inout"])
        token = self.tokenizer.peek()
        params = dict()
        assignment_info = dict()
        while token != "endmodule":
            if token not in keywords:
                token = self.tokenizer.next()
                def_name = token
                if token == ";":
                    pass
                elif token == "(":
                    token = self.tokenizer.next()
                    assert token == "*", "unexpected ( with out a *"+ " " + str(self.tokenizer.line_number)
                    k,v = self.parse_star_parameters()
                    params["VERILOG.star."+k] = v
                else:
                    instance = self.parse_single_instance(netlist, definition, def_name, params)
                    params = dict()
            elif token == "assign":
                _ = self.tokenizer.next()
                name_left, left_left, right_left = self.parse_wire_in_instance()
                token = self.tokenizer.next()
                assert token == "=", "expected = but got " + token
                name_right, left_right, right_right = self.parse_wire_in_instance()

                assignment_info[(name_left, left_left, right_left)] = (name_right, left_right, right_right)

                #print("left side of the assign", name_left + "["+str(left_left) + ":" + str(right_left) + "]", "right side of the assignment", name_right + "["+str(left_right) + ":" + str(right_right) + "]")
                
            else:
                token = self.tokenizer.next()
                name, left, right = self.parse_wire()
                #check and see what a name lookup on the name yeids for the ports
                #go ahead and modify it if it exists.
                if token in portwords:
                    port = self._update_port(definition, name, width = (max(left,right) - min(left,right)), direction = token, lower_index = min(left,right), is_downto = left > right)
                else:
                    cable = self._update_cable(definition, name, width = (max(left,right) - min(left,right)), lower_index = min(left,right), is_downto = left > right)
            token = self.tokenizer.peek()

        for k,v in assignment_info.items():
            cable_list = definition.get_cables(k[0])
            cable_left = next(cable_list)
            # cable_list = definition.get_cables(v[0])
            # cable_right = next(cable_list)
            k_str = k[0]
            if k[1] != None:
                k_str += " [" + str(k[1])
                if k[2] != None:
                    k_str += ":" + str(k[2])
                k_str += "]"
            v_str = v[0]
            if v[1] != None:
                v_str += " [" + str(v[1])
                if k[2] != None:
                    v_str += ":" + str(v[2])
                v_str += "]"
            cable_left["VERILOG.assignment." + k_str + " = " + v_str] = "true"  

        #put in assignment information

    def parse_wire_in_instance(self):
        token = self.tokenizer.next()
        name = token
        left = None
        right = None
        token = self.tokenizer.peek()
        if token == "[":
            token = self.tokenizer.next()
            left = int(self.tokenizer.next())
            token = self.tokenizer.next()
            if token == ":":
                right = int(self.tokenizer.next())
                token = self.tokenizer.next()
            assert token == "]", "expected an end bracket got "+ token + " line " + str(self.tokenizer.line_number)
            #token = self.tokenizer.next()
        return name, left, right

    def parse_wire(self):
        #the next token will be either [ or a letter
        #if [ then the next is the left then : then right
        #if a letter then it will just be 0 downto 0
        token = self.tokenizer.next()
        left = 0
        right = 0
        verilog_types = ["reg", "wire", "integer"]
        v_type = "wire"
        if token in verilog_types:
            v_type = token #TODO use this
            token = self.tokenizer.next()
        if token == "[":
            left = int(self.tokenizer.next())
            assert self.tokenizer.next() == ":", "expected a colon"+ " " + str(self.tokenizer.line_number)
            right = int(self.tokenizer.next())
            assert self.tokenizer.next() == "]", "expected an end bracket"+ " " + str(self.tokenizer.line_number)
            token = self.tokenizer.next()
        while True:
            name = token
            #name, left, right = self.parse_wire_name(self)
            token = self.tokenizer.next()
            #assert token == ";", "expected ; got " + token + " line " + str(self.tokenizer.line_number)
            if token == ";":
                break
            elif token == ",":
                token = self.tokenizer.next()
            else:
                print("unexpected token in cable or port list " + token + " line " + str(self.tokenizer.line_number))
        return name, left, right
            

    def parse_single_instance(self, netlist, parent, reference_name, params):
        
        ref_def = self._get_create_definition(netlist, reference_name)
        instance = parent.create_child()
        for k, v in params.items():
            instance[k] = v
        token = self.tokenizer.next()
        
        if token == "#":
            param = self.parse_instance_parameter_list()
            token = self.tokenizer.next()

            for k, v in param.items():
                instance["VERILOG.parameters."+k] = v

        name = token
        instance.name = name

        instance.reference = ref_def

        port_map = self.parse_port_map(instance)
        
        self.instance_to_port_map[instance] = port_map

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
        assert token == "(", "expected ( for port mapping but got " + token + " line " + str(self.tokenizer.line_number)
        token = self.tokenizer.next()
        # if token == "{":
        #     #we have a combinational port map going on... each pin on the port will be mapped individually
        #     pass
        port_map = dict()
        #import pdb; pdb.set_trace()
        while True:
            if token == ")":
                break
            elif token == "." or token == ",":
                pass
            else:
                port_name = token
                token = self.tokenizer.next()
                assert token == "(", "port needs to be followed by (cable) but got " + token + " line " + str(self.tokenizer.line_number)
                token = self.tokenizer.next()
                multi_cable = False
                if token == "{":
                    multi_cable = True
                    token = self.tokenizer.next()

                while True:
                    cable_name = token
                    token = self.tokenizer.next()
                    if token == "[": #this will be a slice. for now just put it in the value
                        cable_name += " " + token
                        while token != "]":
                            token = self.tokenizer.next()
                            cable_name += token
                        token = self.tokenizer.next()
                    if port_name not in port_map:
                        port_map[port_name] = []
                    port_map[port_name].append(cable_name)
                    #token = self.tokenizer.next()
                    if multi_cable and token == "}":
                        token = self.tokenizer.next()
                        break
                    elif multi_cable and token == ",":
                        token = self.tokenizer.next()
                    elif token == ")":
                        break
                    else:
                        print("unknown token in port mapping", token)
                assert token == ")", "cable list should end with ) but ends with " + token + " line " + str(self.tokenizer.line_number)
                #token = self.tokenizer.next()
            token = self.tokenizer.next()
        
        assert token == ")", "port list needs to be ended with a ) but ends with " + token + " line " + str(self.tokenizer.line_number)


        
        return port_map

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
        
        direction = self.direction_string_map[direction]

        port = next(port_list, None)
        cable = next(cable_list, None)

        if port is None:
            port = definition.create_port()
            port.name = name

        if cable is None:
            cable = definition.create_cable()
            cable.name = name
        
        if width is None and len(port.pins) == 0:
            width = 0 
            
        if width is not None:
            width = width +1
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
            if port.pins[i].wire == None:
                cable.wires[i].connect_pin(port.pins[i])

        return port

    def _update_cable(self, definition, name, width = None,
                direction = None, lower_index = None, is_downto = None, properties = dict()):
        cable_list = definition.get_cables(name)

        direction = self.direction_string_map[direction]
        
        cable = next(cable_list, None)
        
        if cable is None:
            cable = definition.create_cable()
            cable.name = name
            
        if width is None and len(cable.wires) == 0:
            width = 0

        if width is not None:
            width = width + 1
            current_width = len(cable.wires)
            
            if width < current_width:
                print("updating port width does not support reducing size. a port or wire might be declared twice with different lengths?")
                raise NotImplementedError

            wire_add_count = width - current_width
            cable.create_wires(wire_add_count)
    
        if lower_index is not None:
            cable.lower_index = lower_index
        if is_downto is not None:
            cable.is_downto = is_downto

        for k,v in properties.items():
            cable[k] = v

        return cable
