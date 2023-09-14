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
from pathlib import Path
import requests

# ===================
#  Setup Logging
# ===================
# This logger creates stdout and file stream handlers
# LOG_LEVEL for file handler can be dynamically changes durign runtime
# by defualt log file (_spydrnet.log) will be creted in the script directory
LOG_FORMAT = "%(levelname)5s %(filename)s:%(lineno)s (%(threadName)10s) - %(message)s"

logger = logging.getLogger("spydrnet_logs")
# This is global log level other logger can not have lower level than this
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(sys.stdout)
LOG_LEVEL = logging.getLevelName(os.getenv("SPYDRNET_LOG_LEVEL", "INFO"))
stream_handler.setLevel(LOG_LEVEL)
stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(stream_handler)


def enable_file_logging(LOG_LEVEL=None):
    LOG_LEVEL = logging.getLevelName(LOG_LEVEL or "INFO")
    file_handler = logging.FileHandler("_spydrnet.log", mode="w")
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    file_handler.setLevel(LOG_LEVEL)
    logger.addHandler(file_handler)
    return file_handler


# =============================
#  Setup Extension Discovery
# =============================
discovered_plugins = {
    name: name
    for finder, name, ispkg in pkgutil.iter_modules()
    if name.startswith("spydrnet_")
}
logger.debug("Installed Plugins", discovered_plugins.keys())


def get_active_plugins():
    active_plugins = {}
    config_file = None
    config_file_home = Path(str(pathlib.Path.home()), ".spydrnet")
    if Path(config_file_home).is_file():
        config_file = config_file_home
    config_file_local = Path(".", ".spydrnet")
    if Path(config_file_local).is_file():
        config_file = config_file_local
    if config_file:
        for plugin in open(config_file, "r").read().split():
            if discovered_plugins.get(plugin, None):
                if (plugin not in sys.modules) and (plugin not in dir()):  # prevents reimporting over and over again
                    active_plugins.update({plugin: importlib.import_module(plugin)})
                    # print("imported", plugin)
                else:
                    active_plugins.update({plugin: sys.modules[plugin]})
            else:
                logger.debug("Plugin %s is not installed " % plugin)

    return active_plugins


logger.debug("Active Plugins", get_active_plugins().keys())

# Release data
from spydrnet import release

__author__ = "%s <%s>\n%s <%s>\n%s <%s>" % (
    release.authors["Keller"] + release.authors["Skouson"] + release.authors["Wirthlin"]
)
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

from spydrnet.composers import compose
from spydrnet.parsers import parse
from spydrnet.plugins import namespace_manager
from spydrnet.testing.test import run as test
from spydrnet.util import (
    get_cables,
    get_definitions,
    get_hcables,
    get_hinstances,
    get_hpins,
    get_hports,
    get_hwires,
    get_instances,
    get_libraries,
    get_netlists,
    get_pins,
    get_ports,
    get_wires,
)
from spydrnet.util.selection import ALL, BOTH, INSIDE, OUTSIDE
from spydrnet.util.netlist_type import EDIF, VERILOG, EBLIF


def determine_example_netlists_path(download_option):
    example_netlists_path = pathlib.Path("example_netlists")
    temp_dir_loc = pathlib.Path(
        "/tmp/spydrnet_example_netlists/spydrnet-next_release/example_netlists/"
    )
    if "EXAMPLE_NETLISTS_PATH" in os.environ:
        example_netlists_path = pathlib.Path(os.environ["EXAMPLE_NETLISTS_PATH"])
    elif temp_dir_loc.exists():
        example_netlists_path = temp_dir_loc
    else:
        None

    if not example_netlists_path.exists() and download_option:
        print(
            "Could not find example netlists. Download to /tmp/spydrnet_example_netlists? y/n"
        )
        response = input()
        if response == "y":
            print("Downloading example netlists...")
            url = (
                "https://github.com/byuccl/spydrnet/archive/refs/heads/next_release.zip"
            )
            filename = pathlib.Path("/tmp/spydrnet_temp.zip")
            response = requests.get(url)
            filename.write_bytes(response.content)

            import zipfile

            extract_loc = "/tmp/spydrnet_example_netlists"
            with zipfile.ZipFile(filename, "r") as zip_ref:
                zip_ref.extractall(extract_loc)
            env_variable = extract_loc + "/spydrnet-next_release/example_netlists/"
            os.environ["EXAMPLE_NETLISTS_PATH"] = env_variable
            print("Example netlists located in " + os.environ["EXAMPLE_NETLISTS_PATH"])
            example_netlists_path = pathlib.Path(os.environ["EXAMPLE_NETLISTS_PATH"])

    example_netlists_path = example_netlists_path.resolve()
    return example_netlists_path


example_netlists_path = determine_example_netlists_path(False)

base_dir = Path(Path(__file__).absolute()).parent

example_netlist_names = []
verilog_example_netlist_names = []
eblif_example_netlist_names = []


def get_example_netlist_names(path):
    example_netlist_names.clear()
    edif_path = Path(path).joinpath("EDIF_netlists")
    for filename in Path.glob(edif_path, "*"):
        basename = Path(filename).name
        example_netlist_names.append(basename[: basename.index(".")])
    example_netlist_names.sort()

    verilog_example_netlist_names.clear()
    verilog_path = Path(path).joinpath("verilog_netlists")
    for filename in Path.glob(verilog_path, "*"):
        basename = Path(filename).name
        verilog_example_netlist_names.append(basename[: basename.index(".")])
    verilog_example_netlist_names.sort()

    eblif_example_netlist_names.clear()
    eblif_path = Path(path).joinpath("eblif_netlists")
    for filename in Path.glob(eblif_path, "*"):
        basename = Path(filename).name
        eblif_example_netlist_names.append(basename[: basename.index(".")])
    eblif_example_netlist_names.sort()


get_example_netlist_names(example_netlists_path)


def load_example_netlist_by_name(name, netlist_format=EDIF):
    example_netlists_path = determine_example_netlists_path(True)
    get_example_netlist_names(example_netlists_path)
    error_message = "Example netlist not found. Either run 'export EXAMPLE_NETLISTS_PATH=<path>' \
                        or allow downloading to /tmp/spydrnet_example_netlists."
    if netlist_format is EDIF:
        assert name in example_netlist_names, error_message
        return parse(Path(example_netlists_path, "EDIF_netlists", name + ".edf.zip"))
    if netlist_format is VERILOG:
        assert name in verilog_example_netlist_names, error_message
        return parse(Path(example_netlists_path, "verilog_netlists", name + ".v.zip"))
    if netlist_format is EBLIF:
        assert name in eblif_example_netlist_names, error_message
        return parse(Path(example_netlists_path, "eblif_netlists", name + ".eblif.zip"))

    # if no version is recognized, default to edif
    assert name in example_netlist_names, error_message
    return parse(Path(example_netlists_path, "EDIF_netlists", name + ".edf.zip"))
