"""
=====================================
Display Netlist Information Functions
=====================================

Some example functions that can be run to display information in a netlist:
    1) print the hierarchy in a netlist
    2) print each library with its definitions in a netlist
    3) print connections between ports of each instance in a netlist
    4) print the number of times each primitive is instanced
    
Note: because the hierarchy function uses recursion, the maximum recursion depth may be exceeded if used for large designs

| For an even simpler display of netlist information, try using these functions with the Minimal Script example.  

| Also, JensRestemeier (not affiliated with BYU CCL) created a tool to generate images of netlists. See his `github repository <https://github.com/JensRestemeier/EdifTests>`_.
"""

import spydrnet as sdn
from spydrnet.util.selection import Selection

#print the hierarchy of a netlist
def hierarchy(current_instance,indentation="",level=0):
    print(indentation,level,'',current_instance.name," --instance of",current_instance.reference.name,"--")
    for child in current_instance.reference.children:
        hierarchy(child,indentation+"     ",level+1)

#print a list of all libraries and definitions in a netlist
def libraries_definitions(my_netlist):
    for library in my_netlist.libraries:
        definitions = list(definition.name for definition in library.definitions)
        print("DEFINITIONS IN '",library.name,"':",definitions)

#prints each instance and it's connections (what inputs to it and what it outputs to)
def print_connections(current_netlist):
    print("CONNECTIONS:")
    for instance in current_netlist.get_instances(): 
        print("Instance name:",instance.name)
        for out_going_pin in instance.get_pins(selection = Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.direction is sdn.OUT):
            if out_going_pin.wire:
                next_instances = list(str(pin2.inner_pin.port.name + ' of ' + pin2.instance.name) for pin2 in out_going_pin.wire.get_pins(selection = Selection.OUTSIDE, filter = lambda x: x is not out_going_pin))
                print('\t','Port',out_going_pin.inner_pin.port.name,'---->',next_instances)
        for in_coming_pin in instance.get_pins(selection = Selection.OUTSIDE,filter=lambda x: x.inner_pin.port.direction is sdn.IN):
            if in_coming_pin.wire:
                previous_instances = list(pin2 for pin2 in in_coming_pin.wire.get_pins(selection = Selection.OUTSIDE, filter = lambda x: x is not in_coming_pin))
                checked_previous_instances = list(str(x.inner_pin.port.name + ' of ' + x.instance.name) for x in previous_instances if (x.inner_pin.port.direction is sdn.OUT or (x.inner_pin.port.direction is sdn.IN and not x.instance.is_leaf()))is True)
                print('\t',checked_previous_instances,'---->','Port',in_coming_pin.inner_pin.port.name)

#print the number of times each primitive is instanced
def instance_count(current_netlist):
    print("Number of times each primitive is instanced:")
    primitives_library = next(current_netlist.get_libraries("hdi_primitives"),None)
    for primitive in primitives_library.get_definitions():
        count = 0
        for instance in current_netlist.get_instances():
            if primitive.name == instance.reference.name:
                count += 1
        print('\t',primitive.name,": ",count)



netlist = sdn.load_example_netlist_by_name("fourBitCounter")

print("HIERARCHY:")
hierarchy(netlist.top_instance)
libraries_definitions(netlist)
print_connections(netlist)
instance_count(netlist)