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

from spydrnet.ir import Environment, Library, Definition, Instance, Port, InnerPin, OuterPin, Cable, Wire
import os

OUT = Port.Direction.OUT
IN = Port.Direction.IN
INOUT = Port.Direction.INOUT
UNDEFINED = Port.Direction.UNDEFINED

from spydrnet.testing.test import run as test


def parse(filename):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    if extension_lower in [".edf", ".edif"]:
        from spydrnet.parsers.edif.parser import EdifParser
        parser = EdifParser.from_filename(filename)
        parser.parse()
        return parser.netlist
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))


def compose(filename, netlist):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    if extension_lower in {".edf", ".edif"}:
        from spydrnet.composers.edif.composer import ComposeEdif
        composer = ComposeEdif()
        composer.run(netlist, filename)
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
