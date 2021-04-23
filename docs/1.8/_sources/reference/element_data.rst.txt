.. _sec:element-data:

Element Data
============

Each netlist element allows for arbitrary data to be associated with it. This is accomplished using a Python ``dict``.

Keys
----

Keys are ought to be strings with ``.`` seperated namespaces. Element properties from the originating netlist format
belong in the root namespace (without any ``.``). The NULL namespace (keys with a leading ``.``) is reserved for use by
SpyDrNet. For example::

    >>> element['.NAME'] = "name_of_element"
    
The ``'.NAME'`` key in this example is the key ``NAME`` in the NULL namespace. The key is reserved for the reference
name of elements.

Language specific constructs can be sored under key entries within the namespace of the specific language. For example::

    >>> netlist[EDIF.edifVersion] = (2, 0, 0)
    
The key value par stores the EDIF version used by an EDIF netlist.

Setting Data
------------

Data is set using the Python ``__setitem__`` magic function meaning that data can be set using this syntax::

    >>> element['<key>'] = value
    
Getting Data
------------

Data can be read through itteration::

    >>> for key in element:
    >>>     print(key, element[key])
    >>>
    
Or by using the using the Python ``__getitem__`` magic function by itself::

    >>> print(element['<key>'])
    value
    
A read only view of the data dictionary can be obtained from ``element.data``. The returned object acts and feels like
a Python dictionary, but mutator functions are disabled. This allows for the automated managment of the dictionary.

Deleting Data
-------------

Entries in the dictionary can be deleted using the `__delitem__` magic function as follows::

    >>> del element['<key>']
    