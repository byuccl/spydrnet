from spydrnet import ir
from copy import deepcopy, copy, error

'''provide the clone function for spydrnet.'''

def clone(element):
    '''
    Clone any netlist objects
    see the individaul class .clone methods for more information on what happens when you clone
    '''
    return element.clone()