.. SpyDrNet documentation master file, created by
   sphinx-quickstart on Tue Feb  5 12:01:59 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SpyDrNet!
====================

SpyDrNet is a powerful, flexibile framework for analyzing and transforming netlists. Netlists come from various vendors in many different formats. SpyDrNet allows you to look at and alter a netlist in a language inspecific way. SpyDrNet parses a netlist into an intermediate represention (IR) that is designed to be easily traversed and effortlessly manipulated. SpyDrNet provides the tools you need to do whatever you need to do with the netlists that you have.

A netlist contains information about an electronic circuit. Almost all the information needed to implement an electric circuit is avaiable in a netlist. Additional constraints, such as timing, placement, and routing constraints, are contained in seperate location, but they make reference to nets or components in a netlist. Nets are connections between components. Components are functional blocks. The blocks interface with other blocks through ports and ports have individual connections points called pins. A net can be thought of as a physical wire that connects a set of pins together. A block can be either a primitive component, (e.g., look-up table, flip-flop, DSP unit), a blackbox with undefined content, or a hierarchical component with nets and instances of other components contained inside. 

SpyDrNet's name comes from the language it is written in, the things it can do with with netlists, and the clever creatures in nature that do something similar. Spiders create beautiful and intricate webs using strands of silk. The strands are like nets and the connection points between strands are like components. Spiders move around their web and change it like SpyDrNet moves around a netlist and transforms it. The "Spy" in SpyDrNet ties into its ability to peer into a netlist for analysis. The "py" refers to the Python language that SpyDrNet is implemented in. The "Dr" references doctoring or tranforming netlists, and it also stems from this tool comming out of Ph.D. research. And of course, the "Net" refers to netlists, the thing this tool is meant to work on.

Netlists flow through SpyDrNet by first being parsed into an intermediate representation (IR), then being analysed and transformed as an IR, and finally being composed back into a netlist from the IR. This flow is inspired by LLVM and Pandoc. This idea is that a netlist from any format can be brought into the SpyDrNet environment though a parser. Once in the enviromnet as an IR, the netlist can be analysed and tranformed using object oriented programming. Finally, once you are done analyzing and transforming the netlist, you can bring it out of the SpyDrNet through a composer. 

<DIAGRAM OF FLOW>

SpyDrNet supports netlists written in EDIF (Electronic Design Interchange Format). Support is comming soon for structural VHDL, Verilog, VQM (Verilog Quartus Mapping File), generic serialized objects (JSON, XML, YAML). Right now, SpyDrNet is blind to device and vendor and will do with a netlist only exactly what you tell it to do. Support is comming soon for Xilinx and Intel FPGAs are thier respective devices and archtectures.

The IR is organized into eight different object types: Environment, Library, Definition, Port, Pin, Cable, Wire, and Instance. Pin is subclassed into InnerPin and OuterPin. InnerPins belong to a Port and represent the inside connection point for a Pin on a Port of a Definition. OuterPins belong to an Instance and represent the outside connection point for a Pin on an Instance of a Definition. Figure 

What specifically can I do with SpyDrNet that I can't do with any other tool?

Applications (reliability)

.. toctree::
   :maxdepth: 2

   intermediate_representation
   



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
