# Copyright 2020 Dallin Skouson, Andrew Keller, Michael Wirthlin

from spydrnet.ir import *
from collections import deque
from spydrnet.uniquify import uniquify

"""How to flatten (brainstorm):
start at the top and take all of the subelements out and add them to the top definition
Naming will be dificult but I will just skip that for now to get it working.
"""

unique_number = 0

mod_name_uid = 0


def _get_unique_name_modifier():
    global mod_name_uid
    str_out = "sdn_flat_" + str(mod_name_uid)
    mod_name_uid += 1
    return str_out


def _rename_element(e):
    global unique_number
    e.name = e.name + "_flat_" + str(unique_number)
    unique_number += 1


def _redo_connections(instance, port):
    for pin in port.pins:
        out_pin = instance.pins[pin]
        out_wire = out_pin.wire
        in_pin = pin
        in_wire = in_pin.wire

        if in_wire:
            in_wire.disconnect_pin(in_pin)
        if out_wire:
            out_wire.disconnect_pin(out_pin)

        pins_to_move = []
        if in_wire:
            for p in in_wire.pins:
                # if p != in_pin:
                pins_to_move.append(p)

        if out_wire:
            for p in pins_to_move:
                in_wire.disconnect_pin(p)
                out_wire.connect_pin(p)


def _bring_to_top(e, add_to_name, top_definition):
    """move the cable that is internal to the top level."""
    if "EDIF.identifier" in e:
        global mod_name_uid
        good = False
        if mod_name_uid == 45773:
            print(e["EDIF.identifier"])
            print(e)
            good = True
        if isinstance(e, Cable):
            e["EDIF.identifier"] = "cable_" + _get_unique_name_modifier()
        else:
            e["EDIF.identifier"] = "instance_" + _get_unique_name_modifier()

        if good:
            print(e["EDIF.identifier"])
    if isinstance(e, Cable):
        d = e.definition
        d.remove_cable(e)
    else:
        d = e.parent
        d.remove_child(e)
    # _rename_element(c)
    if(add_to_name != ''):
        e.name = add_to_name + "/" + e.name
    else:
        e.name = e.name
    if isinstance(e, Cable):
        top_definition.add_cable(e)
    else:
        top_definition.add_child(e)


# def simple_recursive_netlist_visualizer(netlist):
#     #TODO put this code somewhere where people can use it to visualize simple netlists
#     top_instance = netlist.top_instance
#     #should look something like this:
#     #top
#     #   child1
#     #       child1.child
#     #   child2
#     #       child2.child
#     def recurse(instance, depth):
#         s = depth * "\t"
#         print(s, instance.name, "(", instance.reference.name, ")")
#         for c in instance.reference.children:
#             recurse(c, depth + 1)

#     recurse(top_instance, 0)

def flatten(netlist):
    """
    starts at the top instance and brings all the different subelements to the top level.
    and port boundries are redone into one net.
    """

    # get all the sub instances of the top instance
    instance_queue = deque()
    name_queue = deque()
    top_instance = netlist.top_instance
    top_definition = top_instance.reference
    # put all of tops children on a stack
    for chld in top_definition.children:
        instance_queue.append(chld)
        name_queue.append('')

    to_remove = []
    # for each of the children on the stack
    while len(instance_queue) > 0:
        inst = instance_queue.popleft()
        parent_name = name_queue.popleft()
        # simple_recursive_netlist_visualizer(netlist)
        _bring_to_top(inst, parent_name, top_definition)
        if inst.reference.is_leaf():
            continue
        # put their children on the stack
        for child in inst.reference.children:
            instance_queue.append(child)
            name_queue.append(inst.name)
        temp_cables = []
        for cable in inst.reference.cables:
            temp_cables.append(cable)
        for cable in temp_cables:
            _bring_to_top(cable, inst.name, top_definition)
        for port in inst.reference.ports:
            _redo_connections(inst, port)
        to_remove.append(inst)
    for i in to_remove:
        top_definition.remove_child(i)


# mkdir export
# cd export
# write_edif
# write_xdc -constraints all leon3mp.xdc
