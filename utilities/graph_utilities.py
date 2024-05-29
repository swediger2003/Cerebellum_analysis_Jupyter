# https://networkx.org/documentation/stable/index.html
import networkx as nx

#returns the amount of edges from from_node to to_node in a directed graph G
def degree_between(from_node, to_node, G):
    counter = 0
    for edge in G.edges:
        if (edge[0], edge[1]) == (from_node, to_node):
            counter += 1
    return counter

# given a graph, node, and attribute
def get_attr(node, G, attr_name):
    return G.nodes[node][attr_name]

def cell_type(node, G):
    return get_attr(node, G, 'cell_type')

def all_edges_between(pre_syn, post_syn, G, data = True):
    return [edge for edge in G.out_edges(pre_syn, data = data) if edge[1] == post_syn]

def all_edges_between_sets(pre_syn_set, post_syn_set, G, data = True):
    result = []
    for pre_syn in pre_syn_set:
        result += [edge for edge in G.out_edges(pre_syn, data = data) if edge[1] in post_syn_set and edge not in result]
    return result

def successors_by_type(neuron, neuron_type, G):
    result = []
    for successor in G.successors(neuron):
        if cell_type(successor, G = G) == neuron_type and successor not in result:
            result.append(successor)
    return result

def predecessors_by_type(neuron, neuron_type, G, type_key = 'cell_type'):
    result = []
    for predecessor in G.predecessors(neuron):
        if cell_type(predecessor, G = G) == neuron_type and predecessor not in result:
            result.append(predecessor)
    return result

def successors_from_list_by_type(neuron_list, neuron_type, G):
    result = []
    for neuron in neuron_list:
        for successor in G.successors(neuron):
            if cell_type(successor) == neuron_type and successor not in result:
                result.append(successor)
    return result

# all nodes that are predecessors of any node in the given list and are also of the given neuron type
def predecessors_from_list_by_type(neuron_list, neuron_type, G):
    result = []
    for neuron in neuron_list:
        for predecessor in G.predecessors(neuron):
            if cell_type(predecessor) == neuron_type and predecessor not in result:
                result.append(predecessor)
    return result

# all out edges of all neurons in a list
def out_edges_from_list(list, G, data = True):
    result = []
    passed_coords = []
    for neuron in list:
        for edge in G.out_edges(neuron, data = data):
            coord = edge[2]['xyz']
            if coord not in passed_coords:
                passed_coords.append(coord)
                result.append(edge)
    return result

# all neurons that are successors of any node in the given list
def successors_from_list(list, G):
    result = []
    for neuron in list:
        for successor in G.successors(neuron):
            if successor not in result:
                result.append(successor)
    return result

# generate a subgraph consisting of all edges that are tagged with the given tag. 
def subgraph_by_edge_type(G, edge_tag):
    to_keep = []
    for edge in G.edges(data = True):
        if edge_tag in edge[2]['tags']:
            to_keep.append(edge)
    return nx.subgraph(G, to_keep)