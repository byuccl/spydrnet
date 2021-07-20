Namespace Manager
#################

SpyDrNet's callback framework was leveraged to implement a namespace manager that will raise an exception if a naming rule is violated. The managers themselves also provide an example of how the callback framework can be leveraged.

The namespace manager is a plugin that is loaded when the library is loaded. It will constantly be checking names and rejecting invalid or duplicate names. The active namespace can be set in code to allow for parsing in a different language or other cases where a valid name in the namespace may differ.

Currently there are 2 namespaces implemented. One for EDIF and one called Default.


Namespace Details (Default)
***************************

The namespace managers provide separate namespaces to be created based on element types. Both the default and EDIF namespaces allow for 1 namespace for Libraries indexed by the Netlist, 1 namespace for Definitions indexed by the Library and 3 namespaces for Ports, Cables, and Instances indexed by the Definition. This parallels EDIF and verilog Netlists well. Namespace scopes could be modified by creating a custom namespace manager (see the section below)

The namespace manager checks each of the namespaces when an object is added, removed, or renamed to ensure that the new name does not clash with an old name. Name comparisons are made against the ".NAME" entry in each element's dictionary. This value is set when the .name setter is used as well so no additional care needs to be used. The implementation was done using the dictionary lookup on the key ".NAME" to provide a simpler template on which additional keys could be watched.

The default manager accpets any name and has no restrictions, but it has the framework included to implement this when it is extended. The EDIF manager takes advantage of this feature.

EDIF Details
************

EDIF has a relativly restrictive naming convention. Names are not case sensitive, Their max length is 255 characters, and they cannont contain many special characters. Most names are composed of uper and lower case letters, numbers, and underscores. The only exception is names that begin with a `&` character. To compensate for this some EDIF netlsits use an rename construct to provide a more human readable name and convert the name to something that fits within the namespace as an EDIF identifer.

SpyDrNet's EDIF Namespace manager will look for case insensitive conflicts on the EDIF identifiers that are stored with the key "EDIF.identifier" along side the check for conflicts with the regular name in the default namespace.

Additionally the EDIF namespace manager will check the EDIF identifiers for invalid characters or or lengths longer than 255 characters or 256 if it starts with an &.

Using the namespace managers
****************************

Currently only "DEFAULT" and "EDIF" are avaiable namespaces. Verilog takes advantage of the "DEFAULT" namespace

code required to turn the namespace to a different one. code::

    >>> from spydrnet.plugins import namespace_manager
    >>> 
    >>> ns_default = namespace_manager.default #save the default just to be safe. (optional)
    >>> namespace_manager.default = "EDIF" #can be set to "EDIF" or "DEFAULT"
    >>> 
    >>> do_something_cool() #new namespace rules will apply
    >>> 
    >>> namespace_manager.default = ns_default #set the default back (optional)

The namespace manager that is selected will run in the background and watch for naming conflicts that occur as additions, modifications and removals take place on the netlist. Currently changing the namespace will not update the namespace with the existing netlist or details. Because of this, it is possible that unexpected errors may happen if the namespace is changed between operations (example: add a definition, change the namespace, remove a definition). This will likely be implemented at a future date.

Creating a new Namespace
************************

The directory `spydrnet/plugins/namespace_manager/__init__.py` holds the callback logic while the other files in the directory `edif_namespace.py` and `default_namespace.py` hold the logic that checks if names are valid. Adding additional namespaces requires creating a new class that implements all of the functions present in the default_namespace.py's DefaultNamespace. The DefaultNamespace itself can be inherited and only the functions needed overwritten.

Once implemented the __init__.py can be updated to include the namespace as a possible policy with an appropriate name string. Set the manager to be used with something like the example code above.
