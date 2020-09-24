from spydrnet.ir.first_class_element import FirstClassElement
from spydrnet.ir.library import Library
from spydrnet.ir.instance import Instance
from spydrnet.ir.views.listview import ListView
from spydrnet.global_state import global_callback
from spydrnet.global_state.global_callback import _call_create_netlist
from copy import deepcopy, copy, error


class Netlist(FirstClassElement):
    """
    Represents a netlist object.

    Contains a top level instance and libraries
    """
    __slots__ = ['_libraries', '_top_instance']

    def __init__(self):
        super().__init__()
        self._libraries = list()
        self._top_instance = None
        _call_create_netlist(self)

    def compose(self, *args, **kwargs):
        """
        compose(filename)

        Compose a netlist into a file format.

        Shortcut to :func:`~spydrnet.compose`.
        """
        from spydrnet.composers import compose
        compose(self, *args, **kwargs)

    @property
    def libraries(self):
        """
        Get a list of all libraries included in the netlist.
        """
        return ListView(self._libraries)

    @libraries.setter
    def libraries(self, value):
        """
        Set the libraries.

        This function can only be used to reorder the libraries. Use the remove_library and
        add_library functions to add and remove libraries.

        Parameters
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
        Sets the top instance of the design.

        The instance must not be null and should probably come from this netlist

        Parameters
        ----------
        instance - (Instance) the instance to set as the top instance.

        """
        assert instance is None or isinstance(
            instance, Instance), "Must specify an instance"
        global_callback._call_netlist_top_instance(self, instance)
        # TODO: should We have a DRC that makes sure the instance is of a definition contained in netlist? I think no
        #  but I am open to hear other points of veiw.
        self._top_instance = instance

    def create_library(self):
        """
        Create a library and add it to the netlist and return that library.
        """

        library = Library()
        self.add_library(library)
        return library

    def add_library(self, library, position=None):
        """
        Add an already existing library to the netlist.

        This library should not belong to another netlist. Use
        remove_library from other netlists before adding

        Parameters
        ----------
        library - Library
            The library to be added to the netlist.
        position - int, (default None)
            When set, it is the index at which to add the library in the libraries list.

        """
        assert library not in self._libraries, "Library already included in netlist"
        assert library.netlist is None, "Library already belongs to a different netlist"
        global_callback._call_netlist_add_library(self, library)
        if position is not None:
            self._libraries.insert(position, library)
        else:
            self._libraries.append(library)
        library._netlist = self

    def remove_library(self, library):
        """
        Removes the given library if it is in the netlist

        Parameters
        ----------
        library - Library
            The library to be removed.

        """
        assert library.netlist == self, "Library is not included in netlist"
        self._remove_library(library)
        self._libraries.remove(library)

    def remove_libraries_from(self, libraries):
        """
        Removes all the given libraries from the netlist.

        All libraries must be in the netlist.

        Parameters
        ----------
        libraries - Set
            Libraries to be removed.

        """
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

    def _remove_library(self, library):
        """
        Internal function which will separate a particular libraries binding from the netlist.
        """
        global_callback._call_netlist_remove_library(self, library)
        library._netlist = None

    def _clone_rip(self, memo):
        """
        Need to remove any extraneous references to floating, no parent instances
        """
        for lib in self._libraries:
            for defin in lib._definitions:
                new_ref = set()
                for ref in defin._references:
                    if ref in memo.values():
                        new_ref.add(ref)
                defin._references = new_ref

    def _clone(self, memo):
        """
        Clone leaving all references in tact.

        The element can then either be ripped or ripped and replaced.
        """
        assert self not in memo, "the object should not have been copied twice in this pass"
        c = Netlist()
        memo[self] = c
        c._data = deepcopy(self._data)

        new_libraries = list()
        for library in self._libraries:
            new_libraries.append(library._clone(memo))
        c._libraries = new_libraries

        if self._top_instance == None:
            c._top_instance = None
        else:
            if self._top_instance in memo:
                c._top_instance = memo[self._top_instance]
            else:
                new_top = self.top_instance._clone(memo)
                new_top._clone_rip_and_replace_in_definition(memo)
                new_top._clone_rip_and_replace_in_library(memo)
                c._top_instance = new_top

        for library in c._libraries:
            library._netlist = c
            library._clone_rip_and_replace(memo)
        return c

    def clone(self):
        """
        API safe clone on a netlist.

        This clone function should act just the way you would expect
        All references are internal to the netlist that has been cloned.
        """
        memo = dict()
        c = self._clone(memo)
        c._clone_rip(memo)
        return c
