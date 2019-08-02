.. sec:uniqref

Unique References
=================

A netlist can have more than once instance of a single definition. A unique reference points to a specific instance. For
example, consider a netlist with cell definitions `A` and `B`. Definition `A` instances definition `B` twice. A unique
reference makes it possible to refer to a specific instance in hierarchy. This becomes more important with additional 
levels of hierarchy. Consider another cell definition in the same in the same library that instances definition `A` 
twice. With a unique reference you can point to a specfic instance of the now four instances of `B`.

In the simplest sense, a unique reference is a chain of cell instances: TopInstance, MiddleInstances, and LeafInstance. 
Much like a file path, a unique reference leverages instance hierarchy to refer to a specific instance.

A unique reference can be a string. This form of a unique reference provides a chain of cell instances that are 
deliniated by a hierarchical seperator character. Conventionally, the seperator character is a forward slash, `/`, but 
it can be any character. An example of a unique reference in the form of a string is 
`top_instance/cpu/alu/adder/carry_reg[1]`. This reference can be split into a list of instances by considering each
substring between the hierarchical seperator. 

Going down in hierarchy is not a problem, comming up is the problem. Think of a string attached to the top instance.   