from spydrnet.ir import *

class HierarchicalLookup:

    def __init__(self, ir=None):
        if ir is None:
            raise TypeError
        self.ir = ir
        self._cable_hashmap = dict()
        self._port_hashmap = dict()
        self._instance_hashmap = dict()
        self._build_hashmaps()

    def get_instance_from_name(self, hierarchical_name):
        return self._instance_hashmap[hierarchical_name]
        # Example "processor/core(0)/alu/adder/adder_reg[5]"
        # return <a list of cell instances that uniquely identify that specific instance>
        # Example [<top_cell_instance>, <processor_instance>, <instance_0_of_core>, <instance of alu>, <adder_instance>, <instance 5 of adder_reg>]
        pass

    def get_cable_from_name(self, hierarchical_name):
        return self._cable_hashmap[hierarchical_name]
        # example "processor/core(0)/alu/adder/adder_bus"
        # return <list of cell instances to parent cell with cable appended>
        pass

    def get_wire_from_name(self, hierarchical_name):
        # return <list of cell instances, append by cable, appended by pin>
        pass

    def get_port_from_name(self, hierarchical_name):
        return self._port_hashmap[hierarchical_name]
        # return <list of cell inst, append port>
        pass

    def get_pin_from_name(self, hierarchical_name):
        # return < list of cell inst, append parent port, append pin>
        pass

    def _build_hashmaps(self):
        hierarchical_name = ""
        trace = []
        top = self._find_top()
        hierarchical_name = top.__getitem__('EDIF.identifier')
        # trace.append(top)
        # for instance in top.instances:
        #     name = instance.__getitem__('EDIF.identifier')
        #     trace.append(instance)
        #     self._trace_definition(instance.definition, hierarchical_name + '/' + name, trace)
        #     trace.pop()
        self._trace_definition(top, hierarchical_name, list())
        print()


    def _trace_definition(self, definition, hierarchical_name, trace):
        for cable in definition.cables:
            name = cable.__getitem__('EDIF.identifier')
            trace.append(cable)
            self._cable_hashmap[hierarchical_name + '/' + name] = trace.copy()
            trace.pop()
        for port in definition.ports:
            name = port.__getitem__('EDIF.identifier')
            trace.append(port)
            self.port_hashmap[hierarchical_name + '/' + name] = trace.copy()
            trace.pop()
        for instance in definition.instances:
            name = instance.__getitem__('EDIF.identifier')
            trace.append(instance)
            self._instance_hashmap[hierarchical_name + '/' + name] = trace.copy()
            self._trace_definition(instance.definition, hierarchical_name + '/' + name, trace)
            trace.pop()
        print()

    def _find_top(self):
        top = None
        for library in self.ir.libraries:
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
    lookup = HierarchicalLookup(ir)