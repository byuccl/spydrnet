from spydrnet.ir import Port

from spydrnet.transform.inserter import TMRInserter

from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif

from spydrnet.graph.Graph_Builder import GraphBuilder

from spydrnet.virtual_ir import *
import networkx as nx
import random
import sys
import os
import argparse
import copy

import matplotlib.pyplot as plt

netlist_filename = None
ports_to_replicate_by_name = None
instances_to_replicate_filename = None
output_filename = None

ports_to_replicate = None
instances_to_replicate = None

replicated_ports = None
replicated_instances = None
replicated_nets = None

netlist = None
vitual_top_instance = None

def run():
    parse_arguements()
    parse_netlist()
    populate_virtual_instances()
    get_ports()
    for port in ports_to_replicate:
        print(port.get_hierarchical_name())
    get_instances()
    for instance in instances_to_replicate:
        print(instance.get_hierarchical_name())
        
    apply_tmr()
    compose_netlist()

def parse_arguements():
    global netlist_filename
    global ports_to_replicate_by_name
    global instances_to_replicate_filename
    global output_filename
    
    argument_parser = argparse.ArgumentParser(description="This is a custom TMR application program.")
    argument_parser.add_argument("--netlist_filename", type=str, help="Filename of the netlist to apply it to.")
    argument_parser.add_argument("--ports_to_replicate_by_name", type=str, help="Comma seperated list of top level ports to replicate.")
    argument_parser.add_argument("--instances_to_replicate_filename", type=str, help="Filename of the instances to replicate by hierarchical name.")
    argument_parser.add_argument("--output_filename", type=str, help="Filename of output netlist")
    args = argument_parser.parse_args()
    
    netlist_filename = args.netlist_filename
    ports_to_replicate_by_name = args.ports_to_replicate_by_name.split(',')
    instances_to_replicate_filename = args.instances_to_replicate_filename
    output_filename = args.output_filename
    
def parse_netlist():
    global netlist
    parser = EdifParser.from_filename(netlist_filename)
    parser.parse()
    netlist = parser.netlist
    
def populate_virtual_instances():
    global virtual_top_instance
    virtual_top_instance = generate_virtual_instances_from_top_level_instance(netlist.top_instance)
    
def get_ports():
    global ports_to_replicate
    virtual_port_namemap = dict()
    for port in virtual_top_instance.virtualPorts.values():
        virtual_port_namemap[port.get_hierarchical_name()] = port
    ports_to_replicate = [virtual_port_namemap[x] for x in ports_to_replicate_by_name if x in virtual_port_namemap]
    
def get_instances():
    global instances_to_replicate
    virtual_instance_namemap = dict()
    search_stack = [virtual_top_instance]
    while search_stack:
        current_instance = search_stack.pop()
        virtual_instance_namemap[current_instance.get_hierarchical_name()] = current_instance
        search_stack += current_instance.virtualChildren.values()

    result = list()
    with open(instances_to_replicate_filename) as fi:
        for line in fi:
            line = line.strip()
            if line in virtual_instance_namemap:
                result.append(virtual_instance_namemap[line])
    instances_to_replicate = result
    
def apply_tmr_michael():
    from spydrnet.transform.TMR import TMR
    triplicater = TMR()
    triplicater.run((x.instance for x in instances_to_replicate), None, netlist)
    
def apply_tmr():
    make_non_leaf_definitions_unique()
    replicate_ports()
    replicate_instances()
    replicate_nets()
    add_connections()
    insert_voters()
    
def make_non_leaf_definitions_unique():
    pass
    
def replicate_ports():
    global replicated_ports
    replicated_ports = dict()
    additional_ports = find_submodule_ports_to_replicate()
    if additional_ports:
        for port in additional_ports:
            replicate_port(port)
            
    if ports_to_replicate:
        for port in ports_to_replicate:
            replicate_port(port)

def find_submodule_ports_to_replicate():
    pass
            
