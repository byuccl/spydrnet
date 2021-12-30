.. _extensions:

**********
Extensions
**********

SpyDrNet supports the extension of IR classes.

How It's Done
**************

Modules specified in a .spydrnet file are imported and put into a dictionary named "active_plugins". Then, the *__init__.py* in spydrnet/ir iterates through each IR class and, with each imported module in active_plugins, attempts to add attributes and methods to the SpyDrNet classes.


Using Extensions
****************

Include a .spydrnet File
^^^^^^^^^^^^^^^^^^^^^^^^
    The SpyDrNet *__init__.py* file looks for a **.spydrnet** file first in the current directory and then in the home directory. If no such file is found, no modules will be loaded and no classes will be extended.
    
    The content of the .spydrnet file is simply a list of the modules that should be imported and used to extended the IR classes. For example, a .spydrnet file could contain::

        spydrnet_extension1
        spydrnet_extension2
    

Naming Convention
^^^^^^^^^^^^^^^^^

    Each module used to extend SpyDrNet must be named as "spydrnet_<extension_module_name>"

Class Imports
^^^^^^^^^^^^^
    In order to ensure use of the extended version of each SpyDrNet IR class, import using:

        .. code-block::

            from spydrnet.ir import <ir_class>

    rather than:

        .. code-block::

            from spydrnet.ir.ir_class import <ir_class>

Creating An Extension
*********************

When creating an extension for SpyDrNet, be sure to do the following:

#. Follow the naming convention found above
#. Use the SpyDrNet classes as base classes

An example of a dummy extension is *spydrnet_extension*, which is found in the SpyDrNet repository. See `Element Extension <https://github.com/byuccl/spydrnet/blob/efa736528bd4d4ce51817dec217319530a911f37/spydrnet_extension/ir/element.py#L5>`_ and `FirstClassElement Extension <https://github.com/byuccl/spydrnet/blob/efa736528bd4d4ce51817dec217319530a911f37/spydrnet_extension/ir/first_class_element.py#L14>`_ for a simple example of extending an IR class performed with spydrnet_extension.

For an example of a full, working module that extends the SpyDrNet classes, see `spydrnet_physical <https://github.com/ganeshgore/spydrnet-physical>`_.
