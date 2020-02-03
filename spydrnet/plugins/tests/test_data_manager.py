import unittest
import spydrnet as sdn

from spydrnet.plugins.data_manager import DataManager
from spydrnet.global_state.global_netlist import current_netlist


class TestDataManager(unittest.TestCase):
    def test_basic_setup(self):
        global current_netlist
        netlist = sdn.Netlist()
        current_netlist = netlist
        dm = DataManager()
        lib1 = netlist.create_library()
        lib2 = netlist.create_library()
