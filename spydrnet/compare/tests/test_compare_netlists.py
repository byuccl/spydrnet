import unittest
import os
import tempfile
import glob
import shutil

from spydrnet.compare.compare_netlists import Comparer
import spydrnet as sdn


class TestCompareNetlists(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_of_edif_netlists = os.path.join(sdn.base_dir, "support_files", "EDIF_netlists")
        cls.edif_files = sorted(glob.glob(os.path.join(cls.dir_of_edif_netlists, "*.edf.zip")), key=os.path.getsize)

    @unittest.skip("Test takes a long time right now.")
    def test_large_edif(self):
        for ii, filename in enumerate(self.edif_files):
            if os.path.getsize(filename) <= 1024 * 10:
                continue
            self.compare_parser_and_composer_on(filename, ii)

    def test_small_edif(self):
        for ii, filename in enumerate(self.edif_files):
            if os.path.getsize(filename) > 1024 * 10:
                continue
            self.compare_parser_and_composer_on(filename, ii)

    def compare_parser_and_composer_on(self, filename, ii):
        with self.subTest(i=ii):
            if os.path.exists("temp"):
                shutil.rmtree("temp")
            print(filename)
            orig_netlist = sdn.parse(filename)
            with tempfile.TemporaryDirectory() as tempdirname:
                try:
                    basename_without_final_ext = os.path.splitext(os.path.basename(filename))[0]
                    composer_filename = os.path.join(tempdirname, basename_without_final_ext)
                    orig_netlist.compose(composer_filename)
                    composer_netlist = sdn.parse(composer_filename)
                except Exception as e:
                    shutil.copytree(tempdirname, "temp")
                    raise e
            comparer = Comparer(orig_netlist, composer_netlist)
            comparer.run()
    
    def test_empty_netlists(self):
        nl1 = sdn.ir.Netlist()
        nl2 = sdn.ir.Netlist()
        comp = Comparer(nl1, nl2)
        comp.compare()


if __name__ == '__main__':
    unittest.main()
