from spydrnet.ir import InnerPin, OuterPin, Wire, Netlist, Library, Definition, Cable, Element,\
    Instance, Port
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.selection import Selection
from spydrnet.global_state.global_service import lookup
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_cables(obj, *args, **kwargs):
    """
    get_cables(obj, ...)

    Get cables *within* an object.

    Parameters
    ----------    
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_cables(definition, ...)` would
        return all of the cables associated with the provided definition that match the additional criteria.
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
    selection : Selection.{INSIDE, OUTSIDE, BOTH, ALL}, default: INSIDE
        This parameter determines the wires that are returned based on the instance associated with the object that is
        being searched.
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
    if len(args) > 1 or any(x not in {'patterns', 'key', 'filter', 'is_case', 'is_re', 'selection', 'recursive'}
                            for x in kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    selection = kwargs.get('selection', Selection.INSIDE)
    if isinstance(selection, str):
        if selection in Selection.__members__:
            selection = Selection[selection]
    if isinstance(selection, Selection) is False:
        raise TypeError("selection must be '{}'".format("', '".join(Selection.__members__.keys())))

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
        raise TypeError("get_cables() only supports netlists, libraries, and definitions, or a collection of these as "
                        "the object searched")

    if isinstance(patterns, str):
        patterns = (patterns,)

    return _get_cables(object_collection, patterns, key, is_case, is_re, selection, recursive, filter_func)


def _get_cables(object_collection, patterns, key, is_case, is_re, selection, recursive, filter_func):
    for result in filter(filter_func, _get_cables_raw(object_collection, patterns, key, is_case, is_re, selection,
                                                      recursive)):
        yield result


def _get_cables_raw(object_collection, patterns, key, is_case, is_re, selection, recursive):
    found = set()
    other_cables = set()
    searched_wires = set()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Definition):
            if selection in {Selection.INSIDE, Selection.ALL}:
                for pattern in patterns:
                    pattern_is_absolute = _is_pattern_absolute(pattern, is_case, is_re)
                    if pattern_is_absolute:
                        result = lookup(obj, Cable, key, pattern)
                        if result is not None and result not in found:
                            found.add(result)
                            yield result
                    else:
                        for cable in obj.cables:
                            value = cable[key] if key in cable else ''
                            if cable not in found and _value_matches_pattern(value, pattern, is_case, is_re):
                                found.add(cable)
                                yield cable
                if recursive or selection == Selection.ALL:
                    object_collection += obj.children
            if selection in {Selection.OUTSIDE, Selection.BOTH, Selection.ALL}:
                for port in obj.ports:
                    for pin in port.pins:
                        object_collection.append(pin)
        elif isinstance(obj, Library):
            object_collection += obj.definitions
        elif isinstance(obj, Netlist):
            for library in obj.libraries:
                object_collection += library.definitions
        elif isinstance(obj, Instance):
            if selection in {Selection.INSIDE, Selection.ALL}:
                reference = obj.reference
                if reference:
                    for cable in reference.cables:
                        other_cables.add(cable)
                    if recursive or selection == Selection.ALL:
                        object_collection += reference.children
            if selection in {Selection.BOTH, Selection.OUTSIDE, Selection.ALL}:
                object_collection += obj.pins
        elif isinstance(obj, InnerPin):
            if selection in {Selection.INSIDE, Selection.BOTH, Selection.ALL}:
                wire = obj.wire
                if wire and wire not in searched_wires:
                    searched_wires.add(wire)
                    cable = wire.cable
                    if cable:
                        other_cables.add(cable)
                    if selection == Selection.ALL:
                        object_collection += wire.pins
            if selection in {Selection.OUTSIDE, Selection.BOTH, Selection.ALL}:
                port = obj.port
                if port:
                    definition = port.definition
                    if definition:
                        for instance in definition.references:
                            outer_pin = instance.pins[obj]
                            outer_wire = outer_pin.wire
                            if outer_wire and outer_wire not in searched_wires:
                                searched_wires.add(outer_wire)
                                cable = outer_wire.cable
                                if cable:
                                    other_cables.add(cable)
                                if selection == Selection.ALL:
                                    object_collection += outer_wire.pins
        elif isinstance(obj, OuterPin):
            if selection in {Selection.INSIDE, Selection.BOTH, Selection.ALL}:
                inner_pin = obj.inner_pin
                if inner_pin:
                    inner_wire = inner_pin.wire
                    if inner_wire and inner_wire not in searched_wires:
                        searched_wires.add(inner_wire)
                        cable = inner_wire.cable
                        if cable:
                            other_cables.add(cable)
                        if selection == Selection.ALL:
                            object_collection += inner_wire.pins
            if selection in {Selection.OUTSIDE, Selection.BOTH, Selection.ALL}:
                wire = obj.wire
                if wire and wire not in searched_wires:
                    searched_wires.add(wire)
                    cable = wire.cable
                    if cable:
                        other_cables.add(cable)
                    if selection == Selection.ALL:
                        object_collection += wire.pins
        elif isinstance(obj, Port):
            object_collection += obj.pins
        elif isinstance(obj, Wire):
            if selection == Selection.INSIDE:
                cable = obj.cable
                if cable:
                    other_cables.add(cable)
            elif selection == Selection.OUTSIDE:
                for pin in obj.pins:
                    if isinstance(pin, OuterPin):
                        inner_pin = pin.inner_pin
                        inner_wire = inner_pin.wire
                        if inner_wire:
                            cable = inner_wire.cable
                            if cable:
                                other_cables.add(cable)
                    else:
                        object_collection.append(pin)
            else:
                object_collection += obj.pins
        elif isinstance(obj, Cable):
            if selection == Selection.INSIDE:
                other_cables.add(obj)
            else:
                object_collection += obj.wires
        elif isinstance(obj, HRef):
            if obj.is_valid:
                object_collection.append(obj.item)

    if other_cables:
        namemap = dict()
        for other_cable in other_cables:
            if other_cable not in found:
                found.add(other_cable)
                name = other_cable[key] if key in other_cable else ''
                if name not in namemap:
                    namemap[name] = list()
                namemap[name].append(other_cable)
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
