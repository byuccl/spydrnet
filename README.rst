SpyDrNet
========
A flexible framework for analyzing and transforming `netlists <https://en.wikipedia.org/wiki/Netlist>`_. Built to fill an important gap in FPGA research and reliability. Currently available as a pure Python package.

- **Website and Documentation:** https://byuccl.github.io/spydrnet
- **Mailing List:** https://groups.google.com/forum/#!forum/spydrnet-discuss
- **Source:** https://github.com/byuccl/spydrnet
- **Bug Reports:** https://github.com/byuccl/spydrnet/issues

Simple Examples
---------------

SpyDrNet can be used to create netlists from scratch. Because it is a low-level framework, manual netlist creation can be tedious (much like writting a high level application in assembly). To assist in rapid productivity, parsers and composers are provided for common netlist formats. Currently only `EDIF <https://en.wikipedia.org/wiki/EDIF>`_ is supported, but the roadmap includes structural Verilog, structural VHDL, Verilog Quartus Mapping Files `Intel's VQM <https://www.intel.com/content/www/us/en/programmable/quartushelp/17.0/mapIdTopics/mwh1465406414431.htm>`_ and JSON.

**Loading Example Netlists**

Several example netlists are included with the package to introduce the framework, its features, and functionality. To list and load these netlists, modify the following example: 

    >>> import spydrnet as sdn
    >>> sdn.example_netlist_names
    ['4bitadder', '8051', ... , 'zpu4']
    >>> netlist = sdn.load_example_netlist_by_name('4bitadder')

**Parsing a Netlist**

    >>> netlist = sdn.parse('<netlist_filename>.edf')

**View Data Associated with any Netlist Element**

   >>> netlist.data
   {'EDIF.identifier': 'Z4bitadder', 'EDIF.original_identifier': 'adder', ... }

**List Libraries in a Netlist**

    >>> list(x['EDIF.identifier'] for x in netlist.libraries)
    ['VIRTEX', 'UNILIB', 'work']

**List Definitions in a Library**

    >>> library = netlist.libraries[2]
    >>> list(x['EDIF.identifier'] for x in library.definitions)


**List Ports, Cables, and Instances in a Definition**

    >>> definition = library.definitions[0]
    >>> list(x['EDIF.identifier'] for x in definitions.ports)
    ['data1', 'data2', 'answer', 'clk', 'reset', 'enable']
    >>> list(x['EDIF.identifier'] for x in definitions.cables)
    ['answer_1_0', 'answer_1_1', 'answer_1_2', 'answer_1_3', ... ]
    >>> list(x['EDIF.identifier'] for x in definitions.children)
    ['un3_answer1_axbxc3', 'un2_answer2_axbxc3', 'reset_c_i', ... ]

**Compose a Netlist**

This example exports a netlist into an EDIF formatted netlist file by the given name.

   >>> sdn.compose('<filename>.edf', netlist)

**Additional Examples**

Additional examples are available in the documentation for netlist creation, analysis, and transformation.

How to install
--------------

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

Bugs
----

Bugs can be reported on the `issues page <https://github.com/byuccl/spydrnet/issues>`_ or they can be fixed through a fork / pull request. All changes are welcome. Discussion of ideas for new features is available on the `mailing list <https://groups.google.com/forum/#!forum/spydrnet-discuss>`_.

A Brief History
---------------

The `BYU Configurable Computing Lab <https://ccl.ee.byu.edu/>`_ actively maintains the `BYU EDIF Tools <http://reliability.ee.byu.edu/edif/>`_ - a Java API for creating, modifying, or analyzing EDIF netlists. These tools are tied to the EDIF netlist format and provide JEDIF tools capable of flattening a circuit (by removing hierarchical organization) and applying fault-tolerance techniques such as `triple modular redundancy (TMR) <https://en.wikipedia.org/wiki/Triple_modular_redundancy>`_. Development of SpyDrNet began back in 2016 with the idea of creating an accessible, format independent, tool for netlist analysis and transformation. The underlying intermediate data structure is designed preserve proper netlist reliationship as a generic netlist while allowing for the preservation of format specific constructs. A language agnostic prototype was developed and this prototype soon became useful in the lab for netlist analysis and reliability transformation studies. A more mature (though still having room for growth) tool is presented here. 

Design Notes
------------

We have tried to build this tool around the principles of expandability and modularity. Care has been taken to separate different parts of the program in an organized fashion.

How to contribute
-----------------
If this tool has been useful to you, or have new feature ideas that you would like to implement, feel free to make a pull request, or take a look at the issues to see how to contribute. New ideas, bug fixes and suggestions are also welcome (See `CONTRIBUTING.rst`).

Special Thanks
--------------

Special thanks is given to `NetworkX <https://networkx.github.io/>`_ - "a python package for the creation, manipulation, and study of the structure, dynamics and functions of complex networks."  This mature project has been used as a template for much of SpyDrNet's documentation and code structure. It also has saved enormous effort in heavy graph analysis as a robust and complete library used to analize the relationships between circuit nodes.

License
-------

Released under the 3-Clause BSD license (see `LICENSE.txt`)::

   Copyright (C) 2016-2019 SpyDrNet Developers
   Andrew Keller <andrewmkeller@byu.edu>
   Dallin Skouson <dallinskouson@gmail.com>
   Dr. Michael Wirthlin <wirthlin@byu.edu>
