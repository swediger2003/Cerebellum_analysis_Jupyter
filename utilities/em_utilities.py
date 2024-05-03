pc_to_cf = {
    'pc_2': 'cf_13', # currently not in the contact list
    'pc_3': 'cf_19', # currently not in the contact list
    'pc_9': 'cf_1', 
    'pc_10': 'PC_10 CF PLACEHOLDER', # should have no use, as the CF for pc_10 is not being used for any analysis currently. 
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
    return pc_to_cf[pc]

# turns a given climbing fiber into its associated purkinje cell
def cf_to_pc(cf):
    return invert_dict