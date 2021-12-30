.. _api_summary:

===========
API Summary
===========

Basic object types
------------------
.. toctree::
   :maxdepth: 2

   netlist
   library
   definition
   instance
   port
   innerpin
   outerpin
   cable
   wire
   href

The following three classes are the classes from which the above elements inherit. They are included here for completeness of
documentation and can be used if needed. If the above types will suffice it may be simpler to use them.

.. currentmodule:: spydrnet.ir
.. autosummary::
   :toctree: generated/

   Pin
   Bundle
   Element
   FirstClassElement
   
Getter Functions
----------------

.. currentmodule:: spydrnet
.. autosummary::
   :toctree: generated/
   
   get_netlists
   get_libraries
   get_definitions
   get_ports
   get_pins
   get_cables
   get_wires
   get_instances
   get_hinstances
   get_hports
   get_hpins
   get_hcables
   get_hwires

Other Functions
---------------
.. currentmodule:: spydrnet
.. autosummary::
   :toctree: generated/

   parse

.. currentmodule:: spydrnet
.. autosummary::
   :toctree: generated/

   compose

.. currentmodule:: spydrnet.flatten
.. autosummary::
   :toctree: generated/
   
   flatten

.. currentmodule:: spydrnet.uniquify
.. autosummary::
   :toctree: generated/

   uniquify

.. currentmodule:: spydrnet.clone
.. autosummary::
   :toctree: generated/

   clone



Shortcuts
---------

.. toctree::
   :maxdepth: 2
   
   getter_shortcuts

In Summary
----------

The SpyDrNet API can be used to create, analyze, and transform a netlist. Netlist are represented in memory in an Intermediate Representation. :numref:`fig:ExampleIR` show the representation of a simple circuit in the SpyDrNet Intermediate Representation.
If you would like an example of using the SpyDrNet tool to create a netlist like this, click :ref:`here <sphx_glr_auto_examples_basic_minimal.py>`  

.. _fig:ExampleIR:
.. figure:: ../../figures/ExampleCircuit.png
 :align: center
 :alt: Example Netlist in a SpyDrNet Intermediate Representation

 Example Netlist in the Intermediate Representaion

The API calls documented here can be used in Python as follows:

>>> # create an empty netlist and add an empty library to it
>>> import spydrnet as sdn
>>> netlist = sdn.ir.Netlist()
>>> library = netlist.create_library()
>>>

If the parser is used, the calls can be made in the same way:

>>> # parse an edif file in and add an empty library to the netlist.
>>> import spydrnet as sdn
>>> netlist = sdn.parse('four_bit_counter.edf')

>>> library = netlist.create_library
>>>

