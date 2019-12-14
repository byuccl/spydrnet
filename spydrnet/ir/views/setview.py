class SetView:
    __slots__ = ['_set']

    def __init__(self, set_object):
        self._set = set_object

    def __and__(self, *args, **kwargs):
        return self._set.__and__(*args, *kwargs)

    def __rand__(self, *args, **kwargs):
        return self._set.__rand__(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, SetView):
            return self._set.__eq__(other._set)
        return self._set.__eq__(other)

    def __ge__(self, other):
        if isinstance(other, SetView):
            return self._set.__ge__(other._set)
        return self._set.__ge__(other)

    def __gt__(self, other):
        if isinstance(other, SetView):
            return self._set.__gt__(other._set)
        return self._set.__gt__(other)

    def __iter__(self, *args, **kwargs):
        return self._set.__iter__(*args, **kwargs)

    def __le__(self, other):
        if isinstance(other, SetView):
            return self._set.__le__(other._set)
        return self._set.__le__(other)

    def __len__(self, *args, **kwargs):
        return self._set.__len__(*args, **kwargs)

    def __lt__(self, other):
        if isinstance(other, SetView):
            return self._set.__lt__(other._set)
        return self._set.__lt__(other)

    def __ne__(self, other):
        if isinstance(other, SetView):
            return self._set.__ne__(other._set)
        return self._set.__ne__(other)

    def __or__(self, *args, **kwargs):
        return self._set.__or__(*args, **kwargs)

    def __ror__(self, *args, **kwargs):
        return self._set.__ror__(*args, **kwargs)

    def __sub__(self, *args, **kwargs):
        return self._set.__sub__(*args, **kwargs)

    def __rsub__(self, *args, **kwargs):
        return self._set.__rsub__(*args, **kwargs)

    def __xor__(self, *args, **kwargs):
        return self._set.__xor__(*args, **kwargs)

    def __rxor__(self, *args, **kwargs):
        return self._set.__rxor__(*args, **kwargs)

    def __repr__(self, *args, **kwargs):
        return self._set.__repr__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self._set.__str__(*args, **kwargs)

    def copy(self, *args, **kwargs):
        return self._set.copy(*args, **kwargs)

    def difference(self, *args, **kwargs):
        return self._set.difference(*args, **kwargs)

    def intersection(self, *args, **kwargs):
        return self._set.intersection(*args, **kwargs)

    def isdisjoint(self, *args, **kwargs):
        return self._set.isdisjoint(*args, **kwargs)

    def issubset(self, *args, **kwargs):
        return self._set.issubset(*args, **kwargs)

    def issuperset(self, *args, **kwargs):
        return self._set.issuperset(*args, **kwargs)

    def symmetric_difference(self, *args, **kwargs):
        return self._set.symmetric_difference(*args, **kwargs)

    def union(self, *args, **kwargs):
        return self._set.union(*args, **kwargs)

    def __iand__(self, *args, **kwargs):
        raise TypeError("unsupported operator for type SetView")

    def __ior__(self, *args, **kwargs):
        raise TypeError("unsupported operator for type SetView")

    def __ixor__(self, *args, **kwargs):
        raise TypeError("unsupported operator for type SetView")

    def __isub__(self, *args, **kwargs):
        raise TypeError("unsupported operator for type SetView")
