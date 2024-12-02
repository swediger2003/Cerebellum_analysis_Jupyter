from utilities.defaults import *
import random
from utilities.graph_utilities import *
import matplotlib.pyplot as plt
from utilities.gspread_utilities import cf_synapse_doc

X_MIN, X_MAX = 98000, 170000
Y_MIN, Y_MAX = 53000, 103000
Z_MIN, Z_MAX = 400, 900

def node_within_bounds(node) -> bool:
    try:
        point = G.nodes(data=True)[node]['soma_coord']
        return point_within_bounds(point)
    except KeyError:
        return False

def point_within_bounds(point: tuple[float]) -> bool:
    x, y, z = point
    return (
        X_MIN < x and x < X_MAX
        and
        Y_MIN < y and y < Y_MAX
        and
        Z_MIN < z and z < Z_MAX
    )

G = default_G
# fix random seed. 
random.seed(30072024)

def has_no_soma(cell):
    try:
        G.nodes[cell]['soma_coord']
        return False
    except KeyError:
        return True

mli2s = [cell for cell in G.nodes if cell_type(cell, G = G) == 'MLI2' and node_within_bounds(cell)]
mli1s = [cell for cell in G.nodes if cell_type(cell, G = G) == 'MLI1' and node_within_bounds(cell)]

# randomly select 20 of each type of MLI to use. 
SAMPLE_SIZE = 10

mli2s = random.sample(mli2s, SAMPLE_SIZE)
mli1s = random.sample(mli1s, SAMPLE_SIZE)

# print(mli1s)
# print(mli2s)

reverse = nx.reverse_view(G)

contacts_arrays = []
unique_num_arrays = []

contacts_numbers = []
unique_numbers = []
for mli2 in mli2s:
    
    contact_count = len([edge for edge in reverse.out_edges(mli2) if cell_type(edge[1], G = G) == 'cf'])
    unique_count = len([cell for cell in reverse.successors(mli2) if cell_type(cell, G = G) == 'cf'])

    contacts_numbers.append(contact_count)
    unique_numbers.append(unique_count)
contacts_arrays.append(contacts_numbers)
unique_num_arrays.append(unique_numbers)

contacts_numbers = []
unique_numbers = []
for mli1 in mli1s:
    
    contact_count = len([edge for edge in reverse.out_edges(mli1) if cell_type(edge[1], G = G) == 'cf'])
    unique_count = len([cell for cell in reverse.successors(mli1) if cell_type(cell, G = G) == 'cf'])

    contacts_numbers.append(contact_count)
    unique_numbers.append(unique_count)
contacts_arrays.append(contacts_numbers)
unique_num_arrays.append(unique_numbers)

def scatterplot():
    mli1_contact_coords = [(random.gauss(3, 0.1), random.gauss(count, 0.05)) for count in contacts_arrays[1]]
    mli1_unique_coords = [(random.gauss(4, 0.1), random.gauss(count, 0.05)) for count in unique_num_arrays[1]]
    mli2_contact_coords = [(random.gauss(1, 0.1), random.gauss(count, 0.05)) for count in contacts_arrays[0]]
    mli2_unique_coords = [(random.gauss(2, 0.1), random.gauss(count, 0.05)) for count in unique_num_arrays[0]]
    dots = mli1_contact_coords + mli1_unique_coords + mli2_contact_coords + mli2_unique_coords
    xs, ys = [dot[0] for dot in dots], [dot[1] for dot in dots]
    plt.scatter(xs, ys, alpha = 0.7)
    plt.yticks(range(0, 10, 1))
    plt.xticks(range(1, 5, 1), labels=['MLI2 Contact\n Numbers', 'MLI2 Unique\n Climbing Fibers', 'MLI1 Contact\n Numbers', 'MLI1 Unique\n Climbing Fibers'])
    plt.show()
    # plt.savefig('c:\\Users\\regehr\\Downloads\\CF Contacts per MLI Scatter')

def boxplots():
    plt.boxplot(contacts_arrays + unique_num_arrays)
    plt.yticks(range(0, 10, 1))
    plt.xticks(range(1, 5, 1), labels=['MLI2 Contact\n Numbers', 'MLI2 Unique\n Climbing Fibers', 'MLI1 Contact\n Numbers', 'MLI1 Unique\n Climbing Fibers'])
    plt.show()
    # plt.savefig('c:\\Users\\regehr\\Downloads\\CF Contacts per MLI Boxplots')

def write_per_mli_table():
    sheet = cf_synapse_doc.worksheet('CF Contacts Per MLI')

    table = []
    table.append([
        'Neuron Name', 
        'Cell Type', 
        'Number of Total Contacts from Climbing Fibers',
        'Number of Unique Climbing Fibers Contacting'
    ])
    for i, mli1 in enumerate(mli1s):
        row = []
        row.append(mli1)
        row.append("MLI1")
        row.append(contacts_arrays[1][i])
        row.append(unique_num_arrays[1][i])
        table.append(row)
    for i, mli2 in enumerate(mli2s):
        row = []
        row.append(mli2)
        row.append("MLI2")
        row.append(contacts_arrays[0][i])
        row.append(unique_num_arrays[0][i])
        table.append(row)
    
    sheet.update(table, 'A:Z')

scatterplot()
boxplots()