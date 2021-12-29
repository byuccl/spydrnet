"""
Using Extensions
----------------

A simple example using the spydrnet_extension module to illustrate the extension of SpyDrNet IR classes.

The .spydrnet file contains:

.. code-block::

    spydrnet_extension

which extends both Element and FirstClassElement, two base classes for SpyDrNet IR objects.

Here we import Element and FirstClassElement both from their respective modules and from the spydrnet.ir directory. The first will not be extended while the latter will be.

.. code-block::
    
    from spydrnet.ir.element import Element
    from spydrnet.ir.first_class_element import FirstClassElement
    from spydrnet.ir import Element as ElementExtended
    from spydrnet.ir import FirstClassElement as FirstClassElementExtended

Then we list the attributes and methods found in the extended version but not in the original versions of the classes.

.. code-block::

    print("ElementExtended:")
    print("\t",list(attribute for attribute in dir(ElementExtended) if attribute not in list(thing for thing in dir(Element))))
    print("FirstClassElementExtended:")
    print("\t",list(attribute for attribute in dir(FirstClassElementExtended) if attribute not in list(thing for thing in dir(FirstClassElement))))

We can also simply print lists of the attributes and methods found in each class. One can see that the extended class truly is extended.

.. code-block::

    print("Element: ",list(attribute for attribute in dir(Element)))
    print("ElementExtened: ", list(attribute for attribute in dir(ElementExtended)))
    print("")
    print("FirstClassElement: ",list(attribute for attribute in dir(FirstClassElement)))
    print("FirstClassElementExtended: ",list(attribute for attribute in dir(FirstClassElementExtended)))

**See full source code below**
"""
from spydrnet.ir.element import Element
from spydrnet.ir.first_class_element import FirstClassElement
from spydrnet.ir import Element as ElementExtended
from spydrnet.ir import FirstClassElement as FirstClassElementExtended

print("ElementExtended:")
print("\t",list(attribute for attribute in dir(ElementExtended) if attribute not in list(thing for thing in dir(Element))))
print("FirstClassElementExtended:")
print("\t",list(attribute for attribute in dir(FirstClassElementExtended) if attribute not in list(thing for thing in dir(FirstClassElement))))

print("Element: ",list(attribute for attribute in dir(Element)))
print("ElementExtened: ", list(attribute for attribute in dir(ElementExtended)))
print("")
print("FirstClassElement: ",list(attribute for attribute in dir(FirstClassElement)))
print("FirstClassElementExtended: ",list(attribute for attribute in dir(FirstClassElementExtended)))