from spydrnet.ir import FirstClassElement
from spydrnet.ir import Definition
from spydrnet.ir.views.listview import ListView
from spydrnet.global_state import global_callback
from spydrnet.global_state.global_callback import _call_create_library
from copy import deepcopy, copy, error


class Library(FirstClassElement):
    """
    Represents a library object.

    Contains a pointer to parent netlist and definitions.
    """
    __slots__ = ['_netlist', '_definitions']

    def __init__(self, name = None, properties = None):
        """
        creates an empty object of type Library

        parameters
        ----------

        name - (str) the name of this instance
        properties - (dict) the dictionary which holds the properties
        """
        super().__init__()
        self._netlist = None
        self._definitions = list()
        _call_create_library(self)
        if name!= None:
            self.name = name
        if properties != None:
            assert isinstance(properties, dict), "properties must be a dictionary"
            for key in properties:
                self[key] = properties[key]

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
        assert definition.library == self, "definition is not included in library"
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


    def _clone_rip_and_replace(self, memo):
        '''remove from its current environment and place it into the new cloned environment with references held in the memo dictionary'''
        pass #this function will need to call rip and replace in library on each of the definitions when called from the netlist.
        for definition in self._definitions:
            definition._clone_rip_and_replace(memo)

    def _clone_rip(self, memo):
        '''remove from its current environmnet. This will remove all pin pointers and create a floating stand alone instance.'''   
        # references lists of definitions need to be vacated except those that were cloned.
        for definition in self._definitions:
            new_references = set()
            for ref in definition._references:
                if ref in memo.values():
                    new_references.add(ref)
            for instance in definition._children:
                instance._reference._references.add(instance)
                
            definition._references = new_references


    def _clone(self, memo):
        '''not api safe clone function
        clone leaving all references in tact.
        the element can then either be ripped or ripped and replaced'''
        assert self not in memo, "the object should not have been copied twice in this pass"
        c = Library()
        memo[self] = c
        c._netlist = None
        c._data = deepcopy(self._data)
        
        new_definitions = list()
        for definition in self._definitions:
            new_definitions.append(definition._clone(memo))
        c._definitions = new_definitions

        for definition in c._definitions:
            definition._library = c
            definition._clone_rip_and_replace(memo)
        return c

    def clone(self):
        '''
        Clone the library in an api safe manner.
        The following describes the structure of the returned object:
         * the instances that pointed to reference definitions within the library will have updated references
         * the instances that pointed to reference definitions outside the library will maintain their definitions
         * the references lists (of definitions) both inside and outsde the library will be updated to reflect the change
         * all definitions are cloned within the library.
         '''
        memo = dict()
        c = self._clone(memo)
        c._clone_rip(memo)
        return c
