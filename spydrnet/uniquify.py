# Copyright 2020 Dallin Skouson, Andrew Keller, Michael Wirthlin

from collections import deque
# from spydrnet.ir import *

"""Code to make definitions unique throughout a netlist.
expected parameters,
uniqify -- Makes all definitions unique below the top instance. definitions that are not referenced below the top instance will not be unique.
"""


MOD_NAME_UID = 0


def _get_unique_name_modifier():
    global MOD_NAME_UID
    str_out = "_sdn_unique_" + str(MOD_NAME_UID)
    MOD_NAME_UID += 1
    return str_out


def _make_instance_unique(instance):
    """clone the definition and point the reference to the new definition"""
    reference = instance.reference
    lib = instance.reference.library
    index = lib.definitions.index(reference)
    new_def = instance.reference.clone()
    if instance.reference.name is not None:
        name = instance.reference.name
        unique_suffix = _get_unique_name_modifier()
        new_def.name = name + unique_suffix
        if 'EDIF.identifier' in new_def:
            new_def['EDIF.identifier'] = new_def['EDIF.identifier'] + \
                unique_suffix
    lib.add_definition(new_def, index + 1)
    instance.reference = new_def


def _is_unique(instance):
    """Return if the instance is the only one of its kind in the definition"""
    return len(instance.reference.references) == 1 or instance.reference.is_leaf()


def uniquify(netlist):
    """Make the instances in the netlist unique
    uniqification is done in place. Each instance will correspond to exactly one definition and each definition will correspond to exactly one instance with the exception of leaf cells.
    Leaf cells are can be instanced unlimited numbers of times. Any netlist elements that are not instantiated by the top instance will not be modified and may retain duplicate instances
    Currently there is no guarantee that the original definition names will be maintained, but it is guaranteed that they will be unique within the scope of all hardware that is below the top instance.

    Renaming is predictable. the string: _sdn_unique_# will be added to the end of the definition names.

    :param netlist: the netlist that will be uniquified

    :return: void

    """

    # import pdb; pdb.set_trace()
    # starting with top.
    # top must be unique below top. otherwise we have infinite harware recursion which is does not make much sense.
    instance_queue = deque()

    top_instance = netlist.top_instance

    top_definition = top_instance.reference

    # put all of tops children on a stack
    for chld in top_definition.children:
        instance_queue.append(chld)

    # for each of the children on the stack
    while len(instance_queue) > 0:
        inst = instance_queue.popleft()
        # if they are not unique
        if not _is_unique(inst):
            # uniquify
            _make_instance_unique(inst)
        # put their children on the stack
        for chld in inst.reference.children:
            instance_queue.append(chld)
