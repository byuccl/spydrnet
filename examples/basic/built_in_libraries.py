"""
=====================================
Using Built-In Primitive Libraries
=====================================

A simple example to demonstrate using SpyDrNet's built in primitive libraries.

The b13 example netlist is targeted towards the Xilinx 7 Series family. However, because the primitives are defined in the netlist, we must first compose it out to a new netlist that does not define the primitives.

netlist_1 is parsed in without using the built in primitive library. The output shows that the port directions are undefined.

netlist_2 is parsed in using the XILINX_7SERIES primitive library. The output shows that the port directions are defined.
"""

import spydrnet as sdn
from spydrnet.util.netlist_type import VERILOG
from spydrnet.util.architecture import XILINX_7SERIES


netlist = sdn.load_example_netlist_by_name("b13", VERILOG)
netlist.compose("b13.v", write_blackbox = False)

print("Without using the primitive library:")
netlist_1 = sdn.parse("b13.v")
for definition in netlist_1.get_definitions():
    if definition is not netlist_1.top_instance.reference:
        for port in definition.get_ports():
            print(port.name + " " + str(port.direction))

print("\nUsing the primitive library:")
netlist_2 = sdn.parse("b13.v", architecture=XILINX_7SERIES)
for definition in netlist_2.get_definitions():
    if definition is not netlist_2.top_instance.reference:
        for port in definition.get_ports():
            print(port.name + " " + str(port.direction))
