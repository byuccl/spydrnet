from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.graph.Graph_Builder import GraphBuilder

from gurobipy import *

from spydrnet.virtual_ir import *
import networkx as nx
import random
import os

import matplotlib.pyplot as plt

from itertools import chain


netlist_filename = "b13.edf"
netlist = None
leafcells = None

output_folder = "tight_feedback_tx_contra_reg2"

largest = {
"FSM_onehot_next_bit_reg[7]",
"tx_conta_reg[0]",
"tx_conta_reg[1]",
"send_en_reg",
"FSM_onehot_next_bit_reg[8]",
"tx_conta_reg[2]",
"FSM_onehot_next_bit_reg[9]",
"tx_conta_reg[3]",
"tx_conta_reg[4]",
"tx_conta_reg[5]",
"tx_conta_reg[6]",
"tx_end_reg",
"FSM_onehot_next_bit_reg[0]",
"FSM_onehot_next_bit_reg[1]",
"FSM_onehot_next_bit_reg[2]",
"FSM_onehot_next_bit_reg[3]",
"FSM_onehot_next_bit_reg[4]",
"FSM_onehot_next_bit_reg[5]",
"FSM_onehot_next_bit_reg[6]"
}

largest_plus_one = largest | {"tre_reg"}

second_largest = {
"FSM_sequential_S2_reg[0]",
"FSM_sequential_S2_reg[1]",
"rdy_reg",
"mpx_reg",
"FSM_onehot_S1_reg[7]",
"send_data_reg"
}

large_inbetween = {
"FSM_onehot_S1_reg[3]",
        "FSM_onehot_S1_reg[4]",
        "FSM_onehot_S1_reg[0]",
        "FSM_onehot_S1_reg[2]",
        "FSM_onehot_S1_reg[6]",
        "FSM_onehot_S1_reg[5]",
        "FSM_onehot_S1_reg[1]"
}

feedforward_small = {
"out_reg_reg[7]",
"out_reg_reg[6]",
"out_reg_reg[5]",
"out_reg_reg[4]",
"out_reg_reg[3]",
"out_reg_reg[2]",
"out_reg_reg[1]",
"out_reg_reg[0]",
"data_out_reg"
}

tx_contra_reg = {
"tx_conta_reg[1]",
"tx_conta_reg[5]",
"tx_conta_reg[2]",
"tx_conta_reg[6]",
"send_en_reg",
"tx_conta_reg[0]",
"tx_conta_reg[3]",
"tx_conta_reg[4]",
"tx_end_reg"
}

tx_contra_reg2 = {
"tx_conta_reg[1]",
"tx_conta_reg[5]",
"tx_conta_reg[2]",
"tx_conta_reg[6]",
"tx_conta_reg[0]",
"tx_conta_reg[3]",
"tx_conta_reg[4]"
}

send_en_reg = {
    "send_en_reg",
    "tx_end_reg"
}

random_count = 9 # 75 # 50 # 38 # 20 # 9 

virtual_top_instance = None

model = None

