from spydrnet.ir import Element, FirstClassElement, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance,\
    Port, Cable
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.global_state.global_service import lookup
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_ports(obj, *args, **kwargs):
    """
    get_ports(obj, ...)

    Get ports *within* an object.

    Parameters
    ----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_ports(definition, ...)` would
        return all of the ports associated with the provided definition that match the additional criteria.
    patterns : str, Iterable - optional, positional or named, default: wildcard
        The search patterns. Patterns can be a single string or an Iterable collection of strings. Patterns can be
        absolute or they can contain wildcards or regular expressions. If `patterns` is not provided, then it defaults
        to a wildcard. Patterns are queried against the object property value stored under a specified key. Fast lookups
        are only attempted on absolute patterns that are not regular expressions and contain no wildcards.
    key : str, optional, default: ".NAME"
        This is the key that controls which value is being searched.
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
    ports : generator
        The ports associated with a particular object or collection of objects.
    
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_ports() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'key', 'filter', 'is_case', 'is_re'} for x in kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    filter_func = kwargs.get('filter', lambda x: True)
    is_case = kwargs.get('is_case', True)
    is_re = kwargs.get('is_re', False)
    patterns = args[0] if len(args) == 1 else kwargs.get('patterns', ".*" if is_re else "*")
    key = kwargs.get('key', ".NAME")

    if isinstance(obj, (FirstClassElement, InnerPin, OuterPin, Wire)) is False:
        try:
            object_collection = list(iter(obj))
        except TypeError:
            object_collection = [obj]
    else:
        object_collection = [obj]
    if all(isinstance(x, (Element, HRef)) for x in object_collection) is False:
        raise TypeError("get_ports() supports netlist elements and hierarchical references, or a collection of "
                        "these as the object searched")

    if isinstance(patterns, str):
        patterns = (patterns,)

    return _get_ports(object_collection, patterns, key, is_case, is_re, filter_func)


def _get_ports(object_collection, patterns, key, is_case, is_re, filter_func):
    for result in filter(filter_func, _get_ports_raw(object_collection, patterns, key, is_case, is_re)):
        yield result


def _get_ports_raw(object_collection, patterns, key, is_case, is_re):
    found = set()
    other_ports = set()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Definition):
            for pattern in patterns:
                pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
                if pattern_is_absolute:
                    result = lookup(obj, Port, key, pattern)
                    if result is not None and result not in found:
                        found.add(result)
                        yield result
                else:
                    for port in obj.ports:
                        value = port[key] if key in port else ''
                        if port not in found and _value_matches_pattern(value, pattern, is_case, is_re):
                            found.add(port)
                            yield port
        elif isinstance(obj, Netlist):
            for library in obj.libraries:
                for definition in library.definitions:
                    object_collection.append(definition)
        elif isinstance(obj, Library):
            object_collection += obj.definitions
        elif isinstance(obj, Instance):
            reference = obj.reference
            if reference:
                object_collection.append(reference)
        elif isinstance(obj, Port):
            other_ports.add(obj)
        elif isinstance(obj, InnerPin):
            port = obj.port
            if port:
                other_ports.add(port)
        elif isinstance(obj, OuterPin):
            inner_pin = obj.inner_pin
            if inner_pin:
                object_collection.append(inner_pin)
        elif isinstance(obj, Wire):
            object_collection += obj.pins
        elif isinstance(obj, Cable):
            object_collection += obj.wires
        elif isinstance(obj, HRef):
            if obj.is_valid:
                object_collection.append(obj.item)

    if other_ports:
        namemap = dict()
        for other_port in other_ports:
            if other_port in found:
                continue
            found.add(other_port)
            name = other_port[key] if key in other_port else ''
            if name not in namemap:
                namemap[name] = list()
            namemap[name].append(other_port)
        for pattern in patterns:
            pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
            if pattern_is_absolute:
                if pattern in namemap:
                    result = namemap[pattern]
                    del namemap[pattern]
                    for port in result:
                        yield port
            else:
                names_to_remove = list()
                for name in namemap:
                    if _value_matches_pattern(name, pattern, is_case, is_re):
                        result = namemap[name]
                        names_to_remove.append(name)
                        for port in result:
                            yield port
                for name in names_to_remove:
                    del namemap[name]
