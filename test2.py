import spydrnet as sdn

netlist = sdn.Netlist()


library = netlist.create_library()
#netlist.libraries[0].name = 'work'

definition = library.create_definition()
instance = sdn.Instance()
instance.reference = definition
instance.name = 'Widget_instance'
netlist.top_instance = instance
definition.name = 'Widget'

sdn.compose(netlist, 'test.edf')
sdn.compose(netlist, 'test.v')
