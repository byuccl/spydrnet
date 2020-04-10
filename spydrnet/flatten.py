#Copyright 2020 Dallin Skouson, Andrew Keller, Michael Wirthlin

from spydrnet.ir import *
from collections import deque
from spydrnet.uniquify import uniquify

'''How to flatten (brainstorm):
start at the top and take all of the subelements out and add them to the top definition
Naming will be dificult but I will just skip that for now to get it working.
'''

unique_number = 0

mod_name_uid = 0
def _get_unique_name_modifier():
    global mod_name_uid
    str_out = "_sdn_unique_" + str(mod_name_uid)
    mod_name_uid += 1
    return str_out

def _rename_element(e):
    global unique_number
    e.name = e.name + "_flat_" + str(unique_number)
    unique_number += 1

def _redo_connections(inst):
    for pin in inst.pins:
        out_wire = pin.wire
        in_pin = pin.inner_pin
        in_wire = in_pin.wire
        in_wire = Wire()
        pins_to_move = []
        for p in in_wire.pins:
            if p != pin:
                pins_to_move.append(p)
        for p in pins_to_move:
            in_wire.disconnect_pin(p)
            out_wire.connect_pin(p)
        out_wire.disconnect_pin(pin)

def _bring_to_top_cable(c,top_definition):
    '''move the cable that is internal to the top level.'''
    d = c.definition
    add_to_name = d.name
    d.remove_cable(c)
    #_rename_element(c)
    c.name = add_to_name + "/" + c.name
    top_definition.add_child(c)

def _bring_to_top_inst(i, top_definition):
    '''move the instance that is internal to the top level.'''
    #just remove the instance/cable from the definition to which it belongs then add it to the top definition
    d = i.parent
    add_to_name = d.name
    d.remove_child(i)
    #_rename_element(i)
    i.name = add_to_name + "/" + i.name
    top_definition.add_child(i)
    
def simple_recursive_netlist_visualizer(netlist):
    #TODO put this code somewhere where people can use it to visualize simple netlists
    top_instance = netlist.top_instance
    #should look something like this:
    #top
    #   child1
    #       child1.child
    #   child2
    #       child2.child
    def recurse(instance, depth):
        s = depth * "\t"
        print(s, instance.name, "(", instance.reference.name, ")")
        for c in instance.reference.children:  
            recurse(c, depth + 1)
    
    recurse(top_instance, 0)

def flatten(netlist):
    '''
    starts at the top instance and brings all the different subelements to the top level.
    and port boundries are redone into one net.
    '''

    #get all the sub instances of the top instance
    instance_queue = deque()
    top_instance = netlist.top_instance
    top_definition = top_instance.reference
    #put all of tops children on a stack
    for chld in top_definition.children:
        instance_queue.append(chld)

    to_remove = []
    #for each of the children on the stack
    while len(instance_queue) > 0:
        inst = instance_queue.popleft()
        # simple_recursive_netlist_visualizer(netlist)
        _bring_to_top_inst(inst, top_definition)
        if inst.reference.is_leaf():
            continue
        #put their children on the stack
        for child in inst.reference.children:
            instance_queue.append(child)
        temp_cables = []
        for cable in inst.reference.cables:
            temp_cables.append(cable)
        for cable in temp_cables:
            _bring_to_top_cable(cable, top_definition)
        
        _redo_connections(inst)
        to_remove.append(inst)
    for i in to_remove:
        top_definition.remove_child(i)


#mkdir export
#cd export
#write_edif
#write_xdc -constraints all leon3mp.xdc
