.. _introduction:

Introduction
============

Welcome to SpyDrNet, a tool that will help you analyze and transform netlists. Please note that SpyDrNet is currently in alpha testing and some features may not be bug free or may be incomplete.

SpyDrNet is developed and maintained by the `Configurable Computing Lab`_ of `Brigham Young University`_. This tool is related to the `BYU EDIF Tools`_ and is considered to be the next generation tool for FPGA netlist analysis and tranformation.

.. _Configurable Computing Lab: https://ccl.ee.byu.edu/
.. _Brigham Young University: https://www.byu.edu/
.. _BYU EDIF Tools: http://reliability.ee.byu.edu/edif/

What makes SpyDrNet different is its intermediate representation of netlists (IR) and its ability to interact with other powerful tools. Netlists are represented as a relational data stucture. In the representation, every netlist element (library, definition, port, pin, instance, cable, and wire) is stored in a Netlist object. Relationships between elements are preserved with pointers, and some additional pointers and helper objects are maintained to improve performance and usablility. A Design object within a Netlist holds basic information about about the netlist including the top-level module, the target FPGA chip, and any other information associated with a design that utilized the netlist.  The Netlist object hold information on how elements connect to each other and the hierarchy within the netlist. More detail on the IR is provided in sec:ir_.

.. SpyDrNet is currently in active development. Functionality is currently limited but growing, some of the goals the authors would like to accomplish are:

.. * Provide a runtime API in three different languages: C++, Python, and Java.
.. * Provide parsers and composers for at least five different netlist formats: EDIF, structural Verilog, structural VHDL, Intel's Verilog Quartus Mapping (VQM), and generic JSON. Other parsers can be added. Currently, only EDIF .. is supported.
.. * Provide an intermediate representation that can capture common elements found most netlist formats and preserve language specific elements as needed.
.. * Complete valuable research in the field of FPGA reliability.

.. Digital designs for FPGAs are represented as netlists, a list of components and connections. Netlists come from various vendors in many different formats. SpyDrNet allows you to look at and alter a netlist in a language inspecific way. SpyDrNet parses a netlist into an intermediate represention (IR) that is designed to be easily traversed and effortlessly manipulated. SpyDrNet provides the tools you need to accomplish the netlist analysis and transformation tasks you have in mind.

Using the API Example: Four-Bit Counter
---------------------------------------

>>> import spydrnet as sdn
>>> netlist = sdn.parse('four_bit_counter.edf')
>>>

Before we can start using the more powerful features of Spydrnet, a basic understanding of the Spydrnet API should be gained. We will explore the API by making a simple four-bit counter that can be incremented or decremented based on a outside signal. To begin we need to install Spydrnet, which can be done by using the command “pip install Spydrnet” in the terminal. Once Spydrnet has been install we can use “import Spydrnet” at the top of our python file.  

After we get Spydrnet set up, we start building our four-bit counter by creating a design to hold our work in. By using “design = Spydrnet.createDesgin()”, Spydrnet will generate a Design object for us. After creating the Design object, we need to create Library objects to hold our four-bit counter. 

At this time, Spydrnet is unable to read in a library that holds defines the primitives on FPGA chip, so we need to do this manually. Since we are working on getting primitives into our design, we must use the same names that the FPGA vendor tool expects. Because of this, we will be using Xilinx’s Artix 7 family primitives for this section of the guide. Start by using “prim_lib = design.createLibrary()”. We will be using this library to hold the primitives that we need to create the counter. After making a Library object, we need to create Definitions objects that will populate the Library. To do so, we will use “FDCE = prim_lib.createDefinition(‘FDCE’)”. This will create a Definition object with the identifier ‘FDCE’. 

Once we have created the Definition, we need to add ports. By looking at Xilinx’s documentation for primitives found on the Artix 7, we know we need add ports with the name ‘D’, ‘Q’, ‘C’, ‘CE’, and ‘CLR’. To create ports on a design, we will use definition.createPort(portName, direction). To continue with our example of the FDCE primitive, we will use “FDCE.createPort(‘D’, INPUT)”. For sake of brevity, we will leave the rest of setting up the primitive as an exercise for the reader. In a future update, the ability to import a file that contains the primitives will be supported. 

Once we have the primitive library completed, we can start the process of bringing the primitives together to create a functional four-bit counter. To begin, we will create another library to hold the design elements of four-bit counter.

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
   
**Parsing a netlist**

Normally, one will not create a digital design from scratch, and this is not the main propose of this tool. The normal way of getting a netlist into the tool is to use a parser. Spydrnet already comes will multiple parsers (currently Spydrnet only comes with a EDIF parser in the pre-alpha build). To parse a file, use Spydrnet.parse(pathToNetlist, netlistFormat). The path to the netlist can be either an absolute path or a relative path. For example, if the file fourBitCounter.edf is in the same directory as the python file, one can use design = Spydrnet.parse(fourBitCounter.edf, EDIF). One is not limited to the parsers provided, it is possible to use the Spydrnet API to write a parser for unsupported formats, but that is not covered in this guide. 

**Composing a netlist**

Once all the work on netlist is finished, it become necessary to export the design into a format that vender tools can work with. This can be done by 
Spydrnet.compose(Design, outputName, netlistFormat)/design.compose(outputName, netlistFormat)
. Like with parsing a netlist, it is possible to use the API to write a custom composer but this also not covered in this guide. 

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
