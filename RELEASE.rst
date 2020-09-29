SpyDrNet 1.6.0
--------------
September 24, 2020

* Fixed minor issue with verilog parser composer access
* Update Documentation and its organization

SpyDrNet 1.5.0
--------------
September 1, 2020

* Verilog Parser
* Verilog Composer

SpyDrNet 1.4.0
--------------
April 21, 2020

* Flattening functionality
* Bug fixes

SpyDrNet 1.3.0
--------------
March 19, 2020

This is a major functionality wise release.

* Added Hierarchical references
* Added clone functionality
* Added whole netlist uniquify ability
* Updated/Fixed the composer and parser to use the new element[".NAME"] feature
* Updated/Fixed the namespace manager to allow for multiple netlists in a session
* Updated callback framework to autoregister implemented functions.
* Added verilog tokenizer based on ``ply``
* Added tcl scripts for converting EDIF netlist to Verilog using Vivado
* Added powerful getter functions and shortcuts to ease naviation of the nextlist
* Updated examples and documentation

SpyDrNet 1.2.0
--------------
February 7, 2020

* Added a .name property that points to element[".NAME"]
* Added a figure to the API specification
* Added a EDIF namespace manager using the callback framework
* Added a references to definitions (pointing to all instances of a definition)
* Converted several EDIF netlists to verilog for aiding parser converted with Vivado

SpyDrNet 1.1.0
--------------
January 18, 2020

* Added the callback framework for plugin support
* Updated documentation: logo, links to related projects, very simple ciruit diagram
* Added three examples: flattening, single use definitions, connectivity graph

SpyDrNet 1.0.1
--------------
January 13, 2020

* Fixed bug with indexing in the is array and is scalar functions

SpyDrNet 1.0.0
--------------
December 19, 2019

* Support for datastructure api calls
* Documentation is complete
* Examples included
