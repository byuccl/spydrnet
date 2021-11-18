"""
=====================================
Minimal Script
=====================================

Builds a netlist from scratch
"""
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
pin_widget_b = port_widget_b.create_pin()
pin_widget_c = port_widget_c.create_pin()
pin_widget_d = port_widget_d.create_pin()
pin_widget_o = port_o.create_pin()

# creating the cables for module widget
cable_a = def_widget.create_cable(name='A')
cable_b = def_widget.create_cable(name='B')
cable_c = def_widget.create_cable(name='C')
cable_d = def_widget.create_cable(name='D')
cable_q_1 = def_widget.create_cable(name='Q1')
cable_q_2 = def_widget.create_cable(name='Q2')
cable_o = def_widget.create_cable(name='O')

# creating the wires for widget
wire_a = cable_a.create_wire()
wire_b = cable_b.create_wire()
wire_c = cable_c.create_wire()
wire_d = cable_d.create_wire()
wire_q_1 = cable_q_1.create_wire()
wire_q_2 = cable_q_2.create_wire()
wire_o = cable_o.create_wire()


# initializing definition AND2
def_and2 = library.create_definition(name='AND2')
port_and2_a = def_and2.create_port(name='A', direction=sdn.IN)
port_and2_b = def_and2.create_port(name='B', direction=sdn.IN)
port_and2_q = def_and2.create_port(name='Q', direction=sdn.OUT)

pin_and2_a = port_and2_a.create_pin()
pin_and2_b = port_and2_b.create_pin()
pin_and2_q = port_and2_q.create_pin()

# create two instances of AND2 which resides in widget
inst_and2_1 = def_widget.create_child(name='and2_1', reference=def_and2)
inst_and2_2 = def_widget.create_child(name='and2_2', reference=def_and2)

# initializing definition OR2
def_or2 = library.create_definition(name='OR2')
port_or2_a = def_or2.create_port(name='A', direction=sdn.IN)
port_or2_b = def_or2.create_port(name='B', direction=sdn.IN)
port_or2_q = def_or2.create_port(name='Q', direction=sdn.OUT)

pin_or2_a = port_or2_a.create_pin()
pin_or2_b = port_or2_b.create_pin()
pin_or2_q = port_or2_q.create_pin()

# create an instance of OR2 which resides in widget
inst_or2 = def_widget.create_child(name='or2', reference=def_or2)


# connect all the pins
wire_a.connect_pin(pin_widget_a)
wire_a.connect_pin(inst_and2_1.pins[pin_and2_a])
wire_b.connect_pin(pin_widget_b)
wire_b.connect_pin(inst_and2_1.pins[pin_and2_b])
wire_q_1.connect_pin(inst_and2_1.pins[pin_and2_q])
wire_c.connect_pin(pin_widget_c)
wire_c.connect_pin(inst_and2_2.pins[pin_and2_a])
wire_d.connect_pin(pin_widget_d)
wire_d.connect_pin(inst_and2_2.pins[pin_and2_b])
wire_q_2.connect_pin(inst_and2_2.pins[pin_and2_q])

wire_q_1.connect_pin(inst_or2.pins[pin_or2_a])
wire_q_2.connect_pin(inst_or2.pins[pin_or2_b])
wire_o.connect_pin(pin_widget_o)
wire_o.connect_pin(inst_or2.pins[pin_or2_q])

sdn.compose(netlist, 'test.edf')