"""
============================
Create Netlist with SpyDrNet
============================

Builds a netlist with a lookup table and HDI primitives from scratch ready to be used for a "post-synthesis" project

This script shows how SpyDrNet is capable of creating a real netlist that can be downloaded to an FPGA development board. This specific design is meant for Digilent development boards with Xilinx FPGAs, but should work for other FPGAs that use the same primitives.

Using SpyDrNet, this script creates a netlist with a lookup table and the necessary primitive definitions to implement it on a board. The number of inputs to the lookup table and the configuration of the lookup table can be set by changing the ``LUT_SIZE`` and ``LUT_CONFIG`` variables. The configuration for the lookup table is simply the output from an n-input truth table in hexadecimal. The lookup table will use however many of the lower switches on the FPGA development board necessary for the specified number of inputs. The output will be displayed on the first LED. 

At the end of the script, the netlist will be composed into an EDIF netlist called ```my_LUT.edf``` that can be added as a design source to a "post-synthesis" project in Vivado. To better visualize what is happening, click on "Open Synthesized Design" and then open the "Schematic" to view the netlist. Once added to the project in Vivado, a simple constraints file must be added (`Digilent master XDC files can be found here <https://github.com/Digilent/digilent-xdc>`_), and then a bitstream that can be downloaded onto a board is generated.

Below are SystemVerilog modules that will generate a 4-input LUT after synthesis. The netlist created by the included python script generates something very similar to what Vivado will generate. 

.. code-block:: sv

    module basic_LUT(
        input wire logic A,B,C,D,
        output logic Q
        );

        assign Q = (A & B) || (C & D);

    endmodule

.. code-block:: sv

    module top_LUT(
        input wire logic [3:0] sw,
        output logic led
    );

        basic_LUT my_basic_LUT(
            .A(sw[0]),.B(sw[1]), .C(sw[2]), .D(sw[3]), .Q(led)); 

    endmodule 

Try adding these modules to a fresh RTL project in Vivado and run synthesis. After synthesis is run, open the schematic from the synthesized design. Besides perhaps some naming differences, it should match what is produced by this Python script. 

Below is an example of a constraints file for the Digilent BASYS3 board. Comment/uncomment the switch lines as needed for the number of inputs. 

.. code-block::

    ## LEDs 
    set_property PACKAGE_PIN U16 [get_ports {led[0]}]
        set_property IOSTANDARD LVCMOS33 [get_ports {led[0]}]

    ## Switches
    set_property PACKAGE_PIN V17 [get_ports { sw[0] }]
        set_property IOSTANDARD LVCMOS33 [get_ports { sw[0] }]
    set_property PACKAGE_PIN V16 [get_ports {sw[1]}]
        set_property IOSTANDARD LVCMOS33 [get_ports {sw[1]}]
    set_property PACKAGE_PIN W16 [get_ports {sw[2]}]
        set_property IOSTANDARD LVCMOS33 [get_ports {sw[2]}]
    set_property PACKAGE_PIN W17 [get_ports {sw[3]}]
        set_property IOSTANDARD LVCMOS33 [get_ports {sw[3]}]
    #set_property PACKAGE_PIN W15 [get_ports {sw[4]}]
    #	set_property IOSTANDARD LVCMOS33 [get_ports {sw[4]}]
    #set_property PACKAGE_PIN V15 [get_ports {sw[5]}]
    #	set_property IOSTANDARD LVCMOS33 [get_ports {sw[5]}]


    ## Configuration options, can be used for all designs
    set_property CONFIG_VOLTAGE 3.3 [current_design]
    set_property CFGBVS VCCO [current_design]

Below is all the python code used to create the netlist from scratch with SpyDrNet

"""

import spydrnet as sdn
import string
import sys

# Specify number of inputs for the lookup-table
# Possible sizes for lookup-table: 2, 3, 4, 5, 6. Bigger sizes may not be
# supported on the device you are working with.
LUT_SIZE = 4

