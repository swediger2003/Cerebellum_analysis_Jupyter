from utilities.em_utilities import *
from utilities.defaults import *
from utilities.graph_utilities import *
import os

# https://matplotlib.org/stable/index.html
import matplotlib.pyplot as plt

# below is possibly the worst function ever made. 
def draw_disinhibition_graph(pc, G = G, include_non_predecessor_mli1s = True, include_cf_only_mli1s = False, include_cf_mli1_edges = False, target_pc = None, save = False, generate_legend = False, use_ephaptic = False):
    #set for graph
    fig, ax = plt.subplots()
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    if generate_legend:
        legend = nx.Graph()
        legend.add_nodes_from([250, 125, 25])
        pos = {250: (0, -1), 
              125: (0, -2), 
              25: (0, -3)}
        print(legend.nodes)
        nx.draw(ax = ax, G = legend, node_size = legend.nodes, pos = pos, node_color = 'gray', alpha = 0.8)
        if save:
            plt.savefig(os.path.join(downloads_path, 'Legend.png'), format = 'png')
        return
    
    # unless signified, do not count ephaptic signaling in the graph. 
    if not use_ephaptic:
        remove = [edge for edge in G.edges(keys = True, data = True) if 'ephaptic' in edge[3]['tags']]
        for edge in remove:
            G.remove_edge(edge)

    # if no target_pc is detected, assume that it is the first given PC
    if target_pc is None:
        target_pc = pc
    cf = pc_to_cf(pc)
    
    # direct contacts from cf into mli2s
    mli2s = get_cf_mli2s(pc, G = G)
    
    # function to fetch mli1s in the cf-mli2-mli1 path
    indirect_mli1s = get_disynaptic_mli1s(pc, G = G)
    direct_mli1s = [neuron for neuron in get_monosynaptic_mli1s(pc, G = G) if neuron in indirect_mli1s or include_cf_only_mli1s]
    indirect_mli1s = [neuron for neuron in indirect_mli1s if neuron not in direct_mli1s] # remove indirect contacts if they are also direct contacts, don't want doublecounting
    # remove MLI1s that do not return to the pc if specified
    if not include_non_predecessor_mli1s:
        direct_mli1s = [neuron for neuron in direct_mli1s if neuron in G.predecessors(target_pc)]
        indirect_mli1s = [neuron for neuron in indirect_mli1s if neuron in G.predecessors(target_pc)]

    mli1s = indirect_mli1s + direct_mli1s
    
    #creates a subgraph using only the previously collected MLIs and the relevant PC
    G_copy = nx.subgraph(G, [cf] + mli2s + mli1s + [target_pc]).copy()

    G_reversed = G_copy.reverse()
    returns_to_pc = nx.dfs_tree(G = G_reversed, source = target_pc).nodes
    reachable_from_cf = nx.dfs_tree(G = G, source = cf).nodes
    
    #sets a new attribute 'circuit_layer' to everything in the graph to dictate what layer it will be displayed in
    circuit_layers = 'cf', 'mli2', 'mli1', 'pc'
    for i, layer in enumerate([[cf], mli2s, mli1s, [target_pc]]):
        for neuron in layer:
            G_copy.nodes[neuron]['circuit_layer'] = circuit_layers[i]
    
    #true if edge is from one layer of the graph to the next or from CF to MLI2
    def legal_edge(edge):
        pre_layer  = G_copy.nodes[edge[0]]['circuit_layer']
        post_layer = G_copy.nodes[edge[1]]['circuit_layer']
        return pre_layer == 'cf' or post_layer == 'pc' or (pre_layer, post_layer) == ('mli2', 'mli1')
    
    # use 2 for loops to prune all edges that are not cf->MLI2, MLI2 to MLI1 or MLI1->pc
    to_remove = []
    for edge in G_copy.edges:
        if not legal_edge(edge):
            to_remove.append(edge)
    for edge in to_remove:
        G_copy.remove_edge(edge[0], edge[1])

    #automatically create a dictionary of positions
    multipartite_pos = nx.multipartite_layout(G_copy, subset_key = 'circuit_layer')
    layer_xs = 1, 2, 3, 4
    for i, cell_type_group in enumerate([[cf], mli2s, mli1s, [target_pc]]):
        for neuron in cell_type_group:
            multipartite_pos[neuron][0] = layer_xs[i]

    # create list of point pairs, sort by y coordinate
    coord_list = []
    node_list = []
    for mli1 in mli1s:
        coord = multipartite_pos[mli1]
        coord_list.append(coord)
        node_list.append(mli1)
    coord_list.sort(key = lambda coord: coord[1])
    node_list.sort(key = lambda node: G_copy.out_degree(node))
    for coord, node in zip(coord_list, node_list):
        multipartite_pos[node] = coord
    
    for mli2 in mli2s:
        multipartite_pos[mli2] = np.array([multipartite_pos[mli2][0], multipartite_pos[mli2][1] * 3])

    # move mli2s that do not eventually connect back to the pc to the bottom of the graph
    coord_list = []
    node_list  = []
    for mli2 in mli2s:
        coord = multipartite_pos[mli2]
        coord_list.append(coord)
        node_list.append(mli2)
    coord_list.sort(key = lambda coord: coord[1])
    node_list.sort(key = lambda node: 1 if node in returns_to_pc else 0)
    for coord, node in zip(coord_list, node_list):
        multipartite_pos[node] = coord

    for node in G_copy.nodes():
        if node not in returns_to_pc:
            multipartite_pos[node] = multipartite_pos[node][0], multipartite_pos[node][1] - 0.2

    pc_standin_nodes = []
    direct_pc_standins = []
    indirect_pc_standins = []
    for mli1 in mli1s:
        # need to add a cell directly to the right for each MLI1, with size corresponding to the amount of times a MLI1 synapses onto the relevant PC
        new_node = mli1 + ' to ' + target_pc
        G_copy.add_node(new_node)
        multipartite_pos[new_node] = np.array([multipartite_pos[mli1][0] + 0.2, multipartite_pos[mli1][1]])
        for edge in all_edges_between(mli1, target_pc, G = G_copy):
            G_copy.add_edge(mli1, new_node)
        pc_standin_nodes.append(new_node)
        if mli1 in direct_mli1s:
            direct_pc_standins.append(new_node)
        elif mli1 in indirect_mli1s:
            indirect_pc_standins.append(new_node)
    
    #set the sizes of nodes
    sizes = dict(G_copy.in_degree)
    max_deg = max([size[1] for size in sizes.items() if size[0] != target_pc] + [0])
    for neuron in sizes:
        if neuron != pc:
            sizes[neuron] = 5 * sizes[neuron]
        
    
    # set cell colors for each layer
    cell_colors = {}
    layer_colors = 'white', '#73AF59', '#FF00FF', 'gray', 'white'
    for i, cell_type_group in enumerate([[cf], mli2s, mli1s, pc_standin_nodes, [target_pc]]):
        for cell in cell_type_group:
            cell_colors[cell] = layer_colors[i]
    
    alpha_list = []
    for cell in G_copy.nodes:
        if cell in direct_mli1s:
            alpha_list.append(0.4)
        else:
            alpha_list.append(0.8)    
    
    # print(f'{pc} MLI1s: {mli1s}')

    # if signified, check to highlight MLI1s that make an ephaptic connection with a red outline. 
    highlight_dict = dict([(node, 'white') for node in G.nodes()])
    if use_ephaptic:
        for mli1 in mli1s:
            if any([is_ephaptic(edge) for edge in G.out_edges(mli1, data = True)]):
                # give it a red outline
                highlight_dict[mli1] = 'red'
        highlights = [value for value in highlight_dict.values()]
    # Note: networkx has a parameter to a subfunction of draw called 'edgecolors'. For some reason this is how the border of nodes is given. Don't get confused by this. 

    #changes dict information into list format, using same order as graph nodes for consistency
    size_list = [sizes[neuron] for neuron in G_copy.nodes]
    cell_colors = [cell_colors[neuron] for neuron in G_copy.nodes]
    
    plt.text(1, 1, f'Max Size: {str(max_deg)} connections', fontsize = 8, ha = 'right', va = 'top', transform = plt.gca().transAxes)
    nx.draw(G = G_copy, pos = multipartite_pos, ax = ax, node_color = cell_colors, node_size = size_list, edge_color = 'white', alpha = alpha_list, edgecolors=highlights)
    title = f"{pc} CF Disinhibition to {target_pc}"
    if include_cf_mli1_edges:
        title += ' With CF-MLI1'
    if use_ephaptic:
        title += ' With Ephaptic Connections'
    ax.set_title(title)
    if save:
        plt.savefig(os.path.join(downloads_path, title + '.png'), format ='png')