def replicate_port(virtual_port):
    port = virtual_port.port
    virtual_instance = virtual_port.virtualParent
    instance = virtual_instance.instance
    definition = instance.definition
    new_ports = list()
    for ii in range(1, 3):
        new_port = definition.create_port()
        new_port.direction = port.direction
        new_port.is_downto = port.is_downto
        new_port.is_scalar = port.is_scalar
        new_port.lower_index = port.lower_index
        new_port.initialize_pins(len(port.inner_pins))
        if 'EDIF.identifier' in port:
            new_port['EDIF.identifier'] = port['EDIF.identifier'] + "_TMR_" + str(ii)
        if 'EDIF.original_identifier' in port:
            new_port['EDIF.original_identifier'] = port['EDIF.original_identifier'] + "_TMR_" + str(ii)
        if 'EDIF.properties' in port:
            new_port['EDIF.properties'] = copy.deepcopy(port['EDIF.properties'])
        new_ports.append(new_port)
    if 'EDIF.identifier' in port:
        port['EDIF.identifier'] = port['EDIF.identifier'] + "_TMR_" + '0'
    if 'EDIF.original_identifier' in port:
        port['EDIF.original_identifier'] = port['EDIF.original_identifier'] + "_TMR_" + '0'
    replicated_ports[virtual_port] = new_ports
    
def replicate_instances():
    global replicated_instances
    replicated_instances = dict()

    if instances_to_replicate:
        for instance in instances_to_replicate:
            replicate_instance(instance)
    
    make_property_unique("SOFT_HLUTNM")
            
def replicate_instance(virtual_instance):
    instance = virtual_instance.instance
    virtual_parent = virtual_instance.virtualParent
    parent_instance = virtual_parent.instance
    parent_definition = parent_instance.definition
    new_instances = list()
    for ii in range(1, 3):
        new_instance = parent_definition.create_child()
        new_instance.definition = instance.definition
        if 'EDIF.identifier' in instance:
            new_instance['EDIF.identifier'] = instance['EDIF.identifier'] + "_TMR_" + str(ii)
        if 'EDIF.original_identifier' in instance:
            new_instance['EDIF.original_identifier'] = instance['EDIF.original_identifier'] + "_TMR_" + str(ii)
        if 'EDIF.properties' in instance:
            new_instance['EDIF.properties'] = copy.deepcopy(instance['EDIF.properties'])
        new_instances.append(new_instance)
    if 'EDIF.identifier' in instance:
        instance['EDIF.identifier'] = instance['EDIF.identifier'] + "_TMR_" + '0'
    if 'EDIF.original_identifier' in instance:
        instance['EDIF.original_identifier'] = instance['EDIF.original_identifier'] + "_TMR_" + '0'
    replicated_instances[virtual_instance] = new_instances
    
def make_property_unique(property_key):
    for virtual_instance, copy_instances in replicated_instances.items():
        instance = virtual_instance.instance
        if 'EDIF.properties' in instance:
            for property in instance['EDIF.properties']:
                if property['identifier'] == property_key:
                    property['value'] = property['value'] + "_TMR_0"
                    index = 0
                    for copy_instance in copy_instances:
                        index += 1
                        for copy_property in copy_instance['EDIF.properties']:
                            if copy_property['identifier'] == property_key:
                                copy_property['value'] = copy_property['value'] + "_TMR_" + str(index)
    
def replicate_nets():
    virtual_cables_to_replicate = set()
    for virtual_instance in replicated_instances.keys():
        for virtual_port in virtual_instance.virtualPorts.values():
            if virtual_port.port.direction == Port.Direction.OUT:
                for virtual_pin in virtual_port.virtualPins.values():
                    outer_virtual_wire = virtual_pin.get_outer_virtual_wire()
                    if outer_virtual_wire:
                        virtual_cables_to_replicate.add(outer_virtual_wire.virtualParent)
                    
    for virtual_port in replicated_ports.keys():
        if virtual_port.port.direction == Port.Direction.IN:
            for virtual_pin in virtual_port.virtualPins.values():
                inner_virtual_wire = virtual_pin.get_inner_virtual_wire()
                if inner_virtual_wire:
                    virtual_cables_to_replicate.add(inner_virtual_wire.virtualParent)
    
    global replicated_nets
    replicated_nets = dict()
    for cable in virtual_cables_to_replicate:
        replicate_net(cable)
        
