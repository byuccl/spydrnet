.. _introduction:

Introduction
============

.. currentmodule:: spydrnet

Welcome to SpyDrNet, a tool that will help you analyze and transform 
`netlists <https://en.wikipedia.org/wiki/Netlist>`_. SpyDrNet is developed and maintained by the 
`Configurable Computing Lab`_ of `Brigham Young University`_. This tool is related to the `BYU EDIF Tools`_ and is 
considered to be the next generation tool for FPGA netlist analysis and transformation.

.. _Configurable Computing Lab: https://ccl.ee.byu.edu/
.. _Brigham Young University: https://www.byu.edu/
.. _BYU EDIF Tools: http://reliability.ee.byu.edu/edif/

SpyDrNet Getting Started
------------------------

**Installation**

This package will be available on Python Package Index shortly. Once it is, the stable release of SpyDrNet can be installed using ``pip``::

    > pip install spydrnet

To install from PyPI with all optional dependicies use::

    > pip install spydrnet[all]

SpyDrNet can also be installed from a source archive::

    > pip install spydrnet-1.0.0.tar.gz

Or a built distribution::

    > pip install spydrnet-1.0.0-py3-none-any.whl

If a development environment is desired, the project can be installed in editable mode from the project directory::

    > pip install -e .

**Tool Flow**

Netlists flow through SpyDrNet in a three step process (see :numref:`fig:flow`). First, they are parsed by a *parser* into an intermediate representation (IR). Second, their IR is analyzed and transformed. Finally, their IR is composed by a *composer* back into a netlist format that a 3rd-party tool can use. This flow is inspired by `LLVM`_ and `Pandoc`_. LLVM has a similar flow for compiling computer programs and Pandoc has a similar flow for converting document formats. Using this flow, SpyDrNet is designed to be able to work on any netlist.

.. _LLVM: http://www.aosabook.org/en/llvm.html
.. _Pandoc: https://pandoc.org/

.. _fig:flow:
.. figure:: ../figures/flow.*
   :align: center
   :alt: SpyDrNet Flow

   Flow
   
SpyDrNet can be used to create a netlist from scratch. Thus, the API can be used to implement a parser and composer for arbitrary formats. 
   
*Parsing a netlist*

SpyDrNet currently includes a parser for EDIF::

    >>> netlist = sdn.parse('<netlist_filename>.edf')

*Composing a netlist*

SpyDrNet currently includes a composer for EDIF::

    >>> sdn.compose('<filename>.edf', netlist)

**Loading SpyDrNet**

To load ``spydrnet``, import it into a Python interactive interpreter or code::

    >>> import spydrnet as sdn
    >>>
    
At this point, SpyDrNet features and functionality are accessible via ``sdn.<function/feature>``. The abbreviation of 
``sdn`` is used throughout code examples to reference the ``spydrnet`` package. 

**Intermediate Representation Basics**

Digital designs for FPGAs are represented as netlists, a list of components and connections. Netlists come from various vendors in many different formats. SpyDrNet allows you to look at and alter a netlist in a language inspecific way. SpyDrNet parses a netlist into an intermediate represention (IR) that is designed to be easily traversed and effortlessly manipulated. SpyDrNet aims to provide the tools you need to accomplish the netlist analysis and transformation tasks you have in mind without having to reinvent the wheel. :numref:`fig:IR` shows a summary of the SpyDrNet intermediate representation (IR).

.. _fig:IR:
.. figure:: ../figures/IR.*
   :align: center
   :alt: SpyDrNet Intermediate Representation

   Intermediate Representaion

SpyDrNet's intermediate representation of netlists (IR) is what sets it apart for other EDA tools. The IR is structured to house netlists in a generic way while allowing for format specific constructs to be preserved.

:class:`Element`
    Most IR classes inherit from this Python class. Objects of this class are referred to as a netlist elements. A netlist
    element contains a dictionary for storing data specific to itself. This is accomplished using Python get/set item 
    functions, (see :ref:`sec:element-data`).

:class:`Netlist`
    This class of Python objects is the netlist element with the highest level of organization (a whole netlist). It 
    contains an ordered collection of libraries and any data associated with the netlist as a whole.
   
