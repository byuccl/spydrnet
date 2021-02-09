import spydrnet as sdn

netlist = sdn.Netlist(name='netlist')

#initializing working library
library = netlist.create_library(name='work')

#initializing definition widget
def_widget = library.create_definition(name='widget')
netlist.set_top_instance(def_widget, instance_name='widget')
port_a = def_widget.create_port(name='A', direction=sdn.IN)
port_o = def_widget.create_port(name='O', direction=sdn.OUT)

#initializing definition AND2
def_and2 = library.create_definition(name='AND2')
port_a = def_and2.create_port(name='A', direction=sdn.IN)
port_o = def_and2.create_port(name='O', direction=sdn.OUT)
def_and2.create_cable(name='cable')

#create an instance of AND2 which resides in widget
inst_and2 = def_widget.create_child(name="and2", reference=def_and2)

sdn.compose(netlist, 'test.edf')
sdn.compose(netlist, 'test.v')
