import json
from collections import deque
import os

import networkx as nx

import spydrnet.utility.utility as utility
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.ir import *
import spydrnet.support_files as files

EMPTY = 0


def determine_cells_to_replicate(ir, config):
    """
    Using infomation about the board, determine what cells to replicate
    :param ir: test1
    :param config: test2
    :return: test3
    This is a test
    """
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

    while len(stack) != EMPTY:
        definition = stack.pop()
        for instance in definition.instances:
            if list(instance.outer_pins.keys())[0].wire is None:
                instances.append(instance)
                continue
            if instance.definition not in visited:
                visited.add(instance.definition)
                stack.append(instance.definition)
    return instances


def _sanitize_target(top_definition, instances, top_ports, black_list):
    if not top_ports:
        for port in top_definition.ports:
            for inner_pin in port.inner_pins:
                for pin in inner_pin.wire.pins:
                    if pin is not inner_pin:
                        if pin.instance.definition['EDIF.identifier'] == 'OBUF' \
                                or pin.instance.definition['EDIF.identifier'] == 'IBUF':
                            instances.remove(pin.instance)
    for instance in instances:
        if instance.definition['EDIF.identifier'] in black_list:
            instances.remove(instance)
    return instances


def determine_other_voters(ir, cell_target, voter_target):
    lookup = HierarchicalLookup(ir)
    reduction_voter_location = list()
    for cell in cell_target:
        instance_trace = lookup.get_instance_from_name(utility.get_hierarchical_name(cell))
        for inner_pin, outer_pin in cell.outer_pins.items():
            if inner_pin.port.direction == Port.Direction.IN \
                    or outer_pin.wire.cable['EDIF.identifier'] in voter_target:
                continue
            instances = utility.trace_pin(outer_pin, instance_trace)
            for instance in instances.values():
                if instance not in cell_target:
                    voter_target.append(outer_pin.wire.cable['EDIF.identifier'])
                    reduction_voter_location.append(outer_pin.wire.cable['EDIF.identifier'])
    return reduction_voter_location


def _find_driver(pin):
    if pin.port.direction == Port.Direction.OUT:
        return pin
    for wire_pin in pin.wire.pins:
        if wire_pin is pin or isinstance(wire_pin, InnerPin):
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


def determine_clock_domains(graph):
    if not isinstance(graph, nx.DiGraph):
        raise TypeError('Input needs to be the type DiGraph')
    f = open(os.path.join(files.supportfile_dir, 'clk_ports.json'), 'r')
    data = json.loads(f.read())
    f.close()
    return _find_clock_domains_with_graph(graph, data)


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
                    domain = set(domain.values())
                    if domain not in domains:
                        domains.append(domain)
        else:
            print(node.definition['EDIF.identifier'], "is sequential but has no known clock ports")
    return domains


def _mark_domain(domain, data):
    if len(domain) == EMPTY:
        return
    for pin in domain.keys():
        if pin.inner_pin.port.direction == Port.Direction.OUT:
            break
    driver = pin
    for pin, instance in domain.items():
        if driver is pin:
            continue
        if instance.definition['EDIF.identifier'] in data:
            instance.is_sequential = True
            instance.driver = driver




def find_clock_crossing(graph):
    assert isinstance(graph, nx.DiGraph)
    crossings = list()
    for node in graph.nodes():
        for successor in graph.successors(node):
            if successor.driver != node.driver:
                crossings.append([node, successor])
    return crossings


def find_synchronizers(crossings, ir_graph):
    f = open(os.path.join(files.supportfile_dir, 'clk_ports.json'), 'r')
    data = json.loads(f.read())
    f.close()
    start = set()
    # TODO combine crossings with same destination
    for crossing in crossings:
        num_of_successors = 0
        can_be_sync = False
        for successor in ir_graph.successors(crossing[1]):
            num_of_successors += 1
            if num_of_successors != 1:
                can_be_sync = False
                break
            if successor.definition['EDIF.identifier'] in data:
                can_be_sync = True
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
        synchronizers.append(sync_group)
    return synchronizers

def combination_driven_by_non_replicated(ir_graph, blacklist):
    answer = list()
    for instance in ir_graph.nodes():
        if instance.definition['EDIF.identifier'] not in blacklist and utility.is_combinational(instance):
            answer.append(instance)
    return answer


def find_sequential_elements_driven_by_blackbox(sync_graph):
    solution = set()
    for instance in sync_graph.nodes():
        for pin in instance.outer_pins.values():
            if pin.inner_pin.port.direction == Port.Direction.OUT:
                continue
            driver = _find_driver(pin)
            if driver is None:
                continue
            if _is_blackbox(driver.instance):
                solution.add(instance)


def _is_blackbox(instance):
    if not utility.is_combinational(instance) or not utility.is_sequential(instance):
        return False
    elif list(instance.outer_pins.keys())[0].wire is None:
        return True
    else:
        return False


def find_minimum_return_distance(sync_graph, node):
    if node in sync_graph.successors(node):
        return 1
    out_node = ""
    for successor in sync_graph.successors(node):
        sync_graph.add_edge(out_node, successor)
    in_node = ""
    for predecessor in sync_graph.predecessors(node):
        sync_graph.add_edge(predecessor, in_node)
    visisted = set()
    queue = deque(sync_graph.successors(out_node))
    queue.append('BREAK')
    count = 2
    while len(queue) > 0:
        node = queue.popleft()
        if node in visisted:
            continue
        if node == 'BREAK':
            if len(queue) == 0:
                return None
            queue.append(node)
            count += 1
            continue
        visisted.add(node)
        if in_node in sync_graph.successors(node):
            sync_graph.remove_nodes_from([out_node, in_node])
            return count
        queue.extend(sync_graph.successors(node))
    return None



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
