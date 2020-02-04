from spydrnet.ir.element import Element
from spydrnet.ir.definition import Definition
from spydrnet.ir.views.listview import ListView
from spydrnet.global_state import global_callback


class Library(Element):
    """
    Represents a library object.

    Contains a pointer to parent netlist and definitions.
    """
    __slots__ = ['_netlist', '_definitions']

    def __init__(self):
        super().__init__()
        self._netlist = None
        self._definitions = list()

    @property
    def netlist(self):
        """
        get the netlist that contains this library
        """
        return self._netlist

    @property
    def definitions(self):
        """
        return a list of all the definitions that are included in this library
        """
        return ListView(self._definitions)

    @definitions.setter
    def definitions(self, value):
        """
        set the definitions to a new reordered set of definitions. This function cannot be used to add or remove
        definitions

        Parameters
        ----------

        value - (List containing Definition type objects) The reordered list
        """
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_list) == len(value_set) and set(self._definitions) == value_set, \
            "Set of values do not match, this function can only reorder values, values must be unique"
        self._definitions = value_list

    def create_definition(self):
        """
        create a definition, add it to the library, and return the definition
        """
        definition = Definition()
        self.add_definition(definition)
        return definition

    def add_definition(self, definition, position=None):
        """
        add an existing definition to the library. The definition must not belong to a library including this one.

        parameters
        ----------

        definition - (Definition) the defintion to add to the library

        position - (int, default None) the index in the library list at which to add the definition

        """
        assert definition.library is not self, "Definition already included in library"
        assert definition.library is None, "Definition already belongs to a different library"
        global_callback._call_library_add_definition(self, definition)
        if position is not None:
            self._definitions.insert(position, definition)
        else:
            self._definitions.append(definition)
        definition._library = self

    def remove_definition(self, definition):
        """
        remove the given definition from the library

        parameters
        ----------

        definition - (Definition) the definition to be removed
        """
        assert definition.library == self, "Library is not included in netlist"
        self._remove_definition(definition)
        self._definitions.remove(definition)

    def remove_definitions_from(self, definitions):
        """
        remove a set of definitions from the library. all definitions provided must be in the library

        parameters
        ----------

        definitions - (Set of Definition type objects) the definitions to be removed
        """
        if isinstance(definitions, set):
            excluded_definitions = definitions
        else:
            excluded_definitions = set(definitions)
        assert all(x.library == self for x in excluded_definitions), "Some definitions to remove are not included in " \
                                                                     "the library "
        included_definitions = list()
        for definition in self._definitions:
            if definition not in excluded_definitions:
                included_definitions.append(definition)
            else:
                self._remove_definition(definition)
        self._definitions = included_definitions

    def _remove_definition(self, definition):
        """
        internal function to dissociate a definition from the library
        """
        global_callback._call_library_remove_definition(self, definition)
        definition._library = None