"""
From the specification for version 1.0:

Analysis API calls:
get_designs
get_cells
get_ports
get_cables
get_libraries
get_properties

Of cells of instance of ...


These calls are collected/imported/defined here
"""

from spydrnet.ir import *
from itertools import chain
from spydrnet.global_manager import global_manager

def get_designs(of=None):
    '''
    return all designs that are created
    parameters:
    - of - default is None if it is set to a sub-element of the design it will get the designs that contain the sub-element
    '''
    if(of == None):
        pass
    else:
        pass
    pass

def get_definitions(of=None):
    '''
    return iterator on all definitions that are created
    parameters:
    --of
        default is None
        if it is set to a sub-element of the cell it will get the cells that contain the sub-element
        if it is set to a deisgn it will get the cells within the design
    '''
    if(of == None):
        pass
    else:
        if type(of) == Library:
            #type is iterator
            return of.children()
        elif type(of) == Environment:
            definitions = None
            for i in of.children():
                if(definitions == None):
                    definitions = i.children()
                else:
                    definitions = chain(definitions, i.children())
            #type is iterator
            return definitions
        else:
            pass
    pass

def get_ports(of=None):
    '''
    return all cells that are created
    parameters:
    --of
        default is None
        if it is set to a sub-element of the port it will get the ports that contain the sub-element
        if it is set to a deisgn, library or cell it will get the ports within the design, library or cell
        if it is set to a cable or cable sub-element it will get all the ports attached to the cable or sub-element
    '''

    pass

def get_cables(of=None):
    '''
    return all cells that are created
    parameters:
    --of
        default is None
        if it is set to a sub-element of the cable it will get the cables that contain the sub-element
        if it is set to a deisgn, library or cell it will get the cables within the design, library or cell
        if it is set to a port or port sub-element it will get all the cables attacked to the port or sub-element
    '''

    pass

def get_libraries(of=None):
    '''
    return all cells that are created
    parameters:
    --of
        default is None
        if it is set to a sub-element of the library it will get the libraries that contain the sub-element
        if it is set to a deisgn it will get the libraries within the design
    '''

    pass

def get_properties(of):
    '''
    Return the properties of the object passed in
    parameters:
    --of
        no default
        must pass in a SpyDrNet IR element in order to get the properties.
    '''

    pass
