# https://networkx.org/documentation/stable/index.html
import networkx as nx

# https://docs.gspread.org/en/latest/index.html
import gspread

# https://docs.python.org/3/library/csv.html
import csv

from utilities.gspread_credentials import credentials

from utilities.defaults import default_G as G

from math import log as ln
from math import floor

# define service account to open documents with. 
service_account = gspread.service_account_from_dict(credentials)

# defines document objects, used to import sheets
reconstruction_doc = service_account.open('EM_Reconstructions_CG_SE')
cf_synapse_doc = service_account.open('Manual Check CF Synapses')
neighbor_pathway_doc = service_account.open('Neighboring PC CF Pathways')

# gets commonly used sheets from the documents defined above
collected_data = cf_synapse_doc.worksheet('Collected Data') # contains all synapse data for manually verified synapses from EM. 
node_attributes = cf_synapse_doc.worksheet('Node Attributes') # contains rows that are a node name followed by a list of attributes or tags. 

def find_in_table(search_term, table):
    row_num, col_num = -1, -1
    for i, row in enumerate(table):
        for j, element in enumerate(row):
            if element == search_term:
                row_num, col_num = i, j
    return (row_num, col_num)

def find_row_in_table(search_term, table):
    return find_in_table(search_term, table)[0]

def find_column_in_table(search_term, table):
    return find_in_table(search_term, table)[1]

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
        if neuron not in G.nodes():
            G.add_node(neuron)
            print(len(G.nodes))
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
                    has_tags = True

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
            # do not consider adding an empty string as a tag or attribute. 
            if item == '':
                continue
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

def node_to_row(node_name, G = G):
    row = [node_name]
    data = G.nodes(data=True)[node_name]
    for key, val in data.items():
        # if we stumble onto the tags list, add all tags
        if type(val) is list:
            for item in val:
                row.append(item)
        # if we are not on the tags list and instead on a named attribute, we add that attribute. 
        else:
            row.append(f'{key}:{val}')
    return row

def guess_cell_type(cell_name):
    # go through a variety of cell types and see if the cell name contains markers used as shorthand for the cell. 
    # for example, a cell that contains the letters "pc" is likely a purkinje cell. 
    type_markers = {
        'pc' : 'pc', 
        'grc' : 'grc', 
        'pf' : 'grc', 
        'mli' : 'interneuron', 
        'interneuron' : 'interneuron', 
        'pli' : 'pli', 
        'pcl' : 'interneuron', 
        'fragment': 'fragment'
    }

    for marker, guessed_type in type_markers.items():
        if marker in cell_name:
            return guessed_type
    return 'unknown'

def remove_trailing_spaces_from_table(table):
    new_table = []
    for row in table:
        new_row = []
        for item in row:
            assert(type(item) == str)
            new_row.append(item.strip())
        new_table.append(new_row)
    return new_table


#given a table containing data for edges and a table containing data for nodes, validate that the graph fulfills all necessary conditions for future assumptions. 
# -- all cells must have a cell type. 
def validate_graph_table(edge_table, node_table):

    edge_table = remove_trailing_spaces_from_table(edge_table)
    node_table = remove_trailing_spaces_from_table(node_table)

    new_graph = new_graph_from_edge_table(edge_table)
    update_graph_nodes_from_table(new_graph, node_table)

    nodes = [{
                'name': row[0], 
                'row': i
            } 
            for i, row in enumerate(node_table)]


    duplicate_node, index = find_duplicates([node['name'] for node in nodes])
    if duplicate_node != None:
        raise UserWarning(f'Data sheet contains duplicate of node {duplicate_node} at row {index + 1}.')
    
    incomplete_edges = []
    incomplete_nodes = []

    # iterate over every node and make sure that it has all necessary attributes. If it does not, mark its location and problem. 
    critical_node_attributes = ['cell_type']
    for node in new_graph.nodes:
        for attr in critical_node_attributes:
            try:
                new_graph.nodes[node][attr]
            except KeyError:
                row = find_row_in_table(node, node_table)
                if row < 0:
                    node_table.append([node])
                    row = len(node_table) - 1
                incomplete_nodes.append({
                    'name': node, 
                    'row' : row, 
                    'attr': attr
                })
            
    critical_edge_attributes = ['coord']
    for edge in new_graph.edges(data=True):
        for attr in critical_edge_attributes:
            try:
                edge[2][attr]
            except KeyError:
                incomplete_edges.append({
                    'pre' : edge[0], 
                    'post': edge[1], 
                    'row' : find_row_in_table(edge['coord'], edge_table), 
                    'attr': attr
                    })

    if incomplete_nodes != []:
        auto = False
        for problem in incomplete_nodes:
            if not auto:
                response = input(
                    f'Node {problem["name"]} is missing attribute {problem["attr"]} at row {problem["row"] + 1}.\n Input "auto" to automatically attempt to assign values, type "skip" to skip to next issue, or type value to assign.\n')
                match response:
                    case 'auto':
                        auto = True
                        guessed_type = guess_cell_type(problem['name'])
                        problem['input'] = guessed_type
                        print(f'{problem["name"]}:{guessed_type}\n')
                    case 'quit':
                        break
                    case 'quit':
                        break
                    case 'skip':
                        continue
                    case _:
                        # assign value to attribute. 
                        problem['input'] = response
            else:
                guessed_type = guess_cell_type(problem['name'])
                problem['input'] = guessed_type
                print(f'{problem["name"]}:{guessed_type}\n')
            # now go and edit the thing. 
            new_graph.nodes[problem['name']][problem['attr']] = problem['input']
            node_table[problem['row']] = node_to_row(problem['name'], G=new_graph)

    if incomplete_edges != []:
        for problem in incomplete_edges:
            print(f'Edge from {problem["pre"] } to {problem["post"]} is missing attribute {problem["attr"]} at row {problem["row"]}.')
        raise UserWarning('Cannot save graph with incomplete edges.')
    
    overwrite_sheet = input('Input "yes" to overwrite existing sheet data with validated data.')
    if overwrite_sheet == 'yes':
        write_graph_to_sheet(edge_table, node_table)

    return new_graph

