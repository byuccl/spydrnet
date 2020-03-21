Welcome to SpyDrNet!
====================

.. image:: https://img.shields.io/pypi/v/spydrnet.svg
   :target: https://pypi.org/project/spydrnet/
   
.. image:: https://img.shields.io/pypi/pyversions/spydrnet.svg
   :target: https://pypi.org/project/spydrnet/

.. image:: https://travis-ci.com/byuccl/spydrnet.svg?branch=master
   :target: https://travis-ci.com/byuccl/spydrnet

A flexible framework for analyzing and transforming `netlists <https://en.wikipedia.org/wiki/Netlist>`_. Built to fill an important gap in FPGA research and reliability. Currently available as a pure Python package.

- **Website and Documentation:** https://byuccl.github.io/spydrnet
- **Mailing List:** https://groups.google.com/forum/#!forum/spydrnet-discuss
- **Source:** https://github.com/byuccl/spydrnet
- **Bug Reports:** https://github.com/byuccl/spydrnet/issues

Simple Examples
---------------

SpyDrNet can be used to create netlists from scratch. Because it is a low-level framework, manual netlist creation can be tedious (much like writting a high level application in assembly). To assist in rapid productivity, parsers and composers are provided for common netlist formats. Currently only `EDIF <https://en.wikipedia.org/wiki/EDIF>`_ is supported, but the roadmap includes structural Verilog, structural VHDL, Verilog Quartus Mapping Files (`Intel's VQM <https://www.intel.com/content/www/us/en/programmable/quartushelp/17.0/mapIdTopics/mwh1465406414431.htm>`_), and JSON.

**Loading Example Netlists**

Several example netlists are included with the package to introduce the framework, its features, and functionality. To list and load these netlists, modify the following example: 

.. code:: python

    >>> import spydrnet as sdn
    >>> sdn.example_netlist_names
    ['4bitadder', '8051', ... , 'zpu4']
    >>> netlist = sdn.load_example_netlist_by_name('4bitadder')

**Parsing a Netlist**

.. code:: python

    >>> netlist = sdn.parse('<netlist_filename>.edf')

**View Data Associated with any Netlist Element**

.. code:: python

   >>> netlist.data
   {'.NAME': 'adder', 'EDIF.identifier': 'Z4bitadder', ... }

**List Libraries in a Netlist**

.. code:: python

    >>> list(library.name for library in netlist.libraries)
    ['VIRTEX', 'UNILIB', 'work']

**List Definitions in a Library**

.. code:: python

    >>> library = netlist.libraries[2]
    >>> list(definition.name for definition in library.definitions)
    ['adder']

**List Ports, Cables, and Instances in a Definition**

.. code:: python

    >>> definition = library.definitions[0]
    >>> list(port.name for port in definition.ports)
    ['data1(3:0)', 'data2(3:0)', 'answer(3:0)', 'clk', 'reset', 'enable']
    >>> list(cable.name for cable in definition.cables)
    ['answer_1(0)', 'answer_1(1)', 'answer_1_(2)', 'answer_1(3)', ... ]
    >>> list(instance.name for instance in definition.children)
    ['un3_answer1_axbxc3', 'un2_answer2_axbxc3', 'reset_c_i', ... ]

**Compose a Netlist**

This example exports a netlist into an EDIF formatted netlist file by the given name.

.. code:: python

    >>> sdn.compose(netlist, '<filename>.edf')
   
The following equivalent code may also be used.

.. code:: python
   
    >>> netlist.compose('<filename>.edf')

**Additional Examples**

Additional examples are available in the documentation for netlist creation, analysis, and transformation.

Install
-------

The stable release of SpyDrNet can be installed using ``pip``::

    > pip install spydrnet

To install from PyPI with all optional dependicies use::

    > pip install spydrnet[all]

For more installation instruction, see :ref:`INSTALL.rst`.

Bugs
----

Bugs can be reported on the `issues page <https://github.com/byuccl/spydrnet/issues>`_ or they can be fixed through a fork / pull request. All changes are welcome. Discussion of ideas for new features is available on the `mailing list <https://groups.google.com/forum/#!forum/spydrnet-discuss>`_.

A Brief History
---------------

The `BYU Configurable Computing Lab <https://ccl.ee.byu.edu/>`_ actively maintains the `BYU EDIF Tools <http://reliability.ee.byu.edu/edif/>`_ - a Java API for creating, modifying, or analyzing EDIF netlists. These tools are tied to the EDIF netlist format and provide JEDIF tools capable of flattening a circuit (by removing hierarchical organization) and applying fault-tolerance techniques such as `triple modular redundancy (TMR) <https://en.wikipedia.org/wiki/Triple_modular_redundancy>`_. Development of SpyDrNet began back in 2016 with the idea of creating an accessible, format independent, tool for netlist analysis and transformation. The underlying intermediate data structure is designed preserve proper netlist relationship as a generic netlist while allowing for the preservation of format specific constructs. A language agnostic prototype was developed and this prototype soon became useful in the lab for netlist analysis and reliability transformation studies. A more mature (though still having room for growth) tool is presented here. 

Design Notes
------------

We have tried to build this tool around the principles of expandability and modularity. Care has been taken to separate different parts of the program in an organized fashion.

How to contribute
-----------------
If this tool has been useful to you, or have new feature ideas that you would like to implement, feel free to make a pull request, or take a look at the issues to see how to contribute. New ideas, bug fixes and suggestions are also welcome (See :ref:`CONTRIBUTING.rst`).

Special Thanks
--------------

Special thanks is given to `NetworkX <https://networkx.github.io/>`_ - "a python package for the creation, manipulation, and study of the structure, dynamics and functions of complex networks."  This mature project has been used as a template for much of SpyDrNet's documentation and code structure. It also has saved enormous effort in heavy graph analysis as a robust and complete library used to analyze the relationships between circuit nodes.

License
-------

Released under the BSD 3-Clause License (see :ref:`LICENSE`)::

   Copyright (C) 2019, Brigham Young University
   All rights reserved.
