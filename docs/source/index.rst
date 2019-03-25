.. SpyDrNet documentation master file, created by
   sphinx-quickstart on Tue Feb  5 12:01:59 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Overview
========

SpyDrNet is a powerful, flexibile framework for analyzing and transforming FPGA netlists. It is developed and maintained by the `Configurable Computing Lab`_ of `Brigham Young University`_. This tool is related to 
the `BYU EDIF Tools`_.

.. _Configurable Computing Lab: https://ccl.ee.byu.edu/
.. _Brigham Young University: https://www.byu.edu/
.. _BYU EDIF Tools: http://reliability.ee.byu.edu/edif/

SpyDrNet is currently in active development. Functionality is limited, but some of the goals the authors would like to accomplish are:

* Provide a runtime API in three different languages: C++, Python, and Java.
* Provide parsers and composers for at least five different netlist formats: EDIF, structural verilog, structural VHDL, Intel's Verilog Quartus Mapping (VQM), and generic JSON. Other parsers can be added. Currently, only EDIF is supported.
* Provide an intermediate representation that can capture common elements found most netlist formats and preserve language specific elements as needed.
* Complete valuable research with the tools in the field of FPGA reliability.

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

:numref:`fig:IR` shows the structure of the SpyDrNet intermediate representation (IR) and how individual elements relate to eachother. Elements of the IR are labeled and the relationship between elements are shown using arrow. The top level element is an Environment. An Environment contain zero or more Libraries. A Library contains zero or more Definitions. A Definition contains zero or more Ports, Cables, and Instances. A Port contains zero or more InnerPins, a cable contains zero or more Wires, an Instance contains zero or more OuterPins, and a Wire contains pointers to all of the InnerPins and OuterPins connected to it. Arrows represent pointers between elements. Most pointers are bi-directional. Exceptions include pointers from an OuterPin to the InnerPin it instances and pointers from an Instance to the Definition it instances (represented as a dashed arrow, not to be confused with the pointer between a Definition and an Instance within that Definition).


OuterPins and InnerPins are both pins on a port. OuterPins refer to the pin on the outside of an instance and InnerPins refer to pins on the inside of a definition. An OuterPin contains a pointer to the InnerPin it instances, but InnerPins do not contain pointer to outer pins that reference them.

All netlists have associated with them some sort of design or implmenentation environment. Within the environment is a collection of libraries, an instance of the top level definition, perhaps a targeted device, and other information related to netlist as a whole. Libraries have a collection of definitions and other information pertaining to that specific library. Definitions contain ports, cables, instances, and other information pertaining to that specific definition. Ports contain pins and other information pertaining to that specific port. Cables contain wires, and other information related to that specific cable. Instances contain a pointer to the definition that they instantiate, a collection of pins, and other information pertaining to that specific instance. Wires contain pointers to pins they are connected to. Pins on a port are InnerPins because they are visible from the inside of a definition. Pins on an instance are OuterPins because they are visible from the outside of an instance. :numref:`fig:IR` you can see...

.. _fig:IR:
.. figure:: figures/IR.*
   :align: center
   :alt: SpyDrNet Intermediate Representation

   Intermediate Representaion
 
Digital designs for FPGAs are represented as netlists, a list of components and connections. Netlists come from various vendors in many different formats. SpyDrNet allows you to look at and alter a netlist in a language inspecific way. SpyDrNet parses a netlist into an intermediate represention (IR) that is designed to be easily traversed and effortlessly manipulated. SpyDrNet provides the tools you need to do whatever you need to do with the netlists that you have.

A netlist contains information about an electronic circuit. Almost all the information needed to implement an electric circuit is avaiable in a netlist. Additional constraints, such as timing, placement, and routing constraints, are contained in seperate location, but they make reference to nets or components in a netlist. Nets are connections between components. Components are functional blocks. The blocks interface with other blocks through ports and ports have individual connections points called pins. A net can be thought of as a physical wire that connects a set of pins together. A block can be either a primitive component, (e.g., look-up table, flip-flop, DSP unit), a blackbox with undefined content, or a hierarchical component with nets and instances of other components contained inside. 

The Name of the Tool
--------------------

SpyDrNet's name comes from the language it is written in, the things it can do with with netlists, and the clever creatures in nature that do something similar. Spiders create beautiful and intricate webs using strands of silk. The strands are like nets and the connection points between strands are like components. Spiders move around their web and change it like SpyDrNet moves around a netlist and transforms it. The "Spy" in SpyDrNet ties into its ability to peer into a netlist for analysis. The "py" refers to the Python language that SpyDrNet is implemented in. The "Dr" references doctoring or tranforming netlists and it also references the research that supports the tool. The "Net" refers to a netlist, the thing this tool is meant to work on. Too much fun is had in the name, but what really matters is what the tool can do.



<DIAGRAM OF FLOW>

SpyDrNet supports netlists written in EDIF (Electronic Design Interchange Format). Support is comming soon for structural VHDL, Verilog, VQM (Verilog Quartus Mapping File), generic serialized objects (JSON, XML, YAML). Right now, SpyDrNet is blind to device and vendor and will do with a netlist only exactly what you tell it to do. Support is comming soon for Xilinx and Intel FPGAs are thier respective devices and archtectures.

The IR is organized into eight different object types: Environment, Library, Definition, Port, Pin, Cable, Wire, and Instance. Pin is subclassed into InnerPin and OuterPin. InnerPins belong to a Port and represent the inside connection point for a Pin on a Port of a Definition. OuterPins belong to an Instance and represent the outside connection point for a Pin on an Instance of a Definition. Figure 

What specifically can I do with SpyDrNet that I can't do with any other tool?

Applications (reliability)
   


Documentation
-------------

.. only:: html

    :Release: |version|
    :Date: |today|

.. toctree::
   :maxdepth: 2

   intermediate_representation

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
