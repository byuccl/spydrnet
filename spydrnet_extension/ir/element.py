import typing
from spydrnet.ir.element import Element as ElementBase


class Element(ElementBase):
    ''' Extending base netlist class '''

    def extended_method(self):
        """ Example extended method which return fixed string """
        return "Extended"
