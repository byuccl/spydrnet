class DictView:
    __slots__ = ['_dict']

    def __init__(self, dict_object):
        self._dict = dict_object

    def __eq__(self, other):
        return self._dict.__eq__(other)

    def __ge__(self, other):
        return self._dict.__ge__(other)

    def __gt__(self, other):
        return self._dict.__gt__(other)

    def __hash__(self):
        return self._dict.__hash__()

    def __le__(self, other):
        return self._dict.__le__(other)

    def __len__(self):
        return self._dict.__len__()

    def __lt__(self, other):
        return self._dict.__lt__(other)

    def __ne__(self, other):
        return self._dict.__ne__(other)

    def __repr__(self):
        return self._dict.__repr__()

    def __str__(self):
        return self._dict.__str__()

    def __contains__(self, item):
        return self._dict.__contains__(item)

    def __getitem__(self, item):
        return self._dict.__getitem__(item)

    def __iter__(self):
        return self._dict.__iter__()

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def copy(self):
        return self._dict.copy()

    def fromkeys(self, seq):
        return self._dict.fromkeys(seq)

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()
