from spydrnet import ir
from copy import deepcopy, copy, error

'''provide the clone function for spydrnet.'''

def clone(element):
    '''Clone an element of the netlist and return the cloned element. This can be thought of as SpyDrNet's deep copy function.
    Each element has a different behavior when cloned. Please take care when cloning because each element can retain some connections to its old environment.

    The general strategy when cloning is as follows:
     * objects that referenced other objects that are cloned will now connect to the clone
     * objects that referenced other objects that are not cloned will gerenally still reference the old objects
     * the top cloned object is now orphaned and the parent should be reset.
     * objects above or relating to the cloned object are left untouched.

    This is an outline of how a call to clone will function for each element. Please note copy is used somewhat interchangably below.

    OuterPin
     * copied but still connected to the wire the old one was (to allow upper levels to copy it correctly)
     * connected to the same inner pin (to allow upper levels to copy it correctly)
     * orphaned from the instance

    InnerPin
     * copied but still connected to the wire the old one was (to allow upper levels proper copy capability)
     * connected to the same outter pin (to allow upper levels to copy it correctly)
     * orphaned from the port it used to belong to

    Wire
     * orphaned from the cable
     * still connected to the pins it used to connect but the pins are not connected to it (to allow upper levels to do correct copying)

    Instance
     * reference is left in tact (shallow copy)
     * Orphaned from parent
     * all outer pins are copied but remain connected to the wires they used to be connected to (so that I can change them when copying an instance while copying the dictionary)

    port
     * orphaned from parent
     * all inner pins are copied and remain connected as if copied alone
     * inner pins now belong to this port as parent in same order as old copy

    cable
     * Orphaned from parent
     * all wires are copied following rules for wire copy above
     * wires are assigned to this cable as parent in same order as old copy

    definition
     * creates a copy of each instance, cable, and port as listed above
     * reach into cables and change each reference to a pin to reference the new pin
     * reach into ports and change each reference to a wire to reference the new wires
     * reach into instances and change each reference to wires to reference the new wires
     * reach into instances and change each reference to inner pins to reference the new ones
     * the set of instances of this definition will be left the same

    Libraries
     * copy each definition following the rules for a definition copy
     * reach into the instances and change the reference values to the new copies where they exist
     * the set of references to instances in all definitions will need to be rebuilt

    Netlist
     * copy each library following the rules above
     * reach into each instance and change the reference values to the new copies where they exist
     * the set of reference to instances in all definitions will need to be rebuilt
     
    '''
    if isinstance(element, list):
        raise NotImplementedError("list clone of multiple objects is not yet supported.")
    else:
        #uses python deepcopy behind the scenes. these are overwritten in most objects.
        c = deepcopy(element)
        if isinstance(c, ir.Cable):
            #all wires need to be disconnected from pins
            for w in c._wires:
                w._pins = list()
            pass
        elif isinstance(c, ir.Definition):
            c.references = set()
            #all other connections are internal except the instance references which stay.
            pass
        elif isinstance(c, ir.InnerPin):
            #connections to wires must be cut
            c._wire = None
        elif isinstance(c, ir.OuterPin):
            #connections to wires and inner pins must be cut.
            c._wire = None
            c._inner_pin = None
        elif isinstance(c, ir.Instance):
            #outer pins are still associated in the dictionary with inner pins since the reference is maintained.
            #outer pin connections to wires must be severed.
            for (ip, op) in c._pins.items():
                op._wire = None
                #op._inner_pin = None
            pass
        elif isinstance(c, ir.Library):
            #all connections are internal except the instance references which stay.
            pass
        elif isinstance(c, ir.netlist):
            #all connections are internal
            pass
        elif isinstance(c, ir.Port):
            #all pins must be disconnected from their wires and outer pins.
            for p in c._pins:
                p._wire = None
            pass
        elif isinstance(c, ir.Wire):
            #connections to pins need to be removed
            c._pins = list()
            pass
        else:
            raise NotImplementedError("the object you are trying to clone is not one of the supported objects, (cable, definition, inner/outer pin, instance, library, netlist, port, or wire)")
        return c