def replicate_net(virtual_cable):
    cable = virtual_cable.cable
    virtual_instance = virtual_cable.virtualParent
    instance = virtual_instance.instance
    definition = instance.definition
    new_cables = list()
    for ii in range(1, 3):
        new_cable = definition.create_cable()
        new_cable.is_downto = cable.is_downto
        new_cable.is_scalar = cable.is_scalar
        new_cable.lower_index = cable.lower_index
        new_cable.initialize_wires(len(cable.wires))
        if 'EDIF.identifier' in cable:
            new_cable['EDIF.identifier'] = cable['EDIF.identifier'] + "_TMR_" + str(ii)
        #if 'EDIF.original_identifier' in cable:
        #    value = cable['EDIF.original_identifier'] + "_TMR_" + str(ii)
        #    new_cable['EDIF.original_identifier'] = value
        if 'EDIF.properties' in cable:
            new_cable['EDIF.properties'] = copy.deepcopy(cable['EDIF.properties'])
        new_cables.append(new_cable)
    if 'EDIF.identifier' in cable:
        cable['EDIF.identifier'] = cable['EDIF.identifier'] + "_TMR_" + '0'
    #if 'EDIF.original_identifier' in cable:
    #    cable['EDIF.original_identifier'] = cable['EDIF.original_identifier'] + "_TMR_" + '0'
    replicated_nets[virtual_cable] = new_cables
                    
def add_connections():
    for virtual_instance in replicated_instances.keys():
        for virtual_port in virtual_instance.virtualPorts.values():
            if virtual_port.port.direction == Port.Direction.IN:
                for virtual_pin in virtual_port.virtualPins.values():
                    outer_virtual_wire = virtual_pin.get_outer_virtual_wire()
                    wire_index = outer_virtual_wire.wire.cable.wires.index(outer_virtual_wire.wire)
                    outer_virtual_cable = outer_virtual_wire.virtualParent
                    for index, instance_copy in enumerate(replicated_instances[virtual_instance]):
                        if outer_virtual_cable not in replicated_nets:
                            outer_virtual_wire.wire.connect_pin(instance_copy.get_outer_pin(virtual_pin.pin))
                        else:
                            replicated_nets[outer_virtual_cable][index].wires[wire_index].connect_pin(instance_copy.get_outer_pin(virtual_pin.pin))
            elif virtual_port.port.direction == Port.Direction.OUT:
                for virtual_pin in virtual_port.virtualPins.values():
                    outer_virtual_wire = virtual_pin.get_outer_virtual_wire()
                    wire_index = outer_virtual_wire.wire.cable.wires.index(outer_virtual_wire.wire)
                    outer_virtual_cable = outer_virtual_wire.virtualParent
                    for index, instance_copy in enumerate(replicated_instances[virtual_instance]):
                        if outer_virtual_cable in replicated_nets:
                            replicated_nets[outer_virtual_cable][index].wires[wire_index].connect_pin(instance_copy.get_outer_pin(virtual_pin.pin))
                            
    for virtual_port in replicated_ports.keys():
        if virtual_port.port.direction == Port.Direction.OUT:
            for virtual_pin in virtual_port.virtualPins.values():
                pin_index = virtual_pin.pin.port.inner_pins.index(virtual_pin.pin)
                inner_virtual_wire = virtual_pin.get_inner_virtual_wire()
                wire_index = inner_virtual_wire.wire.cable.wires.index(inner_virtual_wire.wire)
                inner_virtual_cable = inner_virtual_wire.virtualParent
                for index, port_copy in enumerate(replicated_ports[virtual_port]):
                    if inner_virtual_cable not in replicated_nets:
                        inner_virtual_wire.wire.connect_pin(port_copy.inner_pins[pin_index])
                    else:
                        replicated_nets[inner_virtual_cable][index].wires[wire_index].connect_pin(port_copy.inner_pins[pin_index])
        elif virtual_port.port.direction == Port.Direction.IN:
            for virtual_pin in virtual_port.virtualPins.values():
                pin_index = virtual_pin.pin.port.inner_pins.index(virtual_pin.pin)
                inner_virtual_wire = virtual_pin.get_inner_virtual_wire()
                wire_index = inner_virtual_wire.wire.cable.wires.index(inner_virtual_wire.wire)
                inner_virtual_cable = inner_virtual_wire.virtualParent
                for index, port_copy in enumerate(replicated_ports[virtual_port]):
                    if inner_virtual_cable in replicated_nets:
                        replicated_nets[inner_virtual_cable][index].wires[wire_index].connect_pin(port_copy.inner_pins[pin_index])

