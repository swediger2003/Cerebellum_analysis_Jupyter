import utilities.defaults as defaults
import matplotlib.pyplot as plt
from utilities.em_utilities import *

# for each synapse with tag 'pf'
#   get its coord
#   find the coords distance from pcl using distance_from_pc function
#   list of distances form a violin plot using pyplt from mpl

G = defaults.default_G

pf_locations = [edge[2]['coord'] for edge in G.edges(data = True) if 'pf' in edge[2]['tags']]
pf_distances = [distance_from_pcl(coord) for coord in pf_locations]

fig, ax = plt.subplots()

ax.violinplot(pf_distances)

ax.set_xlabel("Relative Frequency")
ax.set_ylabel("Distance from PCL")
ax.set_title("PF Synapse Distribution")

plt.show()