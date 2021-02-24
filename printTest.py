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
