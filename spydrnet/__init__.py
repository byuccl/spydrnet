"""
SpyDrNet
========

SpyDrNet is an EDA tool for analyzing and transforming netlists.

See https://byuccl.github.io/spydrnet for more details.
"""

# Release data
from spydrnet import release

__author__ = '%s <%s>\n%s <%s>\n%s <%s>' % \
    (release.authors['Keller'] + release.authors['Skouson'] +
        release.authors['Wirthlin'])
__license__ = release.license

__date__ = release.date
__version__ = release.version
__release__ = release.release

from spydrnet.ir import *
from spydrnet.util.hierarchical_reference import HRef

OUT = Port.Direction.OUT
IN = Port.Direction.IN
INOUT = Port.Direction.INOUT
UNDEFINED = Port.Direction.UNDEFINED

from spydrnet.util.selection import INSIDE, OUTSIDE, BOTH, ALL

from spydrnet.testing.test import run as test
from spydrnet.parsers import parse
from spydrnet.composers import compose

from spydrnet.plugins import namespace_manager
from spydrnet.util import get_netlists, get_libraries, get_definitions, get_ports, get_cables, get_instances,\
    get_wires, get_pins
from spydrnet.util import get_hinstances, get_hports, get_hpins, get_hcables, get_hwires

import os
base_dir = os.path.dirname(os.path.abspath(__file__))

import glob
example_netlist_names = list()
for filename in glob.glob(os.path.join(base_dir, 'support_files', 'EDIF_netlists', "*")):
    basename = os.path.basename(filename)
    example_netlist_names.append(basename[:basename.index('.')])
example_netlist_names.sort()


def load_example_netlist_by_name(name):
    assert name in example_netlist_names, "Example netlist not found"
    return parse(os.path.join(base_dir, 'support_files', 'EDIF_netlists', name + ".edf.zip"))
