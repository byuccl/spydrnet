import unittest
import os
import tempfile
import glob

from spydrnet.compare.compare_netlists import Comparer
import spydrnet as sdn


class TestCompareNetlists(unittest.TestCase):
    def test_edif(self):
        dir_of_edif_netlists = os.path.join(sdn.base_dir, "support_files", "EDIF_netlists")
        edif_files = sorted(glob.glob(os.path.join(dir_of_edif_netlists, "*.edf.zip")), key=os.path.getsize)
        for ii, filename in enumerate(edif_files):
            with self.subTest(i=ii):
                print(filename)
                orig_netlist = sdn.parse(filename)
                with tempfile.TemporaryDirectory() as tempdirname:
                    basename_without_final_ext = os.path.splitext(os.path.basename(filename))[0]
                    composer_filename = os.path.join(tempdirname, basename_without_final_ext)
                    sdn.compose(composer_filename, orig_netlist)
                    composer_netlist = sdn.parse(composer_filename)
                comparer = Comparer(orig_netlist, composer_netlist)
                comparer.run()


if __name__ == '__main__':
    unittest.main()