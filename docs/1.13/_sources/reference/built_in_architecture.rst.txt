.. _built_in_architecture:

Built In FPGA Architectures
----------------------------

SpyDrNet has built in libraries for the following primitive libraries:

* Xilinx 7-Series
* F4PGA Xilinx 7-Series
* Lattice LIFCL

An optional parameter can be parsed to parse() which will tell the parser to load in the specified primitive library during parsing. This allows primitive information to be known (particularly port directions) even if though it may not be defined in the netlist (as a cell define module or a blackbox).

The supported types are found under **spydrnet.util.architecture**

When a built in architecture parameter is passed, the parser uses the PrimitiveLibraryReader class to load in the primitive library and populate the netlist definitions with information. See below.

.. currentmodule:: spydrnet.parsers.primitive_library_reader
.. autoclass:: PrimitiveLibraryReader 