# Configure the LUT with a hex value. Lookup table can be configured easily by
# creating a n-input truth table, then converting the output column from
# binary to hexadecimal.
# 0xF888 refers to the following logic equation: (A * B) + (C * D)
LUT_CONFIG = 0xF888

if len(bin(LUT_CONFIG)[2:]) > 2 ** LUT_SIZE:
    sys.exit("LUT_CONFIG has too many bits for LUT size")

# Create netlist
netlist = sdn.Netlist(name="netlist")

# Create HDI primitives library within netlist.
prim_library = netlist.create_library(name="hdi_primitives")

# Create all definitions for the primitives library
IBUF_def = prim_library.create_definition(name="IBUF")
# Output Buffer definition
OBUF_def = prim_library.create_definition(name="OBUF")
# Lookup table definition
prim_LUT_def = prim_library.create_definition(name="LUT" + str(LUT_SIZE))
# Inverter definition
INV_def = prim_library.create_definition(name="INV")

# Create input/output ports for IBUF and OBUF definition
IBUF_port_output = IBUF_def.create_port(name="O", direction=sdn.OUT)
IBUF_port_input = IBUF_def.create_port(name="I", direction=sdn.IN)
OBUF_port_output = OBUF_def.create_port(name="O", direction=sdn.OUT)
OBUF_port_input = OBUF_def.create_port(name="I", direction=sdn.IN)

# Create input/output pins for each port
IBUF_pin_output = IBUF_port_output.create_pin()
IBUF_pin_input = IBUF_port_input.create_pin()
OBUF_pin_output = OBUF_port_output.create_pin()
OBUF_pin_input = OBUF_port_input.create_pin()

# Create lookup table output port and accompanying pin
prim_LUT_port_output = prim_LUT_def.create_port(name="O", direction=sdn.OUT)
prim_LUT_pin_output = prim_LUT_port_output.create_pin()

# Create lookup table input ports and pins, and store them in lists
prim_LUT_port_input_list = []
prim_LUT_pin_input_list = []
for i in range(LUT_SIZE):
    prim_LUT_port_input = prim_LUT_def.create_port(
        name="I" + str(i), direction=sdn.IN
    )
    prim_LUT_port_input_list.append(prim_LUT_port_input)
    prim_LUT_pin_input_list.append(prim_LUT_port_input.create_pin())

# Create input/output port for inverter
INV_port_output = INV_def.create_port(name="O", direction=sdn.OUT)
INV_port_input = INV_def.create_port(name="I", direction=sdn.IN)

# Create work library
work_library = netlist.create_library(name="work")

# Create custom LUT definition
my_LUT_def = work_library.create_definition(name="my_LUT")

# Create port and pin for the output of the custom LUT
my_LUT_port_output = my_LUT_def.create_port(name="Q", direction=sdn.OUT)
my_LUT_pin_output = my_LUT_port_output.create_pin()

# Create ports and pins for the inputs to the custom LUT
my_prim_LUT_port_input_list = []
my_LUT_pin_input_list = []
for i in range(LUT_SIZE):
    my_LUT_port_input = my_LUT_def.create_port(
        name=string.ascii_uppercase[i], direction=sdn.IN
    )
    my_prim_LUT_port_input_list.append(my_LUT_port_input)
    my_LUT_pin_input_list.append(my_LUT_port_input.create_pin())

# Create cables with wires to connect primitive LUT instance to ports
my_LUT_cable_list = []
my_LUT_wire_list = []

# cables with wires for input ports
for i in range(LUT_SIZE):
    my_LUT_cable = my_LUT_def.create_cable(name=string.ascii_uppercase[i])
    my_LUT_cable_list.append(my_LUT_cable)
    my_LUT_wire_list.append(my_LUT_cable.create_wire())

# cable with wire output port
my_LUT_cable_Q = my_LUT_def.create_cable(name="Q")
my_LUT_wire_Q = my_LUT_cable_Q.create_wire()

