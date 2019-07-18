import json
import collections

import spydrnet.utility.utility as utility
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.ir import *
import spydrnet.support_files as files


def determine_cells_to_replicate(ir, config):
    replicate_top_ports = config['replicate_top_ports']
    replicate_black_list = config['replicate_black_list']

    top_instance = ir.top_instance
    instances = _get_leaf_instances(top_instance.definition)
    instances = _sanitize_target(top_instance.definition, instances, replicate_top_ports, replicate_black_list)
    return list(instances)

def _get_leaf_instances(top_definition):
    stack = list()
    visited = set()
    instances = list()

    stack.append(top_definition)
    visited.add(top_definition)

    while len(stack) != 0:
        definition = stack.pop()
        for instance in definition.instances:
            if list(instance.outer_pins.keys())[0].wire is None:
                # instances.add(instance)
                instances.append(instance)
                continue
            if instance.definition not in visited:
                visited.add(instance.definition)
                stack.append(instance.definition)
    return instances

def _sanitize_target(top_definition, instances, top_ports, black_list):
    iobuf = set()
    if not top_ports:
        for port in top_definition.ports:
            for inner_pin in port.inner_pins:
                for pin in inner_pin.wire.pins:
                    if pin is not inner_pin:
                        iobuf.add(pin.instance)
                        instances.remove(pin.instance)
    remainder = set()
    for instance in instances:
        temp = instance.definition['EDIF.identifier']
        if instance.definition['EDIF.identifier'] not in black_list:
            remainder.add(instance)
    instances = remainder
    return instances


def determine_other_voters(ir, cell_target, voter_target):
    top_definition = ir.top_instance.definition
    lookup = HierarchicalLookup(ir)
    temp = list()
    for cell in cell_target:
        instance_trace = lookup.get_instance_from_name(utility.get_hierarchical_name(cell))
        for inner_pin, outer_pin in cell.outer_pins.items():
            if inner_pin.port.direction == Port.Direction.IN:
                continue
            if outer_pin.wire.cable['EDIF.identifier'] in voter_target:
                continue
            instances = utility.trace_pin(outer_pin, instance_trace)
            for instance in instances.values():
                if instance not in cell_target:
                    # TODO do not change voter_target
                    voter_target.append(outer_pin.wire.cable['EDIF.identifier'])
                    temp.append(outer_pin.wire.cable['EDIF.identifier'])
    return temp


def _find_driver(pin):
    if pin.port.direction == Port.Direction.OUT:
        return pin
    for wire_pin in pin.wire.pins:
        if wire_pin is pin:
            continue
        if isinstance(wire_pin, InnerPin):
            continue
        if wire_pin.inner_pin.port.direction == Port.Direction.OUT:
            return wire_pin


def _is_voter(instance):
    name = instance['EDIF.identifier']
    print('Length of ' + instance['EDIF.identifier'] + ' is ' + str(len(instance['EDIF.identifier'])))
    if len(name) < 6:
        return False
    print(name[0:6])
    if name[0:6] == "voter_":
        return True
    return False

    name = list()
    return list(name)


def determine_clock_domains(ir=None, graph=None):
    assert (ir is not None and graph is None) or (ir is None and graph is not None)
    f = open(files.supportfile_dir + '/clk_ports.json', 'r')
    data = json.loads(f.read())
    f.close()
    if ir is not None:
        print("IR is currently not supported")
        return
        return _find_clock_domains_with_ir(ir, data)
    else:
        return _find_clock_domains_with_graph(graph, data)


def _find_clock_domains_with_ir(ir, data):
    top_definition = ir.top_instance.definition
    lookup = HierarchicalLookup(ir)
    domains = list()
    # TODO support hierarchy
    for instance in top_definition.instances:
        if utility.is_sequential(instance):
            if instance.definition['EDIF.identifier'] in data.keys():
                instance_trace = lookup.get_instance_from_name(utility.get_hierarchical_name(instance))
                for inner_pin, outer_pin in instance.outer_pins.items():
                    if inner_pin.port['EDIF.identifier'] in data[instance.definition['EDIF.identifier']]:
                        domain = utility.trace_pin(outer_pin, instance_trace)
                        # print("The domain is")
                        for domain_elements in domain.values():
                            pass
                            # print('\t' + domain_elements['EDIF.identifier'])
                        # print('\t' + instance['EDIF.identifier'])
                        domain = set(domain.values())
                        domain.add(instance)
                        if domain not in domains:
                            domains.append(domain)
            else:
                print(instance.definition['EDIF.identifier'], "is sequential but has no known clock ports")
    # print()
    pass


