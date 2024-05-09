# Cerebellum_analysis_jupyter

Cole Gaynor and Sean Ediger

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
Prints all connections between a list of neurons and a specified target neuron.

Usage
Load the neural network data using nx.read_gpickle().\
Explore the provided functions to analyze and visualize connections between neurons.\
Customize the notebook for specific analysis needs.


# mli1_mli2_connections
This Jupyter notebook provides automation scripts for analyzing and visualizing connections between MLI2s and MLI1s  in various Purkinje cell (PC) microcircuits.

Ensure the required dependencies are installed before running the notebook.

## Overview
This notebook automates the analysis and visualization of connections between MLI2s and MLI1s in different PC microcircuits. It provides functions to extract connection data, generate heatmaps, and create Sankey plots for visualization.

## Usage
1. Run the notebook cells sequentially.
2. Modify parameters such as the PC microcircuit and file paths as needed.
3. Execute functions to automate the analysis and visualization of MLI2-MLI1 connections.
4. Contains Climbing Fiber Connections (in lists) with that CF's respective PC. Example: mli2_pc23 are all CF to MLI2 connections and that CF connects to PC_23 (as all cf to pc connections are one-to-one)

## Functions
- **check_all_connects_lists(neurons, connects)**
  - Prints all connections between each neuron in a list of neurons and a certain other neuron.
  - Also prints the number of connections between the two.

- **automate_lists_mli2_mli1(name_neuron, possible_connections, xl_file_path, pc, graph=G)**
  - Opens an Excel file and writes all the desired data from connections.
  - Extracts connections from MLI2s to MLI1s in a specific PC microcircuit.
  - Writes the connection data to the Excel file.

- **visualize_mli2_mli1(mli2_list, mli1_list, pc)**
  - Visualizes MLI2 to MLI1 connections for a specific PC microcircuit using a heatmap.

- **mli2_to_mli1_from_pc(pc, pc_mli2_list, xl_file_path)**
  - Extracts MLI2 to MLI1 connections from a given PC microcircuit and writes the data to an Excel file.

- **visualize_mli2_mli1_all(mli2_list, pc)**
  - Visualizes all MLI1s connecting to a specific PC microcircuit and the MLI2s that connect to those MLI1s.

- **generate_data(pc)**
  - Generates data required for generating a Sankey plot.

- **print_all_connects_circuit(mli2_list, mli1_list, pc)**
  - Prints the number of connections in a circuit from MLI2s to MLI1s and all MLI2-MLI1 pairs.
 
- **nodes(graph=G)**
   - **Description**: Prints all nodes in the graph along with their attributes.

- **connections(name_neuron, possible_connection, graph=G)**
   - **Description**: Prints connections between a specified neuron and a possible connection.

- **numConnections(name_neuron, possible_connection, graph=G)**
   - **Description**: Prints the number of connections between a neuron and a target neuron.

- **all_connections_to(neuron, filter_list=False, sub='', graph=G)**
   - **Description**: Returns all connections to a specified neuron, optionally filtering by cell type.

- **automate_connections_id(name_neuron, possible_connection, xl_file_path, graph=G, col_number=1)**
   - **Description**: Writes connection data between neurons to an Excel file.

- **put_num_connections_df_violin(neurons, possible_connection, col1, col2)**
   - **Description**: Creates a violin plot visualizing the connections from different types of neurons to a target neuron.

- **check_all_connects(neurons, connect)**
   - **Description**: Prints all connections between a list of neurons and a specified target neuron.


- **print_all_connects_circuit(mli2_list, mli1_list, pc**
    - **Description**: Prints the number of connections in a circuit from MLI2s to MLI1s and all MLI2-MLI1 pairs.


Feel free to adjust and utilize these functions to suit your specific analysis needs.

### grc_connects.ipynb

#### Description
This Jupyter Notebook contains code snippets and functions for analyzing Granule Cell connections to different Neurons

#### Dependencies
Ensure you have the following Python packages installed:
- gspread
- math
- matplotlib
- pandas
- seaborn
- pickle
- networkx==2.5

#### Usage
1. Load the neural network data using `nx.read_gpickle()`. (not Super important as this database isn't completely accurate)
2. Explore the provided functions to analyze and visualize connections between neurons.
3. Customize the notebook for specific analysis needs.

#### Functions Overview
1. `nodes(graph=G)`: Prints all nodes in the graph along with their attributes.
2. `connections(name_neuron, possible_connection, graph=G)`: Prints connections between a specified neuron and a possible connection.
3. `numConnections(name_neuron, possible_connection, graph=G)`: Prints the number of connections between a neuron and a target neuron.
4. `all_connections_to(neuron, filter_list=False, sub='', graph=G)`: Returns all connections to a specified neuron, optionally filtering by cell type.
5. `automate_connections_id(name_neuron, possible_connection, xl_file_path, graph=G, col_number=1)`: Writes connection data between neurons to an Excel file.
6. `put_num_connections_df_violin(neurons, possible_connection, col1, col2)`: Creates a violin plot visualizing the connections from different types of neurons to a target neuron.
7. `check_all_connects(neurons, connect)`: Prints all connections between a list of neurons and a specified target neuron.
8. Not Finished.

#### Note
Ensure the required data files are available and properly loaded to perform analysis and visualization tasks.

**Note**: Replace `name_neuron`, `possible_connection`, `xl_file_path`, `col_number`, `neurons`, `col1`, `col2`, and `connect` with appropriate parameters according to your analysis requirements.

