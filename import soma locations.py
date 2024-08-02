import utilities.defaults
from utilities.gspread_utilities import *



G = utilities.defaults.default_G

document = cf_synapse_doc

soma_sheet = document.worksheet('MLI Soma Locations')
soma_table = soma_sheet.get_all_values()

# take table, make a dictionary of cells and their coordinates
location_dict = {}
for row in soma_table:
    # first find the coord
    if ',' in row[1]:
        soma_coordinate = row[1]
    else:
        soma_coordinate = [float(item) for item in row[1:]]
    location_dict[row[0]] = soma_coordinate

# for each cell coord pair, assign a 'coord' attribute to that cell. 
for key, val in location_dict.items():
    G.nodes[key]['soma_coord'] = val

# (ask and then) write the new graph to sheet. 
if input('write new graph to spreadsheet? (yes/no)') == 'yes':
    write_graph_to_sheet()