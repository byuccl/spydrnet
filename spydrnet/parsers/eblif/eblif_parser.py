import spydrnet as sdn
import spydrnet.parsers.eblif.eblif_tokens as et
from spydrnet.parsers.eblif.eblif_tokenizer import Tokenizer
from spydrnet.ir import Netlist
from spydrnet.ir import Instance
from spydrnet.ir import Port
from spydrnet.ir import InnerPin
from spydrnet.ir import Wire
from spydrnet.util.selection import Selection

class EBLIFParser:
    """
    Parse BLIF and EBLIF files into SpyDrNet

    """

    class BlackboxHolder:
        '''this is an internal class that helps manage
        modules that are instanced before they are declared'''

        def __init__(self):
            self.name_lookup = {}
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
        self.current_instance_info = {}
        self.current_instance = None
        self.default_names = {}
        self.comments = []
        self.current_model = None
        self.primitives = None
        self.work = None
        self.blackbox_holder = self.BlackboxHolder()

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
        netlist = Netlist()
        self.netlist = netlist
        self.work = self.netlist.create_library("work")
        self.primitives = self.netlist.create_library("hdi_primitives")
        while self.tokenizer.has_next():
            token = self.tokenizer.next()
            if token == et.COMMENT:
                self.parse_comment()
            elif token == et.MODEL:
                self.parse_model()
            else:
                None
        self.set_subcircuit_names_by_convention()
        self.insert_comments_into_netlist_data()
        self.add_blackbox_definitions()

    def parse_model(self):
        model_name = self.tokenizer.next()
        self.default_names = {}
        self.parse_model_header(model_name)
        self.parse_model_helper(model_name)

    def parse_model_helper(self, model_name):
        model = self.blackbox_holder.get_blackbox(model_name)
        is_blackbox = False
        while self.tokenizer.has_next():
            token = self.tokenizer.next()
            if token == et.COMMENT:
                self.parse_comment()
            elif token == et.SUBCIRCUIT:
                self.parse_subcircuit()
            elif token == et.GATE:
                self.parse_subcircuit(is_gate=True)
            elif token == et.LATCH:
                self.parse_latch()
            elif token == et.NAMES:
                self.parse_name()
            elif token == et.CONN:
                self.parse_conn()
            elif token == et.BLACKBOX:
                self.make_blackbox()
                is_blackbox = True
            elif token == et.END:
                break
            else:
                None
        if is_blackbox:
            self.primitives.add_definition(model)
        else:
            self.work.add_definition(model)

    def parse_model_header(self, model_name):
        model_def = self.blackbox_holder.get_blackbox(model_name)
        self.blackbox_holder.define(model_name)
        if not self.netlist.top_instance:
            parent_instance = Instance(name=model_def.name)
            parent_instance.reference = model_def
            self.netlist.set_top_instance(parent_instance)
            self.netlist.name = model_def.name
        self.current_model = model_def
        self.tokenizer.next() # should be end of line so proceed to next line
        self.parse_model_ports()

    def parse_model_ports(self):
        while self.tokenizer.peek() == et.INPUTS:
            self.parse_input_ports()
        while self.tokenizer.peek() == et.OUTPUTS:
            self.parse_output_ports()
        while self.tokenizer.peek() == et.CLOCK:
            self.parse_clock()

    def parse_input_ports(self):
        self.expect(et.INPUTS)
        self.tokenizer.next()
        while self.tokenizer.token is not et.NEW_LINE:
            port_name, index = self.get_port_name_and_index(self.tokenizer.token)
            index = int(index)
            port = next(self.current_model.get_ports(port_name), None)
            if not port:
                port = self.create_model_port(sdn.Port.Direction.IN, port_name)
                self.current_model.add_port(port)
            else:
                port.direction=sdn.IN
            while len(port.pins) < index+1:
                port.create_pin()
            pin = port.pins[index]
            self.connect_pin_to_wire(pin,port_name,index)
            self.tokenizer.next()

    def parse_output_ports(self):
        self.expect(et.OUTPUTS)
        self.tokenizer.next()
        while self.tokenizer.token is not et.NEW_LINE:
            is_inout = False
            port_name, index = self.get_port_name_and_index(self.tokenizer.token)
            index = int(index)
            port = next(self.current_model.get_ports(port_name), None)
            if not port:
                port = self.create_model_port(sdn.Port.Direction.OUT, port_name)
                self.current_model.add_port(port)
            if port.direction in {sdn.IN, sdn.INOUT}: # it's an input port and now an output, so it's inout
                port.direction = sdn.INOUT
                is_inout = True
            else:
                port.direction = sdn.OUT
            while len(port.pins) < index+1:
                port.create_pin()
            pin = port.pins[index]
            if not is_inout:
                self.connect_pin_to_wire(pin,port_name,index)
            self.tokenizer.next()

    def create_model_port(self, port_direction, port_name):
        port = Port(direction=port_direction)
        port.name = port_name
        return port

    def parse_clock(self):
        self.expect(et.CLOCK)
        self.tokenizer.next()
        try:
            self.current_model["EBLIF.clock"]
        except KeyError:
            self.current_model["EBLIF.clock"] = []
        while self.tokenizer.token is not et.NEW_LINE:
            self.current_model["EBLIF.clock"].append(self.tokenizer.token)
            self.tokenizer.next()

    def connect_pin_to_wire(self, pin, cable_name, wire_index):
        # connect the port to a wire in a cable named after it
        cable = next(self.current_model.get_cables(cable_name), None)
        if not cable:
            cable = self.current_model.create_cable(name=cable_name)
        while (len(cable.wires)-1) < wire_index: # add wires to cable until we get the right index
            wire = Wire()
            cable.add_wire(wire,wire_index)
        wire = cable.wires[wire_index]
        wire.connect_pin(pin)

    def parse_subcircuit(self, is_gate=False):
        self.current_instance_info.clear()
        reference_model = self.tokenizer.next()
        self.check_hierarchy(reference_model)
        definition = self.blackbox_holder.get_blackbox(reference_model)
        self.tokenizer.next()
        while self.tokenizer.token is not et.NEW_LINE:
            self.parse_subcircuit_port(definition)
            self.tokenizer.next()

        instance = self.current_model.create_child(reference=definition)
        self.current_instance = instance
        if is_gate:
            instance["EBLIF.type"] = "EBLIF.gate"
        else:
            instance["EBLIF.type"] = "EBLIF.subckt"

        self.assign_instance_a_default_name(instance)
        self.connect_instance_pins(instance)
        self.parse_instance_info()

    def parse_subcircuit_port(self, definition):
        token = self.tokenizer.token
        equal_index = token.find("=")
        port_name_and_index = token[:equal_index]
        name, index = self.get_port_name_and_index(port_name_and_index)
        port = next(definition.get_ports(name), None)
        if not port:
            port = definition.create_port(name=name)
        if index > (len(port.pins) - 1):
            pin = InnerPin()
            port.add_pin(pin,index)
        self.current_instance_info[port_name_and_index] = token[equal_index+1:]

    def check_hierarchy(self, child_definition_name):
        if child_definition_name == self.netlist.top_instance.reference.name:
            # print(self.current_definition.name + " is instancing the current top instance (" + name+ " which is a "+ self.netlist.top_instance.reference.name+")")
            old_top_instance = self.netlist.top_instance
            new_level = self.current_model
            # we know the current top is not right. So now we can move it up a level.
            # But double check to make sure nothing is instancing the potential new top.
            # Move up levels until we reach a new top
            if len(self.current_model.references) > 0:
                current_level = list(x for x in self.current_model.references)[0]
                while True:
                    current_level = current_level.parent
                    try:
                        current_level.parent
                    except AttributeError:
                        new_level = current_level
                        break

            self.netlist.top_instance = sdn.Instance()
            self.netlist.top_instance.name = new_level.name
            self.netlist.top_instance.reference = new_level
            self.netlist.name = new_level.name

            # this instance should just go away. It was created to be the top instance but we don't want that
            # it has no parent. And now with no reference, it should have no ties to the netlist.
            old_top_instance.reference = None

    def connect_instance_pins(self,instance):
        for key, cable_info in self.current_instance_info.items():
            # cable_info = self.current_instance_info[key]
            cable_name, cable_index = self.get_port_name_and_index(cable_info) # get connected cable name and wire index
            port_name, pin_index = self.get_port_name_and_index(key) # get own port name and pin index
            if cable_name == et.UNCONN:  # intentionally disconnected so put that into metadata
                try:
                    instance[et.UNCONN]
                except KeyError:
                    instance[et.UNCONN] = []
                instance[et.UNCONN].append(port_name+"["+str(pin_index)+"]")
                continue

            port = next(instance.get_ports(port_name))
            while len(port.pins) < (pin_index+1): # multibit port that isn't yet multibit
                port.create_pin()
            pin = next(instance.get_pins(selection=Selection.OUTSIDE, filter=lambda x: x.inner_pin.port.name == port_name and x.inner_pin is x.inner_pin.port.pins[pin_index]))
            self.connect_pin_to_wire(pin, cable_name, cable_index)

    def parse_comment(self):
        token = self.tokenizer.next()
        comment = ""
        while token is not et.NEW_LINE:
            comment+=token+" "
            token = self.tokenizer.next()
        self.comments.append(comment)

    def insert_comments_into_netlist_data(self):
        self.netlist["EBLIF.comment"] = self.comments

    def get_port_name_and_index(self,string):
        index_specified = (string[-1] == "]")
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
                    print("EBLIFParser: Index was: " + old_index + ". To avoid an error, it was changed to " + index)
                return name, int(index)
        else:
            return string, 0

    def assign_instance_a_default_name(self, instance):
        name = instance.reference.name
        index = 0
        if name in self.default_names.keys():
            index = self.default_names[name] + 1
            self.default_names[name]+=1
        else:
            index = 0
            self.default_names[name] = 0
        name = name + "_instance_" + str(index)
        instance.name = name

    def parse_instance_info(self):
        while True:
            peeked_token = self.tokenizer.peek()
            if peeked_token == et.PARAM:
                self.parse_param()
            elif peeked_token == et.CNAME:
                self.parse_cname()
            elif peeked_token == et.ATTRIBUTE:
                self.parse_attribute()
            else:
                if peeked_token == et.NEW_LINE:
                    self.tokenizer.next()
                    continue
                break

    def parse_param(self):
        self.expect(et.PARAM)
        token = self.tokenizer.next()
        info = self.tokenizer.next()
        try:
            self.current_instance["EBLIF.param"]
        except KeyError:
            self.current_instance["EBLIF.param"] = {}
        self.current_instance["EBLIF.param"][token] = info

    def parse_cname(self):
        self.expect(et.CNAME)
        name = self.tokenizer.next()
        self.current_instance["EBLIF.cname"] = name
        self.current_instance.name = name

    def parse_attribute(self):
        self.expect(et.ATTRIBUTE)
        key = self.tokenizer.next()
        value = self.tokenizer.next()
        try:
            self.current_instance["EBLIF.attr"]
        except KeyError:
            self.current_instance["EBLIF.attr"] = {}
        self.current_instance["EBLIF.attr"][key] = value

    def parse_name(self):
        self.current_instance_info.clear()
        self.tokenizer.next()
        port_nets = []
        while self.tokenizer.token is not et.NEW_LINE:
            port_nets.append(self.tokenizer.token)
            self.tokenizer.next()
        single_output_covers = []
        while (self.check_if_init_values(self.tokenizer.peek())): # make sure next token is init values
            single_output_cover=self.tokenizer.next()
            single_output_cover+=" "
            possible_next = self.tokenizer.next()
            if possible_next != et.NEW_LINE:
                single_output_cover+=possible_next
                self.tokenizer.next()
            single_output_covers.append(single_output_cover)

        # then make/get def called logic-gate_# where # is the # of ports-1
        name = "logic-gate_"+str(len(port_nets)-1)
        definition = self.blackbox_holder.get_blackbox(name)
        for i in range(len(port_nets)-1):
            port_name = "in_" + str(i)
            port = next(definition.get_ports(port_name), None)
            if not port:
                port = self.create_names_port("in_" + str(i), Port.Direction.IN)
                definition.add_port(port)
        if not next(definition.get_ports("out"), None):
            definition.add_port(self.create_names_port("out", Port.Direction.OUT))

        # then create an instance of it
        instance = self.current_model.create_child(reference=definition)
        self.current_instance = instance
        instance["EBLIF.output_covers"] = single_output_covers
        instance["EBLIF.type"] = "EBLIF.names"

        for port, net in zip(definition.get_ports(),port_nets):
            self.current_instance_info[port.name] = net
        if "unconn" in port_nets[len(port_nets)-1]:
            self.assign_instance_a_default_name(instance)
        else:
            instance.name = port_nets[len(port_nets)-1] # by convention, the name of the instance is the name of the driven net

        self.connect_instance_pins(instance)
        self.parse_instance_info()

    def check_if_init_values(self,string):
        allowed = {'1','0','-'}
        for char in string:
            if char not in allowed:
                return False
        return True

    def create_names_port(self, name, direction):
        port = Port(direction=direction)
        port.name = name
        port.create_pin()
        return port

    def parse_latch(self):
        self.current_instance_info.clear()
        self.tokenizer.next() # first collect the information
        port_order = ["input","output","type","control","init-val"]
        token_list = []
        port_info = {}
        while self.tokenizer.token is not et.NEW_LINE:
            token_list.append(self.tokenizer.token)
            self.tokenizer.next()
        for order, token in zip(port_order,token_list):
            port_info[order] = token

        name = "generic-latch"
        definition = self.blackbox_holder.get_blackbox(name)
        if len(definition.ports) == 0:
            for order in port_info.keys() :
                if order == "output":
                    port = self.create_names_port(order, Port.Direction.OUT)
                    definition.add_port(port)
                else:
                    port = self.create_names_port(order, Port.Direction.IN)
                    definition.add_port(port)

        # create an instance of it
        instance = self.current_model.create_child(reference=definition)
        instance.name = port_info["output"] # by convention, the latch name is the name of the net it drives
        self.current_instance = instance
        instance["EBLIF.type"] = "EBLIF.latch"

        # then connect the nets to the ports
        for port, net in port_info.items():
            self.current_instance_info[port] = net
        self.connect_instance_pins(instance)
        self.parse_instance_info()

    def parse_conn(self):
        cable_one_info = self.tokenizer.next()
        cable_two_info = self.tokenizer.next()
        cable_one_name, cable_one_index = self.get_port_name_and_index(cable_one_info)
        cable_two_name, cable_two_index = self.get_port_name_and_index(cable_two_info)
        wire_one, wire_two = self.get_connected_wires(cable_one_name, cable_one_index, cable_two_name, cable_two_index)
        self.merge_wires(wire_one, wire_two)

    def get_connected_wires(self, cable_one_name, index_one, cable_two_name, index_two):
        cable_one = next(self.current_model.get_cables(cable_one_name), None)
        if not cable_one:
            cable_one = self.current_model.create_cable(name=cable_one_name)
        while len(cable_one.wires) < (index_one + 1):
            cable_one.create_wire()
        wire_one = cable_one.wires[index_one]

        cable_two = next(self.current_model.get_cables(cable_two_name), None)
        if not cable_two:
            cable_two = self.current_model.create_cable(name=cable_two_name)
        while len(cable_two.wires) < (index_two + 1):
            cable_two.create_wire()
        wire_two = cable_two.wires[index_two]
        return wire_one, wire_two

    def merge_wires(self, wire_one, wire_two):
        # merge them into one new wire inside a new cable and throw both wires away
        name_one = wire_one.cable.name + "_" + str(wire_one.index())
        name_two = wire_two.cable.name + "_" + str(wire_two.index())
        new_cable_name = name_one + "_" + name_two
        new_cable = self.current_model.create_cable(name=new_cable_name)
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
            if instance["EBLIF.type"] not in ["EBLIF.subckt", "EBLIF.gate"]:
                continue
            if "EBLIF.cname" in instance.data:
                continue
            iterator = instance.get_pins(selection=Selection.OUTSIDE, filter=lambda x: x.inner_pin.port.direction is sdn.OUT)
            while True:
                pin = next(iterator, None)
                if pin:
                    if pin.wire:
                        name = pin.wire.cable.name
                        if len(pin.wire.cable.wires) > 1:
                            name+="_"+str(pin.wire.cable.wires.index(pin.wire))
                        instance.name = name
                        break
                else:
                    break

    def expect(self, token):
        self.tokenizer.next()
        self.tokenizer.expect(token)

    def make_blackbox(self):
        # self.current_model["EBLIF.blackbox"] = True
        self.current_model.remove_cables_from(self.current_model.cables)

    def add_blackbox_definitions(self):
        for d in self.blackbox_holder.get_undefined_blackboxes():
            # d["EBLIF.blackbox"] = True
            self.primitives.add_definition(d)
