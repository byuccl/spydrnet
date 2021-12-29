Tutorial
============

SpyDrNet is a tool for the analysis and transformation of structural netlists. A structural netlist is a static representation of an electronic circuit. A circuit consists of a number of electrical components and their connections. Figure :numref:`fig:hierarchical_netlist` shows a graphical representation of a netlist.

.. _fig:hierarchical_netlist:
.. figure:: figures/hierarchical_netlist.*
   :align: center

   Hierarchical representation of a Netlist 

This representation is commonly found in many schematic views of electronic design automation (EDA) or computer aided design (CAD) tools. It presents a top level instance of a definition that in turn instances other definitions. Instances are connected accordingly and connections carry through hierarchical boundaries.

Tool Flow
----------

Digital designs for FPGAs are represented as netlists, a list of components and connections. Netlists come from various vendors in many different formats. SpyDrNet allows you to look at and alter a netlist in a language inspecific way. 

Netlists flow through SpyDrNet in a three step process (see figure below). First, SpyDrNet parses a netlist into an intermediate represention (IR) that is designed to be easily traversed and effortlessly manipulated. Afterwards, the netlist is composed back into a netlist format that a 3rd-party tool can use. SpyDrNet aims to provide the tools you need to accomplish the netlist analysis and transformation tasks you have in mind without having to reinvent the wheel.

This flow is inspired by `LLVM`_ and `Pandoc`_. LLVM has a similar flow for compiling computer programs and Pandoc has a similar flow for converting document formats. Using this flow, SpyDrNet is designed to be able to work on any netlist.

.. _LLVM: http://www.aosabook.org/en/llvm.html
.. _Pandoc: https://pandoc.org/

.. _fig:flow.2:
.. figure:: /figures/flow.*
   :align: center
   :alt: SpyDrNet Flow

   Flow of Using SpyDrNet

**Note:** VHDL is not yet supported by SpyDrNet

Import Package
---------------

To import SpyDrNet to the project, use the following code:

.. code-block::

    import spydrnet as sdn

In this tutorial, we will use 'sdn' as a shortcut to access SpyDrNet commands.

Parsing
-------

The SpyDrNet parser will take an EDIF/Verilog file and put the information into the SpyDrNet data structure. 

To parse a file, enter the following command for an EDIF file (note: .edf and .edn are both supported)

.. code-block::

    netlist = sdn.parse('<netlist_filename>.edf')

Or the following for a Verilog file

.. code-block::

    netlist = sdn.parse('<netlist_filename>.v')

SpyDrNet has built in example netlists. For this tutorial, we will use the example 'one_counter'. This is the same as if we parsed a netlist named 'one_counter'.

.. code-block::

    netlist = sdn.load_example_netlist("one_counter")

Intermediate Representation (IR) Basics
---------------------------------------

A SpyDrNet netlist has many parts. The following is a short run through the basics.

