import typing
from spydrnet.ir.first_class_element import FirstClassElement as FirstClassElementBase


if typing.TYPE_CHECKING:
    # This section is only for typing support
    # This enables auto completion during code editing
    from spydrnet.ir.first_class_element import FirstClassElement as FirstClassElementSDN
    from spydrnet_extension.ir.element import Element as ElementExt
    FirstClassElementBase = type(
        "FirstClassElementBase", (FirstClassElementSDN, ElementExt), {})


class FirstClassElement(FirstClassElementBase):
    ''' Extends the base first FirstClassElement'''

    def first_class_extended(self):
        """ dummy method to demonstrate how to access base variables/methods """
        return self._data
