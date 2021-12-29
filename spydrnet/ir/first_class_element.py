import sys
from spydrnet.ir import Element
from spydrnet.ir.views.dictview import DictView
from spydrnet.global_state import global_callback


class FirstClassElement(Element):
    """
    Base class of all intermediate representation objects.

    An intermediate representation object represents an item in a netlist. Items range in specificity from pins on a
    port or wires in a cable up to an item that represents the netlist as a whole.

    Each element implements a dictionary for storing key-value pairs. The key should be a case sensitive string and the
    value should be a primitive type (string, integer, float, boolean) or potentially nested collections of primitive
    types. The purpose of this dictionary is to provide a space for properties and metadata associated with the element.

    Key namespaces are separated with a *period* character. If the key is void of a *period* than the key resides in the
    root namespace. Keys in the root namespace are considered properties. Other keys are considered metadata. For
    example '<LANG_OF_ORIGIN>.<METADATA_TAG>':<metadata_value> is considered metadata associated with the netlist's
    language of origin.

    Only data pertinent to the netlist should be stored in this dictionary. Cached data (namespace management, anything
    that can be recreated from the netlist) should be excluded from this dictionary. The intent of the IR is to house
    the basis of data for the netlist.

    The only key that is reserved is 'NAME'. It is the primary name of the element. NAME may be undefined or inferred,
    for example, a pin on a port may be nameless, but infer its name for its parent port and position.
    """
    __slots__ = ['_data',]

    def __init__(self):
        """Initialize an element with an empty data dictionary."""
        self._data = dict()

    @property
    def data(self):
        """Data stores information about the element"""
        return DictView(self._data)

    @property
    def name(self):
        """The name of this element"""
        return self._data.get(".NAME", None)

    @name.setter
    def name(self, value):
        """Set the name of the element

        parameters
        ----------

        value - the new name of the element

        """
        if value is None and ".NAME" in self:
            del self[".NAME"]
        else:
            self[".NAME"] = value

    @name.deleter
    def name(self):
        """Delete the name of the element"""
        if ".NAME" in self:
            del self[".NAME"]

    def __setitem__(self, key, value):
        """
        create an entry in the dictionary of the element it will be stored in the metadata.
        """
        global_callback._call_dictionary_set(self, key, value)
        key = sys.intern(key)
        self._data.__setitem__(sys.intern(key), value)

    def __delitem__(self, key):
        """ delete the item from the data structure"""
        global_callback._call_dictionary_delete(self, key)
        self._data.__delitem__(key)

    def __getitem__(self, key):
        return self._data.__getitem__(key)

    def __contains__(self, item):
        return self._data.__contains__(item)

    def __iter__(self):
        return self._data.__iter__()

    def pop(self, item):
        """pop the object from the data structure"""
        global_callback._call_dictionary_pop(self, item)
        return self._data.pop(item)

    def get(self, *args, **kwargs):
        """get the item from the data structure"""
        return self._data.get(*args, **kwargs)

    def __str__(self):
        """Re-define the print function so it is easier to read"""
        rep = str(type(self))
        rep = rep[:-1] + '; '
        if self.name is None:
            rep += 'name undefined'
        else:
            rep += 'name \'' + self.name + '\''
        rep += '>'
        return rep
