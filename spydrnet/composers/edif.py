
import json

"""class that creates an edif file from our IR"""

class ComposeEdif:

    def __init__(self):
        #self.filename = "../../data/json_edif/out.json"
        self.output_filename = "out.edf"
        self.output = None
        self.data = None
        self.lisp_depth = 0

    def run(self, ir=None, file_out="out.edf"):
        """
        compose an edif file from the IR in either file or object form and output it to a file
        **currently only object form will work**
        
        Keyword Arguments:
        ir          -- the object(environment) or file(json) to be composed to edif
        file_out    -- the path and name of the file to which the edif will be written (default "out.edf")
        """
        self.output_filename = file_out
        self.data = ir
        if(isinstance(ir, str)):
            self.filename = ir
            self._read_data_()  #only needed if we start to accept the json format files
            print("currently json files are unsupported! read into an object first.")
        else:
            self.data = ir
        self._open_output_()
        self._output_environment_()
        self._close_output_()
    

    def _read_data_(self):
        """read data in from a json ir file and store it in data"""
        with open(self.filename) as fi:
            self.data = json.load(fi)

    def _open_output_(self):
        self.output = open(self.output_filename, 'w')
    
    def _output_environment_(self):
        global output
        global lisp_depth

        self.lisp_increment()
        self.output.write("edif top")
        self.new_line()
        
        self.lisp_increment()
        self.output.write("edifversion 2 0 0")
        self.lisp_decrement()
        self.new_line()
        
        self.lisp_increment()
        self.output.write("edifLevel 0")
        self.lisp_decrement()
        self.new_line()
        
        self.lisp_increment()
        self.output.write("keywordmap ")
        self.lisp_increment()
        self.output.write("keywordlevel 0")
        self.lisp_decrement()
        self.lisp_decrement()
        self.new_line()

        for library in self.data['libraries']:
            self.output_library(library)

        self.lisp_increment()
        self.output.write("design top")
        self.new_line()
        self.lisp_increment()
        self.output.write("cellref base_mb_wrapper (libraryref work)")
        self.lisp_decrement()
        self.new_line()
        self.lisp_decrement()
        self.new_line()
        
        self.lisp_decrement()
        print("Current LISP level: {}".format(self.lisp_depth))
        
    def output_library(self, library):
        self.lisp_increment()
        self.output.write("Library ")
        self.output_name_of_object(library)
        self.new_line()

        self.lisp_increment()
        self.output.write("edifLevel 0")
        self.lisp_decrement()
        self.new_line()

        self.lisp_increment()
        self.output.write("technology ")
        self.lisp_increment()
        self.output.write("numberDefinition ")
        self.lisp_decrement()
        self.lisp_decrement()
        self.new_line()
        
        for definition in library['definitions']:
            self.output_definition(definition)
        
        self.lisp_decrement()
        self.new_line()

    def output_name_of_object(self, object):
        if 'OldName' in object['metadata']:
            self.lisp_increment()
            self.output.write("rename ")
            self.output.write(object['name'])
            self.output.write(" \"" + object['metadata']['OldName'] + "\"")
            self.lisp_decrement()
        else:
            self.output.write(object['name'])

    
    def output_definition(self, definition):
        self.lisp_increment()
        self.output.write("Cell ")
        self.output_name_of_object(definition)
        self.output.write(" ")
        self.lisp_increment()
        self.output.write("celltype GENERIC")
        self.lisp_decrement()
        self.new_line()
        
        self.lisp_increment()
        self.output.write("view netlist ")
        self.lisp_increment()
        self.output.write("viewtype NETLIST")
        self.lisp_decrement()
        self.new_line()

        self.lisp_increment()
        self.output.write("interface")
        self.new_line()
        for port in definition['portList']:
            self.output_port(port)
        self.lisp_decrement()
        self.new_line()

        self.lisp_increment()
        self.output.write("contents")
        self.new_line()

        for instance in definition['instanceList']:
            self.output_instance(instance)
        for cable in definition['busList']:
            self.output_cable(cable)

        self.lisp_decrement()
        self.new_line()
        self.lisp_decrement()
        self.new_line()
        self.lisp_decrement()
        self.new_line()

    def output_port(self, port):
        self.lisp_increment()
        self.output.write("port ")
        self.output.write(port.getName()) #TODO fuction port.getName() needs to be created
        self.lisp_increment()
        self.output.write("direction ")
        self.output.write(port.getDirection()) #TODO function port.getDirection() needs to be created
        self.lisp_decrement()
        self.lisp_decrement()
        self.new_line()
        
    def output_instance(self, instance):
        self.lisp_increment()
        self.output.write("instance ")
        self.output.write(get_edif_name(instance))
        self.output.write(" ")
        self.lisp_increment()
        self.output.write("viewref ")
        self.output.write("netlist ") #TODO this should be checked against some sort of metadata
        self.lisp_increment()
        self.output.write("cellref ")
        self.definition = instance.getDefinition() #TODO fuction instance.getDefinition() needs to be created
        self.output.write(get_edif_name(definition))
        self.lisp_increment()
        self.output.write("libraryref ")
        self.output.write(get_edif_name(definition.getLibrary()))  #TODO fuction definition.getLibrary() needs to be created
        self.lisp_decrement()
        self.lisp_decrement()
        self.lisp_decrement()
        self.new_line()
        properties = instance.getMetadata("properies")
        for key,value in properties:
            self.output_property(key, value)
        self.lisp_decrement()

    def get_edif_name(self, netlistObj):
        name = netlistObj.getName() #TODO fuction netlistObj.getName() needs to be created
        oldName = netlistObj.getMetadata("oldName") #TODO function netlistObj.getMetadata(key) needs to be created
        if oldName == None:
            return name
        else:
            return "(rename " + name + ' "' + oldName + '")'

    def output_cable(self, cable):
        self.lisp_increment()
        self.output.write("net ")
        self.output.write(self.get_edif_name(cable))
        self.output.write(" ")
        self.lisp_increment()
        self.output.write("joined")
        self.new_line()
        for port in cable.getConnectionList(): #TODO fuction cable.getConnectionList() needs to be created
            self.output_port_ref(port)
        self.new_line()
        self.lisp_decrement()
        self.new_line()
        self.lisp_decrement()

    def output_port_ref(self, port_ref):
        self.lisp_increment()
        self.output.write("portref ")
        self.output.write(self.get_edif_name(port_ref))
        self.output.write(" ")
        self.lisp_increment()
        self.output.write("instanceref ")
        self.lisp_decrement()
        self.lisp_decrement()
        self.new_line()

    def lisp_increment(self):
        self.output.write("(")
        self.lisp_depth += 1

    def new_line(self):
        self.output.write("\n")
        self.output.write("  "*self.lisp_depth)

    def lisp_decrement(self):
        self.output.write(")")
        self.lisp_depth -= 1

    def output_property(self, key, value):
        #TODO this only handles string properties for now
        self.lisp_increment()
        self.output.write("property ")
        self.output.write(key)
        self.output.write(" ")
        self.lisp_increment()
        self.output.write('string "')
        self.output.write(value)
        self.output.write('"')
        self.lisp_decrement()
        self.lisp_decrement()
        self.new_line()

    def _close_output_(self):
        self.output.close()
    

    