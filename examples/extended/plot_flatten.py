"""
=====================================
Flatten A Netlist
=====================================

Remove hierarchy from a netlist. The original hierarchy and new hierarchy (after flattening) will be printed.
"""

import os
import tempfile
import spydrnet as sdn


# Check if given instance is a black box
# instance: std.Instance to check
# Return True if instance is a black box
# (defined by no listed cables or child within child's reference), else return False
def is_black_box(instance):
    definition = instance.reference
    if len(definition.cables) != 0 or len(definition.children) != 0:
        return False
    return True


# Creates a copy of a instance
# parent_instance: The instance that contains the instance be copy (used to keep hierarchical naming)
# instance: The original instance to make the copy of
# new_instance: The instance that will be the copy
# Returns: None
def copy_instance(parent_instance, instance, new_instance):
    # Copy all the data from instance into new_instance
    for key, value in instance.data.items():
        new_instance[key] = value
    # Change new_instance EDIF.identifier to represent its hierarchical name
    new_instance['EDIF.identifier'] = parent_instance['EDIF.identifier'] + \
        '_' + new_instance['EDIF.identifier']
    # Determine if parent_instance and instance have .NAME in it data
    # Uses .NAME if available, else used EDIF.identifier to generate
    # .NAME for new_instance
    if '.NAME' in parent_instance:
        if '.NAME' in instance:
            new_instance['.NAME'] = parent_instance['.NAME'] + '/' \
                + instance['.NAME']
        else:
            new_instance['.NAME'] = parent_instance['.NAME'] + '/' \
                + instance['EDIF.identifier']
    else:
        if '.NAME' in instance:
            new_instance['.NAME'] = parent_instance['EDIF.identifier'] + '/' \
                + instance['.NAME']
        else:
            new_instance['.NAME'] = parent_instance['EDIF.identifier'] + '/' \
                + instance['EDIF.identifier']
    # Have new_instance reference the same definition as instance
    new_instance.reference = instance.reference


# Removes a newly created cable in favor of using the cable that connected to the outside of the instance
# new_cable: Cable that was connecting the new pins instance's parent
# old_cable: Cable that was connecting the old pins in instance
# instance: The instance that is being flatten
# Return: None
def use_outside_cable(new_cable, old_cable, instance):
    wire = None
    # Need to find the wire that connects to the outside of the port that old_cable does
    # Check each pin that old_cable is connected to to find the inside pin for the instance
    for pin in old_cable.wires[0].pins:
        if pin in instance.pins:
            # Get the wire that connects to the outer pin that corresponds to the found inner pin
            wire = instance.pins[pin].wire
            break
    # Loop through each wire in new_cable
    for new_wire in new_cable.wires:
        # Loop through is pin the wire connects to
        for pin in new_wire.pins:
            # Disconnect the new_wire from the pin and connect wire to that pin instead
            new_wire.disconnect_pin(pin)
            wire.connect_pin(pin)
    # Removes new_cable from the definition that holds it
    new_cable.definition.remove_cable(new_cable)


# Remove instances that have been flatten
# instance: std.Instance to be removed
# Returns None
def clean_up(instance):
    # Loop through each outside pin and disconnect it from its wire
    for pin in instance.pins.values():
        pin.wire.disconnect_pin(pin)
    # Remove instances from its parent definition
    instance.parent.remove_child(instance)


# Recursively flatten a given definition
# definition: std.Definition to flatten
# top_definition: Bool saying the given definition is the top definition of the IR
# Returns: list of created instances
def flatten_definition(definition, top_definition=False):
    # Create a copy of the list of children
    children = definition.children.copy()
    created = list()
    # Loop through each pre-existing child of the definition
    for child in children:
        leaf_grandchildren = list()
        child_reference = child.reference
        # Create a copy of the list of the children for the current child reference
        grandchildren = child_reference.children.copy()
        map = dict()
        # Check if progress information should be printed
        if top_definition and not is_black_box(child):
            print("Need to move cells from", child['EDIF.identifier'],
                  "that references", child.reference['EDIF.identifier'])
        # Loop through each grandchild of definition
        for grandchild in grandchildren:
            if not is_black_box(grandchild):
                print("Need to move cells from", grandchild['EDIF.identifier'],
                      "that references", grandchild.reference['EDIF.identifier'])
                # Flatten any children if they contain non_leaf grandchildren
                # Keep track of grandchildren that are leaf nodes
                leaf_grandchildren.extend(flatten_definition(child.reference))
                print("Finished moving cells from",
                      grandchild['EDIF.identifier'])
            else:
                # Keep track of grandchildren that are leaf nodes
                leaf_grandchildren.append(grandchild)
        # Loop though each grandchild that is also a leaf including newly created grandchildren
        for grandchild in leaf_grandchildren:
            # Create a new child inside of definition
            new_instance = definition.create_child()
            # Copy data from the grandchild into the new instance
            copy_instance(child, grandchild, new_instance)
            # Create a key, value relationship between grandchild and new_instance
            map[grandchild] = new_instance
            # Add the new_instances to the list of created instances
            created.append(new_instance)
        # Create a list of the original cables that the child has
        cables = child_reference.cables.copy()
        for cable in cables:
            name_cable = True
            new_cable = definition.create_cable()
            for wire in cable.wires:
                new_wire = new_cable.create_wire()
                for pin in wire.pins:
                    # If the pin is connected to a port of the child, we should use an outside cable instead
                    if isinstance(pin, sdn.InnerPin):
                        name_cable = False
                        continue
                    # Connect the new wire to pins on new instances that correspond pins on the original instances
                    new_wire.connect_pin(map[pin.instance].pins[pin.inner_pin])
            # Check if we should name the cable or should use the outside cable
            if name_cable:
                new_cable['EDIF.identifier'] = child['EDIF.identifier'] + \
                    '_' + cable['EDIF.identifier']
                new_cable.name = new_cable['EDIF.identifier']
            else:
                use_outside_cable(new_cable, cable, child)
        # Remove any original children that is not a leaf
        if not is_black_box(child):
            clean_up(child)
        # Check if progress information should be printed
        if top_definition and not is_black_box(child):
            print("Finished moving cells from", child['EDIF.identifier'])
    return created

#print the hierarchy of a netlist
def hierarchy(current_instance,indentation=""):
    print(indentation,current_instance.name)
    for child in current_instance.reference.children:
        hierarchy(child,indentation+"   ")


example_name1 = "unique_challenge"
example_name2 = "three_layer_hierarchy"
example_name3 = "unique_different_modules"
example_name = example_name1
ir = sdn.load_example_netlist_by_name(example_name)
ir_orig = sdn.load_example_netlist_by_name(example_name) #store the original netlist for display later
top_def = ir.top_instance.reference
flatten_definition(top_def, top_definition=True)

with tempfile.TemporaryDirectory() as td:
    file_name = example_name + '_flat.edf'
    sdn.compose(ir, os.path.join(td, file_name))

# sdn.composers.compose("test.edf", ir)
print()

print("ORIGINAL HIERARCHY")
hierarchy(ir_orig.top_instance)
print("\nHIERARCHY AFTER FLATTENING")
hierarchy(ir.top_instance)