from enum import Enum

class NetlistType(Enum):
    EDIF = 1
    VERILOG = 2
    EBLIF = 3

EDIF = NetlistType.EDIF
VERILOG = NetlistType.VERILOG
EBLIF = NetlistType.EBLIF
