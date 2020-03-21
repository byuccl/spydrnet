from spydrnet import ir
from copy import deepcopy, copy, error

'''provide the clone function for spydrnet.'''

def clone(element):
    '''
    Clone any netlist objects
    
    This function provides access to the various intermediate
    representation clone functions that are defined in their classes.
    '''
    return element.clone()