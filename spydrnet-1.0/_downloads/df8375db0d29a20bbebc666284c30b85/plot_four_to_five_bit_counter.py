"""
====================================
Four Bit Counter To Five Bit Counter
====================================

Extend a four bit counter to a 5 bit counter.
"""


import spydrnet as sdn

def get_pin(instance, identifier):
    for inner_pin, outer_pin in instance.pins.items():
        if inner_pin.port['EDIF.identifier'] == identifier:
            return outer_pin
    return None

ir = sdn.load_example_netlist_by_name("fourBitCounter")

primitives_library = next(x for x in ir.libraries if x['EDIF.identifier'] == 'hdi_primitives')
work_library = next(x for x in ir.libraries if x['EDIF.identifier'] == 'work')
fdce_definition = next(x for x in primitives_library.definitions if x['EDIF.identifier'] == 'FDCE')
obuf_definition = next(x for x in primitives_library.definitions if x['EDIF.identifier'] == 'OBUF')

lut6_definition = primitives_library.create_definition()
lut6_definition['EDIF.identifier'] = "LUT6"
for ii in range(6):
    input_port = lut6_definition.create_port()
    input_port.direction = sdn.IN
    input_port.create_pins(1)
    input_port['EDIF.identifier'] = 'I{}'.format(ii)
output_port = lut6_definition.create_port()
output_port.direction = sdn.OUT
output_port.create_pins(1)
output_port['EDIF.identifier'] = "O"    

top_def = ir.top_instance.reference

ff = top_def.create_child()
ff.reference = fdce_definition
ff['EDIF.identifier'] = 'out_reg_4_'
ff['EDIF.original_identifier'] = 'out_reg[4]'
properties = list()
properties.append({'identifier': 'INIT', 'value': "1'b0"})
ff['EDIF.properties'] = properties

lut = top_def.create_child()
lut['EDIF.identifier'] = 'out_4_lut6'
lut.reference = lut6_definition
properties = [{'identifier': 'INIT', 'value': "64'h7FFF8000FFFE0001"}]
lut['EDIF.properties'] = properties

myOBUF = top_def.create_child()
myOBUF.reference = obuf_definition
myOBUF['EDIF.identifier'] = 'out_OBUF_4__inst'
myOBUF['EDIF.original_identifier'] = 'out_OBUF[4]_inst'

inc_wire = None
out0 = None
out1 = None
out2 = None
out3 = None
clk = None
enable = None
rst = None
for cable in top_def.cables:
    if cable['EDIF.identifier'] == 'inc_dec_IBUF':
        inc_wire = cable.wires[0]
    elif cable['EDIF.identifier'] == 'out_OBUF_0_':
        out0 = cable.wires[0]
    elif cable['EDIF.identifier'] == 'out_OBUF_1_':
        out1 = cable.wires[0]
    elif cable['EDIF.identifier'] == 'out_OBUF_2_':
        out2 = cable.wires[0]
    elif cable['EDIF.identifier'] == 'out_OBUF_3_':
       out3 = cable.wires[0]
    elif cable['EDIF.identifier'] == 'clk_IBUF_BUFG':
        clk = cable.wires[0]
    elif cable['EDIF.identifier'] == 'enable_IBUF':
        enable = cable.wires[0]
    elif cable['EDIF.identifier'] == 'rst_IBUF':
        rst = cable.wires[0]

inc_wire.connect_pin(get_pin(lut, 'I5'))
out0.connect_pin(get_pin(lut, 'I0'))
out1.connect_pin(get_pin(lut, 'I1'))
out2.connect_pin(get_pin(lut, 'I2'))
out3.connect_pin(get_pin(lut, 'I3'))

out4_cable = top_def.create_cable()
out4_cable['EDIF.identifier'] = 'out_OBUF_4_'
out4 = out4_cable.create_wire()
out4.connect_pin(get_pin(lut, 'I4'))
out4.connect_pin(get_pin(ff, 'Q'))
out4.connect_pin(get_pin(myOBUF, 'I'))

lut_out_cable = top_def.create_cable()
lut_out_cable['EDIF.original_identifier'] = 'out[4]_i_1_n_0'
lut_out_cable['EDIF.identifier'] = 'out_4__i_1_n_0'
lut_out = lut_out_cable.create_wire()
lut_out.connect_pin(get_pin(lut, 'O'))
lut_out.connect_pin(get_pin(ff, 'D'))

clk.connect_pin(get_pin(ff, 'C'))
enable.connect_pin(get_pin(ff, 'CE'))
rst.connect_pin(get_pin(ff, 'CLR'))

out_port = next(x for x in top_def.ports if x['EDIF.identifier'] == 'out')
port_pin = out_port.create_pin()
out_port['EDIF.original_identifier'] = 'out[4:0]'
out_cable = top_def.create_cable()
out_cable['EDIF.original_identifier'] = 'out[4]'
out_cable['EDIF.identifier'] = 'out_4_'
out = out_cable.create_wire()

out.connect_pin(get_pin(myOBUF, 'O'))
old_wire = out
for pin in out_port.pins:
    temp = pin.wire
    if temp is not None:
        temp.disconnect_pin(pin)
    old_wire.connect_pin(pin)
    if temp is not None:
        old_wire = temp
        
print()
print("The counter is now a five bit counter.")
