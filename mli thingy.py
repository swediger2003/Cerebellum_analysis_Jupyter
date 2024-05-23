import utilities.gspread_utilities

TEST_GRAPH_NAME = 'graph_files\\test_graph.gml'

utilities.gspread_utilities.save_current_graph_to_file(TEST_GRAPH_NAME)

G = utilities.gspread_utilities.nx.read_gml(TEST_GRAPH_NAME)
print(G)