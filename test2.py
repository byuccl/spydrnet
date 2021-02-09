import spydrnet as sdn

netlist = sdn.Netlist(name='netlist')


library = netlist.create_library()
netlist.libraries[0].name = 'work'

def_widget = library.create_definition(name='widget')
netlist.set_top_instance(def_widget, instance_name='widget')
port_a = def_widget.create_port(name='port_a', direction=sdn.IN)
port_o = def_widget.create_port(name='port_o', direction=sdn.IN)

sdn.compose(netlist, 'test.edf')
sdn.compose(netlist, 'test.v')
