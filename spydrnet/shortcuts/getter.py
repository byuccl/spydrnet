class GetterShortcuts:
    __slots__ = tuple()

    def get_netlists(self, *args, **kwargs):
        from spydrnet.util import get_netlists
        return get_netlists(self, *args, **kwargs)

    def get_libraries(self, *args, **kwargs):
        from spydrnet.util import get_libraries
        return get_libraries(self, *args, **kwargs)

    def get_definitions(self, *args, **kwargs):
        from spydrnet.util import get_definitions
        return get_definitions(self, *args, **kwargs)

    def get_instances(self, *args, **kwargs):
        from spydrnet.util import get_instances
        return get_instances(self, *args, **kwargs)

    def get_ports(self, *args, **kwargs):
        from spydrnet.util import get_ports
        return get_ports(self, *args, **kwargs)

    def get_pins(self, *args, **kwargs):
        from spydrnet.util import get_pins
        return get_pins(self, *args, **kwargs)

    def get_cables(self, *args, **kwargs):
        from spydrnet.util import get_cables
        return get_cables(self, *args, **kwargs)

    def get_wires(self, *args, **kwargs):
        from spydrnet.util import get_wires
        return get_wires(self, *args, **kwargs)

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
