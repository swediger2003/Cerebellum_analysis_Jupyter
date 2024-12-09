from utilities.defaults import *
from utilities.graph_utilities import *

G = default_G

# list of all ectopic grcs
ectopic_grcs = [node for node in default_G if cell_type(node, G = G) == 'ectopic_grc']

# for each ect_grc, get its in edges
in_edges = [list(G.predecessors(node)) for node in ectopic_grcs]

out_edges = [list(G.successors(node)) for node in ectopic_grcs]

# for each node in ect_grcs, plot its location in the cell. 
# each ect_grc has a soma_coord in the database already. 
# 
for neuron in ectopic_grcs:
    print(neuron + " out edges: ")
    print([edge[1] for edge in G.out_edges(neuron)])
    print(neuron + " in edges: ")
    print([edge[1] for edge in G.in_edges(neuron)])

