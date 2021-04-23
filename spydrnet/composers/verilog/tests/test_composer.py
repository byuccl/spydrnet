import unittest
import spydrnet as sdn
from spydrnet import composers
from spydrnet import parsers
import os
import tempfile
import glob

class TestVerilogComposer(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dir_of_verilog_netlists = os.path.join(sdn.base_dir, "support_files", "verilog_netlists")
        cls.verilog_files = sorted(glob.glob(os.path.join(cls.dir_of_verilog_netlists, "*.v.zip")), key = os.path.getsize)

    @unittest.skip("Test takes a long time right now.")
    def test_large_verilog_compose(self):
        i = 0
        errors = 0
        for ii, filename in enumerate(self.verilog_files):
            with self.subTest(i=ii):
                if os.path.getsize(filename) <= 1024 * 10:
                    continue
                if filename.endswith(".zip"):
                    with tempfile.TemporaryDirectory() as tempdirectory:
                        # try:
                            print("*********************"+filename+"*********************")
                            # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename(os.path.join(directory, filename))
                            # netlist = vp.parse()
                            netlist = parsers.parse(filename)
                            composers.compose(netlist, os.path.join(tempdirectory, os.path.basename(filename) +  "-spydrnet.v"))
                            #comp.run(netlist,"temp2/"+filename[:len(filename)-6] + "-spydrnet.v")
                            # comp.run(netlist,os.path.join(tempdirectory, filename[:len(filename)-6] + "-spydrnet.v"))
                            i+=1
                            print("pass")
                        # except Exception as identifier:
                        #     print("FAIL")
                        #     print(identifier)
                        #     errors += 1
                else:
                    continue

        print("processed",i,"errors", errors)
        
        assert errors == 0, "there were errors while parsing and composing files. Please see the output."

    def test_small_verilog_compose(self):
        i = 0
        errors = 0
        for ii, filename in enumerate(self.verilog_files):
            with self.subTest(i=ii):
                if os.path.getsize(filename) > 1024 * 10:
                    continue
                if filename.endswith(".zip"):
                    with tempfile.TemporaryDirectory() as tempdirectory:
                        # try:
                            print("*********************"+filename+"*********************")
                            # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename(os.path.join(directory, filename))
                            # netlist = vp.parse()
                            netlist = parsers.parse(filename)
                            composers.compose(netlist, os.path.join(tempdirectory, os.path.basename(filename) +  "-spydrnet.v"))
                            #comp.run(netlist,"temp2/"+filename[:len(filename)-6] + "-spydrnet.v")
                            # comp.run(netlist,os.path.join(tempdirectory, filename[:len(filename)-6] + "-spydrnet.v"))
                            i+=1
                            print("pass")
                        # except Exception as identifier:
                        #     print("FAIL")
                        #     print(identifier)
                        #     errors += 1
                else:
                    continue

        print("processed",i,"errors", errors)
        
        assert errors == 0, "there were errors while parsing and composing files. Please see the output."