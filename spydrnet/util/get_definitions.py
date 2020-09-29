from spydrnet.ir import InnerPin, OuterPin, Wire, Netlist, Library, Definition, Element, Instance,\
    Port, Cable
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.selection import Selection
from spydrnet.global_state.global_service import lookup
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_definitions(obj, *args, **kwargs):
    """
    get_definitions(obj, ...)

    Get definitions *within* an object.

    Parameters
    ----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_definitions(library, ...)` would
        return all of the definitions associated with the provided library that match the additional criteria.
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
    recursive : bool - optional, default: False
        Specify if search should be recursive or not meaning that sub hierarchical instances within an instance are
        included or not.
    selection : Selection.{INSIDE, OUTSIDE}, default: INSIDE
        This parameter determines the instances that are returned based on the definition that is being searched. This
        parameter only applies to objects that are definitions. If the selection is "INSIDE" (default), then the
        function will return all of the instances that are inside the definition (i.e., the definition's children) that
        match the remainder of the search criteria. If the selection is "OUTSIDE", then the function will return all of
        the instances of the provided definition that match the remainder of the search criteria.
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all
        matching virtual instances are returned. Otherwise, virtual instances that cause the filter function to evaluate
        to true are the only items returned.
    
    Returns
    -------
    definitions : generator
        The definitions associated with a particular object or collection of objects.
    
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_definitions() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'key', 'filter', 'is_case', 'is_re', 'selection', 'recursive'}
                            for x in kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    selection = kwargs.get('selection', Selection.INSIDE)
    if isinstance(selection, str):
        if selection in Selection.__members__:
            selection = Selection[selection]
    if selection not in {Selection.INSIDE, Selection.OUTSIDE}:
        raise TypeError("selection must be '{}'".format("', '".join([Selection.INSIDE.name, Selection.OUTSIDE.name])))

    filter_func = kwargs.get('filter', lambda x: True)
    is_case = kwargs.get('is_case', True)
    is_re = kwargs.get('is_re', False)
    patterns = args[0] if len(args) == 1 else kwargs.get('patterns', ".*" if is_re else "*")
    key = kwargs.get('key', ".NAME")
    recursive = kwargs.get('recursive', False)

    if isinstance(obj, (Element, HRef)) is False:
        try:
            object_collection = list(iter(obj))
        except TypeError:
            object_collection = [obj]
    else:
        object_collection = [obj]
    if all(isinstance(x, (Element, HRef)) for x in object_collection) is False:
        raise TypeError("get_definitions() only supports netlists and libraries or a collection of them as the object "
                        "searched")

    if isinstance(patterns, str):
        patterns = (patterns,)

    return _get_definitions(object_collection, patterns, key, is_case, is_re, selection, recursive, filter_func)


def _get_definitions(object_collection, patterns, key, is_case, is_re, selection, recursive, filter_func):
    for result in filter(filter_func, _get_definitions_raw(object_collection, patterns, key, is_case, is_re,
                                                           selection, recursive)):
        yield result


def _get_definitions_raw(object_collection, patterns, key, is_case, is_re, selection, recursive):
    found = set()
    other_definitions = set()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Library):
            if selection == Selection.INSIDE:
                for pattern in patterns:
                    pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
                    if pattern_is_absolute:
                        result = lookup(obj, Definition, key, pattern)
                        if result is not None and result not in found:
                            found.add(result)
                            yield result
                    else:
                        for definition in obj.definitions:
                            value = definition[key] if key in definition else ''
                            if definition not in found and _value_matches_pattern(value, pattern, is_case, is_re):
                                found.add(definition)
                                yield definition
                if recursive:
                    object_collection += obj.definitions
            else:
                object_collection += obj.definitions
        elif isinstance(obj, Netlist):
            object_collection += obj.libraries
        elif isinstance(obj, Definition):
            if selection == Selection.INSIDE:
                for child in obj.children:
                    reference = child.reference
                    if reference:
                        if reference not in other_definitions:
                            other_definitions.add(reference)
                            if recursive:
                                object_collection.append(reference)
            else:
                for definition in obj.references:
                    parent = definition.parent
                    if parent:
                        if parent not in other_definitions:
                            other_definitions.add(parent)
                            if recursive:
                                object_collection.append(parent)
        elif isinstance(obj, Instance):
            if selection == Selection.INSIDE:
                reference = obj.reference
                if reference:
                    if reference not in other_definitions:
                        other_definitions.add(reference)
                        if recursive:
                            object_collection += reference.children
            else:
                parent = obj.parent
                if parent:
                    if parent not in other_definitions:
                        other_definitions.add(parent)
                        if recursive:
                            object_collection.append(parent)
        elif isinstance(obj, (Port, Cable)):
            definition = obj.definition
            if definition:
                if definition not in other_definitions:
                    other_definitions.add(definition)
        elif isinstance(obj, InnerPin):
            definition = obj.port
            if definition:
                object_collection.append(definition)
        elif isinstance(obj, OuterPin):
            definition = obj.instance
            if definition:
                object_collection.append(definition)
        elif isinstance(obj, Wire):
            cable = obj.cable
            if cable:
                object_collection.append(cable)
        elif isinstance(obj, HRef):
            if obj.is_valid:
                object_collection.append(obj.item)

    if other_definitions:
        namemap = dict()
        for other_definition in other_definitions:
            if other_definition in found:
                continue
            found.add(other_definition)
            name = other_definition[key] if key in other_definition else ''
            if name not in namemap:
                namemap[name] = list()
            namemap[name].append(other_definition)
        for pattern in patterns:
            pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
            if pattern_is_absolute:
                if pattern in namemap:
                    result = namemap[pattern]
                    for definition in result:
                        yield definition
            else:
                names_to_remove = list()
                for name in namemap:
                    if _value_matches_pattern(name, pattern, is_case, is_re):
                        result = namemap[name]
                        names_to_remove.append(name)
                        for definition in result:
                            yield definition
                for name in names_to_remove:
                    del namemap[name]
