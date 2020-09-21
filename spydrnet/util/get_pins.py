from spydrnet.ir import Element, InnerPin, OuterPin, Wire, Netlist, Library, Definition, Instance,\
    Port, Cable
from spydrnet.util.hierarchical_reference import HRef
from spydrnet.util.selection import Selection


def get_pins(obj, *args, **kwargs):
    """
    get_pins(obj, ...)

    Get pins *within* an object.

    Parameters
    ----------
    obj : object, Iterable - required
        The object or objects associated with this query. Queries return a collection objects associated with the
        provided object or objects that match the query criteria. For example, `sdn.get_ports(definition, ...)` would
        return all of the ports associated with the provided definition that match the additional criteria.
    selection : Selection.{INSIDE, OUTSIDE}, default: INSIDE
        Controls the type of pin returned. Setting this parameter to "OUTSIDE" will return the outer pins of the objects
        queried. For cables, this returns the corresponding pin based on this parameter.
    filter : function
        This is a single input function that can be used to filter out unwanted virtual instances. If not specifed, all
        matching virtual instances are returned. Otherwise, virtual instances that cause the filter function to evaluate
        to true are the only items returned.
    
    Returns
    -------
    pins : generator
       The pins associated with a particular object or collection of objects.
    
    """
    # Check argument list
    if len(args) > 0 or any(x not in {'filter', 'selection'} for x in kwargs):
        raise TypeError("Unknown usage. Please see help for more information.")

    # Default values
    selection = kwargs.get('selection', Selection.INSIDE)
    if isinstance(selection, str):
        if selection in Selection.__members__:
            selection = Selection[selection]
    if selection not in {Selection.INSIDE, Selection.OUTSIDE}:
        raise TypeError("selection must be '{}'".format("', '".join([Selection.INSIDE.name, Selection.OUTSIDE.name])))

    filter_func = kwargs.get('filter', lambda x: True)

    if isinstance(obj, (Element, HRef)) is False:
        try:
            object_collection = list(iter(obj))
        except TypeError:
            object_collection = [obj]
    else:
        object_collection = [obj]
    if all(isinstance(x, (Element, HRef)) for x in object_collection) is False:
        raise TypeError("get_ports() supports netlist elements and hierarchical references, or a collection of "
                        "these as the object searched")

    return _get_ports(object_collection, selection, filter_func)


def _get_ports(object_collection, selection, filter_func):
    for result in filter(filter_func, _get_ports_raw(object_collection, selection)):
        yield result


def _get_ports_raw(object_collection, selection):
    found = set()
    while object_collection:
        obj = object_collection.pop()
        if isinstance(obj, Definition):
            for port in obj.ports:
                object_collection += port.pins
        elif isinstance(obj, Netlist):
            for library in obj.libraries:
                for definition in library.definitions:
                    object_collection.append(definition)
        elif isinstance(obj, Library):
            object_collection += obj.definitions
        elif isinstance(obj, Instance):
            object_collection += obj.pins
        elif isinstance(obj, Port):
            object_collection += obj.pins
        elif isinstance(obj, InnerPin):
            if selection == Selection.INSIDE:
                if obj not in found:
                    found.add(obj)
                    yield obj
            else:
                port = obj.port
                if port:
                    definition = port.definition
                    if definition:
                        for instance in definition.references:
                            outer_pin = instance.pins[obj]
                            if outer_pin not in found:
                                found.add(outer_pin)
                                yield outer_pin
        elif isinstance(obj, OuterPin):
            if selection == Selection.OUTSIDE:
                if obj not in found:
                    found.add(obj)
                    yield obj
            else:
                inner_pin = obj.inner_pin
                if inner_pin and inner_pin not in found:
                    found.add(inner_pin)
                    yield inner_pin
        elif isinstance(obj, Wire):
            object_collection += obj.pins
        elif isinstance(obj, Cable):
            object_collection += obj.wires
        elif isinstance(obj, HRef):
            if obj.is_valid:
                item = obj.item
                if isinstance(item, InnerPin) and selection == Selection.OUTSIDE:
                    hport = obj.parent
                    hinstance = hport.parent
                    instance = hinstance.item
                    outer_pin = instance.pins[item]
                    if outer_pin not in found:
                        found.add(outer_pin)
                        yield outer_pin
                else:
                    object_collection.append(obj.item)
