from spydrnet import Element, FirstClassElement, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance,\
    Port, Cable
from spydrnet.global_state.global_service import lookup
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern
from spydrnet.util.selection import Selection


def get_instances(obj, *args, **kwargs):
    """
    get_instances(obj, ...)

    Get instances *within* an object.

    Parameters
    ----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_instances(definition, ...)` would
        return all of the instances *within* the provided definition that match the additional criteria.
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
    selection : Selection.{INSIDE, OUTSIDE}, default: INSIDE
        This parameter determines the instances that are returned based on the definition or instance that is being
        searched. This parameter only applies to objects that are definitions. If the selection is "INSIDE" (default),
        then the function will return all of the instances that are inside the definition (i.e., the definition's
        children) that match the remainder of the search criteria. If the selection is "OUTSIDE", then the function will
        return all of the instances of the provided definition that match the remainder of the search criteria.
    recursive : bool - optional, default: False
        Specify if search should be recursive or not meaning that sub hierarchical instances within an instance are
        included or not.
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all
        matching virtual instances are returned. Otherwise, virtual instances that cause the filter function to evaluate
        to true are the only items returned.
    
    Returns
    -------
    cables : generator
        The cables associated with a particular object or collection of objects.
    
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_cables() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'key', 'filter', 'is_case', 'is_re', 'selection', 'recursive'} for x
                            in kwargs):
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

    if isinstance(obj, (FirstClassElement, InnerPin, OuterPin, Wire)) is False:
        try:
            object_collection = list(iter(obj))
        except TypeError:
            object_collection = [obj]
    else:
        object_collection = [obj]
    if all(isinstance(x, (Element, HRef)) for x in object_collection) is False:
        raise TypeError("get_instances() only supports netlists, libraries, and definitions, or a collection of these "
                        "as the object searched")

    if isinstance(patterns, str):
        patterns = (patterns,)

    return _get_instances(object_collection, patterns, key, is_case, is_re, selection, recursive, filter_func)


def _get_instances(object_collection, patterns, key, is_case, is_re, selection, recursive, filter_func):
    for result in filter(filter_func, _get_instances_raw(object_collection, patterns, key, is_case, is_re, selection,
                                                         recursive)):
        yield result


def _get_instances_raw(object_collection, patterns, key, is_case, is_re, selection, recursive):
    found = set()
    other_instances = list()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Definition):
            if selection == Selection.INSIDE:
                for pattern in patterns:
                    pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
                    if pattern_is_absolute:
                        result = lookup(obj, Instance, key, pattern)
                        if result is not None and result not in found:
                            found.add(result)
                            yield result
                    else:
                        for instance in obj.children:
                            if key in instance:
                                value = instance[key] if key in instance else ''
                                if _value_matches_pattern(value, pattern, is_case, is_re) and instance not in found:
                                    found.add(instance)
                                    yield instance
                if recursive:
                    for child in obj.children:
                        reference = child.reference
                        if reference and reference.is_leaf() is False:
                            object_collection.append(reference)
            else:
                other_instances += obj.references
                if recursive:
                    for instance in obj.references:
                        parent = instance.parent
                        if parent:
                            object_collection.append(parent)
                        else:
                            other_instances.append(instance)
        elif isinstance(obj, Netlist):
            for library in obj.libraries:
                object_collection += library.definitions
        elif isinstance(obj, Library):
            object_collection += obj.definitions
        elif isinstance(obj, Instance):
            if selection is Selection.INSIDE:
                reference = obj.reference
                if reference:
                    other_instances += reference.children
                    if recursive:
                        object_collection += reference.children
            else:
                parent = obj.parent
                if parent:
                    other_instances += parent.references
                    if recursive:
                        object_collection += parent.references
        elif isinstance(obj, (Port, Cable)):
            definition = obj.definition
            if definition:
                other_instances += definition.references
        elif isinstance(obj, InnerPin):
            port = obj.port
            if port:
                object_collection.append(port)
        elif isinstance(obj, OuterPin):
            instance = obj.instance
            if instance:
                other_instances.append(instance)
        elif isinstance(obj, Wire):
            cable = obj.cable
            if cable:
                object_collection.append(cable)
        elif isinstance(obj, HRef):
            if obj.is_valid:
                item = obj.item
                if isinstance(item, Instance):
                    other_instances.append(item)
                else:
                    object_collection.append(item)

    if other_instances:
        namemap = dict()
        for other_instance in other_instances:
            if other_instance in found:
                continue
            found.add(other_instance)
            name = other_instance[key] if key in other_instance else ''
            if name not in namemap:
                namemap[name] = list()
            namemap[name].append(other_instance)
        for pattern in patterns:
            pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
            if pattern_is_absolute:
                if pattern in namemap:
                    result = namemap[pattern]
                    for instance in result:
                        yield instance
            else:
                discard = set()
                for instance in found:
                    value = instance[key] if key in instance else ''
                    if _value_matches_pattern(value, pattern, is_case, is_re):
                        discard.add(instance)
                        yield instance
                found -= discard
