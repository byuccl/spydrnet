class Element:
    __slots__ = tuple()

    def get_hinstances(self, *args, **kwargs):
        from spydrnet.util import get_hinstances
        return get_hinstances(self, *args, **kwargs)

    def get_hports(self, *args, **kwargs):
        from spydrnet.util import get_hports
        return get_hports(self, *args, **kwargs)

    def get_hpins(self, *args, **kwargs):
        from spydrnet.util import get_hpins
        return get_hpins(self, *args, **kwargs)

    def get_hcables(self, *args, **kwargs):
        from spydrnet.util import get_hcables
        return get_hcables(self, *args, **kwargs)

    def get_hwires(self, *args, **kwargs):
        from spydrnet.util import get_hwires
        return get_hwires(self, *args, **kwargs)
