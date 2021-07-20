SpyDrNet 1.8.3
--------------
July 20, 2021

* Bug fix in EDIF parser
* Documentation updates
* Added support for .edn
* Added tests
* Improved vo, vqm parsing

SpyDrNet 1.8.2
--------------
June 24, 2021

* updated tutorial 
* improved How To Contribute page
* general documentation improvements

SpyDrNet 1.8.1
--------------
May 21, 2021

* improved the verilog parser and composer
* added vivado exmaples and refined other existing examples
* this build supports Python 3.5
  

SpyDrNet 1.8.0
--------------
April 23, 2021

* included the miniscript to the graph in API summary in the documentation
* added pretty print functions for some Intermediate Representation
* Warning: The Verilog composer is still in progress but works the same as 1.7.0 for now
* Warning: We don't suggest using Python 3.5 for this release. There is an issue with the Verilog parser associated with Python 3.5
  
SpyDrNet 1.7.0
--------------
January 21, 2021

* Updated Verilog Parser and Composer to be more generic
* included Tutorial in the documentation
* added some API shortcuts and updated its usage in the documentation

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
