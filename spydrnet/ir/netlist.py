from spydrnet.ir.element import Element
from spydrnet.ir.library import Library
from spydrnet.ir.instance import Instance
from spydrnet.ir.views.listview import ListView


class Netlist(Element):
    """
    Represents a netlist object.

    Contains a top level instance and libraries
    """
    __slots__ = ['_libraries', '_top_instance']

    def __init__(self):
        super().__init__()
        self._libraries = list()
        self._top_instance = None

    @property
    def libraries(self):
        """get a list of all libraries included in the netlist"""
        return ListView(self._libraries)

    @libraries.setter
    def libraries(self, value):
        """
        set the libraries. This function can only be used to reorder the libraries. Use the remove_library and
        add_library functions to add and remove libraries.

        parameters
        ----------

        value - the reordered list of libraries
        """
        value_list = list(value)
        value_set = set(value_list)
        assert len(value_list) == len(value_set) and set(self._libraries) == value_set, \
            "Set of values do not match, this assignment can only reorder values, values must be unique"
        self._libraries = value_list

    @property
    def top_instance(self):
        """
        Get the top instance in the netlist.

        Returns
        -------
        Instance
            The top level instance in the environment
        """
        return self._top_instance

    @top_instance.setter
    def top_instance(self, instance):
        """
        sets the top instance of the design. The instance must not be null and should probably come from this netlist

        parameters
        ----------

        instance - (Instance) the instance to set as the top instance.
        """
        assert instance is None or isinstance(instance, Instance), "Must specify an instance"
        # TODO: should We have a DRC that makes sure the instance is of a definition contained in netlist? I think no
        #  but I am open to hear other points of veiw.
        self._top_instance = instance

    def create_library(self):
        '''create a library and add it to the netlist and return that library'''
        library = Library()
        self.add_library(library)
        return library

    def add_library(self, library, position=None):
        """
        add an already existing library to the netlist. This library should not belong to another netlist. Use
        remove_library from other netlists before adding

        parameters
        ----------

        library - (Library) the library to be added to the netlist

        position - (int, default None) when set it is the index at which to add the library in the libraries list

        """
        assert library not in self._libraries, "Library already included in netlist"
        assert library.netlist is None, "Library already belongs to a different netlist"
        if position is not None:
            self._libraries.insert(position, library)
        else:
            self._libraries.append(library)
        library._netlist = self

    def remove_library(self, library):
        """
        removes the given library if it is in the netlist

        parameters
        ----------

        library - (Library) the library to be removed
        """
        assert library.netlist == self, "Library is not included in netlist"
        self._remove_library(library)
        self._libraries.remove(library)

    def remove_libraries_from(self, libraries):
        '''removes all the given libraries from the netlist. All libraries must be in the netlist

        parameters
        ----------

        libraries - (Set) libraries to be removed
        '''
        if isinstance(libraries, set):
            excluded_libraries = libraries
        else:
            excluded_libraries = set(libraries)
        assert all(x.netlist == self for x in excluded_libraries), "Some libraries to remove are not included in " \
                                                                   "netlist "
        included_libraries = list()
        for library in self._libraries:
            if library not in excluded_libraries:
                included_libraries.append(library)
            else:
                self._remove_library(library)
        self._libraries = included_libraries

    @staticmethod
    def _remove_library(library):
        """
        internal function which will separate a particular libraries binding from the netlist
        """
        library._netlist = None