def run():
    parse_netlist()
    populate_virtual_instances()
    leafcells = get_leafcells()
    print("Leafcells including VCC and GND", len(leafcells))
    leafcells = exclude_vcc_and_ground(leafcells)
    print("Leafcells excluding VCC and GND", len(leafcells))
    connectivity_graph = get_leaf_level_connectivity_graph_with_ports()
    
    #look_at_scc_decomposition(connectivity_graph)
    #exit()

    triplicated_top_level_ports = {x for x in get_top_level_ports() if x.port['EDIF.identifier'] in ['clock', 'reset']}
    
    scores = list()
    for _ in range(1):
        selection = {x for x in leafcells if isinstance(x, VirtualInstance) and x.get_name() in tx_contra_reg2}
        driven = nodes_driven_by_nodes(connectivity_graph, selection)
        drive = nodes_that_drive_nodes(connectivity_graph, selection)
        selection = selection | (drive & driven)
        #one_further = set()
        #for x in selection:
        #    one_further |= set(connectivity_graph.successors(x))
        #selection |= one_further
        #selection = look_at_scc_decomposition(connectivity_graph)
        #selection = set(leafcells)
        #selection = max(nx.strongly_connected_components(connectivity_graph), key=len)
        #selection = input_to_largest_scc(connectivity_graph)
        #selection = gurobi_max_min_selection(leafcells, connectivity_graph)
        #selection = random2_selection(leafcells, connectivity_graph)
        #selection = random1_selection(leafcells)
        selection -= set(get_top_level_ports())
        selection -= {x for x in connectivity_graph.nodes if isinstance(x, VirtualInstance) and (x.instance['EDIF.identifier'] in ["VCC", "GND"])}
        subgraph = connectivity_graph.subgraph(selection)
        protected_edge_count = subgraph.number_of_edges()
        voters_needed = [x for x in selection if len(set(connectivity_graph.successors(x)) - selection) > 0]
        print(protected_edge_count)
        print(len(voters_needed))
        scores.append((protected_edge_count - len(voters_needed), selection, voters_needed))
    print(random_count)
    avg = sum(x[0] for x in scores)/len(scores)
    print(avg)
    score, selection, voters_needed = next(x for x in sorted(scores, key=lambda y: y[0]) if x[0] >= avg)
    print("Selection {} reduction_voters {} Score {}".format(len(selection), len(voters_needed), score))
    with open(os.path.join(output_folder, "{}_selection_{}_score.txt".format(len(selection), score)),'w') as fi:
        for select in selection:
            fi.write("{}\n".format(select.get_hierarchical_name()))
    with open(os.path.join(output_folder, "{}_voters_{}_count.txt".format(len(selection), len(voters_needed))),'w') as fi:
        for voter in voters_needed:
            fi.write("{}\n".format(voter.get_hierarchical_name()))
    
    
    #fig, ax = plt.subplots(tight_layout=True)
    
    #ax.hist(scores, bins=100)
    
    #plt.show()
    
    print(connectivity_graph.number_of_nodes())
    print(connectivity_graph.number_of_edges())
    
def parse_netlist():
    global netlist
    parser = EdifParser.from_filename("b13.edf")
    parser.parse()
    netlist = parser.netlist
    
def populate_virtual_instances():
    global virtual_top_instance
    virtual_top_instance = generate_virtual_instances_from_top_level_instance(netlist.top_instance)

def get_leaf_level_connectivity_graph_with_ports():
    #builder = GraphBuilder()
    #builder.build_graph(netlist)
    #ir_graph = builder.ir_graph

    #return ir_graph
    
    D = nx.DiGraph()
    
    leafcells = get_leafcells()
    top_level_ports = get_top_level_ports()
    
    D.add_nodes_from(leafcells)
    D.add_nodes_from(top_level_ports)
    
    for top_level_port in top_level_ports:
        downstream_nodes = get_downstream_leafnodes(top_level_port)
        #print ("downstream from {}".format(top_level_port.get_hierarchical_name()))
        #print ([x.get_hierarchical_name() for x in downstream_nodes])
        for downstream_node in downstream_nodes:
            D.add_edge(top_level_port, downstream_node)
            
    for leafcell in leafcells:
        downstream_nodes = get_downstream_leafnodes(leafcell)
        #print ("downstream from {}".format(leafcell.get_hierarchical_name()))
        #print ([x.get_hierarchical_name() for x in downstream_nodes])
        for downstream_node in downstream_nodes:
            D.add_edge(leafcell, downstream_node)
            
    return D

def get_leafcells():
    leafcells = list()
    search_stack = [virtual_top_instance]
    while search_stack:
        current_instance = search_stack.pop()
        if len(current_instance.virtualChildren) > 0:
            search_stack += current_instance.virtualChildren.values()
        else:
            leafcells.append(current_instance)
    return leafcells
    
def get_top_level_ports():
    return list(virtual_top_instance.virtualPorts.values())
    
def get_downstream_leafnodes(virtualNode):
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
    
def look_at_scc_decomposition(connectivity_graph):
    sequential_graph = get_sequential_graph(connectivity_graph)
    #export_sequential_graph_dot(sequential_graph)
    folded_graph = sequential_graph.copy()
    return_distances = get_return_distances(sequential_graph)
    min_distance = min(return_distances.values())
    while min_distance < float('inf'):
        nodes = {x for x in return_distances.keys() if return_distances[x] == min_distance}
        #driven = nodes_driven_by_nodes(connectivity_graph, nodes)
        #drive = nodes_that_drive_nodes(connectivity_graph, nodes)
        #selection = nodes | (driven & drive)
        #for scc in sorted(nx.strongly_connected_components(connectivity_graph.subgraph(selection)), key=len):
        #    print("scc", len(scc))
        #return selection
        node_to_set = dict()
        for node in nodes:
            if min_distance == 1:
                node_to_set[node] = {node}
            else:
                subgraph = folded_graph.subgraph({x for x in nx.dfs_preorder_nodes(folded_graph, node, min_distance-1) if return_distances[x] <= min_distance})
                scc = next(x for x in nx.strongly_connected_components(subgraph) if node in x)
                node_set = set()
                for scc_node in scc:
                    if scc_node in node_to_set:
                        node_set |= node_to_set[scc_node]
                    else:
                        node_set.add(scc_node)
                for node_set_node in node_set:
                    node_to_set[node_set_node] = node_set
        # collapse final sets
        frozen_sets = {frozenset(x) for x in node_to_set.values()}
        folded_graph.add_nodes_from(frozen_sets)
        for frozen_set in frozen_sets:
            for node in frozen_set:
                node_to_set[node] = frozen_set
        for frozen_set in frozen_sets:
            predecessors = set()
            successors = set()
            for node in frozen_set:
                for other_node in folded_graph.predecessors(node):
                    if other_node not in frozen_set:
                        predecessors.add(node_to_set.get(other_node, other_node))
                for other_node in folded_graph.successors(node):
                    if other_node not in frozen_set:
                        successors.add(node_to_set.get(other_node, other_node))
            folded_graph.remove_nodes_from(frozen_set)
            for predecessor in predecessors:
                folded_graph.add_edge(predecessor, frozen_set)
            for successor in successors:
                folded_graph.add_edge(frozen_set, successor)
        print("folded", min_distance, folded_graph.number_of_nodes())
        # recalculate return distances
        return_distances = get_return_distances(folded_graph)
        # recalculate min
        min_distance = min(return_distances.values())
    export_sequential_graph_dot(sequential_graph, folded_graph=folded_graph)
    print_fold_hierarchy(folded_graph)
    selection = set()
    search_stack = list(folded_graph.nodes())
    while search_stack:
        current_node = search_stack.pop()
        if isinstance(current_node, frozenset):
            if len(current_node) == 1:
                selection.add(next(iter(current_node)))
            else:
                search_stack += list(current_node)
    driven = nodes_driven_by_nodes(connectivity_graph, selection)
    drive = nodes_that_drive_nodes(connectivity_graph, selection)
    selection = selection | (driven & drive)
    for scc in sorted(nx.strongly_connected_components(connectivity_graph.subgraph(selection)), key=len):
        print("scc", len(scc))
    return selection
    return folded_graph

def gen_cluster_hierarchy(fi, nodes, nodeToIndex, prefix = "  ", cluster_index = 0):
    fi.write("{}subgraph cluster_{}{{\n".format(prefix, cluster_index))
    fi.write('    label="FEEDBACK_GROUP";\n')
    for node in sorted((x for x in nodes if not isinstance(x,VirtualPort)), key= lambda y: len(y) if isinstance(y, frozenset) else 0, reverse=True):
        if isinstance(node, frozenset):
            cluster_index += 1
            cluster_index = gen_cluster_hierarchy(fi, node, nodeToIndex, prefix = "  " + prefix, cluster_index= cluster_index)
        else:
            fi.write('{}  {}[label="{}"];\n'.format(prefix,nodeToIndex[node],node.get_name()))
    fi.write(prefix + "}\n")
    return cluster_index

def print_fold_hierarchy(nodes, prefix = ""):
    for node in sorted((x for x in nodes if not isinstance(x,VirtualPort)), key= lambda y: len(y) if isinstance(y, frozenset) else 0, reverse=True):
        if isinstance(node, frozenset):
            print(prefix + "Feedback_node")
            print_fold_hierarchy(node, prefix = "  " + prefix)
        else:
            print(prefix + node.get_name())


def nodes_driven_by_nodes(graph, nodes):
    driven = set()
    for node in nodes:
        search_stack = [node]
        while search_stack:
            current_node = search_stack.pop()
            for next_node in graph.successors(current_node):
                if isinstance(next_node, VirtualInstance) and \
                    not next_node.instance.definition['EDIF.identifier'].startswith('FD') and \
                    next_node not in driven:
                    search_stack.append(next_node)
                    driven.add(next_node)
    return driven

