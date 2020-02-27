from spydrnet import Element, InnerPin, OuterPin, Wire, Netlist, Library
from spydrnet.global_state.global_service import lookup
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_libraries(obj, *args, **kwargs):
    """
    get_libraries(obj, ...)

    Get libraries *within* an object.

    Parameters:
    -----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_libraries(netlist, ...) would
        return all of the libraries associated with the provided netlist that match the additional criteria.
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
    Returns the libraries associated with a particular object
    :param obj:
    :param value:
    :param key:
    :return:
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_libraries() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'key', 'filter', 'is_case', 'is_re'} for x in kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    filter_func = kwargs.get('filter', lambda x: True)
    is_case = kwargs.get('is_case', True)
    is_re = kwargs.get('is_re', False)
    patterns = args[0] if len(args) == 1 else kwargs.get('patterns', ".*" if is_re else "*")
    key = kwargs.get('key', ".NAME")

    if isinstance(obj, (Element, InnerPin, OuterPin, Wire)) is False:
        netlist_collection = list(iter(obj))
        if all(isinstance(x, Netlist) for x in netlist_collection) is False:
            raise ValueError(
                "get_libraries() only supports netlists or a collection of netlists as the object searched")
    else:
        if isinstance(obj, Netlist) is False:
            raise ValueError(
                "get_libraries() only supports netlists or a collection of netlists as the object searched")
        netlist_collection = (obj,)

    if isinstance(patterns, str):
        patterns = (patterns,)

    return _get_libraries(netlist_collection, patterns, key, is_case, is_re, filter_func)


def _get_libraries(netlist_collection, patterns, key, is_case, is_re, filter_func):
    unique_results = set()
    for result in filter(filter_func, _get_libraries_raw(netlist_collection, patterns, key, is_case, is_re)):
        if result not in unique_results:
            unique_results.add(result)
            yield result


def _get_libraries_raw(netlists, patterns, key, is_case, is_re):
    for pattern in patterns:
        pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
        for netlist in netlists:
            if pattern_is_absolute:
                result = lookup(netlist, Library, key, pattern)
                if result is not None:
                    yield result
            else:
                for library in netlist.libraries:
                    if key in library:
                        value = library[key]
                        if _value_matches_pattern(value, pattern, is_case, is_re):
                            yield library