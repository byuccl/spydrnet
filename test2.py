import spydrnet as sdn

netlist = sdn.Netlist(name='netlist')

# initializing working library
library = netlist.create_library(name='work')

# initializing definition widget
def_widget = library.create_definition(name='widget')
netlist.set_top_instance(def_widget, instance_name='widget')
port_a = def_widget.create_port(name='A', direction=sdn.IN)
port_widget_b = def_widget.create_port(name='B', direction=sdn.IN)
port_widget_c = def_widget.create_port(name='C', direction=sdn.IN)
port_widget_d = def_widget.create_port(name='D', direction=sdn.IN)
port_o = def_widget.create_port(name='O', direction=sdn.OUT)

pin_widget_a = port_a.create_pin()
pin_widget_o = port_o.create_pin()

#creating the cables for module widget
cable_a = def_widget.create_cable(name='A')
cable_b = def_widget.create_cable(name='B')
cable_c = def_widget.create_cable(name='C')
cable_d = def_widget.create_cable(name='D')
cable_o = def_widget.create_cable(name='O')


# initializing definition AND2
def_and2 = library.create_definition(name='AND2')
port_and2_a = def_and2.create_port(name='A', direction=sdn.IN)
port_and2_b = def_and2.create_port(name='B', direction=sdn.IN)
port_and2_o = def_and2.create_port(name='O', direction=sdn.OUT)

pin_and2_a = port_and2_a.create_pin()
pin_and2_b = port_and2_b.create_pin()
pin_and2_o = port_and2_o.create_pin()

# create an instance of AND2 which resides in widget
inst_and2_1 = def_widget.create_child(name='and2', reference=def_and2)


wire_a = cable_a.create_wire()
wire_a.connect_pin(inst_and2_1.pins[pin_out_a_2])
wire_a.connect_pin(pin_out_a)

wire_b = cable_b.create_wire()
wire_b.connect_pin(inst_and2_1.pins[pin_out_o_2])
wire_b.connect_pin(pin_out_o)

wire_o = cable_o.create_wire()
wire_o.connect_pin(inst_and2.pins[pin_out_o_2])
wire_o.connect_pin(pin_out_o)

wire_o = cable_o.create_wire()
wire_o.connect_pin(inst_and2.pins[pin_out_o_2])
wire_o.connect_pin(pin_out_o)

wire_o = cable_o.create_wire()
wire_o.connect_pin(inst_and2.pins[pin_out_o_2])
wire_o.connect_pin(pin_out_o)


sdn.compose(netlist, 'test.edf')
sdn.compose(netlist, 'test.v')
