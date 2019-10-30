from spydrnet.global_environment_manager import current_netlist, current_virtual_instance, get_netlists, create_netlist

from spydrnet.api.get_virtual_instances import get_virtual_instances
from spydrnet.api.get_virtual_wires import Selection, get_virtual_wires

from spydrnet.ir import Environment, Library, Definition, Port, InnerPin, OuterPin, Cable, Wire
from spydrnet.virtual_ir import VirtualInstance, VirtualPort, VirtualPin, VirtualCable, VirtualWire, hierarchical_seperator

import networkx as nx

import os
import fnmatch
import re

OUT       = Port.Direction.OUT
IN        = Port.Direction.IN
INOUT     = Port.Direction.INOUT
UNDEFINED = Port.Direction.UNDEFINED

INSIDE  = Selection.INSIDE
OUTSIDE = Selection.OUTSIDE
BOTH    = Selection.BOTH
ALL     = Selection.ALL
    
def parse(filename):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    if extension_lower in [".edf", ".edif"]:
        from spydrnet.parsers.edif.parser import EdifParser
        parser = EdifParser.from_filename(filename)
        parser.parse()
        return current_netlist(parser.netlist)
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))

def get_virtual_ports(*args, **kwargs):
    pass

def get_virtual_pins(*args, **kwargs):
    pass

def get_virtual_cables(*args, **kwargs):
    pass

def get_libraries(*args, **kwargs):
    pass

def get_definitions(*args, **kwargs):
    pass

def get_instances(*args, **kwargs):
    pass

def get_ports(*args, **kwargs):
    pass

def get_pins(*args, **kwargs):
    pass

def get_cables(*args, **kwargs):
    pass

def get_wires(*args, **kwargs):
    pass

def create_connectivity_graph(with_top_level_ports=True):
    C = nx.DiGraph()

    if with_top_level_ports:
        top_level_ports = set(current_virtual_instance().virtualPorts.values())
        C.add_nodes_from(top_level_ports)

    leafcells = set(get_virtual_instances(filter = lambda x: x.is_leaf()))
    C.add_nodes_from(leafcells)

    if with_top_level_ports:
        for port in top_level_ports:
            virtual_pins = (x for x in port if x.direction in {OUT, INOUT})
            virtual_wires = get_virtual_wires(of=virtual_pins, selection=ALL)