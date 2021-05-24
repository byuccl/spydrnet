"""
=====================================
Traversal and Statistics of a Netlist
=====================================

Traverse a netlist and collect statistics on the netlist.
"""


import spydrnet as sdn

# Loads the example
ir = sdn.load_example_netlist_by_name("fourBitCounter")

print("Netlist stats")
print("Top instance:", ir.top_instance['EDIF.identifier'])
print(str(len(ir.libraries)) + " libraries detected")
# Loop through each library in a design
for library in ir.libraries:
    # Gets the name of the current library and reports number of definitions
    print("Library name:", library['EDIF.identifier'])
    print("\t", str(len(library.definitions)), "definitions detected")
    # Loop through each definition in current library
    for definition in library.definitions:
        # Gets the name of the current definition and how many times its been used
        print("\tDefinition name:", definition['EDIF.identifier'])
        print("\t\t", "Defintion used", str(len(definition.references)), "times")
        # Gets the number of Ports in definition
        print("\t\t", str(len(definition.ports)), "ports detected")
        # Loop through each port for the current definition
        for port in definition.ports:
            # Gets the name of the port
            print("\t\t\tPort name:", port['EDIF.identifier'])
            # Gets the direction of the port
            if port.direction is sdn.UNDEFINED:
                print("\t\t\t\tPort Direction: UNDEFINED")
            elif port.direction is sdn.INOUT:
                print("\t\t\t\tPort Direction: INOUT")
            elif port.direction is sdn.IN:
                print("\t\t\t\tPort Direction: IN")
            elif port.direction is sdn.OUT:
                print("\t\t\t\tPort Direction: OUT")
            # Gets the length (number of pins) of the port
            print("\t\t\t\tPort length:", str(len(port.pins)))
        # Get the number of children within the definition
        print("\t\t", str(len(definition.children)), "children detected")
        # Loops through each child
        for child in definition.children:
            # Gets the child's name and its referenced definition
            print("\t\t\tChild name:", child['EDIF.identifier'])
            print("\t\t\t\tReferenced Definition:", child.reference['EDIF.identifier'])
        # Gets the number of cables within the definition
        print("\t\t", str(len(definition.cables)), "cables detected")
        for cable in definition.cables:
            # Gets the name of the cable and the number of wires it contains
            print("\t\t\tCable Name", cable['EDIF.identifier'])
            print("\t\t\t\tNumber of wires:", len(cable.wires))
