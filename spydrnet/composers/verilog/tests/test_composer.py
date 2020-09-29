
import unittest
import spydrnet as sdn
from spydrnet import composers
from spydrnet import parsers
import os
import tempfile

class TestVerilogComposer(unittest.TestCase):

    def test_simple_compose(self):

        i = 0
        errors = 0
        directory = os.path.join(sdn.base_dir, "support_files", "verilog_netlists")
        for filename in os.listdir(directory):
            if filename.endswith(".zip"):
                with tempfile.TemporaryDirectory() as tempdirectory:
                    # try:
                        print("*********************"+filename+"*********************")
                        # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename(os.path.join(directory, filename))
                        # netlist = vp.parse()
                        netlist = parsers.parse(os.path.join(directory, filename))
                        composers.compose(netlist, os.path.join(tempdirectory, filename[:len(filename)-6] + "-spydrnet.v"))
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

