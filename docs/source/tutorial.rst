Tutorial
============

Installation
------------

For installing instructions, please refer :ref:`INSTALL.rst`

Working Environment
-------------------

SpyDrNet is coded in Python, and requires Python 3.5 or newer versions of Python. In order to import SpyDrNet to the project, use the following code:

    >>> import spydrnet as sdn
    >>>

In this tutorial, we will use 'sdn' as a shorcut for SpyDrNet to manipulate all the commands.

Parsing
-------

SpyDrNet currently only supports the parsing and composing for EDIF file

To parse a file, enter the following command

    >>> netlist = sdn.parse('<netlist_filename>.edf')


Nelist is an intermediate representation (IR). We are able to modify the netlist and add new elements. The following code returns the name of the top isntance of the netlist:

    >>> netlist.top_instance.name

This creates a new library and the library is added to the nestlist. For the entire documentation of SpyDrNet, please refer :ref:`sec:api_spec`

    >>> netlist.create_library()




Composing
---------

To compose a file, enter the following command

    >>> sdn.compose(netlist, '<filename>.edf')

A new file named '<filename>.edf' should be generated in the working directory.

Examples
--------

For more of the functionality, features, and uses of SpyDrNet，please visit :ref:`sec:examples`

Creating from scratch
---------------------

We can also create the hardware design from scratch

    >>>nelist = sdn.Netlist('myNetlist')

Below is a list of all the intermediate representations (IR) used by SpyDrNet. See :ref:`sec:api_spec` for API specification.

Intermediate Representation
----------------------------

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
    A definition outlines the contents of each component that can be instantiated elsewhere in the design. It holds information that is pertinant to all instances of itself including subcomponents ports and connections

:class:`Instance`
    This element holds pointers to the definition which it instances, and contains its own set of pins to be connected to within its parent definition.

:class:`Bundle`
    The Bundle class is a parent class of Ports and Cables because each can be thought of as an array. This class defines the structure that helps us properly represent array objects in netlists including the width, direction (to or downto) and starting index. As a parent class this class is not directly instantiated in netlist.

:class:`Port`
    The Port element inherits from Bundles and can be thought of as containing the information on how a Definition connects the outside world to the elements it contains.

:class:`Cable`
    Cables are bundles of connectors between components within a definition. They connect ports to their destination pins

:class:`Pin`
    The pin class is also a parent class, inherited from by the inner pin and outer pin objects. Unlike the Element and Bundle objects, Pins are useful because they can hide some of the implementation details of the underlying inner pins and outer pins.

:class:`InnerPin`
    These pins are collected in Ports and are contained on the inside of the definitions. There is one set of inner pins per definition but they could refer to several sets of OuterPins

:class:`OuterPin`
    These pins are collected on instances. They let us distinguish between connections to multiple instances of a single definition. These objects remove the need to carefuly track hierarcy while navegating a netlist.

:class:`Wire`
    Wires are grouped inside cables and are elements that help hold connection information between single pins on instances within a definition and within it's ports.

   
More detail on the IR is provided in :ref:`sec:api_spec`.