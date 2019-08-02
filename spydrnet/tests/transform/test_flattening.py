import unittest
import copy

import spydrnet.transform.Flattener as flatten
import spydrnet.support_files as files
from spydrnet.ir import *
from spydrnet.parsers.edif.parser import EdifParser
import spydrnet.utility.utility as util
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.utility.Uniqueifier import Uniquifier


class test_flattener(unittest.TestCase):
    flat_lookup = None
    original_lookup = None
    flat_instances = set()
    original_instances = set()
    visited = set()

    def test_all(self):
        for temp, file in files.edif_files.items():
            #if temp != 'unique_challenge.edf' and temp != 'register_file.edf':
            if temp != 'riscv_multi_core.edf':
                # continue
                pass
            self.file = temp
            print("testing", temp)
            self._flatten_design(file)
            print("passed", temp)

    def _flatten_design(self, file_name):
        # parser = EdifParser.from_filename(files.edif_files['register_file.edf'])
        # parser = EdifParser.from_filename(files.edif_files['unique_challenge.edf'])
        parser = EdifParser.from_filename(file_name)
        print('\tParsing')
        parser.parse()
        ir = parser.netlist
        flatten.DEBUG = True
        print('\tFlattening')
        uniquifier = Uniquifier()
        uniquifier.run(ir)
        self.original_lookup = HierarchicalLookup(ir)
        flatten.flatten_design(ir)
        print('\tTesting output')
        self.flat_lookup = HierarchicalLookup(ir)
        self._check_ports(ir.top_instance.definition, ir.top_instance.old_definition)
        for x in range(len(ir.top_instance.definition.ports)):
            flat_port = ir.top_instance.definition.ports[x]
            if flat_port.direction == Port.Direction.OUT:
                continue
            original_port = ir.top_instance.old_definition.lookup_element(Port, 'EDIF.identifier',
                                                                          flat_port['EDIF.identifier'])
            for y in range(len(flat_port.inner_pins)):
                self._check_driven(flat_port.inner_pins[y], original_port.inner_pins[y])
        # print('visited', len(self.flat_instances), 'cells')

    def _check_ports(self, flat_definition, original_definition):
        for port in flat_definition.ports:
            original_port = original_definition.lookup_element(Port, 'EDIF.identifier', port['EDIF.identifier'])
            self.assertTrue(original_port.direction == port.direction, "Failed " + self.file)
            self.assertTrue(len(original_port.inner_pins) == len(original_port.inner_pins), "Failed " + self.file)

    def _check_driven(self, flatten_pin, original_pin):
        # sections = flatten_pin.wire.cable['EDIF.identifier'].split('__')
        # self.assertTrue(sections[0] + '_' == original_pin.wire.cable['EDIF.identifier'])
        flat_trace = list(util.trace_pin(flatten_pin, []).values())
        original_trace = list(util.trace_pin(original_pin, []).values())
        for x in range(len(flat_trace)):
            self.assertTrue(flat_trace[x].old_instance in original_trace, "Failed " + self.file)
            output_ports = self._get_output_ports(flat_trace[x])
            for flat_port in output_ports:
                self.flat_instances.add(flat_trace[x])
                original_port = flat_trace[x].old_instance.definition.lookup_element(Port, 'EDIF.identifier',
                                                                                     flat_port['EDIF.identifier'])
                for y in range(len(flat_port.inner_pins)):
                    flat_test = flat_trace[x].outer_pins[flat_port.inner_pins[y]]
                    original_test = flat_trace[x].old_instance.outer_pins[original_port.inner_pins[y]]
                    self._test(flat_test, original_test)
        pass

    i = 0
    def _test(self, flatten_pin, original_pin):
        if flatten_pin in self.visited:
            return
        self.visited.add(flatten_pin)
        sections = flatten_pin.wire.cable['EDIF.identifier'].split('__')
        if len(sections) == 1:
            sections = flatten_pin.wire.cable['EDIF.identifier'].split('_')
            # self.assertTrue(sections[0] == original_pin.wire.cable['EDIF.identifier'])
        else:
            pass
            # self.assertTrue(sections[0] + '_' == original_pin.wire.cable['EDIF.identifier'])
        try:
            flat_trace = list(util.trace_pin(flatten_pin, []).values())
        except IndexError:
            return
        name = util.get_hierarchical_name(original_pin.instance)
        temp = self.original_lookup.get_instance_from_name(util.get_hierarchical_name(original_pin.instance))
        temp.pop()
        self.i += 1
        original_trace = list(util.trace_pin(original_pin, temp).values())
        if len(original_trace) != len(flat_trace):
            self._print_name(original_trace, flat_trace)
            print(flatten_pin.instance['EDIF.identifier'], 'failed to connect to everything')
        self.assertTrue(len(original_trace) == len(flat_trace), "Failed " + self.file + "\n" + str(len(original_trace)) + '!=' + str(len(flat_trace)))
        for x in range(len(flat_trace)):
            self.flat_instances.add(flat_trace[x])
            self.assertTrue(flat_trace[x].old_instance in original_trace, "Failed " + self.file)
            output_ports = self._get_output_ports(flat_trace[x])
            for flat_port in output_ports:
                original_port = flat_trace[x].old_instance.definition.lookup_element(Port, 'EDIF.identifier',
                                                                                     flat_port['EDIF.identifier'])
                for y in range(len(flat_port.inner_pins)):
                    if flat_port.inner_pins[y] not in flat_trace[x].outer_pins:
                        continue
                    flat_test = flat_trace[x].outer_pins[flat_port.inner_pins[y]]
                    original_test = flat_trace[x].old_instance.outer_pins[original_port.inner_pins[y]]
                    self._test(flat_test, original_test)

    def _get_output_ports(self, instance):
        output = list()
        for inner_pin in instance.outer_pins.keys():
            if inner_pin.port.direction == Port.Direction.OUT:
                output.append(inner_pin.port)
        return output

    def _print_name(self, orignial_trace, flat_trace):
        f = open("original.txt", 'w+')
        for instance in orignial_trace:
            f.write(util.get_hierarchical_name(instance) + '\n')
        f.close()
        f = open("flat.txt", 'w+')
        for instance in flat_trace:
            f.write(instance['EDIF.original_identifier'] + '\n')
        f.close()

if __name__ == '__main__':
    unittest.main()