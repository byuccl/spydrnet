
import json
from spydrnet.ir import *
import inspect #used for debug.
from datetime import datetime



class ComposeEdif:

    """class that creates an edif file from our IR"""

    def __init__(self):
        #self.filename = "../../_data_/json_edif/out.json"
        self._output_ = None
        self._data_  = None
        self._lisp_depth_ = 0

    def run(self, ir=None, file_out="out.edf"):
        """
        compose an edif file from the IR in either file or object form and _output_ it to a file
        **currently only object form will work read the json into an object first**
        
        Keyword Arguments:
        ir -- the object(environment) or file(json) to be composed to edif (default None) 
                        **default should be changed to in.ir**
        file_out -- the path and name of the file to which the edif will be written (default "out.edf")
        """
        self.output_filename = file_out
        self._data_ = ir
        if(isinstance(ir, str)):
            self.filename = ir
            self._read_data_()  #only needed if we start to accept the json format files
            print("currently json files are unsupported! read into an object first.")
        else:
            self._data_ = ir
        self._open_output_()
        self._output_environment_()
        self._close_output_()
    

    def _read_data_(self):
        """read _data_ in from a json ir file and store it in _data_"""
        with open(self.filename) as fi:
            self._data_ = json.load(fi)

    def _open_output_(self):
        self._output_ = open(self.output_filename, 'w')
    
    def _output_environment_(self):
        self._lisp_increment_()
        self._output_.write("edif top")
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
        now = datetime.now()
        self._output_.write("""\n(status\n (written\n  (timeStamp {})\n  (program "Vivado" (version "2018.2"))\n  (comment "Built on '{}'")\n  (comment "Built by 'BYU's spydrnet tool'")\n )\n)""".format(now.strftime("%Y %m %d %H %M %S"), now.strftime("%a %b %d %H:%M:%S %Z %Y")))
        print("WARNING: edif.py Line: {} - hard coded vivado version".format(self._lineno_()-1))
        self._new_line_()
        for library in self._data_.libraries:
            self._output_library_(library)

        self._lisp_increment_()
        self._output_.write("design top")
        self._new_line_()
        self._lisp_increment_()
        self._output_.write("cellref base_mb_wrapper (libraryref work)") #TODO: don't Hard code!!
        print("WARNING: edif.py Line: {} - hard coded top instance".format(self._lineno_()-1))
        self._lisp_decrement_()
        self._new_line_()
        self._lisp_decrement_()
        self._new_line_()
        
        self._lisp_decrement_()
        #print for debug only
        print("Current LISP level: {}".format(self._lisp_depth_))
        
    def _lineno_(self):
        return inspect.currentframe().f_back.f_lineno
       
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
        if 'OldName' in obj._metadata:
            self._lisp_increment_()
            self._output_.write("rename ")
            self._output_.write(obj.name)
            self._output_.write(" \"" + obj.data['OldName'] + "\"")
            self._lisp_decrement_()
        else:
            #print(obj)
            #print(vars(obj))
            #self._output_.write(obj.name)
            self._output_.write(obj._metadata["EDIF.identifier"])

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

        self._lisp_increment_()
        self._output_.write("contents")
        self._new_line_()

        for instance in definition.instances:
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
        #self._output_.write(port.name)
        self._output_name_of_object_(port)
        self._lisp_increment_()
        self._output_.write("direction ")
        #self._output_.write(port.direction)
        self._output_.write(self._direction_to_string_(port.direction))#str(port.direction))
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
        #print(vars(instance))
        self._output_.write(self._get_edif_name_(instance))
        self._output_.write(" ")
        self._lisp_increment_()
        self._output_.write("viewref ")
        self._output_.write("netlist ") #TODO this should be checked against some sort of metadata
        self._lisp_increment_()
        self._output_.write("cellref ")
        definition = instance.definition
        self._output_.write(self._get_edif_name_(definition))
        self._lisp_increment_()
        self._output_.write("libraryref ")
        self._output_.write(self._get_edif_name_(definition.library))
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()
        #print(vars(instance))
        if "properties" in instance._metadata:
            properties = instance._metadata["properties"]
            for key,value in properties:
                self._output_property_(key, value)
        self._lisp_decrement_()

    def _output_cable_(self, cable):
        self._lisp_increment_()
        self._output_.write("net ")
        self._output_.write(self._get_edif_name_(cable))
        self._output_.write(" ")
        self._lisp_increment_()
        self._output_.write("joined")
        self._new_line_()
        #for port in cable.getConnectionList(): #TODO fuction cable.getConnectionList() needs to be created
        for wire in cable.wires:
            for pin in wire.pins:
                #port = pin.port
                #print(type(pin))
                if isinstance(pin, OuterPin):
                    pin = pin.inner_pin
                self._output_port_ref_(pin.port)
        self._new_line_()
        self._lisp_decrement_()
        self._new_line_()
        self._lisp_decrement_()

    def _output_port_ref_(self, port_ref):
        self._lisp_increment_()
        self._output_.write("portref ")
        self._output_.write(self._get_edif_name_(port_ref))
        self._output_.write(" ")
        self._lisp_increment_()
        self._output_.write("instanceref ")
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()

    def _get_edif_name_(self, netlistObj):
        name = netlistObj._metadata["EDIF.identifier"]
        #print(vars(netlistObj))
        if not("oldName" in netlistObj._metadata):
            return name
        else:
            oldName = netlistObj._metadata["oldName"]
            return "(rename " + name + ' "' + oldName + '")'

    def _lisp_increment_(self):
        self._output_.write("(")
        self._lisp_depth_ += 1

    def _new_line_(self):
        self._output_.write("\n")
        self._output_.write("  "*self._lisp_depth_)

    def _lisp_decrement_(self):
        self._output_.write(")")
        self._lisp_depth_ -= 1

    def _output_property_(self, key, value):
        #TODO this only handles string properties for now
        self._lisp_increment_()
        self._output_.write("property ")
        self._output_.write(key)
        self._output_.write(" ")
        self._lisp_increment_()
        self._output_.write('string "')
        self._output_.write(value)
        self._output_.write('"')
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()

    def _close_output_(self):
        self._output_.close()
    

    