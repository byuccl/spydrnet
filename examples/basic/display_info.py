"""
=====================================
Display Netlist Information Functions
=====================================

Some example functions that can be run to display information in a netlist:
    1) print the hierarchy in a netlist
    2) print each library with its definitions in a netlist
    3) print wire connections between ports in a netlist
    4) print the number of times each primitive is instanced
Note: because the hierarchy function uses recursion, the maximum recursion depth may be exceeded if used for large designs

| For an even simpler display of netlist information, try using these functions with the Minimal Script example.  

| Also, JensRestemeier (not affiliated with BYU CCL) created a tool to generate images of netlists. See his `github repository <https://github.com/JensRestemeier/EdifTests>`_.
"""

import spydrnet as sdn

#print the hierarchy of a netlist
def hierarchy(current_instance,indentation=""):
    print(indentation,current_instance.name," --instance of",current_instance.reference.name,"--")
    for child in current_instance.reference.children:
        hierarchy(child,indentation+"     ")

#print a list of all libraries and definitions in a netlist
def libraries_definitions(my_netlist):
    for library in my_netlist.libraries:
        definitions = list(definition.name for definition in library.definitions)
        print("DEFINITIONS IN '",library.name,"':",definitions)

#print the connections in a netlist
def print_connections(current_netlist):
    print("CONNECTIONS:")
    for instance in current_netlist.get_instances(): 
        print("Instance name:",instance.name)
        for pin in instance.pins:
            IN = "EXTERNAL"
            OUT = "EXTERNAL"        
            for pin in pin.wire.pins:
                instance = list(instance.name for instance in pin.get_instances())
                for port in pin.get_ports():
                    #for each pin, get the associated port and check the direction
                    if port.direction is sdn.IN:
                        if IN is "EXTERNAL":
                            IN = port.name + " of " + str(instance)
                        else:
                            IN = IN + ", " + port.name + " of " + str(instance)
                    elif port.direction is sdn.OUT:
                        if OUT is "EXTERNAL":
                            OUT = port.name + " of " + str(instance)
                        else:
                            OUT = OUT + ", " + port.name + " of " + str(instance)
            print("\t",OUT,"---->",IN)

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