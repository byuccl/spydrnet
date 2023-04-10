import pathlib
import unittest

import spydrnet as sdn
from spydrnet import get_libraries


class TestUtil(unittest.TestCase):
    def test_single_object(self):
        netlist = sdn.Netlist()
        library1 = netlist.create_library()
        library1.name = "work"
        library2 = netlist.create_library()
        library2.name = "hdi_primitives"
        library = next(get_libraries(netlist, "work"))
        self.assertEqual(library1, library)

    def test_multiple_objects(self):
        netlist1 = sdn.Netlist()
        library1 = netlist1.create_library()
        netlist2 = sdn.Netlist()
        library2 = netlist2.create_library()
        get_libraries([netlist1, netlist2])

    def test_unused_ports(self):
        test_netlist_path = (
            pathlib.Path(sdn.base_dir)
            / "support_files"
            / "verilog_netlists"
            / "carry4_unused_output.v"
        )

        netlist = sdn.parse(str(test_netlist_path))

        carry4 = next(netlist.get_instances())
        assert carry4.name == "carry4_inst"

        # Check that 3-bit O/S inputs/outputs are wired up correctly (connected to lower 3 pins)
        for pin in carry4.pins:
            if pin.wire.cable.name in ("O", "S"):
                assert pin.index() <= 2
