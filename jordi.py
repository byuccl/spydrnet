import spydrnet as sdn

instance = sdn.Instance()

netlist = sdn.Netlist()
print(netlist.name)

netlist.name = 'my_netlist'
netlist['EDIF.identifier'] = 'identifier'
# primitives_library = sdn.Library()
# libraries = [primitives_library]
# netlist.libraries = libraries
sdn.compose(netlist, 'Jordi.edf')
