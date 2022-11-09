"""
=====================================
Make Instances Unique
=====================================

Creates definitions for non-leaf instances so each instance has its own definition. Each library in both the original and the uniquified netlist will be printed along with each's definitions.
"""

import os
import tempfile
import spydrnet as sdn
import collections


# Check if given instance is a black box
# instance: std.Instance to check
# Return True if instance is a black box
# (defined by no listed cables or child within child's reference), else return False
def is_black_box(instance):
    definition = instance.reference
    if len(definition.cables) != 0 or len(definition.children) != 0:
        return False
    return True


def increment_definition_count(definition):
    if definition not in definition_count:
        definition_count[definition] = 1
    else:
        definition_count[definition] += 1


def trace_definition(definition):
    top_order = collections.deque()
    for child in definition.children:
        if len(child.pins) == 0:
            return top_order
        inner_pin = list(child.pins.keys())[0]
        if inner_pin.wire is None:
            continue
        top_order.extend(trace_definition(child.reference))
    top_order.append(definition)
    increment_definition_count(definition)
    return top_order


def get_reverse_topological_order(ir):
    depth_first_search = collections.deque()
    for child in top_def.children:
        if not is_black_box(child):
            depth_first_search.extend(trace_definition(child.reference))
    visited = set()
    reverse_topological_order = list()
    while len(depth_first_search) != 0:
        definition = depth_first_search.popleft()
        if definition not in visited:
            visited.add(definition)
            reverse_topological_order.append(definition)
    return reverse_topological_order


def copy_metadata(original, copy, copy_num=None):
    for key, data in original.data.items():
        copy[key] = data
    if type(original) is sdn.Definition:
        if 'EDIF.identifier' in copy.data:
            while copy['EDIF.identifier'] + '_UNIQUE_' + str(copy_num) in definition_count:
                copy_num += 1
            definition_count[copy['EDIF.identifier'] +
                             '_UNIQUE_' + str(copy_num)] = 1
            copy['EDIF.identifier'] = copy['EDIF.identifier'] + \
                '_UNIQUE_' + str(copy_num)
        if '.NAME' in copy.data:
            copy['.NAME'] = copy['.NAME'] + '_UNIQUE_' + str(copy_num)


def copy_ports(original, copy):
    for original_port in original.ports:
        new_port = copy.create_port()
        copy_metadata(original_port, new_port)
        new_port.direction = original_port.direction
        for original_inner_pin in original_port.pins:
            original_inner_pin_to_new_inner_pin[original_inner_pin] = new_port.create_pin(
            )
        if hasattr(original_port, 'is_array'):
            new_port.is_array = original_port.is_array
        if hasattr(original_port, 'is_scalar'):
            new_port.is_scalar = original_port.is_scalar


def make_instances_unique(instance):
    if len(definition_copies[instance.reference]) == 0:
        return
    definition = definition_copies[instance.reference].pop()
    # instance.reference = None
    instance.reference = definition


def copy_children(original, copy):
    for original_child in original.children:
        new_child = copy.create_child()
        copy_metadata(original_child, new_child)
        new_child.reference = original_child.reference
        for pin in original_child.pins.keys():
            outer_pin_map[original_child.pins[pin]] = new_child.pins[pin]
        if not is_black_box(original_child):
            make_instances_unique(new_child)
        instance_map[original_child] = new_child


def copy_cable(original, copy):
    for original_cable in original.cables:
        new_cable = copy.create_cable()
        copy_metadata(original_cable, new_cable)
        for original_wire in original_cable.wires:
            new_wire = new_cable.create_wire()

            for original_pin in original_wire.pins:
                if isinstance(original_pin, sdn.InnerPin):
                    new_wire.connect_pin(
                        original_inner_pin_to_new_inner_pin[original_pin])
                else:
                    new_wire.connect_pin(outer_pin_map[original_pin])


def copy_definition(def_to_copy, def_copy, i):
    copy_metadata(def_to_copy, def_copy, i)
    copy_ports(def_to_copy, def_copy)
    copy_children(def_to_copy, def_copy)
    copy_cable(def_to_copy, def_copy)


def definition_clean_up(definition):
    if definition in definition_copies:
        for child in definition.children:
            if child.reference in definition_copies:
                make_instances_unique(child)


def make_definition_copies(def_to_copy, num_of_copies):
    copies = dict()
    copies[def_to_copy] = collections.deque()
    definition_copies[def_to_copy] = list()
    for i in range(num_of_copies):
        def_copy = sdn.Definition()
        copy_definition(def_to_copy, def_copy, i)
        definition_copies[def_to_copy].append(def_copy)
        for y in range(len(def_to_copy.library.definitions)):
            if def_to_copy == def_to_copy.library.definitions[y]:
                break
        try:
            def_to_copy.library.add_definition(def_copy, y)
        except KeyError:
            name = def_to_copy['EDIF.identifier']
            message = 'Try to add a definition with name of ' + \
                name + 'but the name was already use'
            raise KeyError(message)
    definition_clean_up(def_to_copy)
    return definition_copies


def clean(definition):
    for child in definition.children:
        if child.reference in definition_copies:
            make_instances_unique(child)

#print a list of all libraries and definitions in a netlist
def libraries_definitions(my_netlist):
    for library in my_netlist.libraries:
        definitions = list(definition.name for definition in library.definitions)
        print("   DEFINITIONS IN '",library.name,"':",definitions)


definition_count = dict()
original_inner_pin_to_new_inner_pin = dict()
instance_map = dict()
outer_pin_map = dict()
definition_copies = dict()

example_name = 'unique_challenge'
ir = sdn.load_example_netlist_by_name(example_name)
ir_orig = sdn.load_example_netlist_by_name(example_name) #store the original netlist for display later
top_def = ir.top_instance.reference

reverse_topological_order = get_reverse_topological_order(ir)
for definition in reverse_topological_order:
    make_definition_copies(definition, definition_count[definition] - 1)
clean(top_def)

with tempfile.TemporaryDirectory() as td:
    file_name = example_name + '_unique.edf'
    sdn.compose(ir, os.path.join(td, file_name))

#show the original netlist with its definitions and the new netlist with each instance now as a unique definition
print("ORIGINAL")
libraries_definitions(ir_orig)
print("UNIQUE")
libraries_definitions(ir)