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
