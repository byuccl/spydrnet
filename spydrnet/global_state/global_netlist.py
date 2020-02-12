current_netlist = None

def get_current_netlist():
    global current_netlist
    return current_netlist

def set_current_netlist(net):
    global current_netlist
    current_netlist = net