def _find_clock_domains_with_graph(graph, data):
    lookup = None
    domains = list()
    for node in graph.nodes:
        if lookup is None:
            lookup = HierarchicalLookup(node.definition.library.environment)
        if utility.is_combinational(node):
            continue
        if node.definition['EDIF.identifier'] in data.keys():
            instance_trace = lookup.get_instance_from_name(utility.get_hierarchical_name(node))
            instance_trace.pop()
            for inner_pin, outer_pin in node.outer_pins.items():
                if inner_pin.port['EDIF.identifier'] in data[node.definition['EDIF.identifier']]:
                    domain = utility.trace_pin(outer_pin, instance_trace)
                    domain[outer_pin] = node
                    _mark_domain(domain, data)
                    # print("The domain is")
                    for domain_elements in domain.values():
                        pass
                        # print('\t' + domain_elements['EDIF.identifier'])
                    # print('\t' + node['EDIF.identifier'])
                    domain = set(domain.values())
                    if domain not in domains:
                        domains.append(domain)
        else:
            print(node.definition['EDIF.identifier'], "is sequential but has no known clock ports")
    return domains


def _mark_domain(domain, data):
    for pin, instance in domain.items():
        if pin.inner_pin.port.direction == Port.Direction.OUT:
            break
    driver = pin
    for pin, instance in domain.items():
        if driver is pin:
            continue
        if instance.definition['EDIF.identifier'] in data:
            instance.is_sequential = True
            instance.driver = driver
    # print()


import networkx as nx

def find_clock_crossing(graph):
    assert isinstance(graph, nx.DiGraph)
    crossings = list()
    for node in graph.nodes():
        for successor in graph.successors(node):
            if successor.driver != node.driver:
                crossings.append([node, successor])
    return crossings


def find_synchronizers(crossings, ir_graph):
    f = open(files.supportfile_dir + '/clk_ports.json', 'r')
    data = json.loads(f.read())
    f.close()
    start = set()
    # TODO combine crossings with same destination
    for crossing in crossings:
        num_of_successors = 0
        for successor in ir_graph.successors(crossing[1]):
            num_of_successors += 1
            if num_of_successors != 1:
                can_be_sync = False
                break
            if successor.definition['EDIF.identifier'] in data:
                can_be_sync = True
            else:
                can_be_sync = False
        if can_be_sync:
            start.add(crossing[1])
    synchronizers = list()
    for instance in start:
        sync_group = list()
        sync_group.append(instance)
        successor = next(ir_graph.successors(instance))
        sync_group.append(successor)
        num_of_successors = 0
        for successor in ir_graph.successors(sync_group[1]):
            num_of_successors += 1
            if num_of_successors != 1:
                can_be_sync = False
                break
            if successor.definition['EDIF.identifier'] in data:
                can_be_sync = True
            else:
                can_be_sync = False
        if can_be_sync:
            sync_group.append(next(ir_graph.successors(sync_group[1])))
        # print()
        synchronizers.append(sync_group)
    # print()
    return synchronizers



from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.graph.Graph_Builder import GraphBuilder

if __name__ == '__main__':
    parser = EdifParser.from_filename(files.edif_files["three_stage_synchronizer2.edf"])
    parser.parse()
    ir = parser.netlist
    builder = GraphBuilder()
    builder.build_graph(ir)
    sequential_graph = builder.sequential_graph
    # determine_clock_domains(ir=ir)
    determine_clock_domains(graph=sequential_graph)
    temp = find_clock_crossing(sequential_graph)
    find_synchronizers(temp, builder.ir_graph)
