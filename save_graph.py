import utilities.gspread_utilities
import utilities.defaults

filename = utilities.defaults.default_graph_name

utilities.gspread_utilities.save_current_graph_to_file(filename=filename)