from utilities.defaults import *
import random
from utilities.graph_utilities import *
import matplotlib.pyplot as plt

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
    mli1_contact_coords = [(2.9 + random.random() * 0.2, count + random.random() * 0.05) for count in contacts_arrays[1]]
    mli1_unique_coords = [(3.9 + random.random() * 0.2, count + random.random() * 0.05) for count in unique_num_arrays[1]]
    mli2_contact_coords = [(0.9 + random.random() * 0.2, count + random.random() * 0.05) for count in contacts_arrays[0]]
    mli2_unique_coords = [(1.9 + random.random() * 0.2, count + random.random() * 0.05) for count in unique_num_arrays[0]]
    dots = mli1_contact_coords + mli1_unique_coords + mli2_contact_coords + mli2_unique_coords
    xs, ys = [dot[0] for dot in dots], [dot[1] for dot in dots]
    plt.scatter(xs, ys)
    plt.yticks(range(0, 10, 1))
    plt.show()
    # plt.savefig('c:\\Users\\regehr\\Downloads\\CF Contacts per MLI Scatter')

def boxplots():
    plt.boxplot(contacts_arrays + unique_num_arrays)
    plt.yticks(range(0, 10, 1))
    plt.show()
    # plt.savefig('c:\\Users\\regehr\\Downloads\\CF Contacts per MLI Boxplots')

scatterplot()