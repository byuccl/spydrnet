import spydrnet as sdn
from spydrnet.parsers.eblif.eblif_tokens import *
from spydrnet.parsers.eblif.eblif_tokenizer import Tokenizer
from spydrnet.ir import Netlist
from spydrnet.ir import Definition
from spydrnet.ir import Instance
from spydrnet.ir import Port
from spydrnet.ir import InnerPin
from spydrnet.ir.outerpin import OuterPin
from spydrnet.ir import Wire
from spydrnet.util.selection import Selection

class EBLIFParser:
    """
    Parse BLIF and EBLIF files into SpyDrNet

    The first model is considered the netlist's top instance. Any model that follows is used as information for the definitions (aka primitive information)

    """
    #######################################################
    # setup functions
    #######################################################
    @staticmethod
    def from_filename(filename):
        parser = EBLIFParser()
        parser.file_name = filename
        return parser

    @staticmethod
    def from_file_handle(file_handle):
        parser = EBLIFParser()
        parser.file_name = file_handle
        return parser

    def __init__(self):
        self.file_name = None
        self.tokenizer = None
        self.netlist = None
        self.current_instance_info = dict()
        # self.top_instance = None
        self.current_instance = None
        # self.latest_definition = None
        # self.information = dict()
        self.definitions = dict()
        self.cables = dict()
        self.default_names = dict()
        self.top_level_input_ports = dict()
        self.top_level_output_ports = dict()       
        self.comments = list() 
        self.current_model = None
        # self.last_net = None

    def createTokenizer(self):
        self.tokenizer = Tokenizer(self.file_name)

    #######################################################
    # parse functions
    #######################################################
    def parse(self):
        self.createTokenizer()
        self.parse_eblif()
        return self.netlist
    
    def parse_eblif(self):
        while(self.tokenizer.has_next()):
            token = self.tokenizer.next()
            if token == COMMENT:
                self.parse_comment()
            elif token == MODEL:
                if self.netlist:
                    self.parse_other_model()
                else:
                    self.parse_top_model()
            else:
                None
        self.set_subcircuit_names_by_convention()
        self.insert_comments_into_netlist_data()

    def parse_top_model(self):
        netlist = Netlist()
        name = self.tokenizer.next()
        netlist.name = name
        self.netlist = netlist
        self.parse_top_instance()
        self.parse_model_helper()

    def parse_other_model(self):
        name = self.tokenizer.next()
        try:
            self.definitions[name]
        except KeyError:
            # print("Error, no definition found")
            self.definitions[name] = self.create_new_definition()
        definition = self.definitions[name]
        self.tokenizer.next()

        while(self.tokenizer.peek() == INPUTS):
            self.parse_other_model_input_ports(definition)
        
        while(self.tokenizer.peek() == OUTPUTS):
            self.parse_other_model_output_ports(definition)

        while (True):
            self.tokenizer.next()
            if (self.tokenizer.token == BLACKBOX):
                definition["EBLIF.blackbox"] = True
            elif self.tokenizer.token == END:
                break   
    
    def parse_other_model_input_ports(self,definition):
        self.expect(INPUTS)
        self.tokenizer.next()
        while (self.tokenizer.token is not NEW_LINE):
            port_name, index = self.get_port_name_and_index(self.tokenizer.token)
            index = int(index)
            port = next(definition.get_ports(filter=lambda x: x.name == port_name))
            port.direction = sdn.IN
            self.tokenizer.next()
    
    def parse_other_model_output_ports(self,definition):
        self.expect(OUTPUTS)
        self.tokenizer.next()
        while (self.tokenizer.token is not NEW_LINE):
            port_name, index = self.get_port_name_and_index(self.tokenizer.token)
            port = next(definition.get_ports(filter=lambda x: x.name == port_name))
            port.direction = sdn.OUT
            self.tokenizer.next()
    
    def parse_model_helper(self):
         while(self.tokenizer.has_next()):
            token = self.tokenizer.next()
            if token == COMMENT:
                self.parse_comment()
            elif token == SUBCIRCUIT:
                self.parse_sub_circuit()
            elif token == GATE:
                self.parse_sub_circuit(is_gate=True)
            elif token == LATCH:
                self.parse_latch()
            elif token == NAMES:
                self.parse_name()
            elif token == CONN:
                self.parse_conn()
            elif token == END:
                break
            else:
                None
    
    def parse_top_instance(self):
        # Libraries aren't in blif, so just create a single library
        library = self.netlist.create_library(name="library_1")
        top_instance_def = library.create_definition(name=self.netlist.name)
        top_instance = Instance(name=top_instance_def.name)
        top_instance.reference = top_instance_def
        self.netlist.set_top_instance(top_instance)
        self.current_model = top_instance
        self.tokenizer.next() # should be end of line so proceed to next line
        self.parse_top_level_ports()
    
    def parse_top_level_ports(self):
        while(self.tokenizer.peek() == INPUTS):
            self.parse_top_level_inputs()
        while(self.tokenizer.peek() == OUTPUTS):
            self.parse_top_level_outputs()

        while(self.tokenizer.peek() == CLOCK):
            self.parse_top_level_clock()
    
    def parse_top_level_inputs(self):
        self.expect(INPUTS)
        self.tokenizer.next()
        while (self.tokenizer.token is not NEW_LINE):
            port_name, index = self.get_port_name_and_index(self.tokenizer.token)
            index = int(index)
            port = None
            pin = None
            if (port_name in self.top_level_input_ports.keys()):
                port= self.top_level_input_ports[port_name]
                pin = port.create_pin()
            else:
                port = self.create_top_level_port(sdn.Port.Direction.IN,port_name)
                self.netlist.top_instance.reference.add_port(port)
                self.top_level_input_ports[port_name] = port
                pin = port.create_pin()
            self.connect_pins_to_wires(pin,port_name,index)
            self.tokenizer.next()
    
    def parse_top_level_outputs(self):
        self.expect(OUTPUTS)
        self.tokenizer.next()
        while (self.tokenizer.token is not NEW_LINE):
            port_name, index = self.get_port_name_and_index(self.tokenizer.token)
            index = int(index)
            port = None
            pin = None
            if (port_name in self.top_level_output_ports.keys()):
                port= self.top_level_output_ports[port_name]
                pin = port.create_pin()
            else:
                port = self.create_top_level_port(sdn.Port.Direction.OUT,port_name)
                self.netlist.top_instance.reference.add_port(port)
                self.top_level_output_ports[port_name] = port
                pin = port.create_pin()
            self.connect_pins_to_wires(pin,port_name,index)
            self.tokenizer.next()
    
    def parse_top_level_clock(self):
        self.expect(CLOCK)
        self.tokenizer.next()
        try:
            self.netlist.top_instance["EBLIF.clock"]
        except KeyError:
            self.netlist.top_instance["EBLIF.clock"] = list()
        while (self.tokenizer.token is not NEW_LINE):
            self.netlist.top_instance["EBLIF.clock"].append(self.tokenizer.token)
            self.tokenizer.next()

    def create_top_level_port(self,port_direction,port_name):
        port = Port(direction=port_direction)
        port.name = port_name
        return port
    
    def connect_pins_to_wires(self, pin, cable_name, wire_index):
        # connect the port to a wire in a cable named after it
        cable = None
        if (cable_name in self.cables.keys()):
            cable = self.cables[cable_name]
        else:
            cable = self.netlist.top_instance.reference.create_cable(name=cable_name)
            self.cables[cable_name] = cable
        try:
            cable.wires[wire_index]
        except IndexError:
            while (len(cable.wires)-1 < wire_index): # add wires to cable until we get the right index
                wire = Wire()
                cable.add_wire(wire,wire_index)
            # wire = Wire()
            # cable.add_wire(wire,wire_index)
        wire = cable.wires[wire_index]
        wire.connect_pin(pin)

    def parse_sub_circuit(self,is_gate=False):
        # print(self.tokenizer.token)
        self.current_instance_info.clear()
        reference_model = self.tokenizer.next()
        definition = None
        if reference_model not in list(key for key in self.definitions.keys()):  # if the reference model is not found in the netlist, create it
            definition = self.create_new_definition()
            # Note: if a definition is created, instance information is automatically collected
        else:
            definition = self.definitions[reference_model]
            self.collect_subcircuit_information()
        instance = self.netlist.top_instance.reference.create_child(reference = definition)
        self.current_instance = instance
        if is_gate:
            instance["EBLIF.type"] = "EBLIF.gate"
        else:
            instance["EBLIF.type"] = "EBLIF.subckt"
        self.assign_instance_a_default_name(instance)
        # print(self.current_instance_info)
        self.connect_instance_pins(instance)
        self.check_for_and_add_more_instance_info()

    def create_new_definition(self):
        definition = self.netlist.libraries[0].create_definition(name = self.tokenizer.token)
        # print("GONNA MAKE DEFINITION: " + self.tokenizer.token)
        self.tokenizer.next()
        # print("now token is "+self.tokenizer.token)
        while (self.tokenizer.token is not NEW_LINE):
            self.parse_definition_port(definition)
            self.tokenizer.next()
        self.definitions[definition.name] = definition
        return definition

    def parse_definition_port(self,definition):
        port = Port()
        token = self.tokenizer.token
        equal_index = token.find("=")
        port_name_and_index = token[:equal_index]
        name,index = self.get_port_name_and_index(port_name_and_index)
        if name in list(x.name for x in definition.ports):
            # print(name + " is in "+ str(list(x.name for x in definition.ports)))
            port = next(x for x in definition.ports if x.name == name)
            pin = InnerPin()
            port.add_pin(pin,index)
            # print("added a pin at index "+str(index))
            self.current_instance_info[port_name_and_index] = token[equal_index+1:]
        else:
            new_port = Port()
            new_port.name = name
            pin = InnerPin()
            new_port.add_pin(pin,index)
            self.current_instance_info[port_name_and_index] = token[equal_index+1:]
            definition.add_port(new_port)
            # port.create_pin()
        # return port

    def collect_subcircuit_information(self):
        self.tokenizer.next()
        while (self.tokenizer.token is not NEW_LINE):
            token = self.tokenizer.token
            equal_index = token.find("=")
            port_name =token[:equal_index]
            self.current_instance_info[port_name] = token[equal_index+1:]
            self.tokenizer.next()

    def connect_instance_pins(self,instance):
        for key in self.current_instance_info.keys():
            cable_info = self.current_instance_info[key]
            cable_name,cable_index = self.get_port_name_and_index(cable_info) # get connected cable name and wire index
            port_name, pin_index = self.get_port_name_and_index(key) # get own port name and pin index
            if (cable_name == UNCONN):  # intentionally disconnected so put that into metadata
                try:
                    instance[UNCONN]
                except KeyError:
                    instance[UNCONN] = list()
                instance[UNCONN].append(port_name+"["+str(pin_index)+"]")
                continue
            # print(port_name)
            # print(list(x.inner_pin.port.name for x in instance.get_pins(selection=Selection.OUTSIDE)))
            pin = next(instance.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.name == port_name and x.inner_pin is x.inner_pin.port.pins[pin_index]))
            self.connect_pins_to_wires(pin,cable_name,cable_index)

    def parse_comment(self):
        token = self.tokenizer.next()
        comment = ""
        while (token is not NEW_LINE):
            comment+=token+" "
            token = self.tokenizer.next()
        self.comments.append(comment)
    
    def insert_comments_into_netlist_data(self):
        self.netlist["EBLIF.comment"] = self.comments

    def expect(self, token):
        self.tokenizer.next()
        self.tokenizer.expect(token)

    def get_port_name_and_index(self,string):
        index_specified = (string[len(string)-1] == "]")
        if index_specified:
            open_bracket = string.rfind("[")
            if open_bracket == -1:
                return string, 0
            else:
                close_bracket = string.find("]",open_bracket)
                name = string[:open_bracket]
                index = string[open_bracket+1:close_bracket]
                if ":" in index:
                    old_index = index
                    index = index[:index.find(':')]
                    print("Index was: "+old_index+". To avoid an error, it was changed to "+index)
                return name, int(index)
        else:
            return string, 0

    def assign_instance_a_default_name(self,instance):
        name = instance.reference.name
        index = 0
        if name in self.default_names.keys():
            index = self.default_names[name]+1
            self.default_names[name]+=1
        else:
            index = 0
            self.default_names[name] = 0
        name = name+"_instance_"+str(index)
        instance.name = name
    
    def check_for_and_add_more_instance_info(self):
        while(True):
            peeked_token = self.tokenizer.peek()
            if (peeked_token == PARAM):
                self.parse_param()
            elif (peeked_token == CNAME):
                self.parse_cname()
            elif (peeked_token == ATTRIBUTE):
                self.parse_attribute()
            else:
                if (peeked_token == NEW_LINE):
                    self.tokenizer.next()
                    continue
                break
        
    def parse_param(self):
        self.expect(PARAM)
        token = self.tokenizer.next()
        info = self.tokenizer.next()
        try: 
            self.current_instance["EBLIF.param"]
        except KeyError:
            self.current_instance["EBLIF.param"] = dict()
        self.current_instance["EBLIF.param"][token] = info
    
    def parse_cname(self):
        self.expect(CNAME)
        name = self.tokenizer.next()
        self.current_instance["EBLIF.cname"] = name
        self.current_instance.name = name

    def parse_attribute(self):
        self.expect(ATTRIBUTE)
        key = self.tokenizer.next()
        value = self.tokenizer.next()
        try:
            self.current_instance["EBLIF.attr"]
        except KeyError:
            self.current_instance["EBLIF.attr"] = dict()
        self.current_instance["EBLIF.attr"][key] = value

    def parse_name(self):
        self.current_instance_info.clear()
        self.tokenizer.next()
        # if self.look_for_true_false_undef():
        #     return
        port_nets = list()
        while (self.tokenizer.token is not NEW_LINE):
            port_nets.append(self.tokenizer.token)
            self.tokenizer.next()
        single_output_covers = list()
        while (self.check_if_init_values(self.tokenizer.peek())): # make sure next token is init values
            single_output_cover=self.tokenizer.next()
            single_output_cover+=" "+self.tokenizer.next()
            self.tokenizer.next()
            single_output_covers.append(single_output_cover)
    
        # then make/get def called LUT_names_# where # is the # of ports-1
        name = "logic-gate_"+str(len(port_nets)-1)
        try:
            self.definitions[name]
        except KeyError:
            definition = self.netlist.libraries[0].create_definition(name=name)
            self.definitions[name] = definition
            for i in range(len(port_nets)-1):
                port = self.create_names_port("in_"+str(i),Port.Direction.IN)
                definition.add_port(port)
            definition.add_port(self.create_names_port("out",Port.Direction.OUT))
        definition = self.definitions[name]

        # then create an instance of it
        instance = self.netlist.top_instance.reference.create_child()
        instance.reference = definition
        instance["EBLIF.output_covers"] = single_output_covers
        # self.assign_instance_a_default_name(instance)
        self.current_instance = instance
        instance["EBLIF.type"] = "EBLIF.names"
     
        for port, net in zip(definition.get_ports(),port_nets):
            self.current_instance_info[port.name] = net
        if "unconn" in port_nets[len(port_nets)-1]:
            self.assign_instance_a_default_name(instance)
        else:
            instance.name = port_nets[len(port_nets)-1] # by convention, the name of the instance is the name of the driven net

        self.connect_instance_pins(instance)
        self.check_for_and_add_more_instance_info()

    def check_if_init_values(self,string):
        allowed = {'1','0','-'}
        for char in string:
            if char not in allowed:
                return False
        return True

    def look_for_true_false_undef(self):
        if self.tokenizer.token in [TRUE_WIRE,FALSE_WIRE,UNDEF_WIRE]:
            try:
                self.netlist["EBLIF.default_wires"]
            except KeyError:
                self.netlist["EBLIF.default_wires"] = list()
            self.netlist["EBLIF.default_wires"].append(self.tokenizer.token)
            if (self.tokenizer.token is TRUE_WIRE):
                self.tokenizer.next()
                self.tokenizer.next()
            else:
                self.tokenizer.next()
            return True
        return False

    def create_names_port(self,name,direction):
        port = Port(direction=direction)
        port.name = name
        port.create_pin()
        return port

    def parse_latch(self):
        self.current_instance_info.clear()
        self.tokenizer.next() # first collect the information
        port_order = ["input","output","type","control","init-val"]
        token_list = list()
        port_info = dict()
        while (self.tokenizer.token is not NEW_LINE):
            token_list.append(self.tokenizer.token)
            self.tokenizer.next()
        for order, token in zip(port_order,token_list):
            port_info[order] = token

        name = "generic-latch"
        try:
            self.definitions[name]
        except KeyError:
            definition = self.netlist.libraries[0].create_definition(name=name)
            self.definitions[name] = definition
            for order in port_info.keys() :
                if order != "output":
                    port = self.create_names_port(order,Port.Direction.IN)
                    definition.add_port(port)
                else:
                    port = self.create_names_port(order,Port.Direction.OUT)
                    definition.add_port(port)
        definition = self.definitions[name]

        # create an instance of it
        instance = self.netlist.top_instance.reference.create_child()
        instance.reference = definition
        # self.assign_instance_a_default_name(instance)
        instance.name = port_info["output"] # by convention, the latch name is the name of the net it drives
        self.current_instance = instance
        instance["EBLIF.type"] = "EBLIF.latch"

        # then connect the nets to the ports
        for port, net in port_info.items():
            self.current_instance_info[port] = net
        self.connect_instance_pins(instance)
        self.check_for_and_add_more_instance_info()

    def parse_conn(self):
        cable_one_info = self.tokenizer.next()
        cable_two_info = self.tokenizer.next()
        cable_one_name,cable_one_index = self.get_port_name_and_index(cable_one_info)
        cable_two_name,cable_two_index = self.get_port_name_and_index(cable_two_info)
        wire_one,wire_two = self.get_connected_wires(cable_one_name,cable_one_index,cable_two_name,cable_two_index)
        self.merge_wires(wire_one,wire_two)

    def get_connected_wires(self,cable_one_name,index_one,cable_two_name,index_two):
        cable_one = None
        cable_two = None
        if (cable_one_name in self.cables.keys()):
            cable_one = self.cables[cable_one_name]
        else:
            cable_one = self.netlist.top_instance.reference.create_cable(name=cable_one_name)
            self.cables[cable_one_name] = cable_one
        try:
            cable_one.wires[index_one]
        except IndexError:
            wire = Wire()
            cable_one.add_wire(wire,index_one)
        wire_one = cable_one.wires[index_one]

        if (cable_two_name in self.cables.keys()):
            cable_two = self.cables[cable_two_name]
        else:
            cable_two = self.netlist.top_instance.reference.create_cable(name=cable_two_name)
            self.cables[cable_two_name] = cable_two
        try:
            cable_two.wires[index_two]
        except IndexError:
            wire = Wire()
            cable_two.add_wire(wire,index_two)
        wire_two = cable_two.wires[index_two]
        return wire_one,wire_two

    def merge_wires(self,wire_one,wire_two):
        # merge them into one new wire inside a new cable and throw both wires away
        name_one = wire_one.cable.name+"_"+str(wire_one.index())
        name_two = wire_two.cable.name+"_"+str(wire_two.index())
        new_cable_name = name_one+"_"+name_two
        new_cable = self.current_model.reference.create_cable(name=new_cable_name)
        new_wire = new_cable.create_wire()

        wire_one_pins = wire_one.pins.copy()
        for pin in wire_one_pins:
            pin.wire.disconnect_pin(pin)
            new_wire.connect_pin(pin)
        wire_one.cable.remove_wire(wire_one)

        wire_two_pins = wire_two.pins.copy()
        for pin in wire_two_pins:
            pin.wire.disconnect_pin(pin)
            new_wire.connect_pin(pin)
        wire_two.cable.remove_wire(wire_two)

    def set_subcircuit_names_by_convention(self): # by convention, the instance names are defined by the net they drive
        for instance in self.netlist.get_instances(): 
            if instance["EBLIF.type"] in ["EBLIF.subckt","EBLIF.gate"]:
                if "EBLIF.cname" not in instance.data:
                    pin = next(instance.get_pins(selection=Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.direction is sdn.OUT),None)
                    if pin:
                        if pin.wire:
                            name = pin.wire.cable.name
                            if len(pin.wire.cable.wires) > 1:
                                name+="_"+str(pin.wire.cable.wires.index(pin.wire))
                            instance.name = name