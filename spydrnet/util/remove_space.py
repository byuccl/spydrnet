def removing_space(netlist):    
    
    for instance in netlist.get_instances():
        if instance.name is None:
            continue
        if "\\" in instance.name:
            update_name = instance.name.replace(" ", "")
            instance.name = update_name    
    
    for port in netlist.get_ports():
        if port.name is None:
            continue
        if "\\" in port.name:
            update_name = port.name.replace(" ", "")
            port.name = update_name

    for cable in netlist.get_cables():
        if cable.name is None:
            continue
        if "\\" in cable.name:
            update_name = cable.name.replace(" ", "")
            cable.name = update_name

            