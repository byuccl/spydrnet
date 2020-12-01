class GetterShortcuts:
    __slots__ = tuple()

    def get_netlists(self, *args, **kwargs):
        """get_netlists(...)

        Shortcut to :py:func:`~spydrnet.get_netlists`.
        """
        from spydrnet.util import get_netlists
        return get_netlists(self, *args, **kwargs)

    def get_libraries(self, *args, **kwargs):
        """get_libraries(...)

        Shortcut to :py:func:`~spydrnet.get_libraries`.
        """
        from spydrnet.util import get_libraries
        return get_libraries(self, *args, **kwargs)

    def get_definitions(self, *args, **kwargs):
        """get_definitions(...)

        Shortcut to :py:func:`~spydrnet.get_definitions`.
        """
        from spydrnet.util import get_definitions
        return get_definitions(self, *args, **kwargs)

    def get_instances(self, *args, **kwargs):
        """get_instances(...)

        Shortcut to :py:func:`~spydrnet.get_instances`.
        """
        from spydrnet.util import get_instances
        return get_instances(self, *args, **kwargs)

    def get_ports(self, *args, **kwargs):
        """get_ports(...)

        Shortcut to :py:func:`~spydrnet.get_ports`.
        """
        from spydrnet.util import get_ports
        return get_ports(self, *args, **kwargs)

    def get_pins(self, *args, **kwargs):
        """get_pins(...)

        Shortcut to :py:func:`~spydrnet.get_pins`.
        """
        from spydrnet.util import get_pins
        return get_pins(self, *args, **kwargs)

    def get_cables(self, *args, **kwargs):
        """get_cables(...)

        Shortcut to :py:func:`~spydrnet.get_cables`.
        """
        from spydrnet.util import get_cables
        return get_cables(self, *args, **kwargs)

    def get_wires(self, *args, **kwargs):
        """get_wires(...)

        Shortcut to :py:func:`~spydrnet.get_wires`.
        """
        from spydrnet.util import get_wires
        return get_wires(self, *args, **kwargs)

    def get_hinstances(self, *args, **kwargs):
        """get_hinstances(...)

        Shortcut to :py:func:`~spydrnet.get_hinstances`.
        """
        from spydrnet.util import get_hinstances
        return get_hinstances(self, *args, **kwargs)

    def get_hports(self, *args, **kwargs):
        """get_hports(...)

        Shortcut to :py:func:`~spydrnet.get_hports`.
        """
        from spydrnet.util import get_hports
        return get_hports(self, *args, **kwargs)

    def get_hpins(self, *args, **kwargs):
        """get_hpins(...)

        Shortcut to :py:func:`~spydrnet.get_hpins`.
        """
        from spydrnet.util import get_hpins
        return get_hpins(self, *args, **kwargs)

    def get_hcables(self, *args, **kwargs):
        """get_hcables(...)

        Shortcut to :py:func:`~spydrnet.get_hcables`.
        """
        from spydrnet.util import get_hcables
        return get_hcables(self, *args, **kwargs)

    def get_hwires(self, *args, **kwargs):
        """get_hwires(...)

        Shortcut to :py:func:`~spydrnet.get_hwires`.
        """
        from spydrnet.util import get_hwires
        return get_hwires(self, *args, **kwargs)
