import unittest
import spydrnet as sdn

from spydrnet.parsers.edif.parser import EdifParser
from spydrnet import base_dir
import os
import tempfile
import glob
import shutil


class TestEdifTokenizer(unittest.TestCase):
    def test_multi_bit_add_out_of_order(self):
        definition = sdn.Definition()
        cable0 = sdn.Cable()
        cable0.name = "net[0]"
        cable0["EDIF.identifier"] = "net_0_"
        cable1 = sdn.Cable()
        cable1.name = "net[1]"
        cable1["EDIF.identifier"] = "net_1_"
        cable2 = sdn.Cable()
        cable2.name = "net[2]"
        cable2["EDIF.identifier"] = "net_2_"

        cable0.create_wire()
        cable1.create_wire()
        cable2.create_wire()
        
        p0 = sdn.InnerPin()
        p1 = sdn.InnerPin()
        p2 = sdn.InnerPin()

        cable1.wires[0].connect_pin(p0)
        cable1.wires[0].connect_pin(p1)
        cable1.wires[0].connect_pin(p2)

        ep = EdifParser()
        ep.multibit_add_cable(definition, cable0)
        ep.multibit_add_cable(definition, cable2)
        ep.multibit_add_cable(definition, cable1)

        assert len(definition.cables) == 1
        assert len (definition.cables[0].wires) == 3
        assert len(definition.cables[0].wires[0].pins) == 0
        assert len(definition.cables[0].wires[1].pins) == 3
        assert len(definition.cables[0].wires[2].pins) == 0
        assert p0 in definition.cables[0].wires[1].pins
        assert p1 in definition.cables[0].wires[1].pins
        assert p2 in definition.cables[0].wires[1].pins
            

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_of_edif_netlists = os.path.join(sdn.base_dir, "support_files", "EDIF_netlists")
        cls.edif_files = sorted(glob.glob(os.path.join(cls.dir_of_edif_netlists, "*.edf.zip")), key=os.path.getsize)

    @unittest.skip("Test takes a long time right now.")
    def test_large_edif(self):
        for ii, filename in enumerate(self.edif_files):
            if os.path.getsize(filename) <= 1024 * 10:
                continue
            self.ensure_cable_consistency(filename, ii, "edf")

    def test_small_edif_cables(self):
        for ii, filename in enumerate(self.edif_files):
            if os.path.getsize(filename) > 1024 * 10:
                continue
            self.ensure_cable_consistency(filename, ii, "edf")

    def ensure_cable_consistency(self,filename, ii, target_format_extension = None):
        with self.subTest(i=ii):
            if os.path.exists("temp"):
                shutil.rmtree("temp")
            print(filename)
            with tempfile.TemporaryDirectory() as tempdirname:
                netlist = sdn.parse(filename)
                for l in netlist.libraries:
                    for d in l.definitions:
                        for c in d.cables:
                            assert c.definition is not None


if __name__ == '__main__':
    unittest.main()
