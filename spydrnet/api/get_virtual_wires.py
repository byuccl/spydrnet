import re
import fnmatch

from spydrnet.ir import Environment, Library, Definition, Port, InnerPin, OuterPin, Cable, Wire
from spydrnet.virtual_ir import VirtualInstance, VirtualPort, VirtualPin, VirtualCable, VirtualWire, hierarchical_seperator

from spydrnet.global_environment_manager import current_virtual_instance

from enum import Enum

class Selection(Enum):
    INSIDE = 1
    OUTSIDE = 2
    BOTH = 3
    ALL = 4

INSIDE = Selection.INSIDE
OUTSIDE = Selection.OUTSIDE
BOTH = Selection.BOTH
ALL = Selection.ALL

def get_virtual_wires(*args, **kwargs):
    """
    get_virtual_wires(...)

    Get virtual wires in the current netlist. By default, this function returns the virtual wires within the 
    `current_virtual_instance` (non-recursive), but it can be used to return any subset of virtual wires.

    Parameters
    ----------
    patterns : str, Iterable - optional, positional or named, default: wildcard
        The search patterns for virtual wires. Patterns target hierarchical names. Patterns can be a single string or an Iterable 
        collection of strings. Patterns can be absolute or they can contain wildcards or regular expressions. If `patterns` is not
        provided, then it defaults to a wildcard. This parameter cannot be used with `of`.
    hierarchical : bool - optional, named, default: False
        Specify if a non-regexp wildcard should match a hierarchical seperator. This parameter only applies to patterns that are not
        regular expressions. Regular expressions apply to all hierarchical virtual wires. This parameter cannot be use with `of`.
    is_case : bool - optional, named, default: True
        Specify if patterns should be treated as case sensitive. Only applies to patterns.
    is_re : bool - optional, named, default: False
        Specify if patterns are regular expressions. If `False`, a pattern can still contain `*` and `?` wildcards. A `*` matches zero
        or more characters. A `?` matches upto a single character. 
    of : Environment, Library, Definition, Instance, Port, InnerPin, OuterPin, Cable, Wire, VirtualInstance, VirtualPort, VirtualPin, \
    VirtualCable, VirtualWire, Iterable - optional, named
        Use this parameter when looking for virtual wires related to another object. This parameter cannot be used with `patterns`
        or `hierarchical`. Returned items have the following relationships with the objects passed in:

        - They are within an Environment
        - They are within a Library
        - They are within a Definition
        - They are `selection` the virtual instances of this Port
        - They are `selection` the virtual instances that instance this InnerPin
        - They are `selection` the virtual instances that instance this OuterPin
        - They are within this Cable
        - They are connected to this Wire
        - They are `selection` a VirtualInstance
        - They are `selection` the virtual instances that instance this VirtualPort
        - They are `selection` the virtual instances that instance this VirtualPin
        - They are within this VirtualCable
        - They are connected to this VirtualWire
    selection : INSIDE, OUTSIDE, BOTH, ALL - optional, named, default: OUTSIDE
        This parameter only applies when `of` is used with Instances, Ports, Pins, VirtualInstances, VirtualPorts, and VirtualPins. 
        This parameter determines if returned virtual wires are INSIDE or OUTSIDE in relation to the virtial instance of the `of` object.
        Selection can also be set to return BOTH the INSIDE and OUTSIDE virtual wire, or it can be set to return all wires that are connected
        to eachother (through hierarchy).
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all matching virtual
        instances are returned. Otherwise, virtual instances that cause the filter function to evaluate to true are the only items returned.
    
    Returns
    -------
    generator
        All virtual wires matching the query. Returned items are guarenteed to be unique.

    Examples
    --------
    Get all virtual wires (all connected wire segments) that are connected to a set of virtual pins.

    >>> connected_virtual_wires = list(get_virtual_instances(of=set_of_virtual_pins, selection=ALL)

    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_virtual_instances() got multiple values for arguement 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'of', 'hierarchical', 'filter', 'is_case', 'is_re', 'selection'} for x in kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")
    if 'of' in kwargs:
        if (len(args) == 1 or 'patterns' in kwargs):
            raise TypeError("Cannot use 'of' with 'patterns'.")
        elif 'hierarchical' in kwargs:
            raise TypeError("Cannot use 'of' with 'hierarchical'.")

    # Default values
    filter_func = kwargs.get('filter', lambda x: True)
    is_case = kwargs.get('is_case', True)
    is_re = kwargs.get('is_re', False)
    selection = kwargs.get('selection', OUTSIDE)
    
    if 'of' in kwargs:
        return _get_virtual_wires_of(kwargs['of'], selection=selection, filter_func=filter_func)
    else:
        # Additional default values
        hierarchical = kwargs.get('hierarchical', False)
        patterns = args[0] if len(args) == 1 else kwargs.get('patterns', ".*" if is_re else "*")
        return _get_virtual_wires_patterns(patterns, hierarchical=hierarchical, is_case=is_case, is_re=is_re, filter_func=filter_func)


def _get_virtual_wires_of(of, selection=OUTSIDE, filter_func=lambda x: True):
    pass

def _get_virtual_wires_patterns(patterns, hierarchical=False, is_case=True, is_re=False, filter_func=lambda x: True):
    pass