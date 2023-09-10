.. _using_example_netlists:

Using SpyDrNet Example Netlists
----------------------------------

Many EDIF, Verilog, and EBLIF example netlists are found in the SpyDrNet repo under *example_netlists*. In versions of SpyDrNet previous to 1.13, the example netlists were included in the python package. From version 1.13 on, perform the steps below to access the example netlists using *sdn.load_example_netlist_by_name(<name>)*.

Option 1
^^^^^^^^^

1. Download the `example netlists directory <https://github.com/byuccl/spydrnet/tree/move_tests_and_files/example_netlists>`_ from the `SpyDrNet repo <https://github.com/byuccl/spydrnet>`_, or just clone the repo. 

2. In the Linux terminal, run

    .. code-block::

        export EXAMPLE_NETLISTS_PATH=<path to example netlists>

    where the <path to example netlists> is the path to the top level example netlists directory in the spydrnet repo.

3. Use the *sdn.load_example_netlist_by_name(<name>)* to access the example netlist. For example:

    .. code-block::

        import spydrnet as sdn
        netlist = sdn.load_example_netlist_by_name("b13")

Option 2
^^^^^^^^^

Run the following code and type 'y' and then hit enter when asked whether or not to download the example netlists.

.. code-block::

        import spydrnet as sdn
        netlist = sdn.load_example_netlist_by_name(<name>)

Additional Information
^^^^^^^^^^^^^^^^^^^^^^^

It is possible to see the names of the example netlists for each netlist format

.. code-block::
    
    print(sdn.example_netlist_names) # lists the names of the EDIF example netlists
    print(sdn.verilog_example_netlist_names) # lists the names of the Verilog example netlists
    print(sdn.eblif_example_netlist_names) # lists the names of the EBLIF example netlists

By default, sdn.load_example_netlist_by_name() assumes the netlists is EDIF format. To load a Verilog or EBLIF example netlist, do the following:

.. code-block::

    import spydrnet as sdn
    from spydrnet.util.netlist_type import VERILOG, EBLIF

    verilog_example_netlist = sdn.load_example_netlist_by_name(name, VERILOG)
    eblif_example_netlist = sdn.load_example_netlist_by_name(name, EBLIF)