Netlist:
^^^^^^^^
    This class is the highest level of organization (it's a whole netlist). It contains an ordered collection of libraries and any data associated with the netlist as a whole.

Library:
^^^^^^^^
    Contains an ordered collection of definitions

        Use the following code to see the libraries in our netlist:
        
        .. code-block::

            print(netlist.libraries)

        This returns a list of the library objects. To see the names of the libraries, use:
        
        .. code-block::

            for library in netlist.get_libraries():
                print("Library:", library.name)

        As seen in this example, most objects have a name and can be accessed using '.name'

Definition:
^^^^^^^^^^^
    Holds information about an element like its ports, pins, etc. (note: the pins are inner pins...see below). Verilog and System Verilog refer to a definition as a module, VHDL refers to a definition as an entity, and EDIF refers to a definition as a cell.

        To see the definitions in the first library, use:
        
        .. code-block::

            print(netlist.libraries[0].definitions)

        As before, we can use '.name' to see the name of each definition:
        
        .. code-block::

            for definition in netlist.libraries[0].get_definitions():
                print("Definition:", definition.name)

Ports:
^^^^^^
    The input/output "slots" of each definition (e.g. A,B, and Q of a simple AND gate)

        To see the ports for the first definition in the first library, run the following:
        
        .. code-block::

            definition_1 = netlist.libraries[0].definitions[0]
            for port in definition_1.ports:
                print("Port", port.name)

Pins:
^^^^^
    Found on ports. There are two types of pins: inner and outer (see the following explanation). Most of the time, you don't need to worry about what type a pin is because SpyDrNet takes care of it for you.
        
        **InnerPin**: 
            Inner pins are in definitions. Every definition has only one set of inner pins.
        **OuterPin**: 
            Outer pins are on instances. Each instance has a set of outer pins that corresponds to its reference definition’s inner pins. Because of this, a definition may have several sets of outer pins. For example, if a definition is instanced five times, it will have five sets of outer pins.
        
        Run the following code to see the types of pins for the instances and definitions in your netlist:
        
        .. code-block::

            for instance in netlist.get_instances():
                print("Instance:",instance.name," Reference definition:",instance.reference.name)
                print('\t',"Instance's pins' types")
                for pin in instance.pins:
                    print('\t\t',pin.__class__)
                print('\t',"Definition's pins' types")
                for pin in instance.reference.get_pins():
                    print('\t\t',pin.__class__)

Wires:
^^^^^^
    Wires connect pins to pins and thus connect elements to each other. Wires can connect to as many pins as desired (not just two).
    
Cables:
^^^^^^^
    Cables are bundles of wires. Wires are inside cables.

Instances:
^^^^^^^^^^
    An instance of a definition. It holds pointers to the definition which it instances (its reference), and contains its own set of pins (outer pins, specifically).

    An instance is also known as a **"child"**.
    The definition instanced is the **"reference"**.
    The definition that instances the other definition is the **"parent"**. 
        
        To see the instances in the 'work' library, or library[2], use the following code:
        
        .. code-block::

                for instance in netlist.libraries[2].get_instances():
                    print("Instance:", instance.name)
                    print("Instance's Parent:",instance.parent.name)
                    print("Instance's Reference Definition:",instance.reference.name,"\n")

    In the previous code, we saw that the definition '*counter*' instances the definition '*MUXCY_L*' as '*count_cry[0]*'.
    So '*counter*' is the **parent**, '*MUXCY_L*' is the **reference**, and '*count_cry[0]*' is the **instance** and **child** of 'counter'.


**See the following two figures to aid in understanding the SpyDrNet IR:**

.. _fig:IR_2:
.. figure:: /figures/IR.*
    :align: center
    :alt: SpyDrNet Intermediate Representation

    Summary of the SpyDrNet IR 1

.. _fig:IR_3:
.. figure:: /figures/spydrnet_api_elements.png
    :align: center
    :alt: SpyDrNet Intermediate Representation

    Summary of the SpyDrNet IR 2

Other IR Parts
^^^^^^^^^^^^^^^

**Element**
    Most IR classes inherit from this Python class. Objects of this class are referred to as netlist elements. A netlist
    element contains a dictionary for storing data specific to itself. This is accomplished using Python get/set item 
    functions, (see :ref:`sec:element-data`).

**Bundle**
    The Bundle class is a parent class of ports and cables. This class defines the structure that helps us properly represent array objects in netlists including the width, direction (to or downto) and starting index. As a parent class this class is not directly instantiated in netlist.

More detail on the IR is provided in :ref:`api_summary`.

Modifying Netlists
------------------

    Modifying netlists is made possible through SpyDrNet.
    
    **Renaming**:
    
    .. code-block::

        definition_1.name = "a_new_name"

    **Creating**:
        The following creates a new library in our netlist and then creates a new definition inside that library.

        .. code-block::

            new_library = netlist.create_library(name="new_library")
            new_library.create_definition(name="new_definition")

    **Changing Properties:**
        From the example :ref:`sphx_glr_auto_examples_vivado_AND_to_OR.py` in the examples tab, the following line of code "[changes] the value in the properties of the LUT2 instance"
        
        .. code-block::

            properties[0]["value"] = "4'h" + str(hex(LUT_CONFIG)).upper()[2:]

    **See** :ref:`sphx_glr_auto_examples` **for more examples of creating, modifying, and viewing netlists.**

Composing
---------

To compose a netlist file from a SpyDrNet netlist, enter the following command:

.. code-block::

    sdn.compose(netlist, '<filename>.edf')

A new EDIF file named '<filename>.edf' will be generated in the working directory. 
To compose a Verilog file, replace 'edf' with 'v'.