# Create instance of lookup table primitive
my_LUT_inst = my_LUT_def.create_child(
    name="my_LUT_inst", reference=prim_LUT_def
)

# Modify the lookup table configuration
my_LUT_inst_properties = []
my_LUT_inst_properties.append(
    {"identifier": "INIT", "value": "16'h" + str(hex(LUT_CONFIG))[2:]}
)
my_LUT_inst["EDIF.properties"] = my_LUT_inst_properties

# Connect pins from LUT instance to ports
for wire, inner_pin, outer_pin in zip(
    my_LUT_wire_list, my_LUT_pin_input_list, prim_LUT_pin_input_list
):
    wire.connect_pin(inner_pin)
    wire.connect_pin(my_LUT_inst.pins[outer_pin])

my_LUT_wire_Q.connect_pin(my_LUT_inst.pins[prim_LUT_pin_output])
my_LUT_wire_Q.connect_pin(my_LUT_pin_output)

# Create top-level definition
top_def = work_library.create_definition(name="top_LUT")

# Create ports for top-level definition
top_port_sw = top_def.create_port(
    name="sw", is_downto=True, is_scalar=True, direction=sdn.IN
)
top_port_led = top_def.create_port(name="led", direction=sdn.OUT)

# instance basic LUT
my_LUT_inst = top_def.create_child(name="my_LUT_inst", reference=my_LUT_def)

# instance LED output buffer
top_led_OBUF_inst = top_def.create_child(
    name="led_OBUF_inst", reference=OBUF_def
)

# instance switch input buffers
top_sw_IBUF_inst_list = []
for i in range(LUT_SIZE):
    top_sw_IBUF_inst_list.append(
        top_def.create_child(
            name="sw_IBUF_" + str(i) + "__inst", reference=IBUF_def
        )
    )

# connect switches to input of sw_IBUF's
top_cables_sw = top_def.create_cable(name="sw")
top_wires_sw = top_cables_sw.create_wires(LUT_SIZE)
top_pins_sw = top_port_sw.create_pins(LUT_SIZE)

for instance, i in zip(top_sw_IBUF_inst_list, range(LUT_SIZE)):
    top_wires_sw[i].connect_pin(top_pins_sw[i])
    top_wires_sw[i].connect_pin(instance.pins[IBUF_pin_input])

# connect output of sw_IBUF's to input of basic LUT
top_cables_sw_IBUF = top_def.create_cable(name="sw_IBUF")
top_wires_sw_IBUF = top_cables_sw_IBUF.create_wires(LUT_SIZE)

for IBUF_inst, my_LUT_pin, i in zip(
    top_sw_IBUF_inst_list, my_LUT_pin_input_list, range(LUT_SIZE)
):
    top_wires_sw_IBUF[i].connect_pin(IBUF_inst.pins[IBUF_pin_output])
    top_wires_sw_IBUF[i].connect_pin(my_LUT_inst.pins[my_LUT_pin])

# connect output of basic LUT to input of led_OBUF
top_cable_led_OBUF = top_def.create_cable(name="led_OBUF")
top_wire_led_OBUF = top_cable_led_OBUF.create_wire()

top_wire_led_OBUF.connect_pin(top_led_OBUF_inst.pins[OBUF_pin_input])
top_wire_led_OBUF.connect_pin(my_LUT_inst.pins[my_LUT_pin_output])

# connect output of led_OBUF to led
top_led_cable = top_def.create_cable(name="led")
top_led_wire = top_led_cable.create_wire()
top_pin_led = top_port_led.create_pin()

top_led_wire.connect_pin(top_led_OBUF_inst.pins[OBUF_pin_output])
top_led_wire.connect_pin(top_pin_led)

netlist.set_top_instance(top_def, instance_name=top_def.name)

sdn.compose(netlist, "my_LUT.edf")
