Flatten
=======

``flatten`` removes hierarchy below the top instance by moving its children
and cables into the top definition. Before calling it, run ``uniquify`` on the
netlist:

.. code-block:: python

   from spydrnet.flatten import flatten
   from spydrnet.uniquify import uniquify

   uniquify(netlist)
   flatten(netlist)

This order matters when two instances refer to the same non-leaf definition.
Flattening moves the first instance's children and cables out of that shared
definition. Without ``uniquify``, the second instance no longer has its own
children and connections to flatten. ``uniquify`` gives each such instance a
separate definition before the move. See `issue 220
<https://github.com/byuccl/spydrnet/issues/220>`_ for a two-instance example.

Both functions modify the netlist in place. ``uniquify`` starts at the top
instance and does not make unreachable definitions unique.
