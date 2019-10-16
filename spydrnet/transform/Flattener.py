# start at input ports
# trace port to directly connected leaf cells
# connect port to leaf cells
# add leaf cell to dictionary to map to new leaf cell
# while have leaf cells
    # pop leaf cell
    # if leaf cell is in dictionary skip it
    # trace pop_cell to driven cells
    # connect driven cells to pop_cell
    # add driven cells to dictionary to map to new leaf cell
    # add driven_cells to leaf cells

from collections import deque
import random

from spydrnet.ir import *
import spydrnet.utility.utility as util
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.utility.Uniqueifier import Uniquifier


connector_def = None
connector_number = 0
visited_instances = set()
visited_pins = set()
pin_map = dict()
lookup = None
used_name = set()
connectors = list()


DEBUG = False
EMPTY = 0

def flatten_design(ir):
    global connector_def
    global lookup
    global DEBUG
    if DEBUG:
        f = open('mapping.txt', 'w')
        f.close()
    uniquifier = Uniquifier()
    uniquifier.run(ir)
    lookup = HierarchicalLookup(ir)
    flat_definition = _create_flat_definition(ir.top_instance.definition)
    ir.top_instance.definition.library.add_definition(_define_connector(), 0)
    print("Number of ports", len(ir.top_instance.definition.ports))
    port_num = 1
    for port in ir.top_instance.definition.ports:
        print("Working on port number", port_num)
        port_num += 1
        if port.direction == Port.Direction.OUT:
            print("Port as", len(port.inner_pins), "pins")
            pin_num = 1
            for pin in port.inner_pins:
                print("Working on pin number", pin_num)
                pin_num += 1
                _trace_back(pin, flat_definition)
                # _trace_from_port(pin, flat_definition)
        else:
            print("Port is input")
    pass
    ir.top_instance['EDIF.identifier'] = flat_definition['EDIF.identifier']
    if DEBUG:
        ir.top_instance.old_definition = ir.top_instance.definition
        f = open('mapping.txt', 'w')

        for port in flat_definition.ports:
            for inner_pin in port.inner_pins:
                f.write(inner_pin.wire.cable['EDIF.original_identifier'] + '\n')
                if 'EDIF.original_identifier' in inner_pin.wire.cable.debug:
                    f.write(inner_pin.wire.cable.debug['EDIF.original_identifier'])
                else:
                    f.write(inner_pin.wire.cable.debug['EDIF.identifier'])
                f.write('\n')
        f.close()
    ir.top_instance.definition = flat_definition


def _create_flat_definition(top_definition):
    global pin_map
    definition = top_definition.library.create_definition()
    definition['EDIF.identifier'] = top_definition['EDIF.identifier'] + '_flat'
    for port in top_definition.ports:
        new_port = definition.create_port()
        new_port.initialize_pins(len(port.inner_pins))
        for i in range(len(port.inner_pins)):
            pin_map[port.inner_pins[i]] = new_port.inner_pins[i]
        new_port['EDIF.identifier'] = port['EDIF.identifier']
        new_port.direction = port.direction
        if 'EDIF.original_identifier' in port:
            new_port['EDIF.original_identifier'] = port['EDIF.original_identifier']
        if hasattr(port, 'is_array'):
            new_port.is_array = True
    return definition


# def _trace_from_port(pin, flat_definition):
#     global visited_pins
#     global visited_instances
#     global used_name
#     global pin_map
#     connected_pins = pin.wire.pins
#     cable = None
#     wire = None
#     for wire_pin in connected_pins:
#         if wire_pin not in visited_pins and wire is None:
#             cable = Cable()
#             wire = cable.create_wire()
#             name = util.get_hierarchical_name(pin.wire.cable)
#             temp = name.replace('/', '_')
#             temp = temp.replace('&', '')
#             cable['EDIF.identifier'] = temp
#             while cable['EDIF.identifier'] in used_name:
#                 cable['EDIF.identifier'] = temp + '_' + str(random.randint(0, 1000))
#             if temp != name:
#                 cable['EDIF.original_identifier'] = name
#         if wire_pin not in pin_map:
#             if util.is_leaf(wire_pin.instance):
#                 copied_instance = _copy_instance(wire_pin.instance)
#                 flat_definition.add_instance(copied_instance)
#                 other_pins = _get_other_pins(wire_pin.instance, wire_pin)
#                 for pin_prime in other_pins:
#                     _trace_back(pin_prime, flat_definition)
#             pass
#         if wire is not None:
#             wire.connect_pin(pin_map[wire_pin])
#     if cable is not None:
#         flat_definition.add_cable(cable)


