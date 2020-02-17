from spydrnet.callback.callback_listener import CallbackListener
from spydrnet.ir import Library, Definition, Instance, Port, Cable


class DefaultNamespaceManager(CallbackListener):
    def __init__(self):
        super().__init__()
        self.netlists_namespace = dict()  # name -> netlist
        self.library_namespaces = dict()  # netlist -> libraries_namespace; name -> library
        self.definition_namespaces = dict()  # library -> definitions_namespace; name -> definition
        self.port_namespaces = dict()  # definition -> ports_namespace; name -> port
        self.cable_namespaces = dict()  # definition -> cables_namespace; name -> cable
        self.instance_namespaces = dict()  # definition -> instance_namespace; name -> instance
