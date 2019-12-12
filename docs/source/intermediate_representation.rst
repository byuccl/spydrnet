.. _sec:ir:

Intermediate Representation
===========================

The Environment object can be thought of as the base folder of a project that holds other folders. The main function of the Environment object is to hold instances of the Library class, each holding instances of the Definition class. It can be useful to think of each Definition object as defining a class within Spydrnet. When a Definition is instantiated, and Instance object is created within another Definition object. Definition object hold Instance objects of other Definitions as well the Port objects and Cables objects. Port objects, and the InnerPin object that makes up Port objects, indicate how the outside world can interact with Instances of the Definition. Cables objects hold closely related Wire, like a bus, objects that connect Instances within a Definition together as well as connecting them to the Definitions Ports.

The basic elements of a netlist are describe here to draw parallels to the elements found in a SpyDrNet Intermediate Represention (IR). Most netlist formats have associated with them some sort of design or implmenentation environment. Within an environment is a collection libraries. A library contains specific definitions of design components. A definition of a design component goes by many names in different netlist formats: cell, module, component, entity, etc. A definition contains a collection of ports, cables, and instances of other definitions. The term "ports" and "cables" are anagolous to computer ports and cables that most people are familiar with. This terminology was selected because it differs from common convention. Ports are a collection of pins, and cables are a collection of wires. Within netlist formats, the interface to a defintion is defined as a collection of ports, which are typically given a name and sometimes only denoted as a port by there position in the definition signature or by reference to their data flow direction. Ports in a netlist bundle a collection of pins or connections points within the port. Cables in a netlist go by many names: wire, bus, etc. They bundle a collection of wires or connectors within the cable. A wire within a cable contains a collection of pins. These pins can either be on a port of the definition that contains the wire, or on a port of an instance within the definition that contains the wire.

Instance objects are used to represent an instance of a Definition in a netlist. The terms "instance" and "definition" are intentionally overloaded. In object oriented programming (OOP), an object type has a definition that defines the members and methods for objects of that type. In OOP, a definition of an object type can be instantiated to create an instance of that object type. Similarly, in netlist a cell, module, component or entity has associated with it a defininition that define the internals of the netlist object. The definition of a netlist object can be instanced multiple times elsewhere in the netlist. SpyDrNet IR represents the definition of a cell, module, component, or entity (whatever it is called in the originating format) as a Definition element, which is an OOP object instance. Instances of a netlist object are represented as an Instance element, which is an OOP object instance with a pointer to the Definition element that it instances in the netlist. Because pin connections on the ports of a definition are also instanced, each Instance element also holds a collection of OuterPin elements that point to the InnerPin elements that they instance. OuterPins and InnerPins are both pins on a port. OuterPins refer to the pin on the outside of an instance and InnerPins refer to pins on the inside of a definition. An OuterPin contains a pointer to the InnerPin it instances, but InnerPins do not contain pointer to outer pins that reference them.

A bundle of pins or a bundle of wires can either be a scalar bundle or an array bundle. If a bundle is an array, it is indexable meaning that members within the bundle can be indexed. It is possible to have an bundle that is an array with only one member, which should not be confused with a bundle that is a scalar. A bundle that is a scalar is not indexable, any reference to it refers directly to its single member. The concept of a bundle is not divided into two seperate concepts for a bundle that is a scalar and a bundle that is a vector because keeping them as a single concept greatly simplies things.

.. A netlist contains information about an electronic circuit. Almost all the information needed to implement an electric circuit is avaiable in a netlist. Additional constraints, such as timing, placement, and routing constraints, are contained in seperate location, but they make reference to nets or components in a netlist. Nets are connections between components. Components are functional blocks. The blocks interface with other blocks through ports and ports have individual connections points called pins. A net can be thought of as a physical wire that connects a set of pins together. A block can be either a primitive component, (e.g., look-up table, flip-flop, DSP unit), a blackbox with undefined content, or a hierarchical component with nets and instances of other components contained inside. 

Classes
-------

.. automodule:: spydrnet.ir

.. autoclass:: Netlist
    :members:
    :undoc-members:
    
.. autoclass:: Library
    :members:
    :undoc-members:
    
.. autoclass:: Definition
    :members:
    :undoc-members:
    
.. autoclass:: Instance
    :members:
    :undoc-members:
    
.. autoclass:: Port
    :members:
    :undoc-members:
    
.. automodule:: spydrnet.virtual_ir

.. autoclass:: VirtualInstance
    :members:
    :undoc-members:

.. autoclass:: VirtualPort
    :members:
    :undoc-members:
    
.. autoclass:: VirtualPin
    :members:
    :undoc-members:
    
.. autoclass:: VirtualCable
    :members:
    :undoc-members:
    
.. autoclass:: VirtualWire
    :members:
    :undoc-members:
