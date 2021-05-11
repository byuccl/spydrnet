from collections import deque, OrderedDict
from spydrnet.ir.port import Port


class Composer:

    def __init__(self):
        self.file = None
        self.direction_string_map = dict()
        self.direction_string_map[Port.Direction.IN] = "input"
        self.direction_string_map[Port.Direction.OUT] = "output"
        self.direction_string_map[Port.Direction.INOUT] = "inout"
        self.direction_string_map[Port.Direction.UNDEFINED] = "/* undefined port direction */ inout"
        self.written = set()

    def run(self, ir, file_out = "out.v"):
        self._open_file(file_out)
        self._compose(ir)
        

    def _open_file(self, file_name):
        f = open(file_name, "w")
        self.file = f

    def _compose(self, netlist):
        self._write_header(netlist)
        instance = netlist.top_instance
        if instance is not None:
            self._write_from_top(instance)
        for library in netlist.libraries:
            for definition in library.definitions:
                if definition not in self.written:
                    self._write_definition_single(definition)

        
    def _write_header(self, netlist):
        self.file.write("////////////////////////////////////////\n")
        self.file.write("//File generated by SpyDrNet\n")
        if netlist.name is not None:
            self.file.write("//Netlist: " + netlist.name + "\n")
        self.file.write("////////////////////////////////////////\n")
        if netlist.top_instance is None:
            print("WARNING: Netlist has no top instance. Empty file written")
            self.file.write("//top instance is none.\n")

    def _write_from_top(self, instance):
        #self.written = set()
        to_write = deque()
        to_write.append(instance.reference)
        self.file.write('(* STRUCTURAL_NETLIST = "yes" *)\n')
        while(len(to_write) != 0):
            definition = to_write.popleft()
            if definition in self.written:
                continue
            self.written.add(definition)
            for c in definition.children:
                if c.reference not in self.written:
                    to_write.append(c.reference)
            if definition.name is None:
                raise Exception("Definition: ",definition, " .name is undefined")
            self._write_definition_single(definition)

    def _write_definition_single(self, definition):
        if definition.library.name == "SDN_VERILOG_ASSIGNMENT":
            #no need to write assignment definitions.
            return
        need_end_primitive = False
        #if "VERILOG.primitive" in definition and definition["VERILOG.primitive"] == True:
        if definition.library.name == "SDN.verilog_primitives":
            need_end_primitive = True
            self.file.write("`celldefine\n")
        # else:
        self.file.write("module ")

        self._write_escapable_name(definition.name)
        self.file.write("\n")
        self._write_ports(definition)

        for c in definition.cables:
            self._write_cable(c)

        for i in definition.children:
            if i.reference.library.name == "SDN_VERILOG_ASSIGNMENT":
                self._write_assignments(i)
            else:
                self._write_instanciation(i)
        
        # for c in definition.cables:
        #     self._write_assignments(c)

        self.file.write("endmodule\n")
        if need_end_primitive:
            self.file.write("`endcelldefine\n")

    def _get_wire_indicies_in_cable(self, wire):
        '''return the index of the given wire'''
        cable = wire.cable
        return cable.wires.index(wire) + cable.lower_index


    def _get_assignment_cable_indicies_from_port(self, port, instance):
        '''get the cable associated with the outer pins on the instance's port.'''
        
        right_pin = port.pins[0]
        left_pin = port.pins[-1]
        right_pin = instance.pins[right_pin]
        left_pin = instance.pins[left_pin]
        
        
        
        left_wire = left_pin.wire
        right_wire = right_pin.wire
        assert left_wire.cable == right_wire.cable

        if not left_wire.cable.is_downto:
            temp = right_wire
            right_pin = left_wire
            left_wire = temp

        left = self._get_wire_indicies_in_cable(left_wire)
        right = self._get_wire_indicies_in_cable(right_wire)

        name = left_wire.cable.name

        cable = left_wire.cable

        if max(left,right) == (cable.lower_index + len(cable.wires) - 1) and min(left, right) == cable.lower_index:
            left = None
            right = None
        elif left == right:
            left = None
        

        return name, left, right

    def _get_assignment_indicies(self, instance):
        '''it should only be one cable per assignment port the instance must also be an assignment instance'''
        definition = instance.reference
        in_port = next(definition.get_ports("i"), None)
        assert in_port != None
        out_port = next(definition.get_ports("o"), None)
        assert out_port != None

        cable_in_name, in_left, in_right = self._get_assignment_cable_indicies_from_port(in_port, instance)
        cable_out_name, out_left, out_right = self._get_assignment_cable_indicies_from_port(out_port, instance)

        return cable_in_name, cable_out_name, in_left, in_right, out_left, out_right
    # def _get_assignment_indicies(self, instance):
    #     porta = instance.reference.ports[0]
    #     portb = instance.reference.ports[1]
    #     name_list = instance.name.split("_")
    #     width = int(name_list[3])
    #     pin1 = instance.pins[porta.pins[0]]
    #     pin2 = instance.pins[porta.pins[width-1]]
    #     pin3 = instance.pins[portb.pins[0]]
    #     pin4 = instance.pins[portb.pins[width - 1]]
    #     wire1 = pin1.wire
    #     wire2 = pin2.wire
    #     wire3 = pin3.wire
    #     wire4 = pin4.wire
    #     cable1 = wire1.cable
    #     cable2 = wire3.cable
    #     if width == 1:
    #         if len(cable1.wires) == width:
    #             index1 = None
    #             index2 = None
    #         else:
    #             index1 = cable1.wires.index(wire1) + cable1.lower_index
    #             index2 = None
    #         if len(cable2.wires) == width:
    #             index3 = None
    #             index4 = None
    #         else:
    #             index3 = cable2.wires.index(wire3) + cable2.lower_index
    #             index4 = None
    #     else:
    #         if len(cable1.wires) == width:
    #             index1 = None
    #             index2 = None
    #         else:
    #             index1 = cable1.wires.index(wire1) + cable1.lower_index
    #             index2 = cable1.wires.index(wire2) + cable1.lower_index
    #         if len(cable2.wires) == width:
    #             index3 = None
    #             index4 = None
    #         else:
    #             index3 = cable2.wires.index(wire3) + cable2.lower_index
    #             index4 = cable2.wires.index(wire4) + cable2.lower_index

    #     return cable1.name, cable2.name, index1, index2, index3, index4
        

    def _write_assignment_single_cable(self, cable_name, low, high):
        self._write_escapable_name(cable_name)
        if high != None:
            self.file.write("[")
            self.file.write(str(high))
            if low!=None:
                self.file.write(":")
                self.file.write(str(low))
            self.file.write("]")

    def _write_assignments(self, instance):
        cable_in_name, cable_out_name, in_low, in_high, out_low, out_high = self._get_assignment_indicies(instance)
        self.file.write("assign ")
        self._write_assignment_single_cable(cable_out_name, out_low, out_high)
        self.file.write(" = ")
        self._write_assignment_single_cable(cable_in_name, in_low, in_high)
        self.file.write(";\n")

    # def _write_ports(self, definition):
    #     self.file.write("(\n    ")
    #     first = True
    #     port_to_rename = dict()
    #     in_rename = set()
    #     for p in definition.ports:
    #         highest_position = 0
    #         rename_members = OrderedDict()
    #         for k,v in p.data.items():
    #             k = k.split(".")
    #             if k[0] == "VERILOG" and k[1] == "port_rename":
    #                 rename = True
    #                 position = k[2]
    #                 if int(position) > highest_position:
    #                     highest_position = int(position)
    #                 rename_members[int(position)] = v
    #             elif k[0] == "VERILOG" and k[1] == "port_rename_member" and v == "true":
    #                 in_rename.add(p)
    #                 continue

    #         if len(rename_members.keys()) == 0:
    #             pass
    #         elif len(rename_members.keys()) == 1:
    #             port_to_rename[p] = rename_members[0]
    #         else:
    #             rename_str = "{ "
    #             for i in range(highest_position+1):
    #                 if i == 0:
    #                     pass
    #                 else:
    #                     rename_str += " , "
    #                 rename_str += rename_members[i]
                    
    #             rename_str += " } "
    #             port_to_rename[p] = rename_str
                    
    #     for p in definition.ports:
    #         if p in in_rename:
    #             continue
              
    #         if first:
    #             #self.file.write(p.name)    
    #             first = False
    #         else:
    #             self.file.write(",\n    ")
    #             #self.file.write(p.name)
    #         if p in port_to_rename:
    #             self.file.write(".")
    #             self._write_escapable_name(p.name)
    #             self.file.write("(")
    #             self.file.write(port_to_rename[p])
    #             self.file.write(")")
    #         else:
    #             self._write_escapable_name(p.name)
    #     self.file.write("\n);\n")
    #     for p in definition.ports:
    #         if p in port_to_rename:
    #             continue
            
    #         self.file.write(self.direction_string_map[p.direction])
    #         self.file.write(" ")
    #         if not p.is_scalar:
    #             if p.is_downto:
    #                 left = p.lower_index + len(p.pins) - 1
    #                 right = p.lower_index
    #             else:
    #                 left = p.lower_index
    #                 right = p.lower_index + len(p.pins) - 1
    #             self.file.write("["+str(left)+":"+str(right)+"]")
    #         #self.file.write(p.name)
    #         self._write_escapable_name(p.name)
    #         self.file.write(";\n")

    def _write_ports(self, definition):
        '''write all ports in the netlist. needs to take into account port aliasing as well'''
        self._write_header_ports(definition)
        self._write_port_list(definition)

    
    def _write_header_ports(self, definition):
        self.file.write("(")
        first = "\n    "
        for p in definition.ports:
            cables = self._get_cable_list_from_port(p)
            self.file.write(first)
            cable = cables.pop()
            if len(cables) == 0 and cable.name == p.name:
                self._write_escapable_name(p.name)
            else:
                wires = self._get_wires_list_from_port(p)
                self.file.write(".")
                self._write_escapable_name(p.name)
                self.file.write("({")
                between = ""
                for w in wires:
                    self.file.write(between)
                    if w is not None:
                        self._write_escapable_name(w.cable.name)
                        index = self._get_wire_indicies_in_cable(w)
                        self.file.write("[" + str(index) + "]")
                    between = ", "
                self.file.write("})")

            first = ",\n    "
        self.file.write("\n);\n")

    def _get_wires_list_from_port(self, port):
        wires = list()
        none_exist = True
        for p in port.pins:
            if p.wire is not None:
                none_exist = False
            wires.append(p.wire)
        if none_exist:
            return list()
        return wires


    def _get_cable_list_from_port(self, port):
        cables = set()
        for p in port.pins:
            if p.wire != None:
                cables.add(p.wire.cable)
        return cables

    def _write_port_list(self, definition):
        first = "\n"
        for p in definition.ports:
            cables = self._get_cable_list_from_port(p)
            for c in cables:
                self.file.write(first)
                self.file.write(self.direction_string_map[p.direction])
                self.file.write(" ")
                if len(c.wires) > 1 or c.lower_index != 0:
                    left = c.lower_index + len(c.wires) -1
                    right = c.lower_index
                    if not c.is_downto:
                        temp = left
                        left = right
                        right = temp
                    self.file.write("[" + str(left) + ":" + str(right) + "]")
                self._write_escapable_name(c.name)
                self.file.write(";")
        self.file.write("\n\n")

    def _write_cable(self, cable):
        self.file.write("wire ")
        if cable.lower_index != 0 or not cable.is_scalar:
            if cable.is_downto:
                left = cable.lower_index + len(cable.wires) - 1
                right = cable.lower_index
            else:
                left = cable.lower_index
                right = cable.lower_index + len(cable.wires) - 1
            self.file.write("["+str(left)+":"+str(right)+"]")
        #self.file.write(cable.name)
        self._write_escapable_name(cable.name)
        self.file.write(";\n")

    def _write_instanciation(self, instance):
        parameters = dict()
        for k, v in instance.data.items():
            if "VERILOG.star." == k[:13]:
                if v is not None:
                    self.file.write("(* " + k[13:] + " = " + v + " *)\n")
                else:
                    self.file.write("(* " + k[13:] + " *)\n")

            if "VERILOG.parameters." == k[:19]:
                parameters[k[19:]] = v
        #self.file.write(instance.reference.name)
        self._write_escapable_name(instance.reference.name)
        
        if len(parameters.items()) != 0:
            self.file.write(" #(\n")
            first = True
            for k,v in parameters.items():
                if first:
                    first = False
                else:
                    self.file.write(",\n")
                self.file.write("." + k + "(" + v + ")")
            self.file.write(")\n")
        self.file.write(" ")
        #self.file.write(instance.name)
        self._write_escapable_name(instance.name)
        self.file.write("\n(\n")
        first = True
        port_pin_dict = dict()
        for port in instance.reference.ports:
            port_pin_dict[port] = []
        for pin in instance.pins:
            port_pin_dict[pin.inner_pin.port].append(pin)
        for p in instance.reference.ports:
            cable_name = self._write_port_wires(port_pin_dict[p])
            if cable_name is not None:
                if first:
                    first = False
                #TODO: self.file.write(cableconnected to port name)
                else:
                    self.file.write(",\n")
                self.file.write("    .")
                self._write_escapable_name(p.name)
                self.file.write("(")
                #self._write_port_wires(port_pin_dict[p])
                #self.file.write(cable_name)
                self._write_escapable_name(cable_name)
                self.file.write(")")
        self.file.write("\n);\n")
        

    def _write_port_wires(self, pins):
        '''takes a set of pins and returns a string that represents the given bus
        this bus can be a single cable all in order or a set of cables and indices'''
        string_to_write = ""
        previous_cable = None
        counting_down = None
        single_slice = True
        low_index = None
        high_index = None
        last_wire = False
        wire_exists = False

        #function here to help with code reuse. this function is really not needed elsewhere.
        def terminate_slice():
            nonlocal string_to_write
            nonlocal single_slice
            nonlocal low_index
            nonlocal high_index
            nonlocal counting_down
            if string_to_write == "" or string_to_write[0] != "{":
                string_to_write = "{ " + string_to_write
            if not single_slice:
                string_to_write += ", " 
            string_to_write += self._get_indexed_name_from_cable(previous_cable, low_index, high_index, counting_down)
            single_slice = False
            low_index = None
            high_index = None
            counting_down = None

        for pin in pins:
            if pin.wire == None:
                last_wire = True
            else:
                wire_exists = True
                assert last_wire == False, "there is a gap in the port's pins to be wired up " + pin.inner_pin.port.name
                index = self._get_wire_index(pin.wire.cable, pin.wire)
                cable = pin.wire.cable
                
                if previous_cable != None and cable != previous_cable:
                    
                    terminate_slice()

                elif previous_cable != None and cable == previous_cable:
                    if counting_down is None:
                        assert low_index == high_index, "counting_down should always be set if more than one wire has been used"
                        assert low_index != None, "at least one wire should have been seen by now..."
                        if abs(low_index - index) != 1:
                            terminate_slice()
                        else:
                            counting_down = index < low_index
                    elif counting_down and index == low_index - 1:
                        pass #we are still part of the same slice
                    elif not counting_down and index == high_index + 1:
                        pass #we are part of the same slice
                    else:
                        terminate_slice()

                if low_index is None or index < low_index:
                    low_index = index
                if high_index is None or index > high_index:
                    high_index = index
                previous_cable = cable
            
        if not wire_exists:
            return None
        if single_slice:
            assert string_to_write == "", "the string to write should be empty"
            string_to_write = self._get_indexed_name_from_cable(cable, low_index, high_index, counting_down)
        else:
            string_to_write +=", " + self._get_indexed_name_from_cable(cable, low_index, high_index, counting_down)
            string_to_write += " }"

        return string_to_write


    def _get_wire_index(self, cable, wire):
        i = 0
        val = None
        for w in cable.wires:
            if wire == w:
                val = i
                break
            i += 1
        return val + cable.lower_index

    def _get_indexed_name_from_cable(self, cable, low_index, high_index, downto):
        if cable.is_downto == downto:
            if low_index == cable.lower_index:
                if high_index == cable.lower_index + len(cable.wires) - 1:
                    return cable.name
        if high_index == low_index:
            return cable.name + " [" + str(high_index) + "] "
        if downto:
            return cable.name + " [" + str(high_index) + ":" + str(low_index) + "] "
        else:
            return cable.name + " [" + str(low_index) + ":" + str(high_index) + "] "

        


    # def _indicies_from_wires(self, cable, wires, string_to_write):
    #     low = None
    #     high = None
    #     for w in wires:
    #         idx = self._get_wire_index(cable, w)
    #         if (low is None) or idx < low:
    #             low = idx
    #         if (high is None) or idx > high:
    #             high = idx
    #     #if low == cable.lower_index and high == cable.lower_index + len(cable.wires) - 1:
    #     if high - low == len(cable.wires) -1:
    #         pass
    #     elif low == high:
    #         string_to_write += " [" + str(low + cable.lower_index) + "]"
    #     else:
    #         string_to_write += " [" + str(low + cable.lower_index) + ":" + str(high + cable.lower_index) + "]"
    #     return string_to_write

        # pin_cable = pin.wire.cable
        # if len(pins) == len(pin_cable.wires):
        #     #self.file.write(pin_cable.name)
        #     string_to_write += pin_cable.name
        # elif len(pins) == 1:
        #     if len(pin_cable.wires) == 1:
        #         #self.file.write(pin_cable.name)
        #         string_to_write += pin_cable.name
        #     else:
        #         i = 0
        #         for w in pin_cable.wires:
        #             if w == pin.wire:
        #                 break
        #             i += 1
        #         #self.file.write(pin_cable.name)
        #         #self.file.write("[" + str(i) + "]")
        #         string_to_write += pin_cable.name
        #         string_to_write +="[" + str(i) + "]"
        # else:
        #     left_pin = pins[0]
        #     right_pin = pins[len(pins)-1]
        #     i = 0
        #     left_wire_index = None
        #     right_wire_index = None
        #     for w in pin_cable.wires:
        #         if w == left_pin.wire:
        #             left_wire_index = i
        #         if w == right_pin.wire:
        #             right_wire_index = i
        #         i += 1
        #         if left_wire_index == None and right_wire_index == None:
        #             break
        #     #self.file.write(pin_cable.name)
        #     #self.file.write("[" + str(left_wire_index) + ":" + str(right_wire_index) + "]")
        #     string_to_write += pin_cable.name
        #     string_to_write += "[" + str(left_wire_index) + ":" + str(right_wire_index) + "]"
        # return string_to_write

    def _write_escapable_name(self, str_in):
        if str_in[0] == "\\":
            self.file.write(str_in + " ")
        else:
            self.file.write(str_in)