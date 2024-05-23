# https://networkx.org/documentation/stable/index.html
import networkx as nx

# https://docs.gspread.org/en/latest/index.html
import gspread

# https://docs.python.org/3/library/csv.html
import csv

from gspread_credentials import credentials

# define service account to open documents with. 
service_account = gspread.service_account_from_dict(credentials)

# defines document objects, used to import sheets
reconstruction_doc = service_account.open('EM_Reconstructions_CG_SE')
cf_synapse_doc = service_account.open('Manual Check CF Synapses')
neighbor_pathway_doc = service_account.open('Neighboring PC CF Pathways')

# gets commonly used sheets from the documents defined above
collected_data = cf_synapse_doc.worksheet('Collected Data') # contains all synapse data for manually verified synapses from EM. 
node_attributes = cf_synapse_doc.worksheet('Node Attributes') # contains rows that are a node name followed by a list of attributes or tags. 

# writes given graph to file in GML format. 
def write_graph(G, filename):
    nx.write_gml(G, filename)

# Sheet object should be the gspread sheet object, range should be the google sheets coordinate range notation. 
def update_graph_edges_from_sheet(G, sheet_object, range = 'all'):
    if range == 'all':
        table = sheet_object.get_all_values()
    else:
        table = sheet_object.get(range)
    return update_graph_edges_from_table(G, table)

# given a sheet object and range, creates a new graph with edges given by the row of the sheet. 
def new_graph_from_edge_sheet(sheet_object, range = 'all'):
    if range == 'all':
        table = sheet_object.get_all_values()
    else:
        table = sheet_object.get(range)
    G = new_graph_from_edge_table(table)
    return G

def new_graph_from_edge_table(table):
    new_graph = nx.MultiDiGraph()
    G = update_graph_edges_from_table(new_graph, table)
    return G

# given a graph and sheet object, updates the given graph's nodes with attributes from the sheet. 
def update_graph_nodes_from_sheet(G, sheet_object, range = 'all'):
    if range == 'all':
        table = sheet_object.get_all_values()
    else:
        table = sheet_object.get(range)
    return update_graph_nodes_from_table(G, table)

# given a graph and table, adds edges to the graph 
def update_graph_edges_from_table(G, table):
    for row_number, row in enumerate(table):
        pre, post, attributes = row_to_edge(row)
        coord = attributes['coord']
        # if the coordinate of this edge has need been given to any other edge in the graph:
        # also check to make sure that all edges have the tag 'true' before adding them. 
        if all([edge[2]['coord'] != coord for edge in G.edges(data = True)]) and 'true' in attributes['tags']:
            # attributes is a dictionary, unpacked into keyword arguments for the G.add_edge function
            G.add_edge(pre, post, **attributes)
        elif 'true' in attributes['tags']:
            raise UserWarning(f'Two edges have the same coordinate: {coord} is repeated for the second time at row {row_number + 1}')
    return G

# given a table, where each row contains a node name and a list of key:value pairs, update the attribute
def update_graph_nodes_from_table(G, table):
    for row in table:
        neuron = row[0]
        if neuron[-1] == ' ':
            raise UserWarning(f'{neuron} has a trailing space. Fix it!')
        if neuron not in G.nodes():
            continue
        else:
            has_tags = 'tags' in G.nodes[neuron].keys()
            for item in row[1:]:
                if ':' in item:
                    key, value = item.split(':')
                    G.nodes[neuron][key] = value
                # for a value with no key, classify it as a tag, which goes into a list of tags
                else: 
                    if has_tags:
                        G.nodes[neuron]['tags'].append(item)
                    else:
                        G.nodes[neuron]['tags'] = [item]

    return G

# given a filename, sheet, and range, saves edges from that sheet to a file. 
def save_edge_sheet_to_file(filename, sheet_object, range = 'A:C'):
    G = new_graph_from_edge_sheet(sheet_object, range)
    write_graph(G, filename)

def sheet_to_csv_table(sheet_object, filename, range = None):
    if range == None:
        table = sheet_object.get_all_values()
    else:
        table = sheet_object.get(range)
    table_to_csv(table, filename)
    
def table_to_csv(table, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(table)

# takes a table row and gives it the following formatting: 
# Pre-synaptic, Post-synaptic, Coordinate     , ...
# String      , String,      , Tuple of floats, Dict of Attributes, list of tags (Any type)
# if a cell in a row contains a colon, that will be saved as an attribute. Otherwise, it will be saved as a tag. 
def row_to_edge(row):
    result = [None, None, {'tags': []}]
    for i, item in enumerate(row):
        if i >= 2:
            row[i] = item.lower()
    result[0] = row[0]
    result[1] = row[1]
    result[2]['coord'] = string_to_tuple(row[2])
    if len(row) > 2: 
        for item in row[3:]:
            if ':' in item:
                key, value = item.split(':')
                # Don't allow for overwriting attributes
                if key in result[2].keys():
                    raise Exception(f'Edge contains multiple attributes of name {key} at coordinate {result[2]["coord"]}.')
                result[2][key] = value
            # if something has no key:value pair, it is just a tag. 
            else:
                result[2]['tags'].append(item)
    return result
    
# turns a string representation of a tuple into a tuple of floats. 
def string_to_tuple(string):
    # remove beginning and ending parens
    string = string.strip('()')
    # split values by comma
    strings = string.split(',')
    # turn string representations of floats into floats
    result = [float(item) for item in strings]
    return result

def save_current_graph_to_file(filename):
    edge_table = collected_data.get_all_values()
    node_table = node_attributes.get_all_values()

    new_graph = new_graph_from_edge_table(edge_table)
    update_graph_nodes_from_table(new_graph, node_table)

    # check to make sure that there are no nodes missing critical attributes, and give an alert if there are. 
    critical_node_attributes = ['cell_type']
    for node in new_graph.nodes:
        for attr in critical_node_attributes:
            try:
                new_graph.nodes[node][attr]
            except KeyError:
                raise UserWarning(f'Node {node} has no attribute {attr}.') 
            
    critical_edge_attributes = ['coord']
    for edge in new_graph.edges(data=True):
        for attr in critical_edge_attributes:
            try:
                edge[2][attr]
            except KeyError:
                raise UserWarning(f'Edge from {edge[0]} to {edge[1]} has no attributes {attr}.')
        
    write_graph(new_graph, filename)