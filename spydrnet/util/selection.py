from enum import Enum

class Selection(Enum):
    INSIDE = 1
    OUTSIDE = 2
    BOTH = 3
    ALL = 4

INSIDE = Selection.INSIDE
OUTSIDE = Selection.OUTSIDE
BOTH = Selection.BOTH
ALL = Selection.ALL