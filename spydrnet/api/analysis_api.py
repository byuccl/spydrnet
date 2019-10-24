"""
From the specification for version 1.0:

Analysis API calls:

* get_designs
* get_cells
* get_ports
* get_cables
* get_libraries
* get_properties

Of cells of instance of ...


These calls are collected/imported/defined here
"""

from spydrnet.ir import *
from itertools import chain
from spydrnet.global_environment_manager import GlobalEnvironmentManager

def get_envrionments(of=None):
    '''
    All designs that are created
    
    Parameters
    ----------
    of : object
        default is None if it is set to a sub-element of the design it will get the designs that contain the sub-element
        
    Returns
    -------
    list
        All designs that are created
    '''
    if(of == None):
        return GlobalEnvironmentManager.get_all_environments()
    else:
        print("of type not yet supported")
    pass

def get_definitions(of=None):
    '''
    Iterator on all definitions that are created
    
    Parameters
    ----------
    of : object
        default is None
        if it is set to a sub-element of the cell it will get the cells that contain the sub-element
        if it is set to a deisgn it will get the cells within the design
        
    Returns
    -------
    list
        All definitions that are created.
    '''
    if(of == None):
        definitions = None
        for env in GlobalEnvironmentManager.get_all_environments():
            if(definitions == None):
                definitions = env.children()
            else:
                definitions = chain(definitions, env.children())
            return definitions
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
            print("of type not yet supported")
            

def get_ports(of=None):
    '''
    All cells that are created
    
    Parameters
    ----------
    of : object
        default is None
        if it is set to a sub-element of the port it will get the ports that contain the sub-element
        if it is set to a deisgn, library or cell it will get the ports within the design, library or cell
        if it is set to a cable or cable sub-element it will get all the ports attached to the cable or sub-element
        
    Returns
    -------
    list
        All cells that are created
    '''

    if(of == None):
        ports = None
        for env in GlobalEnvironmentManager.get_all_environments():
            for library in env.children():
                for definition in library.children():
                    if ports == None:
                        ports = definition.ports
                    else:
                        ports = chain(ports, definition.ports)
        return ports
    elif type(of) == Environment:
        ports = None
        for library in of.children():
            for definition in library.children():
                if ports == None:
                    ports = definition.ports
                else:
                    ports = chain(ports, definition.ports)
        return ports

    elif type(of) == Definition:
        return of.ports

    elif type(of) == Library:
        ports = None
        for definition in of.children():
            if ports == None:
                ports = definition.ports
            else:
                ports = chain(ports, definition.ports)
        return ports

    else:
        print("of type not yet supported")

    

def get_cables(of=None):
    """
    Find all cells that are created
    
    Parameters
    ----------
    of : object
        default is None
        if it is set to a sub-element of the cable it will get the cables that contain the sub-element  
        if it is set to a design, library or cell it will get the cables within the design, library or cell  
        if it is set to a port or port sub-element it will get all the cables attacked to the port or sub-element
        
    Returns
    -------
    list
        All cells that are created
    """

    if(of == None):
        cables = None
        for env in GlobalEnvironmentManager.get_all_environments():
            for library in env.children():
                for definition in library.children():
                    if cables == None:
                        cables = definition.cables
                    else:
                        cables = chain(cables, definition.cables)
        return cables
    elif type(of) == Environment:
        cables = None
        for library in of.children():
            for definition in library.children():
                if cables == None:
                    cables = definition.cables
                else:
                    cables = chain(cables, definition.cables)
        return cables

    elif type(of) == Definition:
        return of.cables

    elif type(of) == Library:
        cables = None
        for definition in of.children():
            if cables == None:
                cables = definition.cables
            else:
                cables = chain(cables, definition.cables)
        return cables

    else:
        print("of type not yet supported")

    pass

def get_libraries(of=None):
    '''
    All cells that are created
    
    Parameters
    ----------
    of : object
        default is None
        if it is set to a sub-element of the port it will get the ports that contain the sub-element
        if it is set to a deisgn, library or cell it will get the ports within the design, library or cell
        if it is set to a cable or cable sub-element it will get all the ports attached to the cable or sub-element
        
    Returns
    -------
    list
        All cells that are created
    '''
    if(of == None):
        libraries = None
        for env in GlobalEnvironmentManager.get_all_environments():
            if libraries == None:
                libraries = env.children
            else:
                libraries = chain(libraries, env.children)
        return libraries
    else:
        print("of type not yet supported")

def get_properties(of):
    '''
    Get the properties of the object passed in
    
    Parameters
    ----------
    of : object
        no default
        must pass in a SpyDrNet IR element in order to get the properties.
        
    Returns
    -------
    list
        The properties of the object passed in
    '''
    return of.__getitem__("Properties")
