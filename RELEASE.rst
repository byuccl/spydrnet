SpyDrNet 1.12.2
----------------
April 18, 2023

* Bug fix for Verilog parser for partially connected ports being misaligned and fixed primitive name with a space at the end.
* Changed some of the os.path to pathlib to conform to updated coding standards

SpyDrNet 1.12.1
----------------
February 2, 2023

* Bug fix for names in EDIF netlists in which they were cut off if more than 100 characters long. Now the allowed number of characters in a name is 255.
* Slight additions to documentation about doing a release 
* Removing Travis CI (from now on only Github Actions will do automated testing)
* Fixed bug where architecture liraries were not included in the release

SpyDrNet 1.12.0
----------------
November 9, 2022

* Major improvements and fixes for the Verilog netlist parser and composer to broaden support and accuracy
* Built in primitive libraries to allow SpyDrNet to populate port directions of primitives when parsing netlist types that don't always explicitly define primitive cells (Verilog, EBLIF). An option is added to parsing to specify which primitive library to use.
* Improvements, fixes, and simplification to EBLIF netlist parser and composer
* Verilog parser and composer option to remove/add lagging space in names
* Documentation updates and improvements 

SpyDrNet 1.11.1
---------------
April 20, 2022

* Bug Fix. Now EBLIF support should actually be included.

SpyDrNet 1.11.0
---------------
April 9, 2022

* Initial support for parsing and composing EBLIF netlists.

SpyDrNet 1.10.1
----------------
January 1, 2022

* Fixes some parts that did not fully detail dropping support for Python 3.5
* Improvements to documentation about doing a release

SpyDrNet 1.10.0
---------------
December 29, 2021

* Introduces support for loading other modules to extend IR classes
* Drops support for Python 3.5 and adds support for Python 3.9 and 3.10
* Adds Pylint to Github Actions
* Various documentation updates

SpyDrNet 1.9.0
---------------
November 17, 2021

* Incorporates Github Actions for automated testing
* Minor shortcut additions in IR classes
* Minor documentation updates
* Improved comment handling in the Verilog parser
* Enhanced the Verilog composer

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
