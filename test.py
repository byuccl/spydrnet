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
port_A = definition.create_port()
port_A.name = 'A'
port_A['EDIF.identifier'] = 'A'
port_A.direction = 2

port_B = definition.create_port()
port_B.name = 'B'
port_B['EDIF.identifier'] = 'B'
port_B.direction = 2

port_C = definition.create_port()
port_C.name = 'C'
port_C['EDIF.identifier'] = 'C'
port_C.direction = 2

port_D = definition.create_port()
port_D.name = 'D'
port_D['EDIF.identifier'] = 'D'
port_D.direction = 2

port_O = definition.create_port()
port_O.name = 'O'
port_O['EDIF.identifier'] = 'O'
port_O.direction = 3


def_AND2 = library.create_definition()
def_AND2.name = 'AND2'
def_AND2['EDIF.identifier'] = 'AND2'

# create the input and output ports of AND2
AND2_A = def_AND2.create_port()
AND2_A.name = 'A'
AND2_A['EDIF.identifier'] = 'AND2_A'
AND2_A.direction = sdn.IN

AND2_B = def_AND2.create_port()
AND2_B.name = 'B'
AND2_B['EDIF.identifier'] = 'AND2_B'
AND2_B.direction = sdn.IN

AND2_Q = def_AND2.create_port()
AND2_Q.name = 'Q'
AND2_Q['EDIF.identifier'] = 'AND2_Q'
AND2_Q.direction = sdn.OUT

# AND2 = def_AND2.create_child()
# AND2.reference = def_AND2
# AND2['EDIF.identifier'] = 'AND2_inst'
# # AND2.parent = instance

def_OR2 = library.create_definition()
def_OR2.name = 'OR2'
def_OR2['EDIF.identifier'] = 'OR2'

instance = definition.create_child()
instance.name = 'and2'
instance['EDIF.identifier'] = 'and2'
instance.reference = def_AND2

# Create properties for the new instance
#properties = [{'identifier': 'INIT', 'value': "64'h7FFF8000FFFE0001"}]
#instance['EDIF.properties'] = properties


netlist['EDIF.identifier'] = 'Netlist_example'

sdn.compose(netlist, 'test.edf')
sdn.compose(netlist, 'test.v')