def draw_inhibition_graph(pc, G = G, target_pc = None, save = False, squish = False):
    # set for graph
    fig, ax = plt.subplots()

    if target_pc == None:
        target_pc = pc
    cf = pc_to_cf(pc)
        
    direct_mli1s = get_monosynaptic_mli1s(target_pc, cf = cf, G = G)
    mli1s = direct_mli1s
        
    # creates a subgraph using only the previously collected MLIs and the relevant PC
    G_copy = nx.subgraph(G, [cf] + direct_mli1s + [target_pc]).copy()
    
    # sets a new attribute 'circuit_layer' to everything in the graph to dictate what layer it will be displayed in
    circuit_layers = 'cf', 'direct_mli1', 'pc'
    for i, layer in enumerate([[cf], direct_mli1s, [target_pc]]):
        for neuron in layer:
            G_copy.nodes[neuron]['circuit_layer'] = circuit_layers[i]
    
    # true if edge is from one layer of the graph to the next or from CF to MLI2
    def legal_edge(edge):
        pre_layer  = G_copy.nodes[edge[0]]['circuit_layer']
        post_layer = G_copy.nodes[edge[1]]['circuit_layer']
        return pre_layer == 'cf' or post_layer == 'pc'
        
    # use 2 for loops to prune all edges that are not cf -> MLI1 or MLI1 -> pc
    # as far as I can tell this generally will not remove anything, because the graphs have already been sanitized to meet this condition.  
    to_remove = []
    for edge in G_copy.edges:
        if not legal_edge(edge):
            to_remove.append(edge)
    for edge in to_remove:
        G_copy.remove_edge(edge[0], edge[1])

    # automatically create a dictionary of positions
    multipartite_pos = nx.multipartite_layout(G_copy, subset_key = 'circuit_layer')
    layer_xs = 1, 2, 3, 4
    for i, cell_type_group in enumerate([[cf], direct_mli1s, [target_pc]]):
        for neuron in cell_type_group:
            multipartite_pos[neuron][0] = layer_xs[i]
    
    # create list of point pairs, sort by y coordinate
    coord_list = []
    node_list = []
    for mli1 in mli1s:
        coord = multipartite_pos[mli1]
        coord_list.append(coord)
        node_list.append(mli1)
    coord_list.sort(key = lambda coord: coord[1])
    node_list.sort(key = lambda node: G_copy.out_degree(node))
    
    # assign each node pair to its corresponding point pair
    for coord, node in zip(coord_list, node_list):
        multipartite_pos[node] = coord

    pc_standin_nodes = []
    for mli1 in direct_mli1s:
        # need to add a cell directly to the right for each MLI1, with size corresponding to the amount of times a MLI1 synapses onto the relevant PC
        new_node = mli1 + ' to ' + target_pc
        G_copy.add_node(new_node)
        multipartite_pos[new_node] = np.array([multipartite_pos[mli1][0] + 0.2, multipartite_pos[mli1][1]])
        for edge in all_edges_between(mli1, target_pc, G = G_copy):
            G_copy.add_edge(mli1, new_node)
        pc_standin_nodes.append(new_node)
    
    # set the sizes of nodes
    sizes = dict(G_copy.in_degree)
    max_deg = max([size[1] for size in sizes.items() if size[0] != target_pc] + [0])
    GLOBAL_SCALE = 5
    for neuron in sizes:
        if neuron != pc:
            sizes[neuron] = GLOBAL_SCALE * sizes[neuron]
    
    # set cell colors for each layer
    cell_colors = {}
    layer_colors = 'white', '#FF00FF', 'gray', 'white'
    for i, cell_type_group in enumerate([[cf], direct_mli1s, pc_standin_nodes, [target_pc]]):
        for cell in cell_type_group:
            cell_colors[cell] = layer_colors[i]

    ys = [multipartite_pos[node][1] for node in G_copy.nodes]
    xs = [multipartite_pos[node][0] for node in G_copy.nodes]
    maxy = max(ys)
    miny = min(ys)
    avgx = 0.5 * (max(xs) + min(xs)) # avgx is the midpoint of xs

    G_copy.add_nodes_from(['high_marker', 'low_marker'])
    RATIO = 2
    if squish:
        RATIO *= 3
    multipartite_pos['high_marker'], multipartite_pos['low_marker'] = (avgx, RATIO * maxy), (avgx, RATIO * miny)
    cell_colors['high_marker'], cell_colors['low_marker'] = 'white', 'white'
    sizes['high_marker'], sizes['low_marker'] = 10, 10
    
    alpha_list = []
    for cell in G_copy.nodes:
        if cell in direct_mli1s:
            alpha_list.append(0.4)
        else:
            alpha_list.append(0.8)
    
    # get the path to the Downloads directory
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # changes dict information into list format, using same order as graph nodes for consistency
    size_list = [sizes[neuron] for neuron in G_copy.nodes]
    cell_colors = [cell_colors[neuron] for neuron in G_copy.nodes]
    
    plt.text(1, 1, f'Max Size: {str(max_deg)} connections', fontsize = 8, ha = 'right', va = 'top', transform = plt.gca().transAxes)
    nx.draw(G = G_copy, pos = multipartite_pos, ax = ax, node_color = cell_colors, node_size = size_list, edge_color = 'white', alpha = alpha_list)
    title = f'{pc} CF Inhibition to {target_pc}'
    ax.set_title(title)
    if save:
        plt.savefig(os.path.join(downloads_path, title + '.png'), format='png')

if __name__ == '__main__':
    for pc in pc_list:
        draw_disinhibition_graph(pc, G, target_pc=pc_to_neighbor(pc), use_ephaptic=True, save = True)