import spydrnet as sdn

netlist = sdn.Netlist()


library = netlist.create_library()
library['EDIF.identifier'] = 'work'
netlist.libraries[0].name = 'work'

definition = library.create_definition()
instance = sdn.Instance()
instance.reference = definition
instance.name = 'Widget_instance'
instance['EDIF.identifier'] = 'widget_edif_instance'
netlist.top_instance = instance
definition.name = 'Widget'
definition['EDIF.identifier'] = 'Widget'

netlist['EDIF.identifier'] = 'Netlist_example'

sdn.compose(netlist, 'test.edf')
sdn.compose(netlist, 'test.v')
