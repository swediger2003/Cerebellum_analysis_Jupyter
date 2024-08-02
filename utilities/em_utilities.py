# https://numpy.org/doc/stable/
import numpy as np

# https://networkx.org/documentation/stable/index.html
import networkx as nx

from utilities.graph_utilities import *

from .defaults import default_G as G

pc_to_cf_dict = {
    'pc_2': 'cf_13', 
    'pc_3': 'cf_19', 
    'pc_9': 'cf_1', 
    'pc_16': 'cf_3', 
    'pc_22': 'cf_6', 
    'pc_23': 'cf_18', 
    'pc_26': 'cf_23', 
    'pc_32': 'cf_25',
    'pc_34': 'cf_21', 
    'pc_35': 'cf_17', 
    'pc_50': 'cf_2'
}

# given a dict of KEY:VAL, returns a dict of VAL:KEY. 
def invert_dict(dict):
    new_dict = {}
    for key, val in dict.items():
        new_dict[val] = key
    return new_dict

# turns a given purkinje cell into its associated climbing fiber
def pc_to_cf(pc):
    try:
        return pc_to_cf_dict[pc]
    except KeyError:
        raise Exception(f'{pc} does not have an associated climbing fiber.')

# turns a given climbing fiber into its associated purkinje cell
def cf_to_pc(cf):
    try:
        return invert_dict(pc_to_cf_dict)[cf]
    except KeyError:
        raise Exception(f'{cf} is not associated with a Purkinje cell.')
    
# given two coordinate points, return the distance between the two points in microns. 
def distance(point1, point2):
    diff_vector = point1 - point2
    pixel_to_micron = [[0.004, 0, 0], 
                       [0, 0.004, 0] ,
                       [0, 0,  0.04]]
    diff_vector = pixel_to_micron @ diff_vector
    return np.linalg.norm(diff_vector)

# projects vector a onto vector b. 
def project(a, b):
    norm_square = np.dot(b, b)
    scale_factor = np.dot(a, b) / norm_square
    projection = b * scale_factor
    return projection

def cell_type(neuron, G):
    return G.nodes[neuron]['cell_type']

# given a point and a list of 2 points that form a plane, compute the distance from the point to the plane. 
# since only two points are given, one of the points is projected down to z=0 and used as the origin from which the plane also passes through. 
def distance_to_plane(point, plane):
    # define the origin. This should be one of the original vectors projected down to z=0. 
    # translate all vectors relative to the origin by subtracting the origin. 
    # change the scale of all vectors into microns. 
    # remove the component of vector 1 from vector 2. 
    # compute the cross product of vector 1 and vector 2. 
    # normalize all vectors in the basis. 
    # compute the projection of the point vector onto the cross product: straight_line
    # compute the norm of the straight_line vector. this should complete the process. 
    
    plane_point1, plane_point2 = [np.array(vector) for vector in plane]
    point = np.array(point)
    
    project_down = [[1, 0, 0], 
                    [0, 1, 0], 
                    [0, 0, 0]]
    
    pixel_to_micron_scale = [[0.004, 0    , 0   ], 
                             [0    , 0.004, 0   ], 
                             [0    , 0    , 0.04]]
    
    # define the origin. This should be one of the original vectors projected down to z=0. 
    origin = project_down @ plane_point1
    
    # translate all vectors relative to the origin by subtracting the origin. 
    plane_point1, plane_point2, point = [vector - origin for vector in (plane_point1, plane_point2, point)]
    
    # convert all values to microns
    plane_point1, plane_point2, point = [pixel_to_micron_scale @ vector for vector in (plane_point1, plane_point2, point)]
        
    # remove the component of vector 1 from vector 2. 
    projection = project(plane_point1, plane_point2) # compute the component of plane_point2 in the direction of plane_point1. 
    plane_point2 = plane_point2 - projection # remove from plane_point2. 
    
    # plane_point1 and 2 are now orthogonal. Assure yourself that, up to rounding error, their dot product is zero. 
    # assert np.dot(plane_point1, plane_point2) < 0.00000001
    
    #create a third vector to use as a basis for the space
    cross_product = np.cross(plane_point1, plane_point2)   
        
    # normalize all vectors being used (which shouldn't be necessary but allows us to say we have an orthonormal basis)
        
    # check that the basis is orthonormal. 
    for vector in (plane_point1, plane_point2, cross_product):
        for other in (plane_point1, plane_point2, cross_product):
            if all(abs(vector - other) < 0.00000001):
                # assert np.dot(vector, other)  < 0.00000001
                # assert np.linalg.norm(vector) < 0.00000001
                pass
        
    # project the point vector onto the normal vector to the plane:
    projected = project(point, cross_product)
        
    # the distance from the point to the plane is equal to the norm of this projection.
    # return the norm of the component of the point that is normal to the given plane. 
    return np.linalg.norm(projected)

