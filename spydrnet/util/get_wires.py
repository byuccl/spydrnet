from spydrnet import InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance, Port, Cable,\
    Element
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.selection import Selection


def get_wires(obj, *args, **kwargs):
    """
    get_wires(obj, ...)

    Get wires *within* an object.

    Parameters
    ----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection of objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_instances(netlist, ...)` would
        return all of the instances *within* the provided definition that match the additional criteria.
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
    wires : generator
        The wires associated with a particular object or collection of objects.
    
    """
    # Check argument list
    if len(args) > 0 or any(x not in {'selection', 'recursive', 'filter'} for x in
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

    if isinstance(obj, (Element, HRef)) is False:
        try:
            object_collection = list(iter(obj))
        except TypeError:
            object_collection = [obj]
    else:
        object_collection = [obj]
    if all(isinstance(x, (HRef, Element)) for x in object_collection) is False:
        raise TypeError("get_hwires() supports all netlist related objects and hierarchical references or a "
                        "collection of theses as the object searched, unsupported object provided")

    return _get_wires(object_collection, selection, recursive, filter_func)


def _get_wires(object_collection, selection, recursive, filter_func):
    for result in filter(filter_func, _get_wires_raw(object_collection, selection, recursive)):
        yield result


def _get_wires_raw(object_collection, selection, recursive):
    in_yield = set()
    pin_search = set()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Netlist):
            object_collection += obj.libraries
        elif isinstance(obj, Library):
            object_collection += obj.definitions
        elif isinstance(obj, Definition):
            if selection in {Selection.INSIDE, Selection.ALL}:
                # Get all cables inside a hierarchical instance
                for cable in obj.cables:
                    for wire in cable.wires:
                        if wire not in in_yield:
                            in_yield.add(wire)
                            yield wire
                # get internal cables recursively
                if recursive or selection == Selection.ALL:
                    object_collection += obj.children
            if selection in {Selection.OUTSIDE, Selection.BOTH, Selection.ALL}:
                for port in obj.ports:
                    for pin in port.pins:
                        pin_search.add(pin)
        elif isinstance(obj, Instance):
            reference = obj.reference
            if reference:
                object_collection.append(reference)
        elif isinstance(obj, Port):
            for pin in obj.pins:
                pin_search.add(pin)
        elif isinstance(obj, Cable):
            object_collection += obj.wires
        elif isinstance(obj, Wire):
            if selection == Selection.INSIDE:
                if obj not in in_yield:
                    in_yield.add(obj)
                    yield obj
            elif selection == Selection.OUTSIDE:
                for pin in obj.pins:
                    if isinstance(pin, OuterPin):
                        inner_wire = pin.inner_pin.wire
                        if inner_wire:
                            if inner_wire not in in_yield:
                                in_yield.add(inner_wire)
                                yield inner_wire
                    else:
                        cable = obj.cable
                        if cable:
                            definition = cable.definition
                            if definition:
                                for instance in definition.references:
                                    if pin in instance.pins:
                                        outer_pin = instance.pins[pin]
                                        outer_wire = outer_pin.wire
                                        if outer_wire:
                                            if outer_wire not in in_yield:
                                                in_yield.add(outer_wire)
                                                yield outer_wire
            else:
                for pin in obj.pins:
                    pin_search.add(pin)
        elif isinstance(obj, (InnerPin, OuterPin)):
            pin_search.add(obj)
        elif isinstance(obj, HRef):
            if obj.is_valid:
                object_collection.append(obj.item)

    while pin_search:
        new_pin_search = set()
        for pin in pin_search:
            if selection in {Selection.BOTH, Selection.ALL}:
                wire = pin.wire
                if wire and wire not in in_yield:
                    in_yield.add(wire)
                    yield wire
                    if selection == Selection.ALL:
                        for other_pin in wire.pins:
                            new_pin_search.add(other_pin)
                if isinstance(pin, OuterPin):
                    inner_pin = pin.inner_pin
                    if inner_pin:
                        inner_wire = inner_pin.wire
                        if inner_wire and inner_wire not in in_yield:
                            in_yield.add(inner_wire)
                            yield inner_wire
                            if selection == Selection.ALL:
                                for other_pin in inner_wire.pins:
                                    new_pin_search.add(other_pin)
                else:
                    port = pin.port
                    if port:
                        definition = port.definition
                        if definition:
                            for instance in definition.references:
                                outer_pin = instance.pins[pin]
                                outer_wire = outer_pin.wire
                                if outer_wire and outer_wire not in in_yield:
                                    in_yield.add(outer_wire)
                                    yield outer_wire
                                    if selection == Selection.ALL:
                                        for other_pin in outer_wire.pins:
                                            new_pin_search.add(other_pin)
            elif selection == Selection.INSIDE:
                if isinstance(pin, OuterPin):
                    inner_pin = pin.inner_pin
                    if inner_pin:
                        wire = inner_pin.wire
                        if wire and wire not in in_yield:
                            in_yield.add(wire)
                            yield wire
                else:
                    wire = pin.wire
                    if wire and wire not in in_yield:
                        in_yield.add(wire)
                        yield wire
            else:
                if isinstance(pin, OuterPin):
                    wire = pin.wire
                    if wire and wire not in in_yield:
                        in_yield.add(wire)
                        yield wire
                else:
                    port = pin.port
                    if port:
                        definition = port.definition
                        if definition:
                            for instance in definition.references:
                                outer_pin = instance.pins[pin]
                                outer_wire = outer_pin.wire
                                if outer_wire and outer_wire not in in_yield:
                                    in_yield.add(outer_wire)
                                    yield outer_wire
        pin_search = new_pin_search
