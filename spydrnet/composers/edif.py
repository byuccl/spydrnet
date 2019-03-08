
import json
#from spydrnet import * why the error here.



class ComposeEdif:

    """class that creates an edif file from our IR"""

    def __init__(self):
        #self.filename = "../../_data_/json_edif/out.json"
        self._output_ = None
        self._data_ = None
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
        self._new_line_()

        for library in self._data_.libraries:
            self._output_library_(library)

        self._lisp_increment_()
        self._output_.write("design top")
        self._new_line_()
        self._lisp_increment_()
        self._output_.write("cellref base_mb_wrapper (libraryref work)")
        self._lisp_decrement_()
        self._new_line_()
        self._lisp_decrement_()
        self._new_line_()
        
        self._lisp_decrement_()
        #print for debug only
        print("Current LISP level: {}".format(self._lisp_depth_))
        
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
        if 'OldName' in obj.data:
            self._lisp_increment_()
            self._output_.write("rename ")
            self._output_.write(obj.name)
            self._output_.write(" \"" + obj.data['OldName'] + "\"")
            self._lisp_decrement_()
        else:
            self._output_.write(obj.name)

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
        self._output_.write(port.name)
        self._lisp_increment_()
        self._output_.write("direction ")
        self._output_.write(port.direction)
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()
        
    def _output_instance_(self, instance):
        self._lisp_increment_()
        self._output_.write("instance ")
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
        self._output_.write(self._get_edif_name_(definition.Library))
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._lisp_decrement_()
        self._new_line_()
        properties = instance.data["properties"]
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
        for port in cable.getConnectionList(): #TODO fuction cable.getConnectionList() needs to be created
            self._output_port_ref_(port)
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
        name = netlistObj.name
        oldName = netlistObj.data["oldName"]
        if oldName == None:
            return name
        else:
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
    

    