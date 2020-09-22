API
===
.. automodule:: spydrnet

The SpyDrNet API can be used to create, analyze, and transform a netlist. Netlist are represented in memory in an Intermediate Representation. :numref:`fig:ExampleIR` show the representation of a simple circuit in the SpyDrNet Intermediate Representation.


.. _fig:ExampleIR:
.. figure:: ../figures/ExampleCircuit.png
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



.. autosummary::
   :toctree: generated/
   

   ir.Netlist
   ir.Library
   ir.Definition
   ir.Instance
   ir.Port
   ir.InnerPin
   ir.OuterPin
   ir.Cable
   ir.Wire

The following three classes are the classes from which the above elements inherit. They are included here for completeness of
documenataion and can be used if needed. if the above types will suffice it may be simpler to use them.


.. autosummary::
   :toctree: generated/

   ir.Pin
   ir.Bundle
   ir.Element

spydrnet.util
-------------

.. autosummary::
   :toctree: generated/

   util.hierarchical_reference.HRef
   clone.clone
   uniquify.uniquify
   flatten.flatten
   util.get_netlists.get_netlists
   util.get_libraries.get_libraries
   util.get_definitions.get_definitions
   util.get_instances.get_instances
   util.get_ports.get_ports
   util.get_pins.get_pins
   util.get_cables.get_cables
   util.get_wires.get_wires
   util.get_hinstances.get_hinstances
   util.get_hports.get_hports
   util.get_hpins.get_hpins
   util.get_hcables.get_hcables
   util.get_hwires.get_hwires