def nodes_that_drive_nodes(graph, nodes):
    drive = set()
    for node in nodes:
        search_stack = [node]
        while search_stack:
            current_node = search_stack.pop()
            for next_node in graph.predecessors(current_node):
                if isinstance(next_node, VirtualInstance) and \
                    not next_node.instance.definition['EDIF.identifier'].startswith('FD') and \
                    next_node not in drive:
                    search_stack.append(next_node)
                    drive.add(next_node)
    return drive

def get_sequential_graph(combinational_graph):
    ir_graph = combinational_graph.copy()
    node_list = list(ir_graph.nodes)
    for node in node_list:
        if isinstance(node, VirtualInstance) and node.instance.definition['EDIF.identifier'].startswith("FD") == False:
            for predecessor in ir_graph.predecessors(node):
                for successor in ir_graph.successors(node):
                    ir_graph.add_edge(predecessor, successor)
            ir_graph.remove_node(node)
    return ir_graph

def get_return_distances(graph):
    return_distances = dict()
    ir_graph = graph.copy()
    # find return distance for all
    node_list = list(ir_graph.nodes)
    for node in node_list:
        successor_node = "s"
        predecessor_node = "p"
        ir_graph.add_nodes_from([successor_node, predecessor_node])
        successors = list(ir_graph.successors(node))
        for successor in successors:
            ir_graph.add_edge(successor_node, successor)
        predecessors = list(ir_graph.predecessors(node))
        for predecessor in predecessors:
            ir_graph.add_edge(predecessor, predecessor_node)
        try:
            shortest_distance = nx.shortest_path_length(ir_graph, successor_node, predecessor_node)
        except:
            shortest_distance = float('inf')
        return_distances[node] = shortest_distance
        ir_graph.remove_node(predecessor_node)
        ir_graph.remove_node(successor_node)
    return return_distances

def export_sequential_graph_dot(sequential_graph, folded_graph = None, exclude_ports=True):
    if not folded_graph:
        folded_graph = sequential_graph
    if exclude_ports:
        sequential_graph = sequential_graph.subgraph(x for x in sequential_graph.nodes if isinstance(x,VirtualInstance))
    nodeToIndex = dict()
    for index,node in enumerate(sequential_graph.nodes):
        nodeToIndex[node] = index
    subgraph_index = 0
    with open("sequential_graph.dot",'w') as fi:
        fi.write("digraph {\n")
        fi.write("  rankdir=LR;\n")
        if not exclude_ports:
            fi.write("  subgraph cluster_{}{{\n".format(subgraph_index))
            subgraph_index += 1
            fi.write('    label="INPUT PORTS";\n')
            for node in [x for x in sequential_graph.nodes if isinstance(x, VirtualPort) and x.port.direction == Port.Direction.IN]:
                label = "{}".format(node.get_name())
                fi.write('  {}[label="{}"];\n'.format(nodeToIndex[node],label))
            fi.write("  }\n")
        subgraph_index = gen_cluster_hierarchy(fi, folded_graph.nodes(), nodeToIndex, cluster_index=subgraph_index)
        subgraph_index += 1
        if not exclude_ports:
            fi.write("  subgraph cluster_{}{{\n".format(subgraph_index))
            subgraph_index += 1
            fi.write('    label="OUTPUT PORTS";\n')
            for node in [x for x in sequential_graph.nodes if isinstance(x, VirtualPort) and x.port.direction == Port.Direction.OUT]:
                label = "{}".format(node.get_name())
                fi.write('  {}[label="{}"];\n'.format(nodeToIndex[node],label))
            fi.write("  }\n")
        for node in [x for x in sequential_graph.nodes if not isinstance(x, VirtualPort) or x.port['EDIF.identifier'] not in ["clock", "reset"]]:
            for successor in sequential_graph.successors(node):
                fi.write('  {} -> {};\n'.format(nodeToIndex[node], nodeToIndex[successor]))
        fi.write("}\n")
    
