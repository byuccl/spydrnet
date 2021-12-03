"""
SpyDrNet
========

SpyDrNet is an EDA tool for analyzing and transforming netlists.

See https://byuccl.github.io/spydrnet for more details.
"""

import importlib
import logging
import os
import pathlib
import pkgutil
import sys

# ===================
#  Setup Logging
# ===================
# This logger creates stdout and file stream handlers
# LOG_LEVEL for file handler can be dynamically changes durign runtime
# by defualt log file (_spydrnet.log) will be creted in the script directory
LOG_FORMAT = "%(levelname)5s %(filename)s:%(lineno)s (%(threadName)10s) - %(message)s"

logger = logging.getLogger('spydrnet_logs')
# This is global log level other logger can not have lower level than this
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
LOG_LEVEL = logging.getLevelName(os.getenv("SPYDRNET_LOG_LEVEL", "INFO"))
stream_handler.setLevel(LOG_LEVEL)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(stream_handler)


def enable_file_logging(LOG_LEVEL=None):
    LOG_LEVEL = logging.getLevelName(LOG_LEVEL or "INFO")
    file_handler = logging.FileHandler("_spydrnet.log", mode='w')
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    file_handler.setLevel(eval(f"logging.{LOG_LEVEL}"))
    logger.addHandler(file_handler)
    return file_handler


# =============================
#  Setup Extension Discovery
# =============================
discovered_plugins = {
    name: importlib.import_module(name)
    for finder, name, ispkg
    in pkgutil.iter_modules()
    if name.startswith('spydrnet_')
}
logger.debug("Installed Plugins", discovered_plugins.keys())


def get_active_plugins():
    active_plugins = {}
    config_file = os.path.join(".", ".spydrnet") or \
        os.path.join(pathlib.Path.home(), ".spydrnet")
    if os.path.isfile(config_file):
        for plugin in open(config_file, "r").read().split():
            if discovered_plugins.get(plugin, None):
                active_plugins.update({plugin: discovered_plugins[plugin]})
            else:
                logger.debug("Plugin %s is not installed " % plugin)
    else:
        active_plugins.update(discovered_plugins)
    return active_plugins


logger.debug("Active Plugins", get_active_plugins().keys())

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

import os

from spydrnet.composers import compose
from spydrnet.parsers import parse
from spydrnet.plugins import namespace_manager
from spydrnet.testing.test import run as test
from spydrnet.util import (get_cables, get_definitions, get_hcables,
                           get_hinstances, get_hpins, get_hports, get_hwires,
                           get_instances, get_libraries, get_netlists,
                           get_pins, get_ports, get_wires)
from spydrnet.util.selection import ALL, BOTH, INSIDE, OUTSIDE

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
