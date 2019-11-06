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

def create_connectivity_graph(with_top_level_virtual_ports=True):
    C = nx.DiGraph()

    if with_top_level_virtual_ports:
        # find all top level ports and add them to the graph
        top_level_virtual_ports = set(current_virtual_instance().virtualPorts.values())
        # top_level_virtual_ports = set(get_virtual_ports(of=current_virtual_instance()))
        C.add_nodes_from(top_level_virtual_ports)

        # add all source to sink edges
        for tlvpo in filter(lambda tlvpo: tlvpo.direction in {IN, INOUT}, top_level_virtual_ports):
            source_vpis = tlvpo.virtualPins.values()
            # source_vpis = get_virtual_pins(of=virtual_port)
            for source_vpi in source_vpis:
                vws = get_virtual_wires(of=source_vpi, selection=ALL)
                all_vpis = set()
                for vpis in (vw.get_virtualPins() for vw in vws):
                    for vpi in vpis:
                        if vpi is not source_vpi:
                            all_vpis.add(vpi)
                # all_vpis = list(get_virtual_pins(of=vws, filter = lambda vpi: vpi is not source_vpi))
                sink_tlvpos = set(vpi.virtualParent for vpi in all_vpis \
                                  if vpi.virtualParent in top_level_virtual_ports and\
                                      vpi.direction in {OUT, INOUT})
                # sink_vpis_tlvpos = filter(lambda vpi: vpi.direction in {OUT, INOUT}, all_vpis)
                # sink_tlvpos = get_virtual_ports(of=sink_vpis_tlvpos, filter = lamdba vpo: vpo in top_level_virtual_ports)
                sink_vpis_vis = filter(lambda vpi: vpi.direction in {IN, INOUT}, all_vpis)
                sink_vis = get_virtual_instances(of=sink_vpis_vis, filter=lambda vi: vi.is_leaf())

                for sink_tlvpo in sink_tlvpos:
                    C.add_edge(tlvpo, sink_tlvpo)

                for sink_vi in sink_vis:
                    C.add_edge(tlvpo, sink_vi)
        
        # add all sink from source
        for tlvpo in filter(lambda tlvpo: tlvpo.direction in {OUT, INOUT}, top_level_virtual_ports):
            sink_vpis = tlvpo.virtualPins.values()
            # sink_vpis = get_virtual_pins(of=virtual_port)
            for sink_vpi in sink_vpis:
                vws = get_virtual_wires(of=sink_vpi, selection=ALL)
                all_vpis = set()
                for vpis in (vw.get_virtualPins() for vw in vws):
                    for vpi in vpis:
                        if vpi is not sink_vpi:
                            all_vpis.add(vpi)
                # all_vpis = list(get_virtual_pins(of=vws, filter = lambda vpi: vpi is not source_vpi))
                source_tlvpos = set(vpi.virtualParent for vpi in all_vpis \
                                  if vpi.virtualParent in top_level_virtual_ports and\
                                      vpi.direction in {IN, INOUT})
                # source_vpis_tlvpos = filter(lambda vpi: vpi.direction in {IN, INOUT}, all_vpis)
                # source_tlvpos = get_virtual_ports(of=sink_vpis_tlvpos, filter = lamdba vpo: vpo in top_level_virtual_ports)
                source_vpis_vis = filter(lambda vpi: vpi.direction in {OUT, INOUT}, all_vpis)
                source_vis = get_virtual_instances(of=source_vpis_vis, filter=lambda vi: vi.is_leaf())

                for source_tlvpo in source_tlvpos:
                    C.add_edge(source_tlvpo, tlvpo)

                for source_vi in source_vis:
                    C.add_edge(source_vi, tlvpo)

    # Find all leafcells and add them to the graph
    leafcells = set(get_virtual_instances(hierarchical = True, filter = lambda x: x.is_leaf()))
    C.add_nodes_from(leafcells)

    # add all source to sink edges
    for source_vi in leafcells:
        source_vpos = (vpo for vpo in source_vi.virtualPorts.values() if vpo.direction in {OUT, INOUT})
        # source_vpos = get_virtual_ports(of=source_vi, filter=lambda vpo: vpo.direction in {OUT, INOUT})
        for source_vpo in source_vpos:
            source_vpis = source_vpo.virtualPins.values()
            for source_vpi in source_vpis:
                vws = get_virtual_wires(of=source_vpi, selection=ALL)
                all_vpis = set()
                for vpis in (vw.get_virtualPins() for vw in vws):
                    for vpi in vpis:
                        if vpi is not sink_vpi:
                            all_vpis.add(vpi)
                # all_vpis = list(get_virtual_pins(of=vws, filter=lambda vpi: vpi is not source_vpi))
                sink_tlvpos = set(vpi.virtualParent for vpi in all_vpis \
                                  if vpi.virtualParent in top_level_virtual_ports and\
                                      vpi.direction in {OUT, INOUT})
                # sink_vpis_tlvpos = filter(lambda vpi: vpi.direction in {OUT, INOUT}, all_vpis)
                # sink_tlvpos = get_virtual_ports(of=sink_vpis_tlvpos, filter = lamdba vpo: vpo in top_level_virtual_ports)
                sink_vpis_vis = filter(lambda vpi: vpi.direction in {IN, INOUT}, all_vpis)
                sink_vis = get_virtual_instances(of=sink_vpis_vis, filter=lambda vi: vi.is_leaf())

                for sink_tlvpo in sink_tlvpos:
                    C.add_edge(source_vi, sink_tlvpo)

                for sink_vi in sink_vis:
                    C.add_edge(source_vi, sink_vi)

    return C