def _get_other_pins(instance, outer_pin):
    if isinstance(outer_pin, InnerPin):
        print("Fail")
    pins = list()
    for pin in instance.outer_pins.values():
        if pin.inner_pin is not outer_pin.inner_pin:
            pins.append(pin)
    return pins


def _trace_back(pin, flat_definition):
    global visited_pins
    global visited_instances
    global used_name
    global pin_map
    pin_queue = deque()
    pin_queue.append(pin)
    while len(pin_queue) > EMPTY:
        start_pin = pin_queue.popleft()
        if start_pin is None:
            continue
        if start_pin in visited_pins:
            continue
        connected_pins = start_pin.wire.pins
        cable = _create_cable(start_pin)
        wire = cable.create_wire()
        for wire_pin in connected_pins:
            if wire_pin not in pin_map.keys():
                if isinstance(wire_pin, InnerPin):
                    # connector = _create_connector()
                    # flat_definition.add_instance(connector)
                    # if wire_pin.port.direction == Port.Direction.IN:
                    #     pin_map[wire_pin] = connector.get_pin('O')
                    #     pin_map[_get_outer_pin(wire_pin)] = connector.get_pin('I')
                    #     pin_queue.append(_get_outer_pin(wire_pin))
                    # elif wire_pin.port.direction == Port.Direction.OUT:
                    #     pin_map[wire_pin] = connector.get_pin('I')
                    #     pin_map[_get_outer_pin(wire_pin)] = connector.get_pin('O')
                    _add_connector(flat_definition, wire_pin, pin_queue)
                elif util.is_leaf(wire_pin.instance):
                    copied_instance = _copy_instance(wire_pin.instance)
                    flat_definition.add_instance(copied_instance)
                    pin_queue.extend(_get_other_pins(wire_pin.instance, wire_pin))
                else:
                    _add_connector(flat_definition, wire_pin, pin_queue)
                    # connector = _create_connector()
                    # flat_definition.add_instance(connector)
                    # if wire_pin.inner_pin.port.direction == Port.Direction.OUT:
                    #     pin_map[wire_pin] = connector.get_pin('O')
                    #     pin_map[wire_pin.inner_pin] = connector.get_pin('I')
                    #     pin_queue.append(wire_pin.inner_pin)
                    # elif wire_pin.inner_pin.port.direction == Port.Direction.IN:
                    #     pin_map[wire_pin] = connector.get_pin('I')
                    #     pin_map[wire_pin.inner_pin] = connector.get_pin('O')
            wire.connect_pin(pin_map[wire_pin])
            visited_pins.add(wire_pin)
        flat_definition.add_cable(cable)
        
def _add_connector(definition, pin, pin_queue):
    connector = _create_connector()
    definition.add_instance(connector)
    if isinstance(pin, InnerPin):
        if pin.port.direction == Port.Direction.IN:
            pin_map[pin] = connector.get_pin('O')
            pin_map[_get_outer_pin(pin)] = connector.get_pin('I')
            pin_queue.append(_get_outer_pin(pin))
        elif pin.port.direction == Port.Direction.OUT:
            pin_map[pin] = connector.get_pin('I')
            pin_map[_get_outer_pin(pin)] = connector.get_pin('O')
    else:
        # connector = _create_connector()
        # definition.add_instance(connector)
        if pin.inner_pin.port.direction == Port.Direction.OUT:
            pin_map[pin] = connector.get_pin('O')
            pin_map[pin.inner_pin] = connector.get_pin('I')
            pin_queue.append(pin.inner_pin)
        elif pin.inner_pin.port.direction == Port.Direction.IN:
            pin_map[pin] = connector.get_pin('I')
            pin_map[pin.inner_pin] = connector.get_pin('O')

    if isinstance(pin, InnerPin):
        connector.port = pin.port
    else:
        connector.port = pin.inner_pin.port
    connectors.append(connector)



def _map_connector(connector, pin, side_one, side_two):
    pin_map[pin] = connector.get_pin(side_one)
    pin_map[pin.inner_pin] = connector.get_pin(side_two)


def _create_cable(pin):
    global used_name

    cable = Cable()
    _name_object(cable, pin.wire.cable)
    # name = util.get_hierarchical_name(pin.wire.cable)
    # temp = name.replace('/', '_')
    # temp = temp.replace('&', '')
    # cable['EDIF.identifier'] = temp
    # while cable['EDIF.identifier'] in used_name:
    #     cable['EDIF.identifier'] = temp + '_' + str(random.randint(0, 1000))
    # if temp != name:
    #     cable['EDIF.original_identifier'] = name
    return cable


