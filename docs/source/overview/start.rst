Getting Started with SpyDrNet
=============================

SpyDrNet was originally built for EDF netlist, but has since been expanded to Verilog and EBLIF netlists.

* Note 
    This guide makes references to SpyDrNet TMR

Parsing
-------

**Default parsing arguments**

``parse(filename, architecture=None):``

filename 

- Name of the file that is being parsed

architecture 

- Desired board architecture


**General structure**

``netlist = sdn.parse(filename, ...)``

**Basic structure for Verilog netlist**

``netlist = sdn.parse("filename.v", architecture=XILINX_7SERIES)``

**Basic structure for EDF netlists**

``netlist = sdn.parse("filename.edf")``

*edf usually only needs the filename and not the other arguments*

Composing
----------

**Default composing arguments**

``compose(netlist, filename, voters=[], definition_list=[], write_blackbox=True, write_eblif_cname=True, defparam=False):``

netlist 

- Netlist that was parsed in / replicated / changed

filename 

- Desired output name of netlist

voters 

- List of voters that was created in script *this is only needed for verilog netlists*

definition_list 

- List of definitions to write

write_blackbox 

- Flag that skips writing black boxes/verilog primitives

write_eblif_cname 

- Flag

defparam 

- Flag that composes parameters in *defparam* statements instead of using #()


**General structure**

``netlist.compose(filename, ...)``

**Basic structure for Verilog netlist**

``netlist.compose("filename_tmr.v", voters, reinsert_space=True)``

**Basic structure for EDF netlists**

``netlist.compose("filename_tmr.edf")``

*edf usually only needs the filename and not the other arguments*

