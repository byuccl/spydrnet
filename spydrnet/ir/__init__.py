
from spydrnet import get_active_plugins
import importlib
import typing

if typing.TYPE_CHECKING:
    from spydrnet.ir.element import Element
    from spydrnet.ir.first_class_element import FirstClassElement
    from spydrnet.ir.bundle import Bundle
    from spydrnet.ir.pin import Pin
    from spydrnet.ir.innerpin import InnerPin
    from spydrnet.ir.outerpin import OuterPin
    from spydrnet.ir.port import Port
    from spydrnet.ir.wire import Wire
    from spydrnet.ir.cable import Cable
    from spydrnet.ir.instance import Instance
    from spydrnet.ir.definition import Definition
    from spydrnet.ir.library import Library
    from spydrnet.ir.netlist import Netlist

RegisterModule = [('element', 'Element'),
                  ('first_class_element', 'FirstClassElement'),
                  ('bundle', 'Bundle'),
                  ('pin', 'Pin'),
                  ('innerpin', 'InnerPin'),
                  ('outerpin', 'OuterPin'),
                  ('port', 'Port'),
                  ('wire', 'Wire'),
                  ('cable', 'Cable'),
                  ('instance', 'Instance'),
                  ('definition', 'Definition'),
                  ('library', 'Library'),
                  ('netlist', 'Netlist')]

# Following section will extend all the classes imported in this file
for filename, eachModule in RegisterModule:
    cls = getattr(importlib.import_module(
        "spydrnet.ir."+filename), eachModule)
    locals()[eachModule] = type(cls.__name__, (cls,), {})

    for name, plugin in get_active_plugins().items():
        try:
            ext_cls = getattr(importlib.import_module(
                "%s.ir.%s" % (name, filename)), eachModule)
            cls_bases = (ext_cls, cls)
            locals()[eachModule] = type(cls.__name__, cls_bases, {})
            cls = locals()[eachModule]
            # print("extended", eachModule, "with ",name )
        except ModuleNotFoundError:
            pass