def export_scc_dot(C):
    with open("scc_decomposition.dot",'w') as fi:
        fi.write("digraph {\n")
        fi.write("  subgraph {\n")
        fi.write('    label="INPUT PORTS";\n')
        for node in [C.graph['mapping'][x] for x in C.graph['mapping'].keys() if isinstance(x, VirtualPort) and x.port.direction == Port.Direction.IN]:
            fi.write('    {};\n'.format(node))
        fi.write("  }\n")
        fi.write("  subgraph {\n")
        for node in [C.graph['mapping'][x] for x in C.graph['mapping'].keys() if isinstance(x, VirtualInstance)]:
            label = "{}:{}".format(node, str(len(C.nodes[node]['members'])))
            fi.write('  {}[label="{}"];\n'.format(node,label))
        fi.write("  }\n")
        fi.write("  subgraph {\n")
        fi.write('    label="OUTPUT PORTS";\n')
        for node in [C.graph['mapping'][x] for x in C.graph['mapping'].keys() if isinstance(x, VirtualPort) and x.port.direction == Port.Direction.OUT]:
            fi.write('    {};\n'.format(node))
        fi.write("  }\n")
        for node in C.nodes:
            for successor in C.successors(node):
                fi.write('  {} -> {};\n'.format(node, successor))
        fi.write("}\n")
    
def export_dot(filename, C):
    index = 0
    mapping = dict()
    with open(filename, 'w') as fi:
        fi.write("digraph {\n")
        for node in graph.nodes:
            color = ""
            shape = ""
            mapping[node] = index;
            if isinstance(node, tuple):
                label = "\\n".join(node)
                color = ",color=blue"
                shape = ",shape=box"
            else:
                label = node['EDIF.identifier']
                if node.definition['EDIF.identifier'].startswith("FD") == True:
                    shape = ",shape=box"
            fi.write('  {}[label="{}"{}{}];\n'.format(index,label,color,shape))
            index = index + 1
        for node in graph.nodes:
            for successor in graph.successors(node):
                fi.write('  {} -> {};\n'.format(mapping[node], mapping[successor]))
        fi.write('}\n');
    
def random1_selection(leafcells):
    return set(random.sample(leafcells, random_count))
    
def random2_selection(leafcells, connectivity_graph):
    runner_ups = set()
    pool = set(random.sample(leafcells, 1))
    selection = set()
    for jj in range(random_count):
        addition = random.sample(pool, 1)
        pool.remove(addition[0])
        selection.add(addition[0])
        pred = connectivity_graph.predecessors(addition[0])
        succ = connectivity_graph.successors(addition[0])
        pool |= {*pred, *succ} - selection
    return selection
    
def gurobi_max_min_selection(leafcells, connectivity_graph):
    global model
    try:
        model = Model("maxP")
        selection = solve_model(leafcells, connectivity_graph)
        return selection
    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))
        traceback.print_exc(file=sys.stdout)

    except AttributeError:
        print('Encountered an attribute error')

def solve_model(leafcells, connectivity_graph):
    create_variables_constraints_and_objective(leafcells, connectivity_graph)
    return optimize_model()
    
def create_variables_constraints_and_objective(leafcells, connectivity_graph):
    global nodeToIDMap
    global IDtoNodeMap
    global nodeSetVarMap
    global nodeUnsetVarMap
    global maxInstances
    
    nodeToIDMap = dict()
    IDtoNodeMap = dict()
    nodeSetVarMap = dict()
    nodeUnsetVarMap = dict()
    
    nodeIndex = 0
    edgeIndex = 0
    
    for node in connectivity_graph.nodes():
        nodeToIDMap[node] = nodeIndex
        IDtoNodeMap[nodeIndex] = node
        setVar = model.addVar(vtype=GRB.BINARY, name="s{}".format(nodeIndex))
        nodeSetVarMap[node] = setVar
        unsetVar = model.addVar(vtype=GRB.BINARY, name="u{}".format(nodeIndex))
        nodeUnsetVarMap[node] = unsetVar
        
        model.addConstr(setVar + unsetVar == 1, "i{}".format(nodeIndex))
        if isinstance(node, VirtualPort) and node.port['EDIF.identifier'] in ['clock', 'reset']:
            model.addConstr(setVar == 1, "fs{}".format(nodeIndex))
        elif node not in leafcells:
            model.addConstr(unsetVar == 1, "fu{}".format(nodeIndex))
        nodeIndex += 1
    
    plusVars = list()
    minusVars = list()
    for node in connectivity_graph.nodes():
        successors = list(connectivity_graph.successors(node))
        for successor in successors:
            plusVar = model.addVar(vtype = GRB.BINARY, name="p{}".format(edgeIndex))
            model.addConstr(plusVar == and_(nodeSetVarMap[node], nodeSetVarMap[successor]), "a{}".format(edgeIndex))
            plusVars.append(plusVar)
            edgeIndex += 1
        anySuccessor = model.addVar(vtype = GRB.BINARY, name="au{}".format(nodeToIDMap[node]))
        model.addConstr(anySuccessor == or_([nodeUnsetVarMap[s] for s in successors]), "auc{}".format(nodeToIDMap[node]))
        minusVar = model.addVar(vtype = GRB.BINARY, name="m{}".format(nodeToIDMap[node]))
        model.addConstr(minusVar == and_(nodeSetVarMap[node], anySuccessor), "an{}".format(nodeToIDMap[node]))
        minusVars.append(minusVar)
        
    setVars = list(nodeSetVarMap.values())
    maxInstances = random_count + 2
    model.addConstr(quicksum(setVars) <= maxInstances, "c")
    model.setObjective(quicksum(plusVars) - quicksum(minusVars), GRB.MAXIMIZE)
        
