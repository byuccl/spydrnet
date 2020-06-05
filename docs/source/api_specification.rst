.. _sec:api_spec:

API Specification
=================

The SpyDrNet API can be used to create, analyze, and transform a netlist. Netlist are represented in memory in an Intermediate Representation. :numref:`fig:ExampleIR` show the representation of a simple circuit in the SpyDrNet Intermediate Representation.


.. figure:: figures/ExampleCircuit.*
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

.. automodule:: spydrnet.ir

.. autoclass:: Netlist
    :members:
    :undoc-members:
    
.. autoclass:: Library
    :members:
    :undoc-members:
    
.. autoclass:: Definition
    :members:
    :undoc-members:
    
.. autoclass:: Instance
    :members:
    :undoc-members:
    
.. autoclass:: Port
    :members:
    :undoc-members:

.. autoclass:: InnerPin
    :members:
    :undoc-members:

.. autoclass:: OuterPin
    :members:
    :undoc-members:

.. autoclass:: Cable
    :members:
    :undoc-members:

.. autoclass:: Wire
    :members:
    :undoc-members:

The following three classes are the classes from which the above elements inherit. They are included here for completeness of
documenataion and can be used if needed. if the above types will suffice it may be simpler to use them.

.. autoclass:: Pin
    :members:
    :undoc-members:

.. autoclass:: Bundle
    :members:
    :undoc-members:

.. autoclass:: Element
    :members:
    :undoc-members:
