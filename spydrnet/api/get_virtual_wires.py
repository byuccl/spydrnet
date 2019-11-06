import re
import fnmatch

from spydrnet.ir import Environment, Library, Definition, Port, InnerPin, OuterPin, Cable, Wire
from spydrnet.virtual_ir import VirtualInstance, VirtualPort, VirtualPin, VirtualCable, VirtualWire, \
                                hierarchical_seperator, bus_format

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
    try:
        items = iter(of)
    except:
        items = iter((of,))

    found_virtual_wires = set()

    search_stack = list(items)
    while search_stack:
        item = search_stack.pop()
        if isinstance(item, Environment):
            selection = INSIDE
            search_stack += item.libraries
        elif isinstance(item, Library):
            selection = INSIDE
            search_stack += item.definitions
        elif isinstance(item, Definition):
            selection = INSIDE
            search_stack += item.virtual_instances
        elif isinstance(item, Port):
            search_stack += item.inner_pins
        elif isinstance(item, InnerPin):
            search_stack += item.get_virtualPins()
        elif isinstance(item, OuterPin):
            search_stack += item.get_virtualWires()
        elif isinstance(item, Cable):
            search_stack += item.wires
        elif isinstance(item, Wire):
            search_stack += item.get_virtualWires()
        elif isinstance(item, VirtualInstance):
            if selection in {INSIDE, BOTH}:
                for vc in item.virtualCables.values():
                    for vw in vc.virtualWires.values():
                        if vw not in found_virtual_wires:
                            found_virtual_wires.add(vw)
                            if filter_func(vw):
                                yield vw
            elif selection == ALL:
                search_stack += item.virtualCables.values()
            if selection in {OUTSIDE, BOTH, ALL}:
                search_stack += item.virtualPorts.values()
        elif isinstance(item, VirtualPort):
            search_stack += item.virtualPins.values()
        elif isinstance(item, VirtualPin):
            if selection in {INSIDE, BOTH, ALL}:
                inner_virtual_wire = item.get_inner_virtual_wire()
                if inner_virtual_wire and inner_virtual_wire not in found_virtual_wires:
                    found_virtual_wires.add(inner_virtual_wire)
                    if filter_func(inner_virtual_wire):
                        yield inner_virtual_wire
                    if selection == ALL:
                        search_stack += inner_virtual_wire.get_virtualPins()
            if selection in {OUTSIDE, BOTH, ALL}:
                outer_virtual_wire = item.get_outer_virtual_wire()
                if outer_virtual_wire and outer_virtual_wire not in found_virtual_wires:
                    found_virtual_wires.add(outer_virtual_wire)
                    if filter_func(outer_virtual_wire):
                        yield outer_virtual_wire
                    if selection == ALL:
                        search_stack += outer_virtual_wire.get_virtualPins()
        elif isinstance(item, VirtualCable):
            search_stack += item.virtualWires.values()
        elif isinstance(item, VirtualWire):
            if item not in found_virtual_wires:
                found_virtual_wires.add(item)
                if selection in {INSIDE, BOTH, ALL}:
                    if filter_func(item):
                        yield item
                if selection in {OUTSIDE, BOTH, ALL}:
                    for vp in item.get_virtualPins():
                        inner_vw = vp.get_inner_virtual_wire()
                        if inner_vw is not item:
                            if inner_vw and inner_vw not in found_virtual_wires:
                                found_virtual_wires.add(inner_vw)
                                if filter_func(inner_vw):
                                    yield inner_vw
                                if selection == ALL:
                                    search_stack += inner_vw.get_virtualPins()
                        else:
                            outer_vw = vp.get_outer_virtual_wire()
                            if outer_vw and outer_vw not in found_virtual_wires:
                                found_virtual_wires.add(outer_vw)
                                if filter_func(outer_vw):
                                    yield outer_vw
                                if selection == ALL:
                                    search_stack += outer_vw.get_virtualPins()

def _get_virtual_wires_patterns(patterns, hierarchical=False, is_case=True, is_re=False, filter_func=lambda x: True):
    # create a name map, this is an expensive operation, more elegant branch and bounding options are available 
    namemap = dict()
    search_stack = [(current_virtual_instance(), False)]
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
            for vc in current_vi.virtualCables.values():
                hierarchical_names.append(vc.get_name())
                if vc.cable.is_scalar:
                    for vw in vc.virtualWires.values():
                        name = hierarchical_seperator.join(hierarchical_names[1:])
                        namemap[name] = vw
                else:
                    for index, vw in enumerate((vc.virtualWires[x] for x in vc.cable.wires), vc.cable.lower_index):
                        name = hierarchical_seperator.join(hierarchical_names[1:]) + bus_format.format(index)
                        namemap[name] = vw
                hierarchical_names.pop()
            search_stack += map(lambda x: (x,False), current_vi.virtualChildren.values())

    if isinstance(patterns, str):
        patterns = iter((patterns,))
    else:
        patterns = iter(patterns)

    found_virtual_wires = set()
    filter_func_plus_found = lambda x: filter_func(x) and x not in found_virtual_wires

    for pattern in patterns:
        if pattern in namemap:
            vi = namemap[pattern]
            if filter_func_plus_found(vi):
                found_virtual_wires.add(vi)
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
                    pattern_comparison = pattern_comparison_tmp
                else:
                    hs_count = pattern.count(hierarchical_seperator)
                    pattern_comparison = lambda name: name.count(hierarchical_seperator) == hs_count and pattern_comparison_tmp(name)

            for name, vi in namemap.items():
                if pattern_comparison(name) and filter_func_plus_found(vi):
                    found_virtual_wires.add(vi)
                    yield vi