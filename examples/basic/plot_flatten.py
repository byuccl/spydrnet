"""
=====================================
Flattens a netlist
=====================================

Remove hierarchy from a netlist.
"""

import spydrnet as sdn

# Check if given instance is a black box
# instance: std.Instance to check
# Return True if instance is a black box
# (defined by no listed cables or child within child's reference), else return False
def is_black_box(instance):
    definition = instance.reference
    if len(definition.cables) is not 0 or len(definition.children) is not 0:
        return False
    return True


# Creates a copy of a instance
def copy_instance(parent_instance, instance, new_instance):
    for key, value in instance.data.items():
        new_instance[key] = value
    new_instance['EDIF.identifier'] = parent_instance['EDIF.identifier'] + '_' + new_instance['EDIF.identifier']
    if 'EDIF.original_identifier' in parent_instance:
        if 'EDIF.original_identifier' in instance:
            new_instance['EDIF.original_identifier'] = parent_instance['EDIF.original_identifier'] + '/' \
                                                       + instance['EDIF.original_identifier']
        else:
            new_instance['EDIF.original_identifier'] = parent_instance['EDIF.original_identifier'] + '/' \
                                                       + instance['EDIF.identifier']
    else:
        if 'EDIF.original_identifier' in instance:
            new_instance['EDIF.original_identifier'] = parent_instance['EDIF.identifier'] + '/' \
                                                       + instance['EDIF.original_identifier']
        else:
            new_instance['EDIF.original_identifier'] = parent_instance['EDIF.identifier'] + '/' \
                                                       + instance['EDIF.identifier']
    new_instance.reference = instance.reference


def use_outside_cable(new_cable, old_cable, instance):
    wire = None
    for pin in old_cable.wires[0].pins:
        if pin in instance.pins:
            wire = instance.pins[pin].wire
            break
    for new_wire in new_cable.wires:
        for pin in new_wire.pins:
            new_wire.disconnect_pin(pin)
            wire.connect_pin(pin)
    new_cable.definition.remove_cable(new_cable)


def clean_up(instance):
    for pin in instance.pins.values():
        pin.wire.disconnect_pin(pin)
    instance.parent.remove_child(instance)

# Recursively flatten a given definition
def flatten_definition(definition):
    children = definition.children.copy()
    created = list()
    for child in children:
        leaf_grandchildren = list()
        child_reference = child.reference
        grandchildren = child_reference.children.copy()
        map = dict()
        for grandchild in grandchildren:
            if not is_black_box(grandchild):
                print("Need to also flatten", child['EDIF.identifier'], "that references", child.reference['EDIF.identifier'])
                leaf_grandchildren.extend(flatten_definition(child.reference))
            else:
                leaf_grandchildren.append(grandchild)
        for grandchild in leaf_grandchildren:
            new_instance = definition.create_child()
            copy_instance(child, grandchild, new_instance)
            map[grandchild] = new_instance
            created.append(new_instance)
        # TODO Copy Cables from within grandchild definition to flatten or reuse cables connecting to instance
        cables = child_reference.cables.copy()
        for cable in cables:
            name_cable = True
            new_cable = definition.create_cable()
            for wire in cable.wires:
                new_wire = new_cable.create_wire()
                for pin in wire.pins:
                    if isinstance(pin, sdn.InnerPin):
                        name_cable = False
                        continue
                    new_wire.connect_pin(map[pin.instance].pins[pin.inner_pin])
            if name_cable:
                new_cable['EDIF.identifier'] = child['EDIF.identifier'] + '_' + cable['EDIF.identifier']
            else:
                use_outside_cable(new_cable, cable, child)
        if not is_black_box(child):
            clean_up(child)
    print("Finished flattening", definition['EDIF.identifier'])
    return created



example_name1 = "unique_challenge"
example_name2 = "three_layer_hierarchy"
example_name = example_name1
ir = sdn.load_example_netlist_by_name(example_name)
#ir = sdn.load_example_netlist_by_name("unique_challenge")
top_def = ir.top_instance.reference
for child in top_def.children:
    if child['EDIF.identifier'] == 'a0':
        test2 = child.reference
        for inner_child in child.reference.children:
            if inner_child['EDIF.identifier'] == 'b0':
                test = inner_child.reference
        break
flatten_definition(top_def)

from spydrnet.composers.edif.composer import ComposeEdif
compose = ComposeEdif()
file_name = "C:\\hold\\" + example_name + '_flat.edf'
compose.run(ir, file_name)

# sdn.composers.compose("test.edf", ir)
print()