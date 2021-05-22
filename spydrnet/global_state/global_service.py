from spydrnet.ir import Netlist, Library, Definition, Port, Cable, Instance

_registered_lookups = dict()
_registered_hierarchical_lookup = None


def register_lookup(key, func):
    if key in _registered_lookups:
        raise ValueError(
            "Cannot register a fast lookup under the key {}, lookup already registered.")
    else:
        _registered_lookups[key] = func


def deregister_lookup(key):
    if key in _registered_lookups:
        del _registered_lookups[key]


def lookup(parent, element_type, key, value):
    if key in _registered_lookups:
        registered_lookup = _registered_lookups[key]
        return registered_lookup(parent, element_type, key, value)
    else:
        if isinstance(parent, Netlist):
            if element_type is Library:
                for library in parent.libraries:
                    if key in library and value == library[key]:
                        return library
        elif isinstance(parent, Library):
            if element_type is Definition:
                for definition in parent.definitions:
                    if key in definition and value == definition[key]:
                        return definition
        elif isinstance(parent, Definition):
            if element_type is Port:
                for port in parent.ports:
                    if key in port and value == port[key]:
                        return port
            elif element_type is Cable:
                for cable in parent.cables:
                    if key in cable and value == cable[key]:
                        return cable
            elif element_type is Instance:
                for instance in parent.children:
                    if key in instance and value == instance[key]:
                        return instance
    return None
