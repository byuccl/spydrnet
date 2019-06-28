from spydrnet.ir import *
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup

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

    def get_hierarchical_name(self, obj):
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


from spydrnet.parsers.edif.parser import EdifParser
if __name__ == '__main__':
    parser = EdifParser.from_filename("TMR_hierarchy.edf")
    parser.parse()
    ir = parser.netlist
    util = Utility()
    test = util.get_leaf_cells(ir)
    instance = ir.libraries[1].definitions[1].instances[0]
    test1 = util.get_cell_type(instance)
    test2 = util.get_hierarchical_name(instance)