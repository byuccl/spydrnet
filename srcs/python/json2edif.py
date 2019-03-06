import json

filename = "../../data/json_edif/out.json"
output_filename = "../../data/json_edif/out.edf"

output = None

data = None
lisp_depth = 0


def run():
    global data

    read_data()

    open_output()
    output_environment()    
    close_output()

def read_data():
    global data
    with open(filename) as fi:
        data = json.load(fi)

def open_output():
    global output_filename
    global output

    output = open(output_filename, 'w')

def output_environment():
    global output
    global lisp_depth

    lisp_increment()
    output.write("edif top")
    new_line()
    
    lisp_increment()
    output.write("edifversion 2 0 0")
    lisp_decrement()
    new_line()
    
    lisp_increment()
    output.write("edifLevel 0")
    lisp_decrement()
    new_line()
    
    lisp_increment()
    output.write("keywordmap ")
    lisp_increment()
    output.write("keywordlevel 0")
    lisp_decrement()
    lisp_decrement()
    new_line()

    for library in data['libraries']:
        output_library(library)

    lisp_increment()
    output.write("design top")
    new_line()
    lisp_increment()
    output.write("cellref base_mb_wrapper (libraryref work)")
    lisp_decrement()
    new_line()
    lisp_decrement()
    new_line()
    
    lisp_decrement()
    print("Current LISP level: {}".format(lisp_depth))

def output_library(library):
    lisp_increment()
    output.write("Library ")
    output_name_of_object(library)
    new_line()

    lisp_increment()
    output.write("edifLevel 0")
    lisp_decrement()
    new_line()

    lisp_increment()
    output.write("technology ")
    lisp_increment()
    output.write("numberDefinition ")
    lisp_decrement()
    lisp_decrement()
    new_line()
    
    for definition in library['definitions']:
        output_definition(definition)
    
    lisp_decrement()
    new_line()

def output_name_of_object(object):
    if 'OldName' in object['metadata']:
        lisp_increment()
        output.write("rename ")
        output.write(object['name'])
        output.write(" \"" + object['metadata']['OldName'] + "\"")
        lisp_decrement()
    else:
        output.write(object['name'])

def output_definition(definition):
    lisp_increment()
    output.write("Cell ")
    output_name_of_object(definition)
    output.write(" ")
    lisp_increment()
    output.write("celltype GENERIC")
    lisp_decrement()
    new_line()
    
    lisp_increment()
    output.write("view netlist ")
    lisp_increment()
    output.write("viewtype NETLIST")
    lisp_decrement()
    new_line()

    lisp_increment()
    output.write("interface")
    new_line()
    for port in definition['portList']:
        output_port(port)
    lisp_decrement()
    new_line()

    lisp_increment()
    output.write("contents")
    new_line()

    for instance in definition['instanceList']:
        output_instance(instance)
    for cable in definition['busList']:
        output_cable(cable)

    lisp_decrement()
    new_line()
    lisp_decrement()
    new_line()
    lisp_decrement()
    new_line()

def output_port(port):
    global output
    lisp_increment()
    output.write("port ")
    output.write(port.getName()) #TODO fuction port.getName() needs to be created
    lisp_increment()
    output.write("direction ")
    output.write(port.getDirection()) #TODO function port.getDirection() needs to be created
    lisp_decrement()
    lisp_decrement()
    new_line()

def output_instance(instance):
    global output
    lisp_increment()
    output.write("instance ")
    output.write(get_edif_name(instance))
    output.write(" ")
    lisp_increment()
    output.write("viewref ")
    output.write("netlist ") #TODO this should be checked against some sort of metadata
    lisp_increment()
    output.write("cellref ")
    definition = instance.getDefinition() #TODO fuction instance.getDefinition() needs to be created
    output.write(get_edif_name(definition))
    lisp_increment()
    output.write("libraryref ")
    output.write(get_edif_name(definition.getLibrary()))  #TODO fuction definition.getLibrary() needs to be created
    lisp_decrement()
    lisp_decrement()
    lisp_decrement()
    new_line()
    properties = instance.getMetadata("properies")
    for key,value in properties:
        output_property(key, value)
    lisp_decrement()

def output_property(key, value):
    #warning!!! this only handles string properties for now
    lisp_increment()
    output.write("property ")
    output.write(key)
    output.write(" ")
    lisp_increment()
    output.write('string "')
    output.write(value)
    output.write('"')
    lisp_decrement()
    lisp_decrement()
    new_line()

def get_edif_name(netlistObj):
    global output
    name = netlistObj.getName() #TODO fuction netlistObj.getName() needs to be created
    oldName = netlistObj.getMetadata("oldName") #TODO function netlistObj.getMetadata(key) needs to be created
    if oldName == None:
        return name
    else:
        return "(rename " + name + ' "' + oldName + '")'


def output_cable(cable):
    lisp_increment()
    output.write("net ")
    output.write(get_edif_name(cable))
    output.write(" ")
    lisp_increment()
    output.write("joined")
    new_line()
    for port in cable.getConnectionList(): #TODO fuction cable.getConnectionList() needs to be created
        output_port_ref(port)
    new_line()
    lisp_decrement()
    new_line()
    lisp_decrement()

def output_port_ref(port_ref):
    lisp_increment()
    output.write("portref ")
    output.write(get_edif_name(port_ref))
    output.write(" ")
    lisp_increment()
    output.write("instanceref ")
    lisp_decrement()
    lisp_decrement()
    new_line()

def lisp_increment():
    global output
    global lisp_depth
    
    output.write("(")
    lisp_depth += 1

def new_line():
    output.write("\n")
    output.write("  "*lisp_depth)

def lisp_decrement():
    
    global output
    global lisp_depth

    output.write(")")
    lisp_depth -= 1

def close_output():
    global output

    output.close()




run()