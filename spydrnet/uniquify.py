#Copyright 2020 Dallin Skouson, Andrew Keller, Michael Wirthlin

from spydrnet.ir import *
from collections import deque

'''code to make definitions unique throughout a netlist. 
expected parameters,
uniqify -- makes all definitions unique below the top instance. definitions that are not referenced below the top instance will not be unique.
'''


mod_name_uid = 0
def _get_unique_name_modifier():
    global mod_name_uid
    str_out = str(mod_name_uid)
    mod_name_uid += 1
    return str_out

def _make_instance_unique(instance):
    '''clone the definition and point the reference to the new definition'''
    lib = instance.reference.parent
    name = instance.reference["NAME"]
    instance.reference = instance.reference.clone()
    instance.reference['NAME'] = name + _get_unique_name_modifier()


def _is_unique(instance):
    '''return if the instance is the only one of its kind in the definition'''
    return len(instance.reference.references) == 1 or instance.reference.is_leaf()

def uniqify(netlist):
    #TODO remove this line:
    
    

    #starting with top.
    #top must be unique below top. otherwise we have infinite harware recursion which is does not make much sense.    
    instance_queue = deque()

    top_instance = netlist.top_instance

    top_definition = top_instance.reference

    #put all of tops children on a stack
    for ref in top_definition.references:
        instance_queue.append(ref)

    #for each of the children on the stack
    while len(instance_queue) > 0:
        inst = instance_queue.popleft()
        #if they are not unique
        if not _is_unique(inst):
            #uniquify
            _make_instance_unique(inst)
        #put their children on the stack
        for ref in inst.reference.references:
            instance_queue.append(ref)