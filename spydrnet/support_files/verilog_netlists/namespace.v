// Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2018.3 (win64) Build 2405991 Thu Dec  6 23:38:27 MST 2018
// Date        : Mon Feb  3 13:44:35 2020
// Host        : CB461-EE10461 running 64-bit major release  (build 9200)
// Command     : write_verilog -file C:/Users/mbjerreg/verilog/namespace.v -include_xilinx_libs
// Design      : portnameCaseSensitivity
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xc7a100tcsg324-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* STRUCTURAL_NETLIST = "yes" *)
module portnameCaseSensitivity
   (CLK,
    CLk,
    ClK,
    Clk,
    cLK,
    cLk,
    clK,
    clk);
  input CLK;
  input CLk;
  input ClK;
  input Clk;
  input cLK;
  input cLk;
  input clK;
  input clk;


endmodule
