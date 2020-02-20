import weakref
from spydrnet.plugins.namespace_manager import NamespaceManager

_current_netlist = None
_current_namespace_manager = None
_alive_netlists = weakref.WeakSet()


def get_current_netlist():
    return current_netlist()


def set_current_netlist(net):
    current_netlist(net)


def current_netlist(*args):
    args_len = len(args)
    if args_len == 1:
        global _current_netlist
        _current_netlist = args[0]
    elif args_len != 0:
        raise TypeError("current_netlist() takes upto 1 positional argument but {} were given".format(args_len))
    return _current_netlist


def get_netlists(*args, **kwargs):
    return (x for x in _alive_netlists)


def current_namespace_manager(*args):
    args_len = len(args)
    if args_len == 1:
        global _current_namespace_manager
        _current_namespace_manager = args[0]
    elif args_len != 0:
        raise TypeError("current_namespace_manager() takes upto 1 positional argument but {} were given".format(
            args_len))
    return _current_namespace_manager


def _call_create_netlist(netlist):
    _alive_netlists.add(netlist)


def _call_create_library(library):
    pass


def _call_create_definition(definition):
    pass


def _call_create_port(port):
    pass


def _call_create_cable(cable):
    pass


def _call_create_instance(instance):
    pass
