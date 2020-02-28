"""
SpyDrNet
========

SpyDrNet is an EDA tool for netlist analysis and transformation.

See documentation for more details.
"""

# Release data
from spydrnet import release

__author__ = '%s <%s>\n%s <%s>\n%s <%s>' % \
    (release.authors['Keller'] + release.authors['Skouson'] +
        release.authors['Wirthlin'])
__license__ = release.license

__date__ = release.date
__version__ = release.version

from spydrnet.ir import *

OUT = Port.Direction.OUT
IN = Port.Direction.IN
INOUT = Port.Direction.INOUT
UNDEFINED = Port.Direction.UNDEFINED

from spydrnet.testing.test import run as test
from spydrnet.parsers import parse
from spydrnet.composers import compose

from spydrnet.plugins import namespace_manager
from spydrnet.plugins import hierarchical_reference_manager
from spydrnet.util.get_libraries import get_libraries
from spydrnet.util.get_definitions import get_definitions
from spydrnet.util.get_ports import get_ports
from spydrnet.util.get_cables import get_cables
from spydrnet.util.get_instances import get_instances

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
