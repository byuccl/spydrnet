class DictView:
    __slots__ = ['_dict']

    def __init__(self, dict_object):
        self._dict = dict_object

    def __eq__(self, other):
        if isinstance(other, DictView):
            return self._dict.__eq__(other._dict)
        return self._dict.__eq__(other)

    def __hash__(self):
        return self._dict.__hash__()

    def __len__(self):
        return self._dict.__len__()

    def __ne__(self, other):
        if isinstance(other, DictView):
            return self._dict.__ne__(other._dict)
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

    def fromkeys(self, *args, **kwargs):
        return self._dict.fromkeys(*args, **kwargs)

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()
