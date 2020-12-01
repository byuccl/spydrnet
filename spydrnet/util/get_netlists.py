from spydrnet.ir import Element, FirstClassElement, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Port, \
    Cable, Instance
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_netlists(obj, *args, **kwargs):
    """
    get_netlists(obj, ...)

    Get netlists *within* an object.
    
    Parameters
    ----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_libraries(netlist, ...)` would
        return all of the libraries associated with the provided netlist that match the additional criteria.
    
    patterns : str, Iterable - optional, positional or named, (default: wildcard)
        The search patterns. Patterns can be a single string or an Iterable collection of strings. Patterns can be
        absolute or they can contain wildcards or regular expressions. If `patterns` is not provided, then it defaults
        to a wildcard. Patterns are queried against the object property value stored under a specified key. Fast lookups
        are only attempted on absolute patterns that are not regular expressions and contain no wildcards.
    key : str, optional, (default: ".NAME")
        This is the key that controls which value is being searched.
    is_case : bool - optional, named, (default: True)
        Specify if patterns should be treated as case sensitive. Only applies to patterns. Does not alter fast lookup
        behavior (if namespace policy uses case insensitive indexing, this parameter will not prevent a fast lookup
        from returning a matching object even if the case is not an exact match).
    is_re: bool - optional, named, (default: False)
        Specify if patterns are regular expressions. If `False`, a pattern can still contain `*` and `?` wildcards. A
        `*` matches zero or more characters. A `?` matches upto a single character.
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all
        matching virtual instances are returned. Otherwise, virtual instances that cause the filter function to evaluate
        to true are the only items returned.
    
    Returns
    -------
    netlists : generator
        A generator associated with a particular object
    
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_netlists() got multiple values for argument 'patterns'")
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
        raise TypeError("get_netlists() supports netlist elements and hierarchical references or a collection of "
                        "theses as the object searched, unsupported object provided")

    if isinstance(patterns, str):
        patterns = (patterns,)

    return _get_netlists(object_collection, patterns, key, is_case, is_re, filter_func)


def _get_netlists(object_collection, patterns, key, is_case, is_re, filter_func):
    for result in filter(filter_func, _get_netlists_raw(object_collection, patterns, key, is_case, is_re)):
        yield result


def _get_netlists_raw(object_collection, patterns, key, is_case, is_re):
    found = set()
    namemap = dict()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Netlist):
            if obj not in found:
                found.add(obj)
                name = obj.get(key, None)
                if name not in namemap:
                    namemap[name] = list()
                namemap[name].append(obj)
        elif isinstance(obj, Library):
            netlist = obj.netlist
            if netlist:
                object_collection.append(netlist)
        elif isinstance(obj, Definition):
            library = obj.library
            if library:
                object_collection.append(library)
        elif isinstance(obj, Instance):
            reference = obj.reference
            if reference:
                object_collection.append(reference)
        elif isinstance(obj, Port):
            definition = obj.definition
            if definition:
                object_collection.append(definition)
        elif isinstance(obj, InnerPin):
            port = obj.port
            if port:
                object_collection.append(port)
        elif isinstance(obj, OuterPin):
            inner_pin = obj.inner_pin
            if inner_pin:
                object_collection.append(inner_pin)
        elif isinstance(obj, Cable):
            definition = obj.definition
            if definition:
                object_collection.append(definition)
        elif isinstance(obj, Wire):
            cable = obj.cable
            if cable:
                object_collection.append(cable)
        elif isinstance(obj, HRef):
            if obj.is_valid:
                item = obj.item
                if item:
                    object_collection.append(item)

    for pattern in patterns:
        pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
        if pattern_is_absolute:
            if pattern in namemap:
                result = namemap[pattern]
                for netlist in result:
                    if netlist in found:
                        found.remove(netlist)
                        yield netlist
        else:
            yielded = set()
            for netlist in found:
                value = netlist[key] if key in netlist else ''
                if _value_matches_pattern(value, pattern, is_case, is_re):
                    yielded.add(netlist)
                    yield netlist
            found -= yielded
