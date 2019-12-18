"""
=====================================
Traversal and Statistics of a Netlist
=====================================

Traverse a netlist and collect statistics on the netlist.
"""


import spydrnet as sdn


ir = sdn.load_example_netlist_by_name("fourBitCounter")

print("Netlist stats")
print("Top instance:", ir.top_instance['EDIF.identifier'])
print(str(len(ir.libraries)) + " libraies detected")
for library in ir.libraries:
    print("Library name:", library['EDIF.identifier'])
    print("\t", str(len(library.definitions)), "definitions detected")
    for definition in library.definitions:
        print("\tDefinition name:", definition['EDIF.identifier'])
        print("\t\t", "Defintion used", str(len(definition.children)), "times")
        print("\t\t", str(len(definition.ports)), "ports detected")
        for port in definition.ports:
            print("\t\t\tPort name:", port['EDIF.identifier'])
            if port.direction is 0:
                print("\t\t\t\tPort Direction: UNDEFINED")
            if port.direction is 1:
                print("\t\t\t\tPort Direction: INOUT")
            if port.direction is 1:
                print("\t\t\t\tPort Direction: IN")
            if port.direction is 1:
                print("\t\t\t\tPort Direction: OUT")
            print("\t\t\t\tPort length:", str(len(port.pins)))
        print("\t\t", str(len(definition.children)), "children detected")
        for child in definition.children:
            print("\t\t\tChild name:", child['EDIF.identifier'])
            print("\t\t\t\tReferenced Definition:", child.reference['EDIF.identifier'])
        print("\t\t", str(len(definition.cables)), "cables detected")
        for cable in definition.cables:
            print("\t\t\tCable Name", cable['EDIF.identifier'])
            print("\t\t\t\tNumber of wires:", len(cable.wires))