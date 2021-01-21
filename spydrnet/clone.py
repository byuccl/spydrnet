from spydrnet import ir
from copy import deepcopy, copy, error

"""provide the clone function for spydrnet."""


def clone(element):
    """
    Clone any netlist objects

    several premises hold while cloning
     * the object will be orphaned and not belong to any parent
     * the object will maintain internal structure with cloned objects
     * the names will be unchanged
     * external connections will mostly be severed

    Properties
     * cloned using python's built in deepcopy functionality.
     * expected to be string objects but if you store something else there make sure you override deepcopy on that object.

    Instances have some special considerations
     * when cloned without the library containing the reference definition the instance will still point to the definition of it's clone.
     * in the same case as the above point the references of the definition will be updated accordingly
     * when a library is cloned some of the instances may be defined in another library these instances will follow the premises above
     * instances defined and referenced in the cloned library will point to the cloned definition

    """
    return element.clone()
