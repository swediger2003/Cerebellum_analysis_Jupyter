from utilities.defaults import *
import random
from utilities.graph_utilities import *
import matplotlib.pyplot as plt

G = default_G
# fix random seed. 
random.seed(30072024)

mli2s = [cell for cell in G.nodes if cell_type(cell, G = G) == 'MLI2']
mli1s = [cell for cell in G.nodes if cell_type(cell, G = G) == 'MLI1']

# randomly select 20 of each type of MLI to use. 
sample_size = 20

mli2s = random.sample(mli2s, sample_size)
mli1s = random.sample(mli1s, sample_size)

print(mli1s)
print(mli2s)

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