def reinsert_space(netlist,voters):
    
    for voter in voters:
        for obj in voters[voter]:
            obj.name = ''.join((obj.name, "_wire"))  

    for instance in netlist.get_instances():
        if instance.name is None:
            continue
        elif "\\" in instance.name:
            instance.name = ''.join((instance.name, " "))
            
    for port in netlist.get_ports():
        if port.name is None:
            continue
        elif "\\" in port.name:
            port.name = ''.join((port.name, " "))    
        
    for cable in netlist.get_cables():
        if cable.name is None:
            continue
        elif "\\" in cable.name:
            cable.name = ''.join((cable.name, " "))  