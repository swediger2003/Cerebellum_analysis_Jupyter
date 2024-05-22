import networkx as nx
from em_utilities import pc_to_cf
# from em_utilities import mli_type_dict

default_graph_name = 'graph_files\\autogen_graph.gz'
print('AAAAAAAAAAAAAAAA')
with open(default_graph_name, 'r') as default_graph_file:
    for char in default_graph_file:
        print(char)
default_graph = nx.read_gml(default_graph_name)

verified_graph_name = 'graph_files\\autogen_graph.gz'
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
def disynaptic_mli1_to_pc_edges(pc, G = default_graph, data = True):
    mli1s = get_disynaptic_mli1s(pc, G = G)
    return all_edges_between_sets(mli1s, [pc], G = G, data = data)

# Given a pc, generate its list of monosynaptic MLI1s from its climbing fiber and return a list of edges that connect those MLI1s to the PC. 
def monosynaptic_mli1_to_pc_edges(pc, G = default_graph, data = True):
    mli1s = get_monosynaptic_mli1s(pc, G = G)
    return all_edges_between_sets(mli1s, [pc], G = G, data = data)


# Given a list of pc, generate its list of disynaptic MLI2s and MLI1s from its climbing fiber and return a list of edges that connect those MLI2s to those MLI1s.
def climbing_fiber_mli2_to_mli1_edges(pc, G = default_graph, data = True):
    cf = pc_to_cf(pc)
    mli2s = get_cf_mli2s
    mli1s = successors_from_list_by_type(mli2s, 'MLI1', G = G)
    return all_edges_between_sets(mli2s, mli1s, G = G, data = data)

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

# all nodes that are predecessors of any node in the given list and are also of the given neuron type
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

# list of MLI1s that receive contacts directly from a PC's associated CF
def get_monosynaptic_mli1s(pc, G = default_graph):
    cf = pc_to_cf(pc)
    mli1s = successors_by_type(cf, G = G, cell_type = 'MLI1')
    return mli1s

# list of MLI2s that receive contacts from a PC's associated CF
def get_cf_mli2s(pc, G = default_graph):
    cf = pc_to_cf(pc)
    mli2s = successors_by_type(cf, G = G, cell_type = 'MLI2')
    return mli2s

# all out edges of all neurons in a list
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

# all neurons that are successors of any node in the given list
def successors_from_list(list, G = default_graph):
    result = []
    for neuron in list:
        for successor in G.successors(neuron):
            if successor not in result:
                result.append(successor)
    return result