import spydrnet.utility.utility as utility
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.ir import *

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
    instances = set()

    stack.append(top_definition)
    visited.add(top_definition)

    while len(stack) != 0:
        definition = stack.pop()
        for instance in definition.instances:
            if list(instance.outer_pins.keys())[0].wire is None:
                instances.add(instance)
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


# def determine_reduction_location(ir, cell_target):
#     # TODO make this function more general
#     top_definition = ir.top_instance.definition
#     output = list()
#     reduction_location = list()
#     for port in top_definition.ports:
#         if port.direction == Port.Direction.OUT:
#             output.append(port)
#     obufs = list()
#     for port in output:
#         for inner_pin in port.inner_pins:
#             for pin in inner_pin.wire.pins:
#                 if pin is inner_pin:
#                     continue
#                 obufs.append(pin.instance)
#     input = list()
#     for instance in obufs:
#         for inner_pin, outer_pin in instance.outer_pins.items():
#             if inner_pin.port.direction == Port.Direction.IN:
#                 input.append(outer_pin)
#     for pin in input:
#         driver = _find_driver(pin)
#         if not _is_voter(driver.instance):
#             reduction_location.append(driver.wire.cable['EDIF.identifier'])
#     return reduction_location

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
            for instance in instances:
                if instance not in cell_target:
                    voter_target.append(outer_pin.wire.cable['EDIF.identifier'])
                    temp.append(outer_pin.wire.cable['EDIF.identifier'])



def _find_driver(pin):
    for wire_pin in pin.wire.pins:
        if wire_pin is pin:
            continue
        if wire_pin.inner_pin.port.direction == Port.Direction.OUT:
            return wire_pin
    print()

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