def write_graph_to_sheet(edge_table, node_table):
    collected_data.update(edge_table, 'A:Z')
    node_attributes.update(node_table, 'A:Z')

# gets data from the current storage location and saves it to a graph format. 
def save_current_graph_to_file(filename):
    edge_table = collected_data.get_all_values()
    node_table = node_attributes.get_all_values()

    new_graph = validate_graph_table(edge_table, node_table)

    write_graph(new_graph, filename)

# searches through a list for any duplicate entries. If one exists, it 
def find_duplicates(list: list):
    seen_objects = []
    for i, item in enumerate(list):
        if item in seen_objects:
            return item, i
    return None, -1


# turns a 2-d table into a 1-d array. 
def flatten(list):
    values = []
    for list in list:
        for item in list:
            values.append(item)
    return values

def row_to_col(row):
    col = []
    for item in row:
        col.append([item])
    return col

# True if value is a string with all values being a 0-9 digit value. 
def is_numeric(string):
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    return all([char in digits for char in string])

# True if value is a float with no spaces or any of that funny business. 
def is_float(string):
    return all([is_numeric(word) for word in string.split('.')])

def col_to_annotations(sheet_object):
    values = sheet_object.get_all_values()

    # flatten a table into a list
    values = flatten(values)
    
    values = [value.strip(',') for value in values]
    # filter for items that are float values
    values = [value for value in values if is_float(value)]

    # condense the list into a list of 3-tuples in the same order
    i = 0
    tuples = []
    string = ''
    for item in values:
        string += str(item)
        i += 1
        if i % 3 == 0:
            tuples.append(string)
            string = ''
        else: 
            string += ','
    
    return row_to_col(tuples)

def concatenate_tables(*tables):
    final_table = []
    for table in tables:
        final_table += (table)
    return final_table

def decimal_to_base_n(integer, mod):
    result = []
    digits = floor((ln(integer) / ln(mod)))
    exp = digits
    while exp >= 0:
        next_digit, integer = divmod(integer, mod ** exp)
        result.append(next_digit)
        exp -= 1
    return result

# turns a pair of integers (coordinate) into a STRING like A1 or C9. 
# Google Sheets is effectively base 26, so just convert a number to base 26. 
def coord_to_gdocs_coord(coord):
    x, y = coord
    x += 1
    x = decimal_to_base_n(x, 26)
    char_list = [chr(item + 64) for item in x]
    x = ''
    for char in char_list:
        x += char
    return x + str(y)

# turns a pair of integer coordinates into a STRING like A1:C9. 
def coord_pair_to_gdocs_coord_pair(coord1, coord2):
    coord1 = coord_to_gdocs_coord(coord1)
    coord2 = coord_to_gdocs_coord(coord2)

    return coord1 + ':' + coord2

def move_annotations_to_graph_edges():
    DOCUMENT_OBJECT = cf_synapse_doc
    ANNOTATION_SHEET_NAME = "Synapse Annotation Inputs"
    ANNOTATION_SHEET_OBJECT = DOCUMENT_OBJECT.worksheet(ANNOTATION_SHEET_NAME)
    
    annotated_coord_table = col_to_annotations(ANNOTATION_SHEET_OBJECT)
    new_width = len(annotated_coord_table[0])
    new_height = len(annotated_coord_table)
    
    # the amount of synapses already logged
    existing_rows = len(collected_data.get_all_values())

    # we could just concatenate the existing stuff with the new stuff and rewrite, but i am kind of nervous about losing all of that. 

    # add the coord table just below existing ones. 
    new_start_y = existing_rows + 1
    new_end_y = new_start_y + new_height - 1
    new_start_x = 0
    new_end_x = new_start_x + new_width

    gdoc_coord = coord_pair_to_gdocs_coord_pair((new_start_x, new_start_y), (new_end_x, new_end_y))

    return collected_data.update(annotated_coord_table, gdoc_coord)

# just a second name for the function above. 
def transfer_annotations_to_graph():
    move_annotations_to_graph_edges()