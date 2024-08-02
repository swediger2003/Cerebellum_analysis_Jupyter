# https://networkx.org/documentation/stable/index.html
import networkx as nx

default_graph_name = 'graph_files\\cerebellar_graph.gml'
default_G = nx.read_gml(default_graph_name)

pc_list = ['pc_2', 'pc_9', 'pc_16', 'pc_22', 'pc_23', 'pc_26', 'pc_32', 'pc_34', 'pc_35', 'pc_50']