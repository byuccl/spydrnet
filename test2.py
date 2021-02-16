import spydrnet as sdn

netlist = sdn.Netlist(name='netlist')

# initializing working library
library = netlist.create_library(name='work')

# initializing definition widget
def_widget = library.create_definition(name='widget')
netlist.set_top_instance(def_widget, instance_name='widget')
port_a = def_widget.create_port(name='A', direction=sdn.IN)
port_o = def_widget.create_port(name='O', direction=sdn.OUT)
out_a = port_a.create_pin()


# initializing definition AND2
def_and2 = library.create_definition(name='AND2')
port_a_2 = def_and2.create_port(name='A', direction=sdn.IN)
port_o_2 = def_and2.create_port(name='O', direction=sdn.OUT)
out_a_2 = port_a_2.create_pin()
# def_and2.create_cable(name='cable')
wire = sdn.Wire()
wire.connect_pin(out_a)
wire.connect_pin(out_a_2)

# create an instance of AND2 which resides in widget
inst_and2 = def_widget.create_child(name="and2", reference=def_and2)
pins = inst_and2.get_pins()
print(pins)

sdn.compose(netlist, 'test.edf')
sdn.compose(netlist, 'test.v')
