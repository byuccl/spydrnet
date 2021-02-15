import spydrnet as sdn

netlist = sdn.Netlist(name='netlist')

# initializing working library
library = netlist.create_library(name='work')

# initializing definition widget
def_widget = library.create_definition(name='widget')
netlist.set_top_instance(def_widget, instance_name='widget')
port_a = def_widget.create_port(name='A', direction=sdn.IN)
port_o = def_widget.create_port(name='O', direction=sdn.OUT)
pin_out_a = port_a.create_pin()
pin_out_o =  port_o.create_pin()


# initializing definition AND2
def_and2 = library.create_definition(name='AND2')
port_a_2 = def_and2.create_port(name='A', direction=sdn.IN)
port_o_2 = def_and2.create_port(name='O', direction=sdn.OUT)
pin_out_a_2 = port_a_2.create_pin()
pin_out_o_2 = port_o_2.create_pin()

# create an instance of AND2 which resides in widget
inst_and2 = def_widget.create_child(name='and2', reference=def_and2)
pins = inst_and2.get_pins()

# wire.connect_pin(next(pins))
cable = def_widget.create_cable(name='cable')
cable2 = def_widget.create_cable(name='cable2')
wire4 = cable.create_wire()
wire2 = cable2.create_wire()
wire4.connect_pin(pin_out_a_2)
wire4.connect_pin(pin_out_a)
wire2.connect_pin(pin_out_o)
wire2.connect_pin(pin_out_o_2)
#wire4.connect_pin(pin_out_a_2)

sdn.compose(netlist, 'test.edf')
sdn.compose(netlist, 'test.v')
