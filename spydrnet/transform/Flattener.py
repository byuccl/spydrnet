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

def flatten_design(ir):
    global connector_def
    global lookup
    uniquifier = Uniquifier()
    uniquifier.run(ir)
    lookup = HierarchicalLookup(ir)
    flat_definition = _create_flat_definition(ir.top_instance.definition)
    ir.top_instance.definition.library.add_definition(_define_connector(), 0)
    for port in ir.top_instance.definition.ports:
        if port.direction == Port.Direction.OUT:
            for pin in port.inner_pins:
                _trace_back(pin, flat_definition)
    print()
    pass
    ir.top_instance['EDIF.identifier'] = flat_definition['EDIF.identifier']
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
        if hasattr(port, 'is_array'):
            new_port.is_array = True
        print()
    return definition


import random


def _trace_back(pin, flat_definition):
    global lookup
    global visited_instances
    global pin_map
    global visited_pins
    global used_name
    cable = Cable()
    wire = cable.create_wire()
    name = pin.wire.cable['EDIF.identifier'] + '_' + str(random.randint(1, 10000))
    while name in used_name:
        name = pin.wire.cable['EDIF.identifier'] + '_' + str(random.randint(1, 10000))
    cable['EDIF.identifier'] = name
    flat_definition.add_cable(cable)
    wire_pins = set(pin.wire.pins)
    wire_pins -= visited_pins
    visited_pins.add(pin)
    for wire_pin in wire_pins:
        if isinstance(wire_pin, InnerPin):
            _connect_inner_pin(wire_pin, wire)
            outer_pin = _get_outer_pin(wire_pin)
            if outer_pin is not None and outer_pin not in visited_pins:
                _trace_back(outer_pin, flat_definition)
            pass
        else:
            if util.is_leaf(wire_pin.instance):
                if wire_pin.instance not in visited_instances:
                    visited_instances.add(wire_pin.instance)
                    visited_pins.add(wire_pin)
                    new_instance = _copy_instance(wire_pin.instance)
                    flat_definition.add_instance(new_instance)
                    wire.connect_pin(pin_map[wire_pin])
                    outer_pins = set(wire_pin.instance.outer_pins.values()) - visited_pins
                    for test in outer_pins:
                        _trace_back(test, flat_definition)
            else:
                if wire_pin in pin_map:
                    wire.connect_pin(pin_map[wire_pin])
                else:
                    connector = _create_connector()
                    if wire_pin.inner_pin.port.direction == Port.Direction.OUT:
                        wire.connect_pin(connector.get_pin('O'))
                        pin_map[wire_pin] = connector.get_pin('O')
                        pin_map[wire_pin.inner_pin] = connector.get_pin('I')
                    else:
                        wire.connect_pin(connector.get_pin('I'))
                        pin_map[wire_pin] = connector.get_pin('I')
                        pin_map[wire_pin.inner_pin] = connector.get_pin('O')
                    flat_definition.add_instance(connector)
                    wire.connect_pin(pin_map[wire_pin])
                    visited_pins.add(wire_pin)
                    _trace_back(wire_pin.inner_pin, flat_definition)
    wire.connect_pin(pin_map[pin])




def _get_outer_pin(pin):
    global lookup
    name = util.get_hierarchical_name(pin.port)
    stack = lookup.get_port_from_name(name)
    stack.pop()
    if stack == []:
        return None
    return stack[-1].outer_pins[pin]



def _connect_inner_pin(pin, wire):
    global pin_map
    if pin in pin_map:
        wire.connect_pin(pin_map[pin])
        pass
    else:
        outer_pin = _get_outer_pin(pin)
        connector = _create_connector()
        if pin.port.direction == Port.Direction.OUT:
            wire.connect_pin(connector.get_pin('I'))
            pin_map[pin] = connector.get_pin('I')
            if outer_pin is not None:
                pin_map[outer_pin] = connector.get_pin('O')
        else:
            wire.connect_pin(connector.get_pin('O'))
            pin_map[pin] = connector.get_pin('O')
            if outer_pin is not None:
                pin_map[outer_pin] = connector.get_pin('I')
        wire.cable.definition.add_instance(connector)


def _copy_instance(instance_to_copy):
    global pin_map
    global used_name
    new_instance = Instance()
    name = instance_to_copy['EDIF.identifier'] + '_' + str(random.randint(1, 10000))
    while name in used_name:
        name = instance_to_copy['EDIF.identifier'] + '_' + str(random.randint(1, 10000))
    new_instance['EDIF.identifier'] = name
    new_instance.definition = instance_to_copy.definition
    temp = dict()
    for pin in instance_to_copy.outer_pins.values():
        outer_pin = OuterPin()
        outer_pin.inner_pin = pin.inner_pin
        outer_pin.instance = new_instance
        temp[pin.inner_pin] = outer_pin
        pin_map[pin] = outer_pin
    new_instance.outer_pins = temp
    return new_instance
    pass


def _copy_port(port_to_copy):
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


if __name__ == '__main__':
    parser = EdifParser.from_filename(files.edif_files["unique_challenge.edf"])
    parser.parse()
    ir = parser.netlist
    uniquifier = Uniquifier()
    uniquifier.run(ir)
    # flatten(ir)
    flatten_design(ir)
    compose = ComposeEdif()
    compose.run(ir, "flatten.edf")
