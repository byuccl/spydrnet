from spydrnet.ir import *
from spydrnet.parsers.edif.parser import EdifParser


def find_object(ir, my_string, type):
    directory = my_string.split('/')
    start = None
    for library in ir.libraries:
        for definition in library.definitions:
            for instance in definition.instances:
                if instance.__getitem__('EDIF.identifier') == directory[0]:
                    start = definition
    for x in range(len(directory)):
        goal = directory[x]
        if x + 1 != len(directory):
            for instance in start.instances:
                if instance.__getitem__('EDIF.identifier') == directory[x]:
                    start = instance.definition
                    break
        elif start is None:
            return
        else:
            if type == 'cable':
                for cable in start.cables:
                    temp = cable.__getitem__('EDIF.identifier')
                    if cable.__getitem__('EDIF.identifier') == directory[x] or (
                            'EDIF.original_identifier' in cable._metadata and
                            cable.__getitem__('EDIF.original_identifier') == directory[x]):
                        return cable
            elif type == 'instance':
                for instance in start.instances:
                    temp = instance.__getitem__('EDIF.identifier')
                    if instance.__getitem__('EDIF.identifier') == directory[x]:
                        return instance
            elif type == 'port':
                for port in start.ports:
                    temp = port.__getitem__('EDIF.identifier')
                    if port.__getitem__('EDIF.identifier') == directory[x]:
                        return port
            pass


def build_name(ir, obj):
    name = obj.__getitem__("EDIF.identifier")
    if type(obj) == Instance:
        parent_definition = obj.parent_definition
    else:
        parent_definition = obj.definition
    while True:
        end = True
        for library in ir.libraries:
            for definition in library.definitions:
                if definition == parent_definition:
                    continue
                for instance in definition.instances:
                    if instance.definition == parent_definition:
                        end = False
                        name = instance.__getitem__("EDIF.identifier") + '/' + name
                        parent_definition = instance.parent_definition
        if end:
            break
    return name

if __name__ == "__main__":
    filename = "TMR_hierarchy.edf"
    out_filename = "ports_diff_modules_test.edf"
    parser = EdifParser.from_filename(filename)
    parser.parse()
    ir = parser.netlist
    answer = find_object(ir, 'delta/omaga/b')
    print()