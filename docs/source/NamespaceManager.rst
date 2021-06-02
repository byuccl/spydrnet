Namespace Manager
#################

SpyDrNet's callback framework was leveraged to implement a namespace manager that will raise an exception if a naming rule is violated.



Creating a new Namespace
************************

The directory `spydrnet/plugins/namespace_manager/__init__.py` holds the callback logic while the other files in the directory `edif_namespace.py` and `default_namespace.py` hold the logic that checks if names are valid. Adding additional namespaces requires creating a new class that implements all of the functions present in the default_namespace 
