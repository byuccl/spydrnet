import re
import fnmatch

from spydrnet.ir import Environment, Library, Definition, Port, InnerPin, OuterPin, Cable, Wire
from spydrnet.virtual_ir import VirtualInstance, VirtualPort, VirtualPin, VirtualCable, VirtualWire, hierarchical_seperator

from spydrnet.global_environment_manager import current_virtual_instance

def get_virtual_instances(*args, **kwargs):
    """
    get_virtual_instances(...)
    
    Get virtual instances in the current netlist. By default, this function returns the virtual instances within the 
    `current_virtual_instance` (non-recursive), but it can be used to return any subset of virtual instances.

    Parameters
    ----------
    patterns : str, Iterable - optional, positional or named, default: wildcard
        The search patterns for virtual instances. Patterns target hierarchical names. Patterns can be a single string or an Iterable 
        collection of strings. Patterns can be absolute or they can contain wildcards or regular expressions. If `patterns` is not
        provided, then it defaults to a wildcard. This parameter cannot be used with `of`.
    hierarchical : bool - optional, named, default: False
        Specify if a non-regexp wildcard should match a hierarchical seperator. This parameter only applies to patterns that are not
        regular expressions. Regular expressions apply to all hierarchical virtual instances. This parameter cannot be use with `of`.
    is_case : bool - optional, named, default: True
        Specify if patterns should be treated as case sensitive. Only applies to patterns.
    is_re : bool - optional, named, default: False
        Specify if patterns are regular expressions. If `False`, a pattern can still contain `*` and `?` wildcards. A `*` matches zero
        or more characters. A `?` matches upto a single character. 
    of : Environment, Library, Definition, Instance, Port, InnerPin, OuterPin, Cable, Wire, VirtualInstance, VirtualPort, VirtualPin, \
    VirtualCable, VirtualWire, Iterable - optional, named
        Use this parameter when looking for virtual instances related to another object. This parameter cannot be used with `patterns`
        or `hierarchical`. Returned instances have the following relationships with the objects passed in:

        - All virtual instances within an Environment
        - All virtual instances within a Library
        - All virtual instances of a Definition
        - All virtual instances that instance this Port
        - All virtual instances that instance this InnerPin
        - All virutal instances that instance this OuterPin
        - All virtual instances connected to this Cable
        - All virtual instances connected to this Wire
        - All virtual instances within a VirtualInstance (hierarchical search)
        - All virtual instances that instance this VirtualPort
        - All virtual instances that instance this VirtualPin
        - All virtual instances that are connected to this VirtualCable
        - All virtual instances that are connected to this VirtualWire
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all matching virtual
        instances are returned. Otherwise, virtual instances that cause the filter function to evaluate to true are the only items returned.
    
    Returns
    -------
    generator
        All virtual instances matching the query. Returned items are guarenteed to be unique.

    Examples
    --------
    Get all virtual instances that are leafs (have no virtualChilren or virtualCables).

    >>> leafcells = list(get_virtual_instances(filter=lambda x: x.is_leaf()))

    """

    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_virtual_instances() got multiple values for arguement 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'of', 'hierarchical', 'filter', 'is_case', 'is_re'} for x in kwargs):
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

    if 'of' in kwargs:
        return _get_virtual_instances_of(kwargs['of'], filter_func=filter_func)
    else:
        # Additional default values
        hierarchical = kwargs.get('hierarchical', False)
        patterns = args[0] if len(args) == 1 else kwargs.get('patterns', ".*" if is_re else "*")
        return _get_virtual_instances_patterns(patterns, hierarchical=hierarchical, is_case=is_case, is_re=is_re, filter_func=filter_func)

