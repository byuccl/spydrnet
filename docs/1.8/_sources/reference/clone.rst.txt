Clone
=====
Several of the elements in SpyDrNet allow themselves to be cloned with a built in clone function.
This funciton is accessable to the user through both a sdn.clone() call as well as element.clone()
Clone operates differently on each of the elements on which it can be called but there are some
principles they share in common.

Clone will orphan each element that has a parent. For example libraries will be orphaned from
netlists, dictionaries will be orphaned form libraries and so on. The elements will also try to
maintain cloned downward connections but most side level connections will be severed. The following
list attempts to outline the behaviour of each of these components

Netlists
--------
All components will be cloned and connections will be reestablished to the cloned counterpart in
the new netlist. For example a definition named A with an instance a in the original netlist will
have a definition A(clone) with an instance a(clone) that each referece the other. if instance a
was instanced inside of definition B in the original netlist it will be instanced inside of B(clone)
in the new netlist. All wires and pins will likewise maintain their connections

libraries
---------
When cloning only a library the cross library references are maintained. All internal references in
the cloned library will be updated to reference components in the new library. The library will also
be orphaned. 

For example library A contains a definition B. library C contains a definition D. definition B has
an instance that references definition D. if I were to clone library A I would have a library A(clone)
that will contain definition B(clone) definition B will contain a cloned instance with a reference to
D. D will have a new instance, the child of B(clone) in it's references list.

Definition
----------
When cloning a definition all sub elements of the definition will be cloned. this includes instances
ports and cables. These elements will all connect to the new cloned elements the same way the old 
ones connected. The Definition will be orphaned from the library to which it belonged. The references
of the definition will also be cleared so that there is no conflict between the clone and the
existing definition with regards to which definition defines the instances that exist.

Port
----
The port will be cloned with all of its pins. It will belong to no definition and will not be
connected to any wires.

Cable
-----
The cable and all wires will be cloned. They will be disconnected from all pins. And the cable will
not belong to any definition

Instance
--------
The instance will maintain its reference but will not be connected to any wires and will not be the
child of any definition. outer pins will maintain their connections to inner pins.

Pins and Wires
--------------
Pins and wires will be cloned but disconnected from all other pins and wires. outer pins connections
to inner pins will also be disconnected.

Other notes
-----------
First class elements can contain other information in the form of dictionary entries. In the python
implementation of SpyDrNet, these elements are cloned by calling python's built in deep copy on them.
Officially we support string, and other primative type entries in these dictionaries. However if you
feel like aiming a gun at your feet (or you are trying to figure out how to add support for new 
constructs that you need), the clone function should probably work if you implement the deep copy 
function on your entry object.