.. _introduction:

Introduction
============

Welcome tp SpyDrNet, a tool that will help you analyze and transform netlists. Please note that SpyDrNet is currently in a pre-alpha testing and some features, detailed in this guide, may not be fully implemented. Those features that are implimented, may not be bug free. Use at your own risk. 

SpyDrNet is developed and maintained by the `Configurable Computing Lab`_ of `Brigham Young University`_. This tool is related to the `BYU EDIF Tools`_ and is considered to be the next generation tool for FPGA netlist analysis and tranformation.

.. _Configurable Computing Lab: https://ccl.ee.byu.edu/
.. _Brigham Young University: https://www.byu.edu/
.. _BYU EDIF Tools: http://reliability.ee.byu.edu/edif/

What makes SpyDrNet different is its intermediate representation of netlists (IR) and its ability to interact with other powerful EDA tools. how netlists are represented In the representation, everything is stored in a Design object. The Design object holds basic information about a netlist, the top-level module, the target FPGA chip, and the Environment object that holds the information on how primitives connect to each other and the hierarchy within the netlist. 

.. SpyDrNet is currently in active development. Functionality is limited, but some of the goals the authors would like to accomplish are:

.. * Provide a runtime API in three different languages: C++, Python, and Java.
.. * Provide parsers and composers for at least five different netlist formats: EDIF, structural Verilog, structural VHDL, Intel's Verilog Quartus Mapping (VQM), and generic JSON. Other parsers can be added. Currently, only EDIF .. is supported.
.. * Provide an intermediate representation that can capture common elements found most netlist formats and preserve language specific elements as needed.
.. * Complete valuable research in the field of FPGA reliability.

.. Digital designs for FPGAs are represented as netlists, a list of components and connections. Netlists come from various vendors in many different formats. SpyDrNet allows you to look at and alter a netlist in a language inspecific way. SpyDrNet parses a netlist into an intermediate represention (IR) that is designed to be easily traversed and effortlessly manipulated. SpyDrNet provides the tools you need to accomplish the netlist analysis and transformation tasks you have in mind.

Tool Flow
---------

Netlists flow through SpyDrNet in a three step process (see :numref:`fig:flow`). First, they are parsed by a *parser* into an intermediate representation (IR). Second, their IR is analysed and transformed. Finally, their IR is composed by a *composer* back into a netlist format that a 3rd-party tool can use. This flow is inspired by `LLVM`_ and `Pandoc`_. LLVM has a similar flow for compiling computer programs and Pandoc has a similar flow for converting document formats. Using this flow, SpyDrNet is designed to be able to work on any netlist.

.. _LLVM: http://www.aosabook.org/en/llvm.html
.. _Pandoc: https://pandoc.org/

.. _fig:flow:
.. figure:: figures/flow.*
   :align: center
   :alt: SpyDrNet Flow

   Flow

Intermediate Representation:
----------------------------

:numref:`fig:IR` shows a summary of the SpyDrNet intermediate representation (IR). The top level element type is Environment. An Environnment object has pointers to the libraries that belong to it. A Library object has a pointer to the environment it belongs to and it has pointers to the definitions that belong to it. Likewise, a Definition object has a pointer to the library it belongs to and it has pointers to the ports, cables, and instances that belong to it. The same pattern is followed for Port, Cable, and Instance objects. An Instance object has an additional pointer to the definition that it instances (represented as a dashed arrow). A Wire object has a pointer to the cable it belongs to and it has pointers the pins that are connected to it. A Pin object has a pointer to its parent object and it has a pointer to the wire it is connected to. The parent object of an InnerPin is a port, and the parent object of an OuterPin is an instance. An OuterPin object also has an additional pointer to the innerPin that it instances. More details can be found in :ref:`sec:ir`.

.. _fig:IR:
.. figure:: figures/IR.*
   :align: center
   :alt: SpyDrNet Intermediate Representation

   Intermediate Representaion


The Name of the Tool
--------------------

SpyDrNet's name comes from the language it is written in, the things it can do with with netlists, and the clever creatures in nature that do something similar. Spiders create beautiful and intricate webs using strands of silk. The strands are like nets and the connection points between strands are like components. Spiders move around their web and change it like SpyDrNet moves around a netlist and transforms it. The "Spy" in SpyDrNet ties into its ability to peer into a netlist for analysis. The "py" refers to the Python language that SpyDrNet is implemented in. The "Dr" references doctoring or tranforming netlists and it also references the research that supports the tool. The "Net" refers to a netlist, the thing this tool is meant to work on. Too much fun is had in the name, but what really matters is what the tool can do.



.. <DIAGRAM OF FLOW>

.. SpyDrNet supports netlists written in EDIF (Electronic Design Interchange Format). Support is comming soon for structural VHDL, Verilog, VQM (Verilog Quartus Mapping File), generic serialized objects (JSON, XML, YAML). Right now, SpyDrNet is blind to device and vendor and will do with a netlist only exactly what you tell it to do. Support is comming soon for Xilinx and Intel FPGAs are thier respective devices and archtectures.

.. The IR is organized into eight different object types: Environment, Library, Definition, Port, Pin, Cable, Wire, and Instance. Pin is subclassed into InnerPin and OuterPin. InnerPins belong to a Port and represent the inside connection point for a Pin on a Port of a Definition. OuterPins belong to an Instance and represent the outside connection point for a Pin on an Instance of a Definition. Figure 

.. What specifically can I do with SpyDrNet that I can't do with any other tool?

.. Applications (reliability)


SpyDrNet is part of a rising ecosystem of free and open source software (FOSS) for FPGA developement. Think MyHDL, pyEDA, Yosys, L-graph, ABC, BLIF, RapidWright, RapidSmith, RapidSmith2, JHDL, BYU EDIF Tools, VQM, Project X-ray

Netlist formats: EDIF, Structural Verilog, Structural VHDL, FPGA_assembly, NGC (Previous Xilinx Proprietary), VQM, DOT, generic serilization (JSON, XML, YAML, GRAPHML, etc.)

Explaination of Vendor primitives and simulation libraries that can be parsed to extract "Atoms"/"Primitives", etc.