def _get_virtual_instances_of(of, filter_func=lambda x: True):
    try:
        items = iter(of)
    except TypeError:
        items = iter((of,))
    
    found_virtual_instances = set()
    filter_func_plus_found = lambda x: filter_func(x) and x not in found_virtual_instances

    while items:
        next_items = list()
        for item in items:
            if isinstance(item, Environment): # All virtual instances within an Environment
                next_items += item.libraries
            elif isinstance(item, Library): # All virtual instances within a Library
                next_items += item.definitions
            elif isinstance(item, Definition): # All virtual instances of a Definition
                for vi in filter(filter_func_plus_found, item.virtual_instances):
                    found_virtual_instances.add(vi)
                    yield vi
            elif isinstance(item, Port): # All virtual instances that instance this Port
                next_items.append(item.definition)
            elif isinstance(item, InnerPin): # All virtual instances that instance this InnerPin
                next_items.append(item.port)
            elif isinstance(item, OuterPin): # All virutal instances that instance this OuterPin
                instance = item.instance
                parent = instance.parent_definition
                for vi in filter(filter_func_plus_found, (x.virtualChildren[instance] for x in parent.virtual_instances if instance in x.virtualChildren)):
                    found_virtual_instances.add(vi)
                    yield vi
            elif isinstance(item, Cable): # All virtual instances connected to this Cable
                next_items += item.wires
            elif isinstance(item, Wire): # All virtual instances connected to this Wire
                next_items += item.pins
            elif isinstance(item, VirtualInstance): # All virtual instances within a VirtualInstance (hierarchical search)
                next_items += item.virtualChildren
                for vi in filter(filter_func_plus_found, item.virtualChildren.values()):
                    found_virtual_instances.add(vi)
                    yield vi
            elif isinstance(item, VirtualPort): # All virtual instances that instance this VirtualPort
                if filter_func_plus_found(item.virtualParent):
                    found_virtual_instances.add(vi)
                    yield item.virtualParent
            elif isinstance(item, VirtualPin): # All virtual instances that instance this VirtualPin
                next_items.append(item.virtualParent)
            elif isinstance(item, VirtualCable): # All virtual instances that are connected to this VirtualCable
                next_items += item.virtualWires.values()
            elif isinstance(item, VirtualWire): # All virtual instances that are connected to this VirtualWire
                next_items += item.get_virtualPins()
        items = next_items

def _get_virtual_instances_patterns(patterns, hierarchical=False, is_case=True, is_re=False,  filter_func=lambda x: True):
    # create a name map, this is an expensive operation, more elegant branch and bounding options are available 
    namemap = dict()
    search_stack = list(map(lambda x: (x,False), current_virtual_instance().virtualChildren.values()))
    hierarchical_names = list()
    while search_stack:
        current_item = search_stack.pop()
        current_vi = current_item[0]
        visited = current_item[1]
        if visited:
            hierarchical_names.pop()
        else:
            search_stack.append((current_vi,True))
            hierarchical_names.append(current_vi.get_name())
            namemap[hierarchical_seperator.join(hierarchical_names)] = current_vi
            search_stack += map(lambda x: (x,False), current_vi.virtualChildren.values())

    if isinstance(patterns, str):
        patterns = iter((patterns,))
    else:
        patterns = iter(patterns)

    found_virtual_instances = set()
    filter_func_plus_found = lambda x: filter_func(x) and x not in found_virtual_instances

    for pattern in patterns:
        if pattern in namemap:
            vi = namemap[pattern]
            if filter_func_plus_found(vi):
                found_virtual_instances.add(vi)
                yield vi
        elif is_re or any(x in pattern for x in ["*", "?"]):
            if is_re:
                regex_pattern = re.compile(pattern, flags=0 if is_case else re.IGNORECASE)
                pattern_comparison = lambda name: regex_pattern.match(name)
            else:
                if is_case:
                    pattern_comparison_tmp = lambda name: fnmatch.fnmatchcase(name, pattern)
                else:
                    pattern_comparison_tmp = lambda name: fnmatch.fnmatch(name, pattern)
                if hierarchical:
                    hs_count = pattern.count(hierarchical_seperator)
                    pattern_comparison = lambda name: name.count(hierarchical_seperator) == hs_count and pattern_comparison_tmp(name)
                else:
                    pattern_comparison = pattern_comparison_tmp

            for name, vi in namemap.items():
                if pattern_comparison(name) and filter_func_plus_found(vi):
                    found_virtual_instances.add(vi)
                    yield vi