# This function takes an input of a single point and list of points. For all of the planes defined by point i, i+1 in the list, 
# the distance between point and the plane is calculated, in microns. Then, return the minimum distance of that list. 
def distance_from_planes(point, plane_point_list):
    minimum_discovered_distance = np.inf
    for i in range(0, len(plane_point_list) - 1):
        plane_point1, plane_point2 = plane_point_list[i], plane_point_list[i+1]
        # print(distance_to_plane(point, (plane_point1, plane_point2)))
        minimum_discovered_distance = min(minimum_discovered_distance, distance_to_plane(point, (plane_point1, plane_point2)))
    return minimum_discovered_distance

# the Purkinje Cell Layer is represented by planes defined by point i, i+1 in this list. This is around the bottom of the PCL. 
pcl_points = [[36591.30859, 99053.46094, 500],
              [58370.33594, 99943.27344, 500],
              [100273.0078, 97749.88281, 500],
              [156308.2813, 91476.78906, 500],
              [198027.4844, 83397.96875, 500],
              [210138.9531, 79896.3125 , 500] ]

def distance_from_pcl(point):
    return distance_from_planes(point, pcl_points)

def ephatptic_subgraph(G):
    return subgraph_by_edge_type(G, 'ephaptic')

pc_to_neighbor_dict = {
    'pc_2': 'pc_1', 
    'pc_9': 'pc_16', 
    'pc_16': 'pc_9', 
    'pc_22': 'pc_23', 
    'pc_23': 'pc_22', 
    'pc_26': 'pc_25', 
    'pc_32': 'pc_28',
    'pc_34': 'pc_35', 
    'pc_35': 'pc_34', 
    'pc_50': 'pc_3'
}

def pc_to_neighbor(pc):
    return pc_to_neighbor_dict[pc]

#returns a LIST of mli1 id's that corresponds to all MLI1s that are synapsed onto by a climbing fiber MLI2
def get_disynaptic_mli1s(pc, G):
    cf = pc_to_cf(pc)
    predecessors = [mli1 for mli1 in G.predecessors(pc) if cell_type(mli1, G = G) == 'MLI1']
    disynaptic_mli1s = [neuron for neuron in nx.dfs_tree(G, source = cf, depth_limit = 2) if neuron in predecessors]
    return disynaptic_mli1s

# list of MLI1s that receive contacts directly from a PC's associated CF
def get_monosynaptic_mli1s(pc, G):
    cf = pc_to_cf(pc)
    mli1s = successors_by_type(cf, G = G, neuron_type = 'MLI1')
    return mli1s

# list of MLI2s that receive contacts from a PC's associated CF
def get_cf_mli2s(pc, G):
    cf = pc_to_cf(pc)
    mli2s = successors_by_type(cf, G = G, neuron_type = 'MLI2')
    return mli2s

# Given a pc, generate its list of disynaptic MLI1s from its climbing fiber and return a list of edges that connect those MLI1s to the PC. 
def disynaptic_mli1_to_pc_edges(pc, G, data = True):
    mli1s = get_disynaptic_mli1s(pc, G = G)
    return all_edges_between_sets(mli1s, [pc], G = G, data = data)

# Given a pc, generate its list of monosynaptic MLI1s from its climbing fiber and return a list of edges that connect those MLI1s to the PC. 
def monosynaptic_mli1_to_pc_edges(pc, G, data = True):
    mli1s = get_monosynaptic_mli1s(pc, G = G)
    return all_edges_between_sets(mli1s, [pc], G = G, data = data)

# Given a list of pc, generate its list of disynaptic MLI2s and MLI1s from its climbing fiber and return a list of edges that connect those MLI2s to those MLI1s.
def climbing_fiber_mli2_to_mli1_edges(pc, G, data = True):
    cf = pc_to_cf(pc)
    mli2s = get_cf_mli2s
    mli1s = successors_from_list_by_type(mli2s, 'MLI1', G = G)
    return all_edges_between_sets(mli2s, mli1s, G = G, data = data)

def has_tag(edge, tag):
    try:
        return tag in edge[2]['tags'] or tag in edge[2].keys()
    except KeyError:
        return False

def is_ephaptic(edge):
    return has_tag(edge, 'ephaptic')