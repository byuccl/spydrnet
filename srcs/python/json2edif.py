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
        pass
    lisp_decrement()
    new_line()

    for instance in definition['instanceList']:
        pass
    for cable in definition['busList']:
        pass

    lisp_decrement()
    new_line()
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