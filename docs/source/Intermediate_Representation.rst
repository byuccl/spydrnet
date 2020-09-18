Intermediate Representation
===========================

The SpyDrNet API can be used to create, analyze, and transform a netlist. Netlist are represented in memory in an Intermediate Representation. :numref:`fig:ExampleIR` show the representation of a simple circuit in the SpyDrNet Intermediate Representation.


.. _fig:ExampleIR:
.. figure:: ./figures/ExampleCircuit.png
 :align: center
 :alt: Example Netlist in a SpyDrNet Intermediate Representation

 Example Netlist in the Intermediate Representaion

The API calls documented here can be used in Python as follows:

>>> # create an empty netlist and add an empty library to it
>>> import spydrnet as sdn
>>> netlist = sdn.ir.Netlist()
>>> library = netlist.create_library()
>>>

Similarly if the parser is used the calls can be made in the same way:

>>> # parse an edif file in and add an empty library to the netlist.
>>> import spydrnet as sdn
>>> netlist = sdn.parse('four_bit_counter.edf')

>>> library = netlist.create_library
>>>

spydrnet.ir
-----------

.. automodule:: spydrnet.ir

.. autosummary::
   :toctree: generated/
   

   Netlist
   Library
   Definition
   Instance
   Port
   InnerPin
   OuterPin
   Cable
   Wire

The following three classes are the classes from which the above elements inherit. They are included here for completeness of
documenataion and can be used if needed. if the above types will suffice it may be simpler to use them.

.. automodule:: spydrnet.ir

.. autosummary::
   :toctree: generated/

   Pin
   Bundle
   Element

spydrnet.util.hierarchical_reference
------------------------------------

.. automodule:: 
   spydrnet.util.hierarchical_reference

.. autosummary::
   :toctree: generated/

   HRef

spydrnet.clone
--------------

.. automodule:: 
   spydrnet.clone

.. autosummary::
   :toctree: generated/

   clone

.. automodule:: 
   spydrnet.uniquify

.. autosummary::
   :toctree: generated/

   uniquify

.. automodule:: 
   spydrnet.flatten

.. autosummary::
   :toctree: generated/

   flatten

.. automodule:: 
   spydrnet.util.get_netlists

.. autosummary::
   :toctree: generated/

   get_netlists

.. automodule:: 
   spydrnet.util.get_libraries

.. autosummary::
   :toctree: generated/

   get_libraries

.. automodule:: 
   spydrnet.util.get_definitions

.. autosummary::
   :toctree: generated/

   get_definitions
