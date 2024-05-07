import networkx as nx
from em_utilities import pc_to_cf
# from em_utilities import mli_type_dict

default_graph_name = 'verified_graph.gz'
default_graph = nx.read_gml(default_graph_name)

verified_graph_name = 'verified_graph.gz'
G = nx.read_gml(verified_graph_name)

#returns the amount of edges from from_node to to_node in a directed graph G
def degree_between(from_node, to_node, G = default_graph):
    counter = 0
    for edge in G.edges:
        if (edge[0], edge[1]) == (from_node, to_node):
            counter += 1
    return counter

def cell_type(neuron, G = default_graph):
    return G.nodes[neuron][cell_type]

def all_edges_between(pre_syn, post_syn, G = default_graph, data = True):
    return [edge for edge in G.out_edges(pre_syn, data = data) if edge[1] == post_syn]

def all_edges_between_sets(pre_syn_set, post_syn_set, G = default_graph, data = True):
    result = []
    for pre_syn in pre_syn_set:
        result += [edge for edge in G.out_edges(pre_syn, data = data) if edge[1] in post_syn_set and edge not in result]
    return result    

# Given a pc, generate its list of disynaptic MLI1s from its climbing fiber and return a list of edges that connect those MLI1s to the PC. 
def disynaptic_mli1_to_pc_edges(pc, G = default_graph):
    pass

# Given a pc, generate its list of monosynaptic MLI1s from its climbing fiber and return a list of edges that connect those MLI1s to the PC. 
def monosynaptic_mli1_to_pc_edges(pc, G = default_graph):
    pass

# Given a list of pc, generate its list of disynaptic MLI2s and MLI1s from its climbing fiber and return a list of edges that connect those MLI2s to those MLI1s.
def climbing_fiber_mli2_to_mli1_edges(pc, G = default_graph):
    cf = pc_to_cf(pc)
    

def successors_by_type(neuron, neuron_type, G = default_graph):
    result = []
    for successor in G.successors(neuron):
        if cell_type(successor, G = G) == neuron_type and successor not in result:
            result.append(successor)
    return result

def predecessors_by_type(neuron, neuron_type, G = default_graph):
    result = []
    for predecessor in G.predecessors(neuron):
        if cell_type(predecessor, G = G) == neuron_type and predecessor not in result:
            result.append(predecessor)
    return result

def successors_from_list_by_type(neuron_list, neuron_type, G = default_graph):
    result = []
    for neuron in neuron_list:
        for successor in G.successors(neuron):
            if cell_type(successor) == neuron_type and successor not in result:
                result.append(successor)
    return result

def predecessors_from_list_by_type(neuron_list, neuron_type, G = default_graph):
    result = []
    for neuron in neuron_list:
        for predecessor in G.predecessors(neuron):
            if cell_type(predecessor) == neuron_type and predecessor not in result:
                result.append(predecessor)
    return result

#returns a LIST of mli1 id's that corresponds to all MLI1s that are synapsed onto by a climbing fiber MLI2
def get_disynaptic_mli1s(pc, G = default_graph):
    cf = pc_to_cf(pc)
    predecessors = [mli1 for mli1 in G.predecessors(pc) if cell_type(mli1, G = G) == 'MLI1']
    disynaptic_mli1s = [neuron for neuron in nx.dfs_tree(G, source = cf, depth_limit = 2) if neuron in predecessors]
    return disynaptic_mli1s

def out_edges_from_list(list, G = default_graph, data = True):
    result = []
    passed_coords = []
    for neuron in list:
        for edge in G.out_edges(neuron, data = data):
            coord = edge[2]['xyz']
            if coord not in passed_coords:
                passed_coords.append(coord)
                result.append(edge)
    return result

def successors_from_list(list, G = default_graph):
    result = []
    for neuron in list:
        for successor in G.successors(neuron):
            if successor not in result:
                result.append(successor)
    return result

# must be given a table that contains no duplicate edges. its location should have already been converted to a tuple. 
def construct_graph_from_table(table, filename):
    new_graph = nx.MultiDiGraph()
    data = table
    for row in data:
        if row[3] == 'TRUE':
            coord = row[2]
            new_graph.add_edge(row[0], row[1], location = coord)
    for cell in new_graph.nodes():
        if cell in mli_type_dict.keys():
            new_graph.nodes[cell]['cell_type'] = mli_type_dict[cell]
        elif cell[:2] == 'cf':
            new_graph.nodes[cell]['cell_type'] = 'cf'
        else:
            try:
                new_graph.nodes[cell]['cell_type'] = cell_type(cell, G = default_graph)
            except KeyError:
                new_graph.nodes[cell]['cell_type'] = ''
    nx.write_gml(new_graph, filename)