from utilities.graph_utilities import G
from utilities.gspread_utilities import *

for node in G.nodes:
    print(G.nodes[node]['cell_type'])

# get the data written to a test file, then see if we can read it back out?
TEST_NAME = 'test_graph.gml'
save_current_graph_to_file(TEST_NAME)
    
G = nx.read_gml(TEST_NAME)
print(G)