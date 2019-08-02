import json

from spydrnet.ir import *
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
import spydrnet.support_files as sf

class Utility:

    def __init__(self):
        pass

    def get_leaf_cells(self, ir):
        leaf_cells = list()
        top = self._find_top(ir)
        self._trace_definition(top, "", leaf_cells)
        return leaf_cells

    def get_cell_type(self, instance=None):
        if instance is None:
            raise TypeError("Expected one argument got zero")
        else:
            if type(instance) is Instance:
                return instance.definition
            else:
                raise TypeError("Expected a Instance, got a", type(instance))

    def _trace_definition(self, definition, name, leaf_cells):
        if name == "":
            name = definition.__getitem__("EDIF.identifier")
        for instance in definition.instances:
            for inner_pin, outer_pin in instance.outer_pins.items():
                if inner_pin.wire is None:
                    leaf = name + '/' + instance.__getitem__("EDIF.identifier")
                    leaf_cells.append(name + '/' + instance.__getitem__("EDIF.identifier"))
                break
            self._trace_definition(instance.definition, name + '/' + instance.__getitem__("EDIF.identifier"), leaf_cells)

    def _find_top(self, ir):
        top = None
        for library in ir.libraries:
            for definition in library.definitions:
                if top is None and not len(definition.instances) == 0:
                    top = definition
                    continue
                for instance in definition.instances:
                    parent_definition = instance.parent_definition
                    if instance.definition is top:
                        top = definition
        return top


sequential_elements = set()
combinational_elements = set()
other_elements = set()


def is_sequential(obj):
    global sequential_elements
    if len(sequential_elements) == 0:
        _read_file()
    if isinstance(obj, Instance):
        definition = obj.definition
        test = definition["EDIF.identifier"] in sequential_elements
        return definition["EDIF.identifier"] in sequential_elements
    elif isinstance(obj, Definition):
        definition = obj
        return definition["EDIF.identifier"] in sequential_elements
    else:
        raise TypeError("Needs to be an instance or definition got ", type(obj))


def is_combinational(obj):
    global combinational_elements
    if len(combinational_elements) == 0:
        _read_file()
    if isinstance(obj, Instance):
        definition = obj.definition
        test = definition["EDIF.identifier"] in combinational_elements
        return definition["EDIF.identifier"] in combinational_elements
    elif isinstance(obj, Definition):
        definition = obj
        return definition["EDIF.identifier"] in combinational_elements
    else:
        raise TypeError("Needs to be an instance or definition got ", type(obj))

def is_leaf(obj):
    global combinational_elements
    global sequential_elements
    if len(combinational_elements) == 0:
        _read_file()
    if isinstance(obj, Instance):
        defintion = obj.definition
        return defintion['EDIF.identifier'] in combinational_elements or defintion['EDIF.identifier'] in sequential_elements
    elif isinstance(obj, Definition):
        return obj['EDIF.identifier'] in combinational_elements or obj['EDIF.identifier'] in sequential_elements
    else:
        raise TypeError("Needs to be an instance or definition go ", type(obj))


def _read_file():
    global sequential_elements
    global combinational_elements
    global other_elements
    # TODO dynamically point to directory were architectures info is store
    # TODO enable user to supply extra architecture definitions
    f = open(sf.supportfile_dir + '/cell_type.json', 'r')
    data = json.loads(f.read())
    f.close()
    sequential_elements = set(data['sequential_elements'])
    combinational_elements = set(data['combinational_elements'])
    other_elements = set(data['other_elements'])
    if len(sequential_elements) == 0:
        sequential_elements.add("EMTPY")
    if len(combinational_elements) == 0:
        combinational_elements.add("EMPTY")
    if len(other_elements) == 0:
        other_elements.add("EMPTY")


def trace_pin(pin, instance_stack):
    # instances = list()
    instances = dict()
    for wire_pin in pin.wire.pins:
        if wire_pin is pin:
            continue
        if isinstance(wire_pin, OuterPin):
            if wire_pin.inner_pin.wire is None:
                instances[wire_pin] = wire_pin.instance
                continue
            instance_stack.append(wire_pin.instance)
            instances.update(trace_pin(wire_pin.inner_pin, instance_stack))
            instance_stack.pop()
        else:
            try:
                instance = instance_stack.pop()
            except IndexError:
                raise IndexError
            for inner_pin, outer_pin in instance.outer_pins.items():
                if inner_pin is wire_pin:
                    instances.update(trace_pin(outer_pin, instance_stack))
                    break
            instance_stack.append(instance)
    return instances


def get_hierarchical_name(obj):
    name = obj.__getitem__("EDIF.identifier")
    if type(obj) == Instance:
        parent_definition = obj.parent_definition
        ir = obj.parent_definition.library.environment
    else:
        parent_definition = obj.definition
        ir = obj.definition.library.environment
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
    name = parent_definition.__getitem__("EDIF.identifier") + '/' + name
    return name


def move_definition(definition, target_library=None):
    if target_library is None:
        definition_library = definition.library
        for i in range(len(definition_library.environment.libraries)):
            if definition_library == definition_library.environment.libraries[i]:
                break
        if i == len(definition_library.environment.libraries) - 1:
            print("ERROR")
        else:
            # definition.library = definition_library.environment.libraries[i + 1]
            definition.library = None
            definition['EDIF.identifier'] = definition['EDIF.identifier'] + '_BLACK_BOX'
            definition_library.definitions.remove(definition)
            definition_library.environment.libraries[i + 1].add_definition(definition, 0)

    else:
        print("This feature is not coded yet")



import os
import glob

from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
if __name__ == '__main__':
    parser = EdifParser.from_filename("TMR_hierarchy.edf")
    parser.parse()
    ir = parser.netlist
    util = Utility()
    test = util.get_leaf_cells(ir)
    instance = ir.libraries[1].definitions[1].instances[0]
    test1 = util.get_cell_type(instance)
    test2 = get_hierarchical_name(instance)
    move_definition(ir.libraries[0].definitions[0])
    composer = ComposeEdif()
    composer.run(ir)
    print()
