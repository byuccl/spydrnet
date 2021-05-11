import json
from spydrnet.ir import *
import inspect  # used for debug.
from datetime import datetime
from spydrnet.composers.edif.edifify_names import EdififyNames


class ComposeEdif:
    """class that creates an edif file from our IR"""

    def __init__(self):
        # self.filename = "../../_data_/json_edif/out.json"
        self._output_ = None
        self._data_ = None
        self._lisp_depth_ = 0
        self.test = 0

    def run(self, ir=None, file_out="out.edf"):
        """
        compose an edif file from the IR input a netlist object form and _output_ it to a file

        Keyword Arguments:
        ir -- the object(environment) to be composed to edif (default None)

        file_out -- the path and name of the file to which the edif will be written (default "out.edf")
        """
        self.output_filename = file_out
        self._edifify_netlist(ir)
        self._data_ = ir
        if (isinstance(ir, str)):
            self.filename = ir
            self._read_data_()  # only needed if we start to accept the json format files
            print(
                "currently input files directly to the composer are unsupported! read in with the parser first.")
        else:
            self._data_ = ir
        self._open_output_()
        self._output_environment_()
        self._close_output_()

    def _edifify_netlist(self, netlist):

        # functions defined to be used as dependency getters in topological sort
        # declared here to be used more as functional oriented code.
        def _get_definition_dependency_same_library(definition):
            library = definition.library
            dependency_set = set()
            for inst in definition.children:
                if inst.reference.library == library:
                    dependency_set.add(inst.reference)
            return dependency_set

        def _get_library_dependency(library):
            depend_set = set()
            for definition in library.definitions:
                for child in definition.children:
                    if child.reference is None:
                        raise Exception("definition: ", child,
                                        ".reference is undefined")
                    if child.reference.library != library:
                        depend_set.add(child.reference.library)
            return depend_set

        # try:
        netlist.libraries = self._topological_sort(
            netlist.libraries, _get_library_dependency)
        for library in netlist.libraries:
            library.definitions = self._topological_sort(
                library.definitions, _get_definition_dependency_same_library)
        # except:
        #     #import pdb; pdb.set_trace()

        names = EdififyNames()
        if netlist.top_instance is None:
            raise Exception("netlist.top_instance undefined")
        if netlist.name is None:
            netlist.name = netlist.top_instance.name
        self._add_rename_property(netlist, [], names)
        self._add_rename_property(netlist.top_instance, [], names)
        for lib in netlist.libraries:
            self._add_rename_property(lib, netlist.libraries, names)
            for definition in lib.definitions:
                self._add_rename_property(definition, lib.definitions, names)
                for cable in definition.cables:
                    self._add_rename_property(cable, definition.cables, names)
                for instance in definition.children:
                    self._add_rename_property(
                        instance, definition.children, names)
                for port in definition.ports:
                    self._add_rename_property(port, definition.ports, names)

    def _topological_sort(self, list_of_objects, dependecy_function):

        visited = set()
        output_list = []
        get_dependents = dependecy_function

        def iterate(o):
            nonlocal visited
            nonlocal output_list
            nonlocal get_dependents
            stack = [o]
            while(len(stack) > 0):
                o = stack[-1]
                for child in get_dependents(o):
                    if child not in visited:
                        stack.append(child)
                if stack[-1] == o:
                    stack.pop()
                    if o not in visited:
                        visited.add(o)
                        output_list.append(o)

        # def recur(o):
        #     nonlocal visited
        #     nonlocal output_list
        #     nonlocal get_dependents
        #     visited.add(o)
        #     for dependent in get_dependents(o):
        #         if dependent not in visited:
        #             recur(dependent)
        #     output_list.append(o)

        for o in list_of_objects:
            if o not in visited:
                iterate(o)

        return output_list

    def _add_rename_property(self, obj, namespace_list, rename_helper):
        if obj.name is None:
            raise Exception('obj, ', obj, '.name undifined')
        name = obj.name
        if "EDIF.identifier" in obj.data:
            return
        rename = rename_helper.make_valid(obj, namespace_list)
        obj["EDIF.identifier"] = rename
        if rename != name:
            obj["EDIF.rename"] = True

    def _read_data_(self):
        """read _data_ in from a json ir file and store it in _data_"""
        with open(self.filename) as fi:
            self._data_ = json.load(fi)

    def _open_output_(self):
        self._output_ = open(self.output_filename, 'w', buffering=1)

    def _output_environment_(self):
        self._lisp_increment_()
        self._output_.write("edif ")
        self._output_name_of_object_(self._data_)
        self._new_line_()

        self._lisp_increment_()
        self._output_.write("edifversion 2 0 0")
        self._lisp_decrement_()
        self._new_line_()

        self._lisp_increment_()
        self._output_.write("edifLevel 0")
        self._lisp_decrement_()
        self._new_line_()

        self._lisp_increment_()
        self._output_.write("keywordmap ")
        self._lisp_increment_()
        self._output_.write("keywordlevel 0")
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._output_status_()
        self._new_line_()
        for library in self._data_.libraries:
            #if library.name != "SDN.verilog_primitives":
            self._output_library_(library)

        self._lisp_increment_()
        self._output_.write("design ")
        self._output_name_of_object_(self._data_.top_instance)
        self._new_line_()
        self._lisp_increment_()
        self._output_.write("cellref ")
        test = self._data_.top_instance
        if self._data_.top_instance.reference is None:
            raise Exception("netlist.reference undefined")
        self._output_.write(
            self._data_.top_instance.reference['EDIF.identifier'])
        self._lisp_increment_()
        self._output_.write("libraryref ")
        self._output_.write(
            self._data_.top_instance.reference.library['EDIF.identifier'])
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()
        self._lisp_decrement_()
        self._new_line_()

        self._lisp_decrement_()

        assert self._lisp_depth_ == 0, "There was an error with parenthesis matching off by " + \
            str(self._lisp_depth_)

    def _output_status_(self):
        self._new_line_()
        self._lisp_increment_()
        self._output_.write("status")
        self._new_line_()
        self._lisp_increment_()
        self._output_.write("written")
        self._new_line_()
        self._lisp_increment_()
        self._output_.write("timeStamp ")
        now = datetime.now()
        self._output_.write("{}".format(now.strftime("%Y %m %d %H %M %S")))
        self._lisp_decrement_()
        self._new_line_()
        if 'EDIF.status.written.program' in self._data_:
            self._lisp_increment_()
            self._output_.write("program ")
            self._output_.write('"{}" '.format(
                self._data_['EDIF.status.written.program']))
            if 'EDIF.status.written.program.version' in self._data_:
                self._lisp_increment_()
                self._output_.write("version ")
                self._output_.write('"{}"'.format(
                    self._data_['EDIF.status.written.program.version']))
                self._lisp_decrement_()
            self._lisp_decrement_()
        self._new_line_()
        self._lisp_increment_()
        self._output_.write('comment "Built by \'BYU spydrnet tool\'"')
        self._lisp_decrement_()
        self._new_line_()
        self._lisp_decrement_()
        self._new_line_()
        self._lisp_decrement_()

    def _output_library_(self, library):
        self._lisp_increment_()
        self._output_.write("Library ")
        self._output_name_of_object_(library)
        self._new_line_()

        self._lisp_increment_()
        self._output_.write("edifLevel 0")
        self._lisp_decrement_()
        self._new_line_()

        self._lisp_increment_()
        self._output_.write("technology ")
        self._lisp_increment_()
        self._output_.write("numberDefinition ")
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()

        for definition in library.definitions:
            self._output_definition_(definition)

        self._lisp_decrement_()
        self._new_line_()

    def _output_name_of_object_(self, obj):
        # if '.NAME' not in obj or (obj['.NAME'] == obj['EDIF.identifier'] and obj.get('EDIF.rename', False) is False):
        #     self._output_.write(obj['EDIF.identifier'])
        # else:
        #     identifier = obj['EDIF.identifier']
        #     rename_name = obj.get('.NAME', identifier)
        #     self._lisp_increment_()
        #     self._output_.write("rename ")
        #     self._output_.write(identifier)
        #     self._output_.write(' "' + rename_name + '"')
        #     self._lisp_decrement_()
        rename, name = self._get_name_string_(obj)
        if rename:
            self._lisp_increment_()
            self._output_.write(name)
            self._lisp_decrement_()
        else:
            self._output_.write(name)

    def _get_name_string_(self, obj):
        if '.NAME' not in obj or (obj['.NAME'] == obj['EDIF.identifier'] and obj.get('EDIF.rename', False) is False):
            rename = False
            name = obj['EDIF.identifier']
        else:
            rename = True
            identifier = obj['EDIF.identifier']
            rename_name = obj.get('.NAME', identifier)
            name = "rename " + identifier + ' "' + rename_name + '"'
        return rename, name

    def _output_definition_(self, definition):
        self._lisp_increment_()
        self._output_.write("Cell ")
        self._output_name_of_object_(definition)
        self._output_.write(" ")
        self._lisp_increment_()
        self._output_.write("celltype GENERIC")
        self._lisp_decrement_()
        self._new_line_()

        self._lisp_increment_()
        self._output_.write("view netlist ")
        self._lisp_increment_()
        self._output_.write("viewtype NETLIST")
        self._lisp_decrement_()
        self._new_line_()

        self._lisp_increment_()
        self._output_.write("interface")
        self._new_line_()
        for port in definition.ports:
            self._output_port_(port)
        self._lisp_decrement_()
        self._new_line_()

        if len(definition.children) + len(definition.cables) > 0:
            self._lisp_increment_()
            self._output_.write("contents")
            self._new_line_()

            for instance in definition.children:
                self._output_instance_(instance)
            for cable in definition.cables:
                self._output_cable_(cable)

            self._lisp_decrement_()
            self._new_line_()
        self._lisp_decrement_()
        self._new_line_()
        self._lisp_decrement_()
        self._new_line_()

    def _output_port_(self, port):
        self._lisp_increment_()
        self._output_.write("port ")
        if len(port.pins) > 1:
            # TODO Clean up code in this if statement
            self._lisp_increment_()
            self._output_.write("array ")
            self._output_name_of_object_(port)
            self._output_.write(" ")
            self._output_.write(str(len(port.pins)))
            self._lisp_decrement_()
            self._output_.write(" ")
            self._lisp_increment_()
            self._output_.write("direction ")
            self._output_.write(self._direction_to_string_(
                port.direction))  # str(port.direction))
            self._lisp_decrement_()
            self._lisp_decrement_()
            self._new_line_()
            return
        self._output_name_of_object_(port)
        self._lisp_increment_()
        self._output_.write("direction ")
        self._output_.write(self._direction_to_string_(
            port.direction))  # str(port.direction))
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()

    def _direction_to_string_(self, direction):
        if direction == Port.Direction.INOUT:
            return "INOUT"
        elif direction == Port.Direction.IN:
            return "INPUT"
        elif direction == Port.Direction.OUT:
            return "OUTPUT"
        else:
            return "UNDEFINED"

    def _output_instance_(self, instance):
        self._lisp_increment_()
        self._output_.write("instance ")
        # print(vars(instance))
        # self._output_.write(self._get_edif_name_(instance))
        self._output_name_of_object_(instance)
        self._output_.write(" ")
        self._lisp_increment_()
        self._output_.write("viewref ")
        # TODO this should be checked against some sort of metadata
        self._output_.write("netlist ")
        self._lisp_increment_()
        self._output_.write("cellref ")
        definition = instance.reference
        self._output_.write(self._get_edif_name_(definition))
        self._lisp_increment_()
        self._output_.write("libraryref ")
        self._output_.write(self._get_edif_name_(definition.library))
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()
        # print(vars(instance))
        if "EDIF.properties" in instance:
            properties = instance["EDIF.properties"]
            for prop in properties:
                self._output_property_(prop)
        self._lisp_decrement_()

    def _output_cable_(self, cable):
        for wire in cable.wires:
            self._lisp_increment_()
            self._output_.write("net ")
            self._output_name_of_cable_wire_(cable, wire)
            self._output_.write(" ")
            self._lisp_increment_()
            self._output_.write("joined")
            self._new_line_()
            # for port in cable.getConnectionList(): #TODO fuction cable.getConnectionList() needs to be created
            for pin in wire.pins:
                # port = pin.port
                # print(type(pin))
                if isinstance(pin, OuterPin):
                    self._output_inner_pin_(pin)
                    pin = pin.inner_pin
                else:
                    self._output_port_ref_(
                        pin.port, self._get_edif_name_(cable), pin)
            self._new_line_()
            self._lisp_decrement_()
            self._new_line_()
            self._lisp_decrement_()

    def _output_name_of_cable_wire_(self, cable, wire):
        if len(cable.wires) == 1 and not cable.is_array:
            self._output_name_of_object_(cable)
        else:
            # cable_name = self._get_name_string_(cable)
            cable_index = self._get_wire_index_(cable, wire)
            identifier = cable['EDIF.identifier'] + \
                "_" + str(cable_index) + "_"
            rename_name = cable.get('.NAME', identifier) + \
                "[" + str(cable_index) + "]"
            name = "rename " + identifier + ' "' + rename_name + '"'
            self._lisp_increment_()
            self._output_.write(name)
            self._lisp_decrement_()

    def _get_wire_index_(self, cable, wire):
        i = 0
        val = None
        for w in cable.wires:
            if wire == w:
                val = i
                break
            i += 1
        return val + cable.lower_index

    def _output_inner_pin_(self, pin):
        inner_pin = pin.inner_pin
        self._lisp_increment_()
        self._output_.write("portref ")
        if pin.inner_pin.port.is_array:
            self._lisp_increment_()
            self._output_.write("member ")
            self._output_.write(self._get_edif_name_(inner_pin.port))
            for x in range(len(inner_pin.port.pins)):
                if inner_pin == inner_pin.port.pins[x]:
                    self._output_.write(" " + str(x))
                    self._lisp_decrement_()
        else:
            self._output_.write(self._get_edif_name_(inner_pin.port))
        self._output_.write(" ")
        self._lisp_increment_()
        self._output_.write("instanceref ")
        self._output_.write(pin.instance["EDIF.identifier"])
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()
        pass

    def _output_port_ref_(self, port_ref, cable_name, pin):
        self._lisp_increment_()
        self._output_.write("portref ")
        if port_ref.is_array:
            for x in range(len(port_ref.pins)):
                # print(self.test)
                if port_ref.pins[x].wire is None:
                    # self.test += 1
                    # self._lisp_decrement_()
                    # print("test")
                    continue
                # if cable_name == port_ref.inner_pins[x].wire.cable["EDIF.identifier"]:
                if port_ref.pins[x] == pin:
                    break
            self._lisp_increment_()
            self._output_.write("member ")
            self._output_.write(self._get_edif_name_(port_ref))
            self._output_.write(" ")
            self._output_.write(str(x))
            self._lisp_decrement_()
        else:
            self._output_.write(self._get_edif_name_(port_ref))
        self._lisp_decrement_()
        self._new_line_()

    def _get_edif_name_(self, netlistObj):
        name = netlistObj["EDIF.identifier"]
        if not ("oldName" in netlistObj):
            return name
        else:
            oldName = netlistObj["oldName"]
            return "(rename " + name + ' "' + oldName + '")'

    def _lisp_increment_(self):
        self._output_.write("(")
        self._lisp_depth_ += 1

    def _new_line_(self):
        self._output_.write("\n")
        self._output_.write("  " * self._lisp_depth_)

    def _lisp_decrement_(self):
        self._output_.write(")")
        self._lisp_depth_ -= 1

    def _output_property_(self, prop):
        # TODO this only handles string properties for now
        self._lisp_increment_()
        self._output_.write("property ")
        if 'original_identifier' in prop:
            self._lisp_increment_()
            self._output_.write("rename ")
            self._output_.write(prop['identifier'])
            self._output_.write(' "')
            self._output_.write(prop['original_identifier'])
            self._output_.write('"')
            self._lisp_decrement_()
        else:
            self._output_.write(prop['identifier'])
        value = prop['value']
        self._output_.write(" ")
        self._lisp_increment_()
        if isinstance(value, str):
            self._output_.write('string "')
            self._output_.write(value)
            self._output_.write('"')
        elif isinstance(value, bool):
            self._output_.write('boolean ')
            self._lisp_increment_()
            self._output_.write(str(value))
            self._lisp_decrement_()
        else:
            self._output_.write('integer ')
            self._output_.write(str(value))
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()

    def _close_output_(self):
        self._output_.close()
