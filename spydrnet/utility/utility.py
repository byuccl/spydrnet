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
        print()

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
    # test = util.get_leaf_cells(ir)
    instance = ir.libraries[1].definitions[1].instances[0]
    test = util.get_cell_type(instance)
    print()