def _name_object(object_to_name, name_source):
    name = util.get_hierarchical_name(name_source)
    temp = name.replace('/', '_')
    temp = temp.replace('&', '')
    object_to_name['EDIF.identifier'] = temp
    while object_to_name['EDIF.identifier'] in used_name:
        object_to_name['EDIF.identifier'] = temp + '_' + str(random.randint(0, 1000))
    if temp != name:
        if name[-1] == '_':
            for x in range(2, len(name)):
                if name[-x].isalpha():
                    break
                if name[-x] == '_':
                    name = name[:-x] + '[' + name[-x + 1: -1] + ']'
        object_to_name['EDIF.original_identifier'] = name
    used_name.add(temp)
    if DEBUG:
        if isinstance(name_source, Cable):
            object_to_name.debug = name_source
            # f = open('mapping.txt', 'a')
            # if 'EDIF.original_identifier' in name_source:
            #     f.write(name_source['EDIF.original_identifier'] + '\t' + name)
            # else:
            #     f.write(name_source['EDIF.identifier'] + '\t' + name)
            # f.write('\n')
            # f.close()



def _get_outer_pin(pin):
    global lookup
    name = util.get_hierarchical_name(pin.port)
    stack = lookup.get_port_from_name(name)
    stack.pop()
    if stack == []:
        print()
    if stack == [] or pin not in stack[-1].outer_pins:
        return None
    return stack[-1].outer_pins[pin]


def _copy_instance(instance_to_copy):
    global pin_map
    global used_name
    global DEBUG
    new_instance = Instance()
    _name_object(new_instance, instance_to_copy)
    # name = util.get_hierarchical_name(instance_to_copy)
    # while name in used_name:
    #     name = name + '_' + str(random.randint(1, 10000))
    # used_name.add(name)
    # temp = name.replace('/', '_')
    # new_instance['EDIF.identifier'] = temp.replace('&', '')
    # if new_instance['EDIF.identifier'] != name:
    #     new_instance['EDIF.original_identifier'] = name
    new_instance.definition = instance_to_copy.definition
    temp = dict()
    for pin in instance_to_copy.outer_pins.values():
        outer_pin = OuterPin()
        outer_pin.inner_pin = pin.inner_pin
        outer_pin.instance = new_instance
        temp[pin.inner_pin] = outer_pin
        pin_map[pin] = outer_pin
    new_instance.outer_pins = temp
    if 'EDIF.properties' in instance_to_copy:
        new_instance['EDIF.properties'] = instance_to_copy['EDIF.properties']
    if DEBUG:
        new_instance.old_instance = instance_to_copy
        instance_to_copy.new_instance = new_instance
    return new_instance
    pass


def _create_connector():
    global connector_def
    global connector_number
    instance = Instance()
    instance.definition = connector_def
    instance['EDIF.identifier'] = 'connector_' + str(connector_number)
    connector_number += 1
    temp = dict()
    for port in connector_def.ports:
        outer_pin = OuterPin()
        outer_pin.inner_pin = port.inner_pins[0]
        outer_pin.instance = instance
        temp[port.inner_pins[0]] = outer_pin
    instance.outer_pins = temp
    return instance


def _define_connector():
    global connector_def
    connector_def = Definition()
    connector_def['EDIF.identifier'] = 'Connector'
    connector_def['EDIF.cellType'] = 'celltype'
    connector_def['EDIF.view.identifier'] = 'netlist'
    connector_def['EDIF.view.viewType'] = 'viewtype'
    in_port = connector_def.create_port()
    in_port.direction = Port.Direction.IN
    in_port['metadata_prefix'] = ['EDIF']
    in_port['EDIF.identifier'] = 'I'
    in_pin = in_port.create_pin()
    out_port = connector_def.create_port()
    out_port.direction = Port.Direction.OUT
    out_port['metadata_prefix'] = ['EDIF']
    out_port['EDIF.identifier'] = 'O'
    out_pin = out_port.create_pin()
    cable = connector_def.create_cable()
    #######################################################
    cable['EDIF.identifier'] = 'temp'
    ##################################################
    wire = cable.create_wire()
    wire.connect_pin(in_pin)
    wire.connect_pin(out_pin)
    return connector_def

from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
import spydrnet.support_files as files
import time


if __name__ == '__main__':
    DEBUG = True
    print("Parsing")
    parser = EdifParser.from_filename(files.edif_files["aes_128_noBRAM.edf"])
    parser.parse()
    ir = parser.netlist
    print("Flattening design")
    uniquifier = Uniquifier()
    # uniquifier.run(ir)
    # flatten(ir)
    start_time = time.time()
    flatten_design(ir)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("composing netlist")
    compose = ComposeEdif()
    compose.run(ir, "flatten.edf")
    temp = list()
    for connector in connectors:
        for pin in connector.outer_pins.values():
            if pin.wire is None:
                temp.append(connector)
                break
    print()
