
import unittest
import spydrnet as sdn
from spydrnet.composers.verilog.composer import Composer
import os

class TestVerilogComposer(unittest.TestCase):

    def test_simple_compose(self):
        # #netlist = sdn.load_example_netlist_by_name("hierarchical_luts")
        # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/4bitadder.v.zip")
        # netlist = vp.parse()
        # comp = Composer()
        # comp.run(netlist,"out0.v")
        # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/8051.v.zip")
        # netlist = vp.parse()
        # comp = Composer()
        # comp.run(netlist,"out1.v")
        # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/adder.v.zip")
        # netlist = vp.parse()
        # comp = Composer()
        # comp.run(netlist,"out2.v")
        # # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/b13.v.zip")
        # # netlist = vp.parse()
        # # comp = Composer()
        # # comp.run(netlist,"out3.v")
        # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/basic_clock_crossing.v.zip")
        # netlist = vp.parse()
        # comp = Composer()
        # comp.run(netlist,"out4.v")
        # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/basic_synchronizer.v.zip")
        # netlist = vp.parse()
        # comp = Composer()
        # comp.run(netlist,"out5.v")
        # # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/bram.v.zip")
        # # netlist = vp.parse()
        # # comp = Composer()
        # # comp.run(netlist,"out6.v")
        # # vp = sdn.parsers.verilog.parser.VerilogParser.from_filename("/home/dallin/Documents/byuccl/SpyDrNet/spydrnet/support_files/verilog_netlists/carrychain.v.zip")
        # # netlist = vp.parse()
        # # comp = Composer()
        # # comp.run(netlist,"out7.v")

        i = 0
        errors = 0
        directory = "spydrnet/support_files/verilog_netlists/"
        for filename in os.listdir(directory):
            if filename.endswith(".zip"):
                try:
                    print("*********************"+filename+"*********************")
                    vp = sdn.parsers.verilog.parser.VerilogParser.from_filename(directory + filename)
                    netlist = vp.parse()
                    comp = Composer()
                    comp.run(netlist,"temp2/"+filename[:len(filename)-6] + "-spydrnet.v")
                    i+=1
                    print("pass")
                except Exception as identifier:
                    print("FAIL")
                    print(identifier)
                    errors += 1
            else:
                continue

        print("processed",i,"errors", errors)
        
        assert errors == 0, "there were errors while parsing and composing files. Please see the output."