def optimize_model():
    global selectedInstances
    global protectedEdges
    global neededReductionVoters
    model.optimize()

    #for c in model.getConstrs():
    #   print(c)
    #for v in model.getVars():
    #   print('%s %g' % (v.varName, v.x))
    selectedInstances_inst = [IDtoNodeMap[int(x.varName[1:])] for x in model.getVars() if x.varName.startswith("s") and x.x == 1]
    selectedInstances = len(selectedInstances_inst)
    protectedEdges = len([x for x in model.getVars() if x.varName.startswith("p") and x.x == 1])
    neededReductionVoters = len([x for x in model.getVars() if x.varName.startswith("m") and x.x == 1])
    print('Obj: %g' % model.objVal)
    print("Max Coverage:", random_count)
    print("Max Instances:", maxInstances)
    print("Selected Instances:", selectedInstances)
    print("Protected Nets:", protectedEdges)
    print("Necessary Reduction Voters:", neededReductionVoters)
    return set(selectedInstances_inst)
    
def input_to_largest_scc(connectivity_graph):
    largest_scc = max(nx.strongly_connected_components(connectivity_graph), key=len)
    found_nodes = set(largest_scc)
    search_nodes = list(largest_scc)
    while search_nodes:
        current_node = search_nodes.pop()
        for predecessor in connectivity_graph.predecessors(current_node):
            if predecessor not in found_nodes:
                search_nodes.append(predecessor)
                found_nodes.add(predecessor)
    return found_nodes - largest_scc

'''
def get_downstream_pins(virtualPin):
    downstream_pins = set()
    virtualPort = virtualPin.virtualParent
    virtualInstance = virtualPort.virtualParent
    wire = None
    if virtualPort.port.direction == Port.Direction.IN:
        wire = virtualPin.pin.wire
    elif virtualPort.port.direction == Port.Direction.OUT:
        instance = virtualInstance.instance
        virtualParent = virtualInstance.virtualParent
        pin = virtualPin.pin
        if pin in instance.outer_pins:
            outer_pin = instance.outer_pins[virtualPin.pin]
            wire = outer_pin.wire

    if wire:
        cable = wire.cable
        virtualCable = virtualInstance.virtualCables[cable]
        virtualWire = virtualCable.virtualWires[wire]
        otherVirtualPins = virtualWire.get_virtualPins()
        for otherVirtualPin in otherVirtualPins:
            if otherVirtualPin is not virtualPin:
                otherVirtualPort = otherVirtualPin.virtualParent
                otherVirtualInstance = otherVirtualPort.virtualParent
                if otherVirtualInstance is virtualInstance:
                    if otherVirtualPin.pin.port.direction == Port.Direction.OUT:
                        downstream_pins.add(otherVirtualPin)
                else:
                    if otherVirtualPin.pin.port.direction == Port.Direction.IN:
                        downstream_pins.add(otherVirtualPin)
    
    return downstream_pins
'''

def exclude_vcc_and_ground(leafcells):
    return [x for x in leafcells if x.instance.definition['EDIF.identifier'] not in ["VCC", "GND"]]

run()