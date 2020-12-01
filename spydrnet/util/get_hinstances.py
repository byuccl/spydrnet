from spydrnet import FirstClassElement, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance, Port, Cable
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_hinstances(obj, *args, **kwargs):
    """
    get_hinstances(obj, ...)

    Get hierarchical references to instances *within* an object.

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
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all
        matching virtual instances are returned. Otherwise, virtual instances that cause the filter function to evaluate
        to true are the only items returned.
    
    Returns
    -------
    href_instances : generator
        The hierarchical references to instances associated with a particular object or collection of objects.
    
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_hinstances() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'recursive', 'filter', 'is_case', 'is_re'} for x in kwargs):
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
        raise TypeError("get_hinstances() supports all netlist related objects and hierarchical references or a "
                        "collection of theses as the object searched, unsupported object provided")

    if isinstance(patterns, str):
        patterns = (patterns,)
    assert isinstance(patterns, (FirstClassElement, InnerPin, OuterPin, Wire)) is False

    return _get_instances(object_collection, patterns, recursive, is_case, is_re, filter_func)


def _get_instances(object_collection, patterns, recursive, is_case, is_re, filter_func):
    for result in filter(filter_func, _get_instances_raw(object_collection, patterns, recursive, is_case, is_re)):
        yield result


def _get_instances_raw(object_collection, patterns, recursive, is_case, is_re):
    in_namemap = set()
    in_yield = set()
    namemap = dict()
    instance_search = set()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Netlist):
            top_instance = obj.top_instance
            if top_instance:
                href = HRef.from_parent_and_item(None, top_instance)
                _update_namemap(href, recursive, in_namemap, namemap)
        elif isinstance(obj, HRef):
            if obj.is_valid is False:
                continue
            item = obj.item
            if isinstance(item, Instance):
                _update_namemap(obj, recursive, in_namemap, namemap)
            elif isinstance(item, (Port, Cable)):
                hinstance = obj.parent
                if hinstance and hinstance not in in_yield:
                    in_yield.add(hinstance)
                    yield hinstance
            elif isinstance(item, (InnerPin, Wire)):
                hcable_or_hport = obj.parent
                if hcable_or_hport:
                    hinstance = hcable_or_hport.parent
                    if hinstance and hinstance not in in_yield:
                        in_yield.add(hinstance)
                        yield hinstance
        elif isinstance(obj, Library):
            object_collection += obj.definitions
        elif isinstance(obj, Definition):
            instance_search |= obj.references
        elif isinstance(obj, Instance):
            instance_search.add(obj)
        elif isinstance(obj, (Port, Cable)):
            definition = obj.definition
            if definition:
                object_collection.append(definition)
        elif isinstance(obj, InnerPin):
            port = obj.port
            if port:
                definition = port.definition
                if definition:
                    object_collection.append(definition)
        elif isinstance(obj, OuterPin):
            instance = obj.instance
            if instance:
                instance_search.add(instance)
        elif isinstance(obj, Wire):
            cable = obj.cable
            if cable:
                definition = cable.definition
                if definition:
                    object_collection.append(definition)

    if instance_search:
        for href in HRef.get_all_hrefs_of_instances(instance_search):
            if href not in in_yield:
                in_yield.add(href)
                yield href

    for href in in_yield:
        in_namemap.discard(href)

    if in_namemap:
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


def _update_namemap(href, recursive, found, namemap):
    currently_recursive = True
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
