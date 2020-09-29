from spydrnet import FirstClassElement, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance, Port, Cable
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.selection import Selection
from spydrnet.util.patterns import _is_pattern_absolute, _value_matches_pattern


def get_hwires(obj, *args, **kwargs):
    """
    get_hwires(obj, ...)

    Get hierarchical references to wires *within* an object.

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
    selection : Selection.{INSIDE, OUTSIDE, BOTH, ALL}, default: INSIDE
        This parameter determines the wires that are returned based on the instance associated with the object that is
        being searched.
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all
        matching virtual instances are returned. Otherwise, virtual instances that cause the filter function to evaluate
        to true are the only items returned.
    
    Returns
    -------
    href_wires : generator
        The hierarchical references to wires associated with a particular object or collection of objects.
    
    """
    # Check argument list
    if len(args) == 1 and 'patterns' in kwargs:
        raise TypeError("get_hwires() got multiple values for argument 'patterns'")
    if len(args) > 1 or any(x not in {'patterns', 'selection', 'recursive', 'filter', 'is_case', 'is_re'} for x in
                            kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    selection = kwargs.get('selection', Selection.INSIDE)
    if isinstance(selection, str):
        if selection in Selection.__members__:
            selection = Selection[selection]
    if isinstance(selection, Selection) is False:
        raise TypeError("selection must be '{}'".format("', '".join(Selection.__members__.keys())))

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
        raise TypeError("get_hwires() supports all netlist related objects and hierarchical references or a "
                        "collection of theses as the object searched, unsupported object provided")

    if isinstance(patterns, str):
        patterns = (patterns,)
    assert isinstance(patterns, (FirstClassElement, InnerPin, OuterPin, Wire)) is False

    return _get_hwires(object_collection, selection, patterns, recursive, is_case, is_re, filter_func)


def _get_hwires(object_collection, selection, patterns, recursive, is_case, is_re, filter_func):
    for result in filter(filter_func, _get_hwires_raw(object_collection, selection, patterns, recursive, is_case, is_re)):
        yield result


def _get_hwires_raw(object_collection, selection, patterns, recursive, is_case, is_re):
    in_namemap = set()
    in_yield = set()
    namemap = dict()
    hpin_search = set()
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
                if selection == Selection.INSIDE and obj not in bypass_namesearch:
                    _update_hwire_namemap(obj, recursive, in_namemap, namemap)
                else:
                    bypass_namesearch.discard(obj)
                    reference = item.reference
                    if reference:
                        if selection in {Selection.INSIDE, Selection.ALL}:
                            # Get all cables inside a hierarchical instance
                            for cable in reference.cables:
                                hcable = HRef.from_parent_and_item(obj, cable)
                                for wire in cable.wires:
                                    hwire = HRef.from_parent_and_item(hcable, wire)
                                    if hwire not in in_yield:
                                        in_yield.add(hwire)
                                        yield(hwire)
                            # get internal cables recursively
                            if recursive or selection == Selection.ALL:
                                for child in reference.children:
                                    href_child = HRef.from_parent_and_item(obj, child)
                                    bypass_namesearch.add(href_child)
                                    object_collection.append(href_child)
                        if selection in {Selection.OUTSIDE, Selection.BOTH, Selection.ALL}:
                            for port in reference.ports:
                                href_port = HRef.from_parent_and_item(obj, port)
                                for pin in port.pins:
                                    href_pin = HRef.from_parent_and_item(href_port, pin)
                                    hpin_search.add(href_pin)
            elif isinstance(item, Port):
                for pin in item.pins:
                    href_pin = HRef.from_parent_and_item(obj, pin)
                    hpin_search.add(href_pin)
            elif isinstance(item, Cable):
                for wire in item.wires:
                    href_wire = HRef.from_parent_and_item(obj, wire)
                    object_collection.append(href_wire)
            elif isinstance(item, Wire):
                if selection == Selection.INSIDE:
                    if obj not in in_yield:
                        in_yield.add(obj)
                        yield obj
                elif selection == Selection.OUTSIDE:
                    href_parent_cable = obj.parent
                    href_parent_instance = href_parent_cable.parent
                    for pin in item.pins:
                        if isinstance(pin, OuterPin):
                            href_inst = HRef.from_parent_and_item(href_parent_instance, pin.instance)
                            inner_wire = pin.inner_pin.wire
                            if inner_wire:
                                inner_cable = inner_wire.cable
                                href_cable = HRef.from_parent_and_item(href_inst, inner_cable)
                                href_wire = HRef.from_parent_and_item(href_cable, inner_wire)
                                if href_wire not in in_yield:
                                    in_yield.add(href_wire)
                                    yield href_wire
                        else:
                            href_parent = href_parent_instance.parent
                            if href_parent:
                                instance = href_parent_instance.item
                                if pin in instance.pins:
                                    outer_pin = instance.pins[pin]
                                    outer_wire = outer_pin.wire
                                    if outer_wire:
                                        outer_cable = outer_wire.cable
                                        href_cable = HRef.from_parent_and_item(href_parent, outer_cable)
                                        href_wire = HRef.from_parent_and_item(href_cable, outer_wire)
                                        if href_wire not in in_yield:
                                            in_yield.add(href_wire)
                                            yield href_wire
                else:
                    if obj not in in_yield:
                        in_yield.add(obj)
                        yield obj
                    href_cable = obj.parent
                    href_inst = href_cable.parent
                    for pin in item.pins:
                        if isinstance(pin, OuterPin):
                            href_sub_inst = HRef.from_parent_and_item(obj.parent, pin.instance)
                            inner_pin = pin.inner_pin
                            port = inner_pin.port
                            href_port = HRef.from_parent_and_item(href_sub_inst, port)
                            href_pin = HRef.from_parent_and_item(href_port, pin)
                        else:
                            port = pin.port
                            href_port = HRef.from_parent_and_item(href_inst, port)
                            href_pin = HRef.from_parent_and_item(href_port, pin)
                        object_collection.append(href_pin)
            elif isinstance(item, InnerPin):
                hpin_search.add(obj)
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

    if hpin_search:
        for hwire in _get_hwires_from_hpins(hpin_search, selection):
            if hwire not in in_yield:
                in_yield.add(hwire)
                yield hwire

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


def _update_hwire_namemap(href_instance, recursive, found, namemap):
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
                for cable in reference.cables:
                    hcable = HRef.from_parent_and_item(href_instance, cable)
                    name_stack.append(cable.name if cable.name else '')
                    cable_hname = '/'.join(name_stack[1:])
                    for wire_index, wire in enumerate(cable.wires):
                        hwire = HRef.from_parent_and_item(hcable, wire)
                        if hwire not in found:
                            found.add(hwire)
                            if cable.is_scalar:
                                hname = cable_hname
                            else:
                                hname = "{}[{}]".format(cable_hname, cable.lower_index + wire_index)
                            if hname not in namemap:
                                namemap[hname] = list()
                            namemap[hname].append(hwire)
                    name_stack.pop()
                if recursive:
                    for child in reference.children:
                        if child.reference and child.reference.is_leaf() is False:
                            href_child = HRef.from_parent_and_item(href_instance, child)
                            search_stack.append((href_child, False))


def _get_hwires_from_hpins(hpin_search, selection):
    found_hwires = set()
    search_stack = list(hpin_search)
    while search_stack:
        hpin = search_stack.pop()
        if selection in {Selection.INSIDE, Selection.BOTH, Selection.ALL}:
            hwire_inside = _get_inner_hwire_from_hpin(hpin)
            if hwire_inside and hwire_inside not in found_hwires:
                found_hwires.add(hwire_inside)
                yield hwire_inside
                if selection is Selection.ALL:
                    search_stack += (x for x in _get_hpins_from_hwire(hwire_inside) if x != hpin)

        if selection in {Selection.OUTSIDE, Selection.BOTH, Selection.ALL}:
            hwire_outside = _get_outer_hwire_from_hpin(hpin)
            if hwire_outside and hwire_outside not in found_hwires:
                found_hwires.add(hwire_outside)
                yield hwire_outside
                if selection is Selection.ALL:
                    search_stack += (x for x in _get_hpins_from_hwire(hwire_outside) if x != hpin)


def _get_inner_hwire_from_hpin(hpin):
        wire = hpin.item.wire
        if wire:
            cable = wire.cable
            if cable:
                hport = hpin.parent
                hinst = hport.parent
                hcable = HRef.from_parent_and_item(hinst, cable)
                hwire = HRef.from_parent_and_item(hcable, wire)
                return hwire


def _get_outer_hwire_from_hpin(hpin):
    hport = hpin.parent
    hinst = hport.parent
    instance = hinst.item
    pin = hpin.item
    if pin in instance.pins:
        outer_pin = instance.pins[hpin.item]
        outer_wire = outer_pin.wire
        if outer_wire:
            cable = outer_wire.cable
            if cable:
                hcable = HRef.from_parent_and_item(hinst.parent, cable)
                hwire = HRef.from_parent_and_item(hcable, outer_wire)
                return hwire


def _get_hpins_from_hwire(hwire):
    hcable = hwire.parent
    hinst = hcable.parent
    for pin in hwire.item.pins:
        if isinstance(pin, InnerPin):
            port = pin.port
            if port:
                hport = HRef.from_parent_and_item(hinst, port)
                hpin = HRef.from_parent_and_item(hport, pin)
                yield hpin
        else:
            instance = pin.instance
            inner_pin = pin.inner_pin
            if instance and inner_pin:
                port = inner_pin.port
                if port:
                    other_hinst = HRef.from_parent_and_item(hinst, instance)
                    other_hport = HRef.from_parent_and_item(other_hinst, port)
                    other_hpin = HRef.from_parent_and_item(other_hport, inner_pin)
                    yield other_hpin
