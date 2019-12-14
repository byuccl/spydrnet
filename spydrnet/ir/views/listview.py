class ListView:
    __slots__ = ['_list']

    def __init__(self, list_object):
        self._list = list_object

    def __add__(self, other):
        return self._list.__add__(other)

    def __getitem__(self, other):
        return self._list.__getitem__(other)

    def __contains__(self, item):
        return self._list.__contains__(item)

    def __eq__(self, other):
        return self._list.__eq__(other)

    def __hash__(self):
        return self._list.__hash__()

    def __ge__(self, other):
        if isinstance(other, ListView):
            return self._list.__ge__(other._list)
        return self._list.__ge__(other)

    def __gt__(self, other):
        if isinstance(other, ListView):
            return self._list.__gt__(other._list)
        return self._list.__gt__(other)

    def __iter__(self):
        return self._list.__iter__()

    def __le__(self, other):
        if isinstance(other, ListView):
            return self._list.__le__(other._list)
        return self._list.__le__(other)

    def __len__(self):
        return self._list.__len__()

    def __lt__(self, other):
        if isinstance(other, ListView):
            return self._list.__lt__(other._list)
        return self._list.__lt__(other)

    def __ne__(self, other):
        return self._list.__ne__(other)

    def __mul__(self, other):
        return self._list.__mul__(other)

    def __rmul__(self, n):
        return self._list.__rmul__(n)

    def __reversed__(self):
        return self._list.__reversed__()

    def __repr__(self):
        return self._list.__repr__()

    def __str__(self):
        return self._list.__str__()

    def __radd__(self, other):
        return other + self._list

    def __iadd__(self, other):
        raise TypeError("unsupported operator for type SetView")

    def __imul__(self, other):
        raise TypeError("unsupported operator for type SetView")

    def copy(self):
        return self._list.copy()

    def count(self, object):
        return self._list.count(object)

    def index(self, *args, **kwargs):
        return self._list.index(*args, **kwargs)