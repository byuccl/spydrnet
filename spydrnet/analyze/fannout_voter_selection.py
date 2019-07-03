import networkx as nx
import matplotlib.pyplot as plt
import re


D = nx.DiGraph()
keyPointsToCut = set()


def run():
    # read_in_graph()
    perform_feedback_cut()
    # print_cut_points()


def read_in_graph():
    global D

    #with open("graphEdges.txt", 'r') as fi:
    #    for line in fi:
    #        match = re.match("\((\d+), *(\d+)\)", line)
    #        if match:
    #            tail = int(match.group(1))
    #            head = int(match.group(2))
    #            D.add_edge(tail, head)
#
    #with open("nodeType.txt", "r") as fi:
    #    for line in fi:
    #        match = re.match("(\d+) (\S+)", line)
    #        if match:
    #            id_number = int(match.group(1))
    #            if id_number not in D.nodes:
    #                D.add_node(id_number)
    #            type_name = match.group(2)
    #            D.nodes[id_number]["type"] = type_name
#
    #with open("graphIDmap.txt", "r") as fi:
    #    for line in fi:
    #        match = re.match("(\d+) (\S+)", line)
    #        if match:
    #            id_number = int(match.group(1))
    #            name = match.group(2)
    #            if id_number not in D.nodes:
    #                D.add_node(id_number)
    #            D.nodes[id_number]["name"] = name





def perform_feedback_cut():
    global keyPointsToCut

    selfloop_nodes = {edge[0] for edge in D.selfloop_edges()}
    keyPointsToCut |= selfloop_nodes
    graph_without_selfloops = D.subgraph(D.nodes - selfloop_nodes)

    scc_to_break_up = [scc for scc in nx.strongly_connected_components(graph_without_selfloops) if len(scc) > 1]
    while len(scc_to_break_up) > 0:
        scc = scc_to_break_up.pop()
        sub_graph = D.subgraph(scc)
        for node in sub_graph.nodes:
            test = D.nodes[node]
            print()
        highest_fanout = max([node for node in sub_graph.nodes if D.nodes[node]["type"].startswith("FD")],
                             key=lambda node: sub_graph.out_degree(node))
        keyPointsToCut.add(highest_fanout)
        sub_graph = sub_graph.subgraph(sub_graph.nodes - {highest_fanout})
        scc_to_break_up += [scc for scc in nx.strongly_connected_components(sub_graph) if len(scc) > 1]


def print_cut_points():
    for keyPoint in keyPointsToCut:
        print(D.nodes[keyPoint]["name"])


run()