:class:`Library`
    This netlist element contains an ordered collection of cell or module definitions associated with a library.
    
:class:`Definition`
    A Definition outlines the contents of each component that can be instantiated elsewhere in the design. It holds information that is pertinant to all instances of itself including subcomponents ports and connections

:class:`Instance`
    This element holds pointers to the definition which it instances, and contains its own set of pins to be connected to within its parent definition.

:class:`Bundle`
    The Bundle class is a parent class of Ports and Cables because each can be thought of as an array. This class defines the structure that helps us properly represent array objects in netlists including the width, direction (to or downto) and starting index. As a parent class this class is not directly instantiated in netlist.

:class:`Port`
    The Port element inherits from Bundles and can be thought of as containing the information on how a Definition connects the outside world to the elements it contains.

:class:`Cable`
    Cables are bundles of connectors between components within a definition. They connect ports to their destination pins

:class:`Pin`
    The Pin class is also a parent class, inherited from by the inner pin and outer pin objects. Unlike the Element and Bundle objects, Pins are useful because they can hide some of the implementation details of the underlying inner pins and outer pins.

:class:`InnerPin`
    These pins are collected in Ports and are contained on the inside of the definitions. There is one set of inner pins per definition but they could refer to several sets of OuterPins

:class:`OuterPin`
    These pins are collected on instances. They let us distinguish between connections to multiple instances of a single definition. These objects remove the need to carefuly track hierarcy while navegating a netlist.

:class:`Wire`
    Wires are grouped inside cables and are elements that help hold connection information between single pins on instances within a definition and within it's ports.

   
More detail on the IR is provided in :ref:`api_summary`.

.. SpyDrNet is currently in active development. Functionality is limited but growing, contributions are welcome. please browse the github wiki and projects to get an idea of what is coming in the future. Some of the things that the SpyDrNet team would like to accomplish are listed here:

.. * Provide a runtime API in three different languages: C++, Python, and Java and perhaps more in the future.
.. * Provide parsers and composers for at least five different netlist formats: EDIF, structural Verilog, structural VHDL, Intel's Verilog Quartus Mapping (VQM), and generic JSON. Other parsers can be added. Currently, only EDIF .. is supported.
.. * Provide an intermediate representation that can capture common elements found most netlist formats and preserve language specific elements as needed.
.. * Complete valuable research in the field of FPGA reliability.


Aracnid Etymology
-----------------

Spiders are masters at spinning webs. These webs often created like nets are stronger than steel when stretched and much more elastic. SpyDrNet aims to give end users the ability to pass these traits on to their netlists by enabling reliability and other applications through generic analysis and transformations on netlist. Of course this is just scratching the surface of the ways in which this name is applicable to the tool. Finding these fun meanings is (as it is said in academia) left as an exercise to the curious reader. For now we would rather discuss what this tool can be used to do. 

Other Information
-----------------

SpyDrNet is part of a rising ecosystem of free and open source software (FOSS) for FPGA development. Consider `MyHDL`_, `PyEDA`_, `Yosys`_, `LiveHD`_, `ABC`_, `BLIF`_, `RapidWright`_, `RapidSmith`_, `RapidSmith2`_, `JHDL`_, `BYU EDIF Tools`_, VQM, and `Project X-ray`_.

.. _MyHDL: http://www.myhdl.org/
.. _PyEDA: https://pyeda.readthedocs.io/en/latest/
.. _Yosys: http://www.clifford.at/yosys/
.. _LiveHD: https://github.com/masc-ucsc/livehd
.. _ABC: https://people.eecs.berkeley.edu/~alanmi/abc/
.. _BLIF: http://www.cs.columbia.edu/~cs6861/sis/blif/index.html
.. _RapidWright: https://www.rapidwright.io/
.. _RapidSmith: http://rapidsmith.sourceforge.net/
.. _RapidSmith2: https://github.com/byuccl/RapidSmith2
.. _JHDL: http://www.jhdl.org/
.. _BYU EDIF Tools: http://reliability.ee.byu.edu/edif/
.. _Project X-ray: https://github.com/SymbiFlow/prjxray

