

import spydrnet as sdn


netlist = sdn.Netlist(name='netlist')
cable = sdn.Cable(name='cable')
instance = sdn.Instance()
print(netlist)
netlist.top_instance = instance
print(netlist)
print(cable)
print(instance)
library = netlist.create_library(name='lib')
print(library)
definition = sdn.Definition()
print(definition)
pin = sdn.Pin()
cable = sdn.Cable()
print(cable)
wire = cable.create_wire()
wire.connect_pin(pin)
print(pin)
print(wire)
port = sdn.Port()
port.direction = sdn.IN
print(port)
