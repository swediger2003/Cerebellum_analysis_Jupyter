# Cerebellum_analysis_jupyter
Analysis of circuits in the Cerebellar Cortex while working at Harvard Med\
Files:
### Synapse_automation_MLIs_PCs:
## Description:
This Jupyter Notebook contains code snippets and functions related to analyzing neural network data, specifically focusing on connections between MLIs (Molecular Layer Interneurons) and PC's (Purkinje Cells).

To run this notebook, you'll need the following Python packages:

- numpy
- openpyxl
- matplotlib
- pandas
- seaborn
- pickle
- networkx=2.5

You will also need to import and load the corresponding gz file attached in the repository. Here's how to do it (need networkx version 2.5):

fname = 'db_mli_pc_231209_v2.gz'
G = nx.read_gpickle(fname)

Functions Overview
1. nodes(graph=G)
Prints all nodes in the graph along with their attributes.

2. connections(name_neuron, possible_connection, graph=G)
Prints connections between a specified neuron and a possible connection.

3. numConnections(name_neuron, possible_connection, graph=G)
Prints the number of connections between a neuron and a target neuron.

4. all_connections_to(neuron, filter_list=False, sub='', graph=G)
Returns all connections to a specified neuron, optionally filtering by cell type.

5. automate_connections_id(name_neuron, possible_connection, xl_file_path, graph=G, col_number=1)
Writes connection data between neurons to an Excel file.

6. put_num_connections_df_violin(neurons, possible_connection, col1, col2)
Creates a violin plot visualizing the connections from different types of neurons to a target neuron.

7. check_all_connects(neurons, connect)\
Prints all connections between a list of neurons and a specified target neuron.\

Usage
Load the neural network data using nx.read_gpickle().\
Explore the provided functions to analyze and visualize connections between neurons.\
Customize the notebook for specific analysis needs.\
