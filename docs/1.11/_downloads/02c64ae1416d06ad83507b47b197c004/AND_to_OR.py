"""
============================
Modify Netlist with SpyDrNet
============================

This example shows how SpyDrNet can parse in a netlist, modify it, and compose a new netlist.

The script parses in a simple example netlist that is just an AND gate implemented with a LUT. The instance of the LUT2 primitive definition is found, and then the properties of it are modified to change the configuration of the LUT.

Below are tables of an AND gate and an OR gate. A LUT is configured by setting the ``'value':'<LUT_configuation>'`` pair in the metadata ``[EDIF.properties]`` dictionary associated with the LUT2 instance. The ``'<LUT_configuration>'`` string is composed from the output of an n-input truth table in hexadecimal. Below is a demonstration of how to determine the ``'<LUT_configuration>'`` string.

+-----------+
| AND gate  |
+---+---+---+
| A | B | Q |
+===+===+===+
| 0 | 0 | 0 |
+---+---+---+
| 0 | 1 | 0 |
+---+---+---+
| 1 | 0 | 0 |
+---+---+---+
| 1 | 1 | 1 |
+---+---+---+

The output Q for the AND gate is the following: ``Q = 4'b1000``, or in hexadecimal, ``Q=4'h8``. Replace '<LUT_configuration>' with ``'4'h8'``

+-----------+
| OR gate   |
+---+---+---+
| A | B | Q |
+===+===+===+
| 0 | 0 | 0 |
+---+---+---+
| 0 | 1 | 1 |
+---+---+---+
| 1 | 0 | 1 |
+---+---+---+
| 1 | 1 | 1 |
+---+---+---+

The output Q for the OR gate is the following: ``Q = 4'b1110``, or in hexadecimal, ``Q=4'hE``.

The netlist example that is loaded in has a LUT configured to be an AND gate, but with SpyDrNet, you can modify that LUT to be something else. The LUT configuration ``'4'h8'`` (an AND gate) for the LUT in the netlist will be changed to ``'4'hE'`` (an OR gate) in this example.

After making this configuration, the new netlist will be composed twice, showing that SpyDrNet can either create an EDIF netlist file or a Verilog netlist file that both represent the same netlist.

"""

import spydrnet as sdn


# Change this line to change the configuration of the LUT in the design.
LUT_CONFIG = 0xE

logic_gate_netlist = sdn.load_example_netlist_by_name("AND_gate")

# Alternatively you can parse in your own netlist by changing the line below.
# logic_gate_netlist = sdn.parse('<my_netlist.edf>')


# Find the LUT2 definition
for definition in logic_gate_netlist.get_definitions():
    if definition.name == "LUT2":
        lut_instances = definition.references
        # Once the LUT2 definition has been found, go through its instances
        for instance in lut_instances:
            properties = instance["EDIF.properties"]
            # Change the value in the properties of the LUT2 instance
            properties[0]["value"] = "4'h" + str(hex(LUT_CONFIG)).upper()[2:]

# The netlist is composed into both an EDIF file and also in a Verliog file
sdn.compose(logic_gate_netlist, "OR_gate.edf")
sdn.compose(logic_gate_netlist, "OR_gate.v")
