import unittest
import tempfile
import shutil
from pathlib import Path

from spydrnet.compare.compare_netlists import Comparer
import spydrnet as sdn


class TestCompareNetlists(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_of_edif_netlists = Path(sdn.example_netlists_path, "EDIF_netlists")
        cls.dir_of_verilog_netlists = Path(
            sdn.example_netlists_path, "verilog_netlists"
        )
        cls.edif_files = sorted(Path.glob(cls.dir_of_edif_netlists, "*.edf.zip"))
        cls.verilog_files = sorted(Path.glob(cls.dir_of_verilog_netlists, "*.v.zip"))

    @unittest.skip("Test takes a long time right now.")
    def test_large_edif(self):
        for ii, filename in enumerate(self.edif_files):
            if Path(filename).stat().st_size <= 1024 * 10:
                continue
            self.compare_parser_and_composer(filename, ii, "edf")

    def test_small_edif(self):
        for ii, filename in enumerate(self.edif_files):
            if Path(filename).stat().st_size > 1024 * 10:
                continue
            self.compare_parser_and_composer(filename, ii, "edf")

    @unittest.skip("Test takes a long time right now.")
    def test_large_verilog(self):
        for ii, filename in enumerate(self.verilog_files):
            if Path(filename).stat().st_size <= 1024 * 10:
                continue
            self.compare_parser_and_composer(filename, ii, "v")
        # assert False

    def test_small_verilog(self):
        for ii, filename in enumerate(self.verilog_files):
            if Path(filename).stat().st_size > 1024 * 10:
                continue
            self.compare_parser_and_composer(filename, ii, "v")
        # assert False

    def compare_parser_and_composer(self, filename, ii, target_format_extension=None):
        with self.subTest(i=ii):
            if Path("temp").exists():
                shutil.rmtree("temp")
            print(filename)
            with tempfile.TemporaryDirectory() as tempdirname:
                try:
                    orig_netlist = sdn.parse(filename)
                    basename_without_final_ext = Path(Path(filename).name).stem
                    if target_format_extension is None:
                        composer_filename = Path(
                            tempdirname, basename_without_final_ext
                        )
                    else:
                        composer_filename = Path(
                            tempdirname,
                            basename_without_final_ext + "." + target_format_extension,
                        )
                    orig_netlist.compose(composer_filename)
                    print(composer_filename)
                    composer_netlist = sdn.parse(composer_filename)
                    comparer = Comparer(orig_netlist, composer_netlist)
                    comparer.run()
                except Exception as e:
                    shutil.copytree(tempdirname, "temp")
                    raise e

    @unittest.skip("Test takes a long time right now.")
    def test_large_verilog_to_edif(self):
        for ii, filename in enumerate(self.verilog_files):
            if Path(filename).stat().st_size <= 1024 * 10:
                continue
            self.compare_parser_and_composer(filename, ii, "edf")
        # assert False

    @unittest.skip(
        "currently not working properly for the number of cables on some examples please use with caution"
    )
    def test_small_verilog_to_edif(self):
        for ii, filename in enumerate(self.verilog_files):
            if Path(filename).stat().st_size > 1024 * 10:
                continue
            self.compare_parser_and_composer(filename, ii, "edf")
        # assert False

    def test_empty_netlists(self):
        nl1 = sdn.ir.Netlist()
        nl2 = sdn.ir.Netlist()
        comp = Comparer(nl1, nl2)
        comp.compare()


if __name__ == "__main__":
    unittest.main()
