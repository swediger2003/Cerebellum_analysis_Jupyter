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

mli2s = [cell for cell in G.nodes if cell_type(cell, G = G) == 'MLI2' and node_within_bounds(cell)]
mli1s = [cell for cell in G.nodes if cell_type(cell, G = G) == 'MLI1' and node_within_bounds(cell)]

# randomly select 20 of each type of MLI to use. 
SAMPLE_SIZE = 20

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

plt.boxplot(contacts_arrays + unique_num_arrays)
plt.yticks(range(0, 25, 2))
plt.show()
plt.savefig('c:\\Users\\regehr\\Downloads\\CF Contacts per MLI Boxplots')