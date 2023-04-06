from spydrnet.ir import FirstClassElement


class Bundle(FirstClassElement):
    """Parent class of ports and cables.

    Since both of these objects represent arrays of objects they both inherit from
    this parent class.
    """
    __slots__ = ['_definition', '_is_downto', '_is_scalar', '_lower_index']

    def __init__(self):
        super().__init__()
        self._definition = None
        self._is_downto = True
        self._is_scalar = True
        self._lower_index = 0

    @property
    def definition(self):
        """Get the definition that this bundle belongs to.

        The definition is responsible for changing this value.
        """
        return self._definition

    @property
    def is_downto(self):
        """Get the downto status of the bundle.

        Downto is False if the right index is higher than the left one. True
        otherwise
        """
        return self._is_downto

    @is_downto.setter
    def is_downto(self, value):
        """Change the downto value.

        Downto is False if the right index is higher than the left index. True otherwise.

        parameters
        ----------

        value - (boolean) True if the value is downto False if the value is to.
        """
        self._is_downto = value

    def _items(self):
        """
        this function must be overridden in classes which extend this to return either a list of pins or wires
        """
        raise NotImplementedError

    @property
    def is_scalar(self):
        """Return True if the item is a scalar False otherwise.

        The item is not a scalar if it has more than one pin orwire in it.
        if it has one pin or wire in it it may be a scalar.
        This mimics vhdl's downto usage which canrepresent single pin arrays
        ie. std_logic_vector(0 downto 0) which would have a single pin but not be a scalar.
        """
        _items = self._items()
        if _items and len(_items) > 1:
            return False
        return self._is_scalar

    @is_scalar.setter
    def is_scalar(self, value):
        """Set the scalar status of single item bundles.

        The item is not a scalar if it has more than one pin or wire in it. if it has one or zero pins this function
        can be used to set the value or wire in it it may be a scalar. This mimics vhdl's downto usage which can
        represent single pin arrays ie. std_logic_vector(0 downto 0) which would have a single pin but not be a scalar.

        parameters
        ----------

        value - (boolean) True if the item is to be a scalar False if it is not. Multi element bundles cannot set
        is_scalar to True.
        """
        _items = self._items()
        if _items and len(_items) > 1 and value is True:
            raise RuntimeError(
                "Cannot set is_scalar to True on a multi-item bundle")
        else:
            self._is_scalar = value

    @property
    def is_array(self):
        """This is the logical inverse of is_scalar.

        See the is_scalar documentation for more insight into the properties of this value.
        """
        return not self.is_scalar

    @is_array.setter
    def is_array(self, value):
        """This is the logical inverse of is_scalar.

        See the is_scalar documentation for more insight into the properties of this value.

        parameters
        ----------

        value - (boolean) True if the object is an array. False otherwise. Multi element bundles cannot set is_array to
        false.
        """
        _items = self._items()
        if _items and len(_items) > 1 and value is False:
            raise RuntimeError(
                "Cannot set is_array to False on a multi-item bundle")
        else:
            self._is_scalar = not value

    @property
    def lower_index(self):
        """Get the value of the lower index of the array.

        This would be the right index in the case of downto and the left
        in the case of to
        """
        return self._lower_index

    @lower_index.setter
    def lower_index(self, value):
        """Set the lower index of the array.

        In the case of to this is the left index and the right in the case of downto

        parameters
        ----------

        value - (int) the lower index value for the bundle.
        """
        self._lower_index = value
