from spydrnet import Element, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_hwires(obj, *args, **kwargs):
    """
    get_hinstances(obj, ...)

    Get hierarchical references to wires of or *within* an object.

    Parameters:
    -----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection of objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_instances(netlist, ...) would
        return all of the instances *within* the provided definition that match the additional criteria.
    selection : Selection, INSIDE, OUTSIDE, BOTH, ALL, default: INSIDE
        This parameter determines the wires that are returned based on the instance associated with the object that is
        being searched.
    patterns : str, Iterable - optional, positional or named, default: wildcard
        The search patterns. Patterns can be a single string or an Iterable collection of strings. Patterns can be
        absolute or they can contain wildcards or regular expressions. If `patterns` is not provided, then it defaults
        to a wildcard.
    recursive : bool - optional, default: True
        Specify if search should be recursive or not meaning that sub hierarchical instances within an instance are
        included or not. This parameter only applies when the provided object is a netlist or a hierarchical reference
        to an instance
    is_case : bool - optional, named, default: True
        Specify if patterns should be treated as case sensitive. Only applies to patterns. Does not alter fast lookup
        behavior (if namespace policy uses case insensitive indexing, this parameter will not prevent a fast lookup
        from returning a matching object even if the case is not an exact match).
    is_re: bool - optional, named, default: False
        Specify if patterns are regular expressions. If `False`, a pattern can still contain `*` and `?` wildcards. A
        `*` matches zero or more characters. A `?` matches upto a single character.
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all
        matching virtual instances are returned. Otherwise, virtual instances that cause the filter function to evaluate
        to true are the only items returned.
    Returns hierarchical references to wires associated with a particular object or collection of objects.
    :return:
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_cables() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'recursive', 'filter', 'is_case', 'is_re'} for x in kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    filter_func = kwargs.get('filter', lambda x: True)
    recursive = kwargs.get('recursive', True)
    is_case = kwargs.get('is_case', True)
    is_re = kwargs.get('is_re', False)
    patterns = args[0] if len(args) == 1 else kwargs.get('patterns', ".*" if is_re else "*")

    if isinstance(obj, (Element, InnerPin, OuterPin, Wire)) is False:
        try:
            object_collection = list(iter(obj))
        except TypeError:
            object_collection = (obj,)
    else:
        object_collection = (obj,)
    if all(isinstance(x, Netlist) for x in object_collection) is False:
        raise TypeError("get_hinstances() only supports netlists or a collection of netlists as the object searched")

    if isinstance(patterns, str):
        patterns = (patterns,)

    return _get_instances(object_collection, patterns, recursive, is_case, is_re, filter_func)


def _get_instances(object_collection, patterns, recursive, is_case, is_re, filter_func):
    for result in filter(filter_func, _get_instances_raw(object_collection, patterns, recursive, is_case, is_re)):
        yield result


def _get_instances_raw(object_collection, patterns, recursive, is_case, is_re):
    namemap = _generate_namemap(object_collection, recursive)
    for pattern in patterns:
        pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
        if pattern_is_absolute:
            result = namemap[pattern]
            for href in result:
                yield href
        else:
            for name in namemap:
                if _value_matches_pattern(name, pattern, is_case, is_re):
                    result = namemap[name]
                    for item in result:
                        yield item


def _generate_namemap(object_collection, recursive):
    found = set()
    namemap = dict()
    top_instances = list()
    for obj in object_collection:
        if isinstance(obj, Netlist):
            top_instance = obj.top_instance
            if top_instance:
                href = HRef.from_parent_and_item(None, top_instance)
                top_instances.append(href)
    while top_instances:
        currently_recursive = True
        href = top_instances.pop()
        search_stack = [(href, False)]
        name_stack = list()
        while search_stack:
            href, visited = search_stack.pop()
            if visited:
                name_stack.pop()
            else:
                search_stack.append((href, True))
                name_stack.append(href.item.name if href.item.name else '')
                if len(name_stack) > 1:
                    hname = '/'.join(name_stack[1:])
                    if hname not in namemap:
                        namemap[hname] = list()
                    namemap[hname].append(href)
                if currently_recursive:
                    currently_recursive = recursive
                    item = href.item
                    reference = item.reference
                    if reference:
                        for child in reference.children:
                            href_child = HRef.from_parent_and_item(href, child)
                            if href_child not in found:
                                found.add(href_child)
                                search_stack.append((href_child, False))
    return namemap