def insert_voters():
    for virtual_instance in replicated_instances.keys():
        for virtual_port in virtual_instance.virtualPorts.values():
            if virtual_port.port.direction == Port.Direction.OUT:
                for virtual_pin in virtual_port.virtualPins.values():
                    outer_virtual_wire = virtual_pin.get_outer_virtual_wire()
                    outer_virtual_cable = outer_virtual_wire.virtualParent
                    virtual_pins = outer_virtual_wire.get_virtualPins()
                    non_replicated_pins = set()
                    for virtual_pin in virtual_pins:
                        if virtual_pin_connected_to_non_replicated_node(virtual_pin):
                            non_replicated_pins.add(virtual_pin)
                    if non_replicated_pins:
                        new_cable = outer_virtual_cable.virtualParent.instance.definition.create_cable()
                        new_cable.is_downto = outer_virtual_cable.cable.is_downto
                        new_cable.is_scalar = outer_virtual_cable.cable.is_scalar
                        new_cable.lower_index = outer_virtual_cable.cable.lower_index
                        new_cable.initialize_wires(len(outer_virtual_cable.cable.wires))
                        if 'EDIF.identifier' in outer_virtual_cable.cable:
                            new_cable['EDIF.identifier'] = outer_virtual_cable.cable['EDIF.identifier'] + "_VOTER"
                        #if 'EDIF.original_identifier' in cable:
                        #    value = cable['EDIF.original_identifier'] + "_TMR_" + str(ii)
                        #    new_cable['EDIF.original_identifier'] = value
                        if 'EDIF.properties' in outer_virtual_cable.cable:
                            new_cable['EDIF.properties'] = copy.deepcopy(outer_virtual_cable.cable['EDIF.properties'])
                        for virtual_pin in non_replicated_pins:
                            if len(virtual_pin.virtualParent.virtualParent.instance.definition.children) == 0 and \
                                len(virtual_pin.virtualParent.virtualParent.instance.definition.cables) == 0:
                                pin = virtual_pin.get_outer_pin()
                            else:
                                pin = virtual_pin.pin
                            pin.wire.disconnect_pin(pin)
                            new_cable.wires[0].connect_pin(pin)
                            
                        voter = create_voter(outer_virtual_cable.cable['EDIF.identifier'] + "_VOTER")
                        outer_virtual_cable.virtualParent.instance.definition.add_child(voter)
                        new_cable.wires[0].connect_pin(voter.get_pin('O'))
                        
                        outer_virtual_wire.wire.connect_pin(voter.get_pin('I0'))
                        
                        
                        wire_index = outer_virtual_wire.wire.cable.wires.index(outer_virtual_wire.wire)
                        outer_virtual_cable = outer_virtual_wire.virtualParent
                        for index, cable_copy in enumerate(replicated_nets[outer_virtual_cable], 1):
                            cable_copy.wires[wire_index].connect_pin(voter.get_pin('I{}'.format(index)))
                            # if outer_virtual_cable in replicated_nets:
                            # replicated_nets[outer_virtual_cable][index].wires[wire_index].connect_pin(instance_copy.get_outer_pin(virtual_pin.pin))
                            
    # for virtual_port in replicated_ports.keys():
        # if virtual_port.port.direction == Port.Direction.IN:
            # for virtual_pin in virtual_port.virtualPins.values():
                # pin_index = virtual_pin.pin.port.inner_pins.index(virtual_pin.pin)
                # inner_virtual_wire = virtual_pin.get_inner_virtual_wire()
                # wire_index = inner_virtual_wire.wire.cable.wires.index(inner_virtual_wire.wire)
                # inner_virtual_cable = inner_virtual_wire.virtualParent
                # for index, port_copy in enumerate(replicated_ports[virtual_port]):
                    # if inner_virtual_cable in replicated_nets:
                        # replicated_nets[inner_virtual_cable][index].wires[wire_index].connect_pin(port_copy.inner_pins[pin_index])
                        
def virtual_pin_connected_to_non_replicated_node(virtual_pin):
    virtual_port = virtual_pin.virtualParent
    if virtual_port in replicated_ports:
        return False
    else:
        virtual_instance = virtual_port.virtualParent
        if virtual_instance in replicated_instances:
            return False
        else:
            return True
            
    
            
def create_voter(name):
    voter = Instance()
    voter["EDIF.identifier"] = name
    properties = list()
    property = dict()
    property["identifier"] = "INIT"
    property["value"] = "8'hE8"
    properties.append(property)
    voter["EDIF.properties"] = properties
    voter.definition = netlist.get_library('hdi_primitives').get_definition('LUT3')
    return voter

def compose_netlist():
    composer = ComposeEdif()
    composer.run(netlist, output_filename)

run()