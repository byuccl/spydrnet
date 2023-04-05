Getting Started with SpyDrNet
=============================

SpyDrNet was originally built for EDF netlist, but has since been expanded to Verilog and EBLIF netlists.

* Note 
    This guide makes references to SpyDrNet TMR

Parsing
-------

**Default parsing arguments**

``parse(filename, architecture=None, remove_space=False, path_used=False):``

filename 

- Name of the file that is being parsed

architecture 

- Desired board architecture

remove_space 

- Flag used for verilog netlists to insure that the triplicated primitives do not have a space in the middle of their name

path_used 

- Flag that allows for the use of pathlib.Path to find files not in current directory


**General structure**

``netlist = sdn.parse(filename, ...)``

**Basic structure for Verilog netlist**

``netlist = sdn.parse("filename.v", architecture=XILINX_7SERIES, remove_space=True)``

**Basic structure for EDF netlists**

``netlist = sdn.parse("filename.edf")``

*edf usually only needs the filename and not the other arguments*



Composing
----------

**Default composing arguments**

``compose(netlist, filename, voters=[], definition_list=[], write_blackbox=True, write_eblif_cname=True, defparam=False, reinsert_space=False):``

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

reinsert_space 

- Flag to If remove_space was used in the parser (for verilog netlists) reinsert_space needs to be used to allow the primitves to have the correct syntax for Vivado

**General structure**

``netlist.compose(filename, ...)``

**Basic structure for Verilog netlist**

``netlist.compose("filename_tmr.v", voters, reinsert_space=True)``

**Basic structure for EDF netlists**

``netlist.compose("filename_tmr.edf")``

*edf usually only needs the filename and not the other arguments*

