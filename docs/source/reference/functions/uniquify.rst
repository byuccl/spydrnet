Uniquify
=========

version 1.3.0

Background
----------
Netlists may have many instances of any given definition. This is sometimes
true of high level and user defined constructs and frequently true of
constructs like LUT6s or other leaf cells.

Uniquify aims to ensure that all non-leaf cell instances are instances of
unique definitions. In other words if there are two instances of any given
definition, new definitions will be created for each of the existing
instances.

This type of uniquify is useful for applying various transformations and 
analysies to netlists.

Implementation
--------------
Uniquify can be called like this sdn.uniquify(netlist) where netlist is a
netlist object. This can only be called on a netlist and it will start at
the top instance and ensure that each instance below it will be unique.
Instances that are not under the top instance are not garanteed to be
unique. Cells that have the is_leaf property set will not be made unique.