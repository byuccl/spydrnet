import unittest
import spydrnet as sdn
from spydrnet.parsers.verilog.verilog_token_factory import TokenFactory

# these code snippets may have copyright protection other than what the License file entails please use with caution

very_simple = '''// Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2020.2 (lin64) Build 3064766 Wed Nov 18 09:12:47 MST 2020
// Date        : Wed Mar 17 14:51:06 2021
// Host        : DMachine running 64-bit Linux Mint 20.1
// Command     : write_verilog ediftoverilog
// Design      : synth_th1_slaac
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xc7k70tfbv676-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* STRUCTURAL_NETLIST = "yes" *) 
module synth_th1_slaac
   (XP_IN);
  input [7:0]XP_IN;


endmodule'''

very_simple_multi_line = '''/* Copyright 1986-2020 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2020.2 (lin64) Build 3064766 Wed Nov 18 09:12:47 MST 2020
// Date        : Wed Mar 17 14:51:06 2021
// Host        : DMachine running 64-bit Linux Mint 20.1
// Command     : write_verilog ediftoverilog
// Design      : synth_th1_slaac
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xc7k70tfbv676-1
// --------------------------------------------------------------------------------
*/
`timescale 1 ps / 1 ps

(* STRUCTURAL_NETLIST = "yes" *) 
module synth_th1_slaac
   (XP_IN);
  input [7:0]XP_IN;


endmodule'''

port_remap = '''
(* STRUCTURAL_NETLIST = "yes" *)
module synth_th1_slaac
   (.XP_IN({\^XP_IN [0],\^XP_IN [1],\^XP_IN [2],\^XP_IN [3],\^XP_IN [4],\^XP_IN [5],\^XP_IN [6],\^XP_IN [7]}));

  input [7:0]\^XP_IN ;

  wire [7:0]\^XP_IN ;
  
endmodule
'''

comments = '''
/*/ this should be
treated
as a single comment /*/

//* this should be a single line comment
these should not be part of the comment

/*

multi line with extra white space


*/
'''

final_comments = '''
module synth_th1_slaac
   (XP_IN);
  input [7:0]XP_IN;

endmodule
//* Final design comments
'''


class TestVerilogParser(unittest.TestCase):

    def run_token_count(self, string):
        tf = TokenFactory()
        running_total = 0

        for character in string:
            token = tf.add_character(character)
            if token is not None:
                running_total += 1
        token = tf.flush()
        if token is not None:
            running_total += 1
        return running_total

    def test_counts(self):
        to_run = [(very_simple_multi_line, 24, "very_simple_multi_line"), (very_simple, 35, "very_simple"),
                  (port_remap, 74, "port_remap"), (comments, 11, "comments"), (final_comments, 16, "port_remap")]
        for p in to_run:
            s, c, n = p
            assert c == self.run_token_count(
                s), "the number of expected tokens did not match up with the number parsed " + n


if __name__ == '__main__':
    unittest.main()
