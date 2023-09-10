# Do not import ir in this Module

import typing
if typing.TYPE_CHECKING:
    from spydrnet.ir.element import Element
    from spydrnet.ir.first_class_element import FirstClassElement
    from spydrnet.ir.netlist import Netlist
    from spydrnet.ir.library import Library
    from spydrnet.ir.definition import Definition
    from spydrnet.ir.port import Port
    from spydrnet.ir.cable import Cable
    from spydrnet.ir.wire import Wire
    from spydrnet.ir.instance import Instance
    from spydrnet.ir.innerpin import InnerPin
    from spydrnet.ir.outerpin import OuterPin
    from spydrnet.ir.bundle import Bundle
    from spydrnet.ir.pin import Pin
