.. _netlist_types:

Netlist Types
--------------

SpyDrNet supports three netlist types: EDIF, Verilog, and EBLIF. All types can be parsed into and composed out of SpyDrNet. However, crossing between types (parsing in one type and composing out another type) is not guaranteed to always work. Crossing types will likely be improved in a future version.

Some functions take a netlist type in as a parameter. Netlist types can be imported from spydrnet.util.netlist_type
