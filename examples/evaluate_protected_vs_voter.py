from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.graph.Graph_Builder import GraphBuilder
from spydrnet.virtual_ir import *

import networkx as nx

import glob
import os
import re

directory = os.path.normpath(r"B:\akeller9\Xilinx\forMatthew\b13")

def run():
    search_path = os.path.join(directory,"*.edf")
    print(search_path)
    fi = open("result_attributes.csv", 'w')
    fi.write("test,tmr_inst,protected_edges,reduction_voters,non_tmr_srcs,non_tmr_snks,weakly_connected\n")
    convert = lambda text: int(text) if text.isdigit() else text
    for file in sorted(glob.glob(search_path), key= lambda item: \
            [convert(text) for text in re.split('([0-9]+)', item)]):
        report(file, fi=fi)
        
    fi.close()
        
def report(file, fi=None):
    testname = os.path.splitext(os.path.basename(file))[0]
    netlist = parse_netlist(file)
    virtual_top_level_instance = populate_virtual_instances(netlist)
    leafcells = get_leafcells(virtual_top_level_instance)
    connectivity_graph = get_leaf_level_connectivity_graph_with_ports(virtual_top_level_instance)
    tmr_virtual_instances = {x for x in leafcells if isinstance(x, VirtualInstance) and x.get_name().endswith("TMR_1")}
    subgraph = connectivity_graph.subgraph(tmr_virtual_instances)
    
    print(testname)
    tmr_inst_cnt = len(tmr_virtual_instances)
    print("  TMR'd Instances: {}".format(tmr_inst_cnt))
    protected_edge_cnt = subgraph.number_of_edges()
    print("  Protected Edges: {}".format(protected_edge_cnt))
    reduction_voters_edge_cnt = len({x for x in leafcells if isinstance(x, VirtualInstance) and x.get_name().endswith("VOTER")})
    print("  Reduction Voters: {}".format(reduction_voters_edge_cnt))
    needed_reduction_voter_edge_cnt = len({x for x in tmr_virtual_instances if len(set(connectivity_graph.successors(x)) - tmr_virtual_instances) > 0})
    assert reduction_voters_edge_cnt == needed_reduction_voter_edge_cnt
    print("  Needed Reduction Voters: {}".format(reduction_voters_edge_cnt))
    non_tmr_srcs_cnt = sum([connectivity_graph.in_degree(x) - subgraph.in_degree(x) for x in tmr_virtual_instances])
    print("  non_tmr_srcs: {}".format(non_tmr_srcs_cnt))
    non_tmr_snks_cnt = sum([connectivity_graph.out_degree(x) - subgraph.out_degree(x) for x in tmr_virtual_instances])
    print("  non_tmr_snks: {}".format(non_tmr_snks_cnt))
    weakly_connected_cnt = nx.number_weakly_connected_components(subgraph)
    print("  weakly_connected: {}".format(weakly_connected_cnt))
    if fi:
        fi.write("{},{},{},{},{},{},{}\n".format(testname, tmr_inst_cnt, protected_edge_cnt, reduction_voters_edge_cnt, non_tmr_srcs_cnt, non_tmr_snks_cnt, weakly_connected_cnt))
    
def parse_netlist(filename):
    global netlist
    parser = EdifParser.from_filename(filename)
    parser.parse()
    netlist = parser.netlist
    return netlist
    
def populate_virtual_instances(netlist):
    virtual_top_instance = generate_virtual_instances_from_top_level_instance(netlist.top_instance)
    return virtual_top_instance
    
def get_leaf_level_connectivity_graph_with_ports(virtual_top_instance):
    #builder = GraphBuilder()
    #builder.build_graph(netlist)
    #ir_graph = builder.ir_graph

    #return ir_graph
    
    D = nx.DiGraph()
    
    leafcells = get_leafcells(virtual_top_instance)
    top_level_ports = get_top_level_ports(virtual_top_instance)
    
    D.add_nodes_from(leafcells)
    D.add_nodes_from(top_level_ports)
    
    for top_level_port in top_level_ports:
        downstream_nodes = get_downstream_leafnodes(virtual_top_instance, top_level_port)
        #print ("downstream from {}".format(top_level_port.get_hierarchical_name()))
        #print ([x.get_hierarchical_name() for x in downstream_nodes])
        for downstream_node in downstream_nodes:
            D.add_edge(top_level_port, downstream_node)
            
    for leafcell in leafcells:
        downstream_nodes = get_downstream_leafnodes(virtual_top_instance, leafcell)
        #print ("downstream from {}".format(leafcell.get_hierarchical_name()))
        #print ([x.get_hierarchical_name() for x in downstream_nodes])
        for downstream_node in downstream_nodes:
            D.add_edge(leafcell, downstream_node)
            
    return D

def get_leafcells(virtual_top_instance):
    leafcells = list()
    search_stack = [virtual_top_instance]
    while search_stack:
        current_instance = search_stack.pop()
        if len(current_instance.virtualChildren) > 0:
            search_stack += current_instance.virtualChildren.values()
        else:
            leafcells.append(current_instance)
    return leafcells
    
def get_top_level_ports(virtual_top_instance):
    return list(virtual_top_instance.virtualPorts.values())
    
def get_downstream_leafnodes(virtual_top_instance, virtualNode):
    downstream_leafnodes = set()
    visited_pins = set()
    search_pins = list()
    if isinstance(virtualNode, VirtualPort):
        if virtualNode.port.direction == Port.Direction.IN:
            search_pins += virtualNode.virtualPins.values()
    elif isinstance(virtualNode, VirtualInstance):
        for virtualPort in virtualNode.virtualPorts.values():
            if virtualPort.port.direction == Port.Direction.OUT:
                search_pins += virtualPort.virtualPins.values()
    
    while search_pins:
        current_pin = search_pins.pop()
        if current_pin in visited_pins:
            continue
        visited_pins.add(current_pin)
        
        inner_virtualWire = current_pin.get_inner_virtual_wire()
        outer_virtualWire = current_pin.get_outer_virtual_wire()
        
        if inner_virtualWire:
            for pin in inner_virtualWire.get_virtualPins():
                if pin is not current_pin:
                    search_pins.append(pin)
                    virtualPort = pin.virtualParent
                    virtualInstance = virtualPort.virtualParent
                    if virtualInstance is virtual_top_instance and pin.pin.port.direction == Port.Direction.OUT:
                        downstream_leafnodes.add(virtualPort)
                    elif len(virtualInstance.virtualCables) == 0 and len(virtualInstance.virtualChildren) == 0 and \
                        pin.pin.port.direction == Port.Direction.IN:
                        downstream_leafnodes.add(virtualInstance)
        
        if outer_virtualWire:      
            for pin in outer_virtualWire.get_virtualPins():
                if pin is not current_pin:
                    search_pins.append(pin)
                    virtualPort = pin.virtualParent
                    virtualInstance = virtualPort.virtualParent
                    if virtualInstance is virtual_top_instance and pin.pin.port.direction == Port.Direction.OUT:
                        downstream_leafnodes.add(virtualPort)
                    elif len(virtualInstance.virtualCables) == 0 and len(virtualInstance.virtualChildren) == 0 and \
                        pin.pin.port.direction == Port.Direction.IN:
                        downstream_leafnodes.add(virtualInstance)
        
    return downstream_leafnodes
    
run()