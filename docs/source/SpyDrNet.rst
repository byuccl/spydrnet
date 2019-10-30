



SPECIFICATION
=============

Specification for version 1.0 of the tools.

Some of the features that are needed for this release include
* The ability to parse EDIF files.
* The ability to compose EDIF files. (note other formats are a priority for future releases)
* Our current Intermediate Representation
* Our current Implementation of Virtual Instances

With virtual instances and the intermediate representation the documentation needs to be collected into one central location. Also functional tests should be created (we might already have some of these. we could collect them into one place) to test the overall functionality of the intermediate representation and virtual instances.

The remaining features that need more work are outlined in the following sections
* Documentation
* API

Documentation
-------------
The tools contain the following bits of documentation:
* A getting started users guide
* Function level documentation of end user facing APIs
* A deep look at the intermediate representation
* Intro to the intermediate representation
* Readme
* This Specification

a breif summary of each piece of documentation is provided below

**The Getting Started Users Guide**
This guide outlines how to dive in and start using the tools from a new users perspective. It also outlines some of the key features of the tools through a hello world type example of how to use the tools.

**Function Level Documentaiton of End User Facing APIs**
This guide provides API specification that is used by the tools. This guide gives users the inputs and outputs that the API provides. It allows the user to create their own parsers, composers, analysis, and transformation tools on top of the SpyDrNet tool. End users should feel free to contribute tools that they find of particular interest to the examples portion of the codebase

**A deep look at the intermediate representation**
This guide is an important reference for users who wish to become more familiar with the interals of the tool. This guide is a recomended read for those who want to work directly on extending or improving the tools because it outlines the details of the internal representation and how they were thought about and decided. The virtual instances should also be described as well as what function the fill. I feel that most of this document exists but needs to be collected from various places

**Intro to the Intermediate Representation**
This document will provide a high level overview of what components are in the intermdiate representation. It will include information in a way easy for the new user to understand and figure out. Since the intermediate representation is a generic netlist this document should be written as a reference for users of other netlists. Deeper information can be linked to in the previously mentioned document

**Readme**
This document outlines the details of how to get the tool installed and where to find the other documentation. it should contain the following information:
Dependencies
Recomended packages as well as a breif summary of why
How to install the tool on Windows, Linux (Mac?)
A very quick example of how to import the tool
How to find the other documentation


Intermediate Representation
---------------------------
In this releas we need to include the intermediate representation. This representation is already coded in our code base. Some additional tests should be run on the representation to ensure we are releasing

Virtual instances
-----------------

virtual instances - this is key!!!

virtual elements -
mirror of real elements in the design
what is an instance:
an instantiation of a definition in a netlist
definitions can be instanced more than once 
becuase it can be instanced more than once virtual instances uniquely identify the instances of the definitions
it is a hierarchical location in the actual netlist instantiation as well
you can know exactly where you are in the netlist

"A virtual instance is a unique reference to an instance of a definition" 

The information is stored in the netlist the virtual instance provide a unique pointer to instances of elements
This simplifies access to the netlist for graph analysis without worrying about implementing this yourself.

The inner pin is the virtual pin
outer pin is not created until it is connected
outer pin can be found from the inner pin


The intermediate representation

The API

getting started guide

Write out what the things are supposed to do

API
---

This section defines the API for the tools that can be used to extend the tools and do cool things to netlists. The API can be roughly split into 3 categories. The creation, The analysis, and The modification. Each element in the design has functions that allow creation and deletion. The API can also be split into the virtual and the netlist components. The API functions that are included in this release are the following:

Creation API on non-virtual netlist objects

* create_netlist()
* create_definition()
* create_instance()
* create_port()
* create_cable()
* create_library()
* create_property()

The api of each of these calls is simple. Each of the calls creates an orphaned object of the type with the name passed in as a parameter
The parameters are a name
???if an object of the creation type is passed in the return is an exact deep copy of that object.


Outline for the rest of the specification
-----------------------------------------
virtual instances are included
beware of those
current netlist and instances are included in the top level netlist
The top level is really a netlist
Change the word environment to netlist
The state is kept at the top level in the Global environment manager

The API needs
get_definitions
get_cells
get_virtual_instances

get_virtual_instances

persist_once_global_data (singleton at the top level)

slots (in the python dictionary of each object)

get_virtual_pins
