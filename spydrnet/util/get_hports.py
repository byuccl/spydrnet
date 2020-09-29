from spydrnet import FirstClassElement, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance, Port, Cable
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_hports(obj, *args, **kwargs):
    """
    get_hports(obj, ...)

    Get hierarchical references to ports *within* an object.

    Parameters
    ----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection of objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_instances(netlist, ...)` would
        return all of the instances *within* the provided definition that match the additional criteria.
    patterns : str, Iterable - optional, positional or named, default: wildcard
        The search patterns. Patterns can be a single string or an Iterable collection of strings. Patterns can be
        absolute or they can contain wildcards or regular expressions. If `patterns` is not provided, then it defaults
        to a wildcard.
    recursive : bool - optional, default: False
        Specify if search should be recursive or not meaning that sub hierarchical pins within an instance are
        included or not.
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
    
    Returns
    -------
    href_ports : generator
        The hierarchical references to ports associated with a particular object or collection of objects.
    
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_hports() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'recursive', 'filter', 'is_case', 'is_re'} for x in
                            kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    filter_func = kwargs.get('filter', lambda x: True)
    recursive = kwargs.get('recursive', False)
    is_case = kwargs.get('is_case', True)
    is_re = kwargs.get('is_re', False)
    patterns = args[0] if len(args) == 1 else kwargs.get('patterns', ".*" if is_re else "*")

    if isinstance(obj, (FirstClassElement, InnerPin, OuterPin, Wire)) is False:
        try:
            object_collection = list(iter(obj))
        except TypeError:
            object_collection = [obj]
    else:
        object_collection = [obj]
    if all(isinstance(x, (HRef, FirstClassElement, InnerPin, OuterPin, Wire)) for x in object_collection) is False:
        raise TypeError("get_hports() supports all netlist related objects and hierarchical references or a "
                        "collection of theses as the object searched, unsupported object provided")

    if isinstance(patterns, str):
        patterns = (patterns,)
    assert isinstance(patterns, (FirstClassElement, InnerPin, OuterPin, Wire)) is False

    return _get_hports(object_collection, patterns, recursive, is_case, is_re, filter_func)


def _get_hports(object_collection, patterns, recursive, is_case, is_re, filter_func):
    for result in filter(filter_func, _get_hports_raw(object_collection, patterns, recursive, is_case, is_re)):
        yield result


def _get_hports_raw(object_collection, patterns, recursive, is_case, is_re):
    in_namemap = set()
    in_yield = set()
    namemap = dict()
    bypass_namesearch = set()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Netlist):
            top_instance = obj.top_instance
            if top_instance:
                href = HRef.from_parent_and_item(None, top_instance)
                object_collection.append(href)
        elif isinstance(obj, HRef):
            if obj.is_valid is False:
                continue
            item = obj.item
            if isinstance(item, Instance):
                if obj not in bypass_namesearch:
                    _update_hport_namemap(obj, recursive, in_namemap, namemap)
                else:
                    bypass_namesearch.discard(obj)
                    reference = item.reference
                    if reference:
                        # Get all cables inside a hierarchical instance
                        for port in reference.ports:
                            hport = HRef.from_parent_and_item(obj, port)
                            if hport not in in_yield:
                                in_yield.add(hport)
                                yield(hport)
                        # get internal cables recursively
                        if recursive:
                            for child in reference.children:
                                href_child = HRef.from_parent_and_item(obj, child)
                                bypass_namesearch.add(href_child)
                                object_collection.append(href_child)
            elif isinstance(item, Port):
                if obj not in in_yield:
                    in_yield.add(obj)
                    yield (obj)
            elif isinstance(item, Cable):
                for wire in item.wires:
                    href_wire = HRef.from_parent_and_item(obj, wire)
                    object_collection.append(href_wire)
            elif isinstance(item, Wire):
                    href_parent_cable = obj.parent
                    href_parent_instance = href_parent_cable.parent
                    for pin in item.pins:
                        if isinstance(pin, OuterPin):
                            instance = pin.instance
                            if instance:
                                href_inst = HRef.from_parent_and_item(href_parent_instance, pin.instance)
                                inner_pin = pin.inner_pin
                                if inner_pin:
                                    inner_port = inner_pin.port
                                    if inner_port:
                                        href_port = HRef.from_parent_and_item(href_inst, inner_port)
                                        if href_port not in in_yield:
                                            in_yield.add(href_port)
                                            yield href_port
                        else:
                            port = pin.port
                            if port:
                                href_port = HRef.from_parent_and_item(href_parent_instance, port)
                                if href_port not in in_yield:
                                    in_yield.add(href_port)
                                    yield href_port
            elif isinstance(item, InnerPin):
                hport = obj.parent
                if hport not in in_yield:
                    in_yield.add(hport)
                    yield hport
        elif isinstance(obj, Library):
            object_collection += obj.definitions
        elif isinstance(obj, Definition):
            hrefs = set(HRef.get_all_hrefs_of_instances(obj.references))
            bypass_namesearch |= hrefs
            object_collection += hrefs
        elif isinstance(obj, Instance):
            hrefs = set(HRef.get_all_hrefs_of_instances(obj))
            bypass_namesearch |= hrefs
            object_collection += hrefs
        elif isinstance(obj, (Port, Cable, InnerPin, OuterPin, Wire)):
            object_collection += HRef.get_all_hrefs_of_item(obj)

    for href in in_yield:
        in_namemap.discard(href)

    if in_namemap:  # namemap is to cable
        for pattern in patterns:
            pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
            if pattern_is_absolute:
                if pattern in namemap:
                    result = namemap[pattern]
                    for href in result:
                        if href in in_namemap:
                            in_namemap.remove(href)
                            yield href
            else:
                for name in namemap:
                    if _value_matches_pattern(name, pattern, is_case, is_re):
                        result = namemap[name]
                        for href in result:
                            if href in in_namemap:
                                in_namemap.remove(href)
                                yield href


def _update_hport_namemap(href_instance, recursive, found, namemap):
    search_stack = [(href_instance, False)]
    name_stack = list()
    while search_stack:
        href_instance, visited = search_stack.pop()
        if visited:
            name_stack.pop()
        else:
            search_stack.append((href_instance, True))
            name_stack.append(href_instance.item.name if href_instance.item.name else '')
            item = href_instance.item
            reference = item.reference
            if reference:
                for port in reference.ports:
                    hport = HRef.from_parent_and_item(href_instance, port)
                    name_stack.append(port.name if port.name else '')
                    port_hname = '/'.join(name_stack[1:])
                    if hport not in found:
                        found.add(hport)
                        if port_hname not in namemap:
                            namemap[port_hname] = list()
                        namemap[port_hname].append(hport)
                    name_stack.pop()
                if recursive:
                    for child in reference.children:
                        if child.reference:
                            href_child = HRef.from_parent_and_item(href_instance, child)
                            search_stack.append((href_child, False))
