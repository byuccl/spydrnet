from spydrnet.ir.views.dictview import DictView
from spydrnet.ir import OuterPin


class OuterPinsView(DictView):

    def __init__(self, dict_object):
        super().__init__(dict_object)

    def __contains__(self, item):
        if item not in self._dict:
            if isinstance(item, OuterPin):
                return item.inner_pin in self._dict
            return False
        return True

    def __getitem__(self, item):
        if isinstance(item, OuterPin):
            return self._dict[item.inner_pin]
        return self._dict[item]

    def __iter__(self):
        return iter(self._dict.values())

    def get(self, key, default=None):
        if isinstance(key, OuterPin):
            return self._dict.get(key.inner_pin, default)
        return self._dict.get(key, default)
