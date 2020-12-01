// Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2018.3 (win64) Build 2405991 Thu Dec  6 23:38:27 MST 2018
// Date        : Mon Feb  3 13:47:11 2020
// Host        : CB461-EE10461 running 64-bit major release  (build 9200)
// Command     : write_verilog -file C://Users//mbjerreg//verilog/register_file.v -include_xilinx_libs
// Design      : register_top
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xc7a100tcsg324-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

module register4
   (clk,
    we,
    datain,
    dataout);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout;

  wire \<const0> ;
  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout;
  wire we;

  GND GND
       (.G(\<const0> ));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop0
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[0]),
        .Q(dataout[0]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop1
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[1]),
        .Q(dataout[1]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop2
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[2]),
        .Q(dataout[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop3
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[3]),
        .Q(dataout[3]));
endmodule

(* ORIG_REF_NAME = "register4" *) 
module register4__1
   (clk,
    we,
    datain,
    dataout);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout;

  wire \<const0> ;
  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout;
  wire we;

  GND GND
       (.G(\<const0> ));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop0
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[0]),
        .Q(dataout[0]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop1
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[1]),
        .Q(dataout[1]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop2
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[2]),
        .Q(dataout[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop3
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[3]),
        .Q(dataout[3]));
endmodule

(* ORIG_REF_NAME = "register4" *) 
module register4__2
   (clk,
    we,
    datain,
    dataout);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout;

  wire \<const0> ;
  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout;
  wire we;

  GND GND
       (.G(\<const0> ));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop0
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[0]),
        .Q(dataout[0]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop1
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[1]),
        .Q(dataout[1]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop2
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[2]),
        .Q(dataout[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop3
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[3]),
        .Q(dataout[3]));
endmodule

(* ORIG_REF_NAME = "register4" *) 
module register4__3
   (clk,
    we,
    datain,
    dataout);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout;

  wire \<const0> ;
  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout;
  wire we;

  GND GND
       (.G(\<const0> ));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop0
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[0]),
        .Q(dataout[0]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop1
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[1]),
        .Q(dataout[1]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop2
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[2]),
        .Q(dataout[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop3
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[3]),
        .Q(dataout[3]));
endmodule

(* ORIG_REF_NAME = "register4" *) 
module register4__4
   (clk,
    we,
    datain,
    dataout);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout;

  wire \<const0> ;
  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout;
  wire we;

  GND GND
       (.G(\<const0> ));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop0
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[0]),
        .Q(dataout[0]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop1
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[1]),
        .Q(dataout[1]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop2
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[2]),
        .Q(dataout[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop3
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[3]),
        .Q(dataout[3]));
endmodule

(* ORIG_REF_NAME = "register4" *) 
module register4__5
   (clk,
    we,
    datain,
    dataout);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout;

  wire \<const0> ;
  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout;
  wire we;

  GND GND
       (.G(\<const0> ));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop0
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[0]),
        .Q(dataout[0]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop1
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[1]),
        .Q(dataout[1]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop2
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[2]),
        .Q(dataout[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop3
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[3]),
        .Q(dataout[3]));
endmodule

(* ORIG_REF_NAME = "register4" *) 
module register4__6
   (clk,
    we,
    datain,
    dataout);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout;

  wire \<const0> ;
  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout;
  wire we;

  GND GND
       (.G(\<const0> ));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop0
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[0]),
        .Q(dataout[0]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop1
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[1]),
        .Q(dataout[1]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop2
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[2]),
        .Q(dataout[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop3
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[3]),
        .Q(dataout[3]));
endmodule

(* ORIG_REF_NAME = "register4" *) 
module register4__7
   (clk,
    we,
    datain,
    dataout);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout;

  wire \<const0> ;
  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout;
  wire we;

  GND GND
       (.G(\<const0> ));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop0
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[0]),
        .Q(dataout[0]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop1
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[1]),
        .Q(dataout[1]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop2
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[2]),
        .Q(dataout[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  FDCE #(
    .INIT(1'b0),
    .IS_CLR_INVERTED(1'b0),
    .IS_C_INVERTED(1'b0),
    .IS_D_INVERTED(1'b0)) 
    flop3
       (.C(clk),
        .CE(we),
        .CLR(\<const0> ),
        .D(datain[3]),
        .Q(dataout[3]));
endmodule

module register_file_8x4
   (clk,
    we,
    datain,
    dataout1,
    dataout2,
    raddr1,
    raddr2,
    waddr);
  input clk;
  input we;
  input [3:0]datain;
  output [3:0]dataout1;
  output [3:0]dataout2;
  input [2:0]raddr1;
  input [2:0]raddr2;
  input [2:0]waddr;

  wire clk;
  wire [3:0]datain;
  wire [3:0]dataout1;
  wire \dataout1[0]_INST_0_i_1_n_0 ;
  wire \dataout1[0]_INST_0_i_2_n_0 ;
  wire \dataout1[1]_INST_0_i_1_n_0 ;
  wire \dataout1[1]_INST_0_i_2_n_0 ;
  wire \dataout1[2]_INST_0_i_1_n_0 ;
  wire \dataout1[2]_INST_0_i_2_n_0 ;
  wire \dataout1[3]_INST_0_i_1_n_0 ;
  wire \dataout1[3]_INST_0_i_2_n_0 ;
  wire [3:0]dataout2;
  wire \dataout2[0]_INST_0_i_1_n_0 ;
  wire \dataout2[0]_INST_0_i_2_n_0 ;
  wire \dataout2[1]_INST_0_i_1_n_0 ;
  wire \dataout2[1]_INST_0_i_2_n_0 ;
  wire \dataout2[2]_INST_0_i_1_n_0 ;
  wire \dataout2[2]_INST_0_i_2_n_0 ;
  wire \dataout2[3]_INST_0_i_1_n_0 ;
  wire \dataout2[3]_INST_0_i_2_n_0 ;
  wire [3:0]out0;
  wire [3:0]out1;
  wire [3:0]out2;
  wire [3:0]out3;
  wire [3:0]out4;
  wire [3:0]out5;
  wire [3:0]out6;
  wire [3:0]out7;
  wire [2:0]raddr1;
  wire [2:0]raddr2;
  wire [2:0]waddr;
  wire we;
  wire [7:0]write_address;

  MUXF7 \dataout1[0]_INST_0 
       (.I0(\dataout1[0]_INST_0_i_1_n_0 ),
        .I1(\dataout1[0]_INST_0_i_2_n_0 ),
        .O(dataout1[0]),
        .S(raddr1[2]));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout1[0]_INST_0_i_1 
       (.I0(out3[0]),
        .I1(out2[0]),
        .I2(raddr1[1]),
        .I3(out1[0]),
        .I4(raddr1[0]),
        .I5(out0[0]),
        .O(\dataout1[0]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout1[0]_INST_0_i_2 
       (.I0(out7[0]),
        .I1(out6[0]),
        .I2(raddr1[1]),
        .I3(out5[0]),
        .I4(raddr1[0]),
        .I5(out4[0]),
        .O(\dataout1[0]_INST_0_i_2_n_0 ));
  MUXF7 \dataout1[1]_INST_0 
       (.I0(\dataout1[1]_INST_0_i_1_n_0 ),
        .I1(\dataout1[1]_INST_0_i_2_n_0 ),
        .O(dataout1[1]),
        .S(raddr1[2]));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout1[1]_INST_0_i_1 
       (.I0(out3[1]),
        .I1(out2[1]),
        .I2(raddr1[1]),
        .I3(out1[1]),
        .I4(raddr1[0]),
        .I5(out0[1]),
        .O(\dataout1[1]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout1[1]_INST_0_i_2 
       (.I0(out7[1]),
        .I1(out6[1]),
        .I2(raddr1[1]),
        .I3(out5[1]),
        .I4(raddr1[0]),
        .I5(out4[1]),
        .O(\dataout1[1]_INST_0_i_2_n_0 ));
  MUXF7 \dataout1[2]_INST_0 
       (.I0(\dataout1[2]_INST_0_i_1_n_0 ),
        .I1(\dataout1[2]_INST_0_i_2_n_0 ),
        .O(dataout1[2]),
        .S(raddr1[2]));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout1[2]_INST_0_i_1 
       (.I0(out3[2]),
        .I1(out2[2]),
        .I2(raddr1[1]),
        .I3(out1[2]),
        .I4(raddr1[0]),
        .I5(out0[2]),
        .O(\dataout1[2]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout1[2]_INST_0_i_2 
       (.I0(out7[2]),
        .I1(out6[2]),
        .I2(raddr1[1]),
        .I3(out5[2]),
        .I4(raddr1[0]),
        .I5(out4[2]),
        .O(\dataout1[2]_INST_0_i_2_n_0 ));
  MUXF7 \dataout1[3]_INST_0 
       (.I0(\dataout1[3]_INST_0_i_1_n_0 ),
        .I1(\dataout1[3]_INST_0_i_2_n_0 ),
        .O(dataout1[3]),
        .S(raddr1[2]));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout1[3]_INST_0_i_1 
       (.I0(out3[3]),
        .I1(out2[3]),
        .I2(raddr1[1]),
        .I3(out1[3]),
        .I4(raddr1[0]),
        .I5(out0[3]),
        .O(\dataout1[3]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout1[3]_INST_0_i_2 
       (.I0(out7[3]),
        .I1(out6[3]),
        .I2(raddr1[1]),
        .I3(out5[3]),
        .I4(raddr1[0]),
        .I5(out4[3]),
        .O(\dataout1[3]_INST_0_i_2_n_0 ));
  MUXF7 \dataout2[0]_INST_0 
       (.I0(\dataout2[0]_INST_0_i_1_n_0 ),
        .I1(\dataout2[0]_INST_0_i_2_n_0 ),
        .O(dataout2[0]),
        .S(raddr2[2]));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout2[0]_INST_0_i_1 
       (.I0(out3[0]),
        .I1(out2[0]),
        .I2(raddr2[1]),
        .I3(out1[0]),
        .I4(raddr2[0]),
        .I5(out0[0]),
        .O(\dataout2[0]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout2[0]_INST_0_i_2 
       (.I0(out7[0]),
        .I1(out6[0]),
        .I2(raddr2[1]),
        .I3(out5[0]),
        .I4(raddr2[0]),
        .I5(out4[0]),
        .O(\dataout2[0]_INST_0_i_2_n_0 ));
  MUXF7 \dataout2[1]_INST_0 
       (.I0(\dataout2[1]_INST_0_i_1_n_0 ),
        .I1(\dataout2[1]_INST_0_i_2_n_0 ),
        .O(dataout2[1]),
        .S(raddr2[2]));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout2[1]_INST_0_i_1 
       (.I0(out3[1]),
        .I1(out2[1]),
        .I2(raddr2[1]),
        .I3(out1[1]),
        .I4(raddr2[0]),
        .I5(out0[1]),
        .O(\dataout2[1]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout2[1]_INST_0_i_2 
       (.I0(out7[1]),
        .I1(out6[1]),
        .I2(raddr2[1]),
        .I3(out5[1]),
        .I4(raddr2[0]),
        .I5(out4[1]),
        .O(\dataout2[1]_INST_0_i_2_n_0 ));
  MUXF7 \dataout2[2]_INST_0 
       (.I0(\dataout2[2]_INST_0_i_1_n_0 ),
        .I1(\dataout2[2]_INST_0_i_2_n_0 ),
        .O(dataout2[2]),
        .S(raddr2[2]));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout2[2]_INST_0_i_1 
       (.I0(out3[2]),
        .I1(out2[2]),
        .I2(raddr2[1]),
        .I3(out1[2]),
        .I4(raddr2[0]),
        .I5(out0[2]),
        .O(\dataout2[2]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout2[2]_INST_0_i_2 
       (.I0(out7[2]),
        .I1(out6[2]),
        .I2(raddr2[1]),
        .I3(out5[2]),
        .I4(raddr2[0]),
        .I5(out4[2]),
        .O(\dataout2[2]_INST_0_i_2_n_0 ));
  MUXF7 \dataout2[3]_INST_0 
       (.I0(\dataout2[3]_INST_0_i_1_n_0 ),
        .I1(\dataout2[3]_INST_0_i_2_n_0 ),
        .O(dataout2[3]),
        .S(raddr2[2]));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout2[3]_INST_0_i_1 
       (.I0(out3[3]),
        .I1(out2[3]),
        .I2(raddr2[1]),
        .I3(out1[3]),
        .I4(raddr2[0]),
        .I5(out0[3]),
        .O(\dataout2[3]_INST_0_i_1_n_0 ));
  LUT6 #(
    .INIT(64'hAFA0CFCFAFA0C0C0)) 
    \dataout2[3]_INST_0_i_2 
       (.I0(out7[3]),
        .I1(out6[3]),
        .I2(raddr2[1]),
        .I3(out5[3]),
        .I4(raddr2[0]),
        .I5(out4[3]),
        .O(\dataout2[3]_INST_0_i_2_n_0 ));
  register4__1 reg0
       (.clk(clk),
        .datain(datain),
        .dataout(out0),
        .we(write_address[0]));
  (* SOFT_HLUTNM = "soft_lutpair0" *) 
  LUT4 #(
    .INIT(16'h0002)) 
    reg0_i_1
       (.I0(we),
        .I1(waddr[1]),
        .I2(waddr[0]),
        .I3(waddr[2]),
        .O(write_address[0]));
  register4__2 reg1
       (.clk(clk),
        .datain(datain),
        .dataout(out1),
        .we(write_address[1]));
  (* SOFT_HLUTNM = "soft_lutpair0" *) 
  LUT4 #(
    .INIT(16'h0020)) 
    reg1_i_1
       (.I0(we),
        .I1(waddr[1]),
        .I2(waddr[0]),
        .I3(waddr[2]),
        .O(write_address[1]));
  register4__3 reg2
       (.clk(clk),
        .datain(datain),
        .dataout(out2),
        .we(write_address[2]));
  (* SOFT_HLUTNM = "soft_lutpair1" *) 
  LUT4 #(
    .INIT(16'h0020)) 
    reg2_i_1
       (.I0(we),
        .I1(waddr[0]),
        .I2(waddr[1]),
        .I3(waddr[2]),
        .O(write_address[2]));
  register4__4 reg3
       (.clk(clk),
        .datain(datain),
        .dataout(out3),
        .we(write_address[3]));
  (* SOFT_HLUTNM = "soft_lutpair1" *) 
  LUT4 #(
    .INIT(16'h0080)) 
    reg3_i_1
       (.I0(we),
        .I1(waddr[1]),
        .I2(waddr[0]),
        .I3(waddr[2]),
        .O(write_address[3]));
  register4__5 reg4
       (.clk(clk),
        .datain(datain),
        .dataout(out4),
        .we(write_address[4]));
  (* SOFT_HLUTNM = "soft_lutpair2" *) 
  LUT4 #(
    .INIT(16'h0200)) 
    reg4_i_1
       (.I0(we),
        .I1(waddr[1]),
        .I2(waddr[0]),
        .I3(waddr[2]),
        .O(write_address[4]));
  register4__6 reg5
       (.clk(clk),
        .datain(datain),
        .dataout(out5),
        .we(write_address[5]));
  (* SOFT_HLUTNM = "soft_lutpair2" *) 
  LUT4 #(
    .INIT(16'h2000)) 
    reg5_i_1
       (.I0(we),
        .I1(waddr[1]),
        .I2(waddr[0]),
        .I3(waddr[2]),
        .O(write_address[5]));
  register4__7 reg6
       (.clk(clk),
        .datain(datain),
        .dataout(out6),
        .we(write_address[6]));
  (* SOFT_HLUTNM = "soft_lutpair3" *) 
  LUT4 #(
    .INIT(16'h2000)) 
    reg6_i_1
       (.I0(we),
        .I1(waddr[0]),
        .I2(waddr[1]),
        .I3(waddr[2]),
        .O(write_address[6]));
  register4 reg7
       (.clk(clk),
        .datain(datain),
        .dataout(out7),
        .we(write_address[7]));
  (* SOFT_HLUTNM = "soft_lutpair3" *) 
  LUT4 #(
    .INIT(16'h8000)) 
    reg7_i_1
       (.I0(we),
        .I1(waddr[1]),
        .I2(waddr[0]),
        .I3(waddr[2]),
        .O(write_address[7]));
endmodule

(* STRUCTURAL_NETLIST = "yes" *)
module register_top
   (btnc,
    btnd,
    btnl,
    btnr,
    btnu,
    clk,
    anode,
    segment,
    sw);
  input btnc;
  input btnd;
  input btnl;
  input btnr;
  input btnu;
  input clk;
  output [7:0]anode;
  output [7:0]segment;
  input [12:0]sw;

  wire \<const0> ;
  wire \<const1> ;
  (* IOSTANDARD = "LVCMOS33" *) wire [7:0]anode;
  (* IOSTANDARD = "LVCMOS33" *) wire btnc;
  wire btnc_IBUF;
  (* IOSTANDARD = "LVCMOS33" *) wire btnd;
  wire btnd_IBUF;
  (* IOSTANDARD = "LVCMOS33" *) wire btnl;
  wire btnl_IBUF;
  (* IOSTANDARD = "LVCMOS33" *) wire btnr;
  wire btnr_IBUF;
  (* IOSTANDARD = "LVCMOS33" *) wire btnu;
  wire btnu_IBUF;
  (* IOSTANDARD = "LVCMOS33" *) wire clk;
  wire clk_IBUF;
  wire clk_IBUF_BUFG;
  wire [3:0]dataout1;
  wire [3:0]dataout2;
  wire seg_i_10_n_0;
  wire seg_i_11_n_0;
  wire seg_i_12_n_0;
  wire seg_i_1_n_0;
  wire seg_i_2_n_0;
  wire seg_i_3_n_0;
  wire seg_i_4_n_0;
  wire seg_i_5_n_0;
  wire seg_i_6_n_0;
  wire seg_i_7_n_0;
  wire seg_i_8_n_0;
  wire seg_i_9_n_0;
  (* IOSTANDARD = "LVCMOS33" *) wire [7:0]segment;
  wire [6:0]segment_OBUF;
  wire [12:0]sw;
  wire [12:0]sw_IBUF;

  GND GND
       (.G(\<const0> ));
  VCC VCC
       (.P(\<const1> ));
  OBUF \anode_OBUF[0]_inst 
       (.I(\<const0> ),
        .O(anode[0]));
  OBUF \anode_OBUF[1]_inst 
       (.I(\<const1> ),
        .O(anode[1]));
  OBUF \anode_OBUF[2]_inst 
       (.I(\<const1> ),
        .O(anode[2]));
  OBUF \anode_OBUF[3]_inst 
       (.I(\<const1> ),
        .O(anode[3]));
  OBUF \anode_OBUF[4]_inst 
       (.I(\<const1> ),
        .O(anode[4]));
  OBUF \anode_OBUF[5]_inst 
       (.I(\<const1> ),
        .O(anode[5]));
  OBUF \anode_OBUF[6]_inst 
       (.I(\<const1> ),
        .O(anode[6]));
  OBUF \anode_OBUF[7]_inst 
       (.I(\<const1> ),
        .O(anode[7]));
  IBUF btnc_IBUF_inst
       (.I(btnc),
        .O(btnc_IBUF));
  IBUF btnd_IBUF_inst
       (.I(btnd),
        .O(btnd_IBUF));
  IBUF btnl_IBUF_inst
       (.I(btnl),
        .O(btnl_IBUF));
  IBUF btnr_IBUF_inst
       (.I(btnr),
        .O(btnr_IBUF));
  IBUF btnu_IBUF_inst
       (.I(btnu),
        .O(btnu_IBUF));
  BUFG clk_IBUF_BUFG_inst
       (.I(clk_IBUF),
        .O(clk_IBUF_BUFG));
  IBUF clk_IBUF_inst
       (.I(clk),
        .O(clk_IBUF));
  register_file_8x4 regfile
       (.clk(clk_IBUF_BUFG),
        .datain(sw_IBUF[3:0]),
        .dataout1(dataout1),
        .dataout2(dataout2),
        .raddr1(sw_IBUF[6:4]),
        .raddr2(sw_IBUF[9:7]),
        .waddr(sw_IBUF[12:10]),
        .we(btnc_IBUF));
  seven_segment seg
       (.data({seg_i_1_n_0,seg_i_2_n_0,seg_i_3_n_0,seg_i_4_n_0}),
        .segment(segment_OBUF));
  LUT6 #(
    .INIT(64'hFEF2F2FE020E0E02)) 
    seg_i_1
       (.I0(seg_i_5_n_0),
        .I1(btnu_IBUF),
        .I2(btnr_IBUF),
        .I3(dataout1[3]),
        .I4(seg_i_6_n_0),
        .I5(dataout2[3]),
        .O(seg_i_1_n_0));
  LUT2 #(
    .INIT(4'h8)) 
    seg_i_10
       (.I0(dataout2[0]),
        .I1(dataout1[0]),
        .O(seg_i_10_n_0));
  LUT6 #(
    .INIT(64'hD4DD4444DDDDD4DD)) 
    seg_i_11
       (.I0(dataout2[2]),
        .I1(dataout1[2]),
        .I2(dataout1[0]),
        .I3(dataout2[0]),
        .I4(dataout1[1]),
        .I5(dataout2[1]),
        .O(seg_i_11_n_0));
  (* SOFT_HLUTNM = "soft_lutpair5" *) 
  LUT4 #(
    .INIT(16'hDD4D)) 
    seg_i_12
       (.I0(dataout2[1]),
        .I1(dataout1[1]),
        .I2(dataout2[0]),
        .I3(dataout1[0]),
        .O(seg_i_12_n_0));
  LUT6 #(
    .INIT(64'hFEF2F2FE020E0E02)) 
    seg_i_2
       (.I0(seg_i_7_n_0),
        .I1(btnu_IBUF),
        .I2(btnr_IBUF),
        .I3(dataout1[2]),
        .I4(seg_i_8_n_0),
        .I5(dataout2[2]),
        .O(seg_i_2_n_0));
  LUT6 #(
    .INIT(64'hFEF2F2FE020E0E02)) 
    seg_i_3
       (.I0(seg_i_9_n_0),
        .I1(btnu_IBUF),
        .I2(btnr_IBUF),
        .I3(dataout1[1]),
        .I4(seg_i_10_n_0),
        .I5(dataout2[1]),
        .O(seg_i_3_n_0));
  LUT6 #(
    .INIT(64'hFF03FFFC00FD0000)) 
    seg_i_4
       (.I0(btnl_IBUF),
        .I1(btnd_IBUF),
        .I2(btnu_IBUF),
        .I3(btnr_IBUF),
        .I4(dataout1[0]),
        .I5(dataout2[0]),
        .O(seg_i_4_n_0));
  LUT5 #(
    .INIT(32'h3FC0D10C)) 
    seg_i_5
       (.I0(btnl_IBUF),
        .I1(btnd_IBUF),
        .I2(seg_i_11_n_0),
        .I3(dataout1[3]),
        .I4(dataout2[3]),
        .O(seg_i_5_n_0));
  LUT6 #(
    .INIT(64'hEEEEE888E8888888)) 
    seg_i_6
       (.I0(dataout2[2]),
        .I1(dataout1[2]),
        .I2(dataout2[0]),
        .I3(dataout1[0]),
        .I4(dataout1[1]),
        .I5(dataout2[1]),
        .O(seg_i_6_n_0));
  LUT5 #(
    .INIT(32'h3FC0D10C)) 
    seg_i_7
       (.I0(btnl_IBUF),
        .I1(btnd_IBUF),
        .I2(seg_i_12_n_0),
        .I3(dataout1[2]),
        .I4(dataout2[2]),
        .O(seg_i_7_n_0));
  (* SOFT_HLUTNM = "soft_lutpair5" *) 
  LUT4 #(
    .INIT(16'hE888)) 
    seg_i_8
       (.I0(dataout2[1]),
        .I1(dataout1[1]),
        .I2(dataout1[0]),
        .I3(dataout2[0]),
        .O(seg_i_8_n_0));
  LUT6 #(
    .INIT(64'h33F3CC0CDD1D00C0)) 
    seg_i_9
       (.I0(btnl_IBUF),
        .I1(btnd_IBUF),
        .I2(dataout2[0]),
        .I3(dataout1[0]),
        .I4(dataout1[1]),
        .I5(dataout2[1]),
        .O(seg_i_9_n_0));
  OBUF \segment_OBUF[0]_inst 
       (.I(segment_OBUF[0]),
        .O(segment[0]));
  OBUF \segment_OBUF[1]_inst 
       (.I(segment_OBUF[1]),
        .O(segment[1]));
  OBUF \segment_OBUF[2]_inst 
       (.I(segment_OBUF[2]),
        .O(segment[2]));
  OBUF \segment_OBUF[3]_inst 
       (.I(segment_OBUF[3]),
        .O(segment[3]));
  OBUF \segment_OBUF[4]_inst 
       (.I(segment_OBUF[4]),
        .O(segment[4]));
  OBUF \segment_OBUF[5]_inst 
       (.I(segment_OBUF[5]),
        .O(segment[5]));
  OBUF \segment_OBUF[6]_inst 
       (.I(segment_OBUF[6]),
        .O(segment[6]));
  OBUF \segment_OBUF[7]_inst 
       (.I(\<const0> ),
        .O(segment[7]));
  IBUF \sw_IBUF[0]_inst 
       (.I(sw[0]),
        .O(sw_IBUF[0]));
  IBUF \sw_IBUF[10]_inst 
       (.I(sw[10]),
        .O(sw_IBUF[10]));
  IBUF \sw_IBUF[11]_inst 
       (.I(sw[11]),
        .O(sw_IBUF[11]));
  IBUF \sw_IBUF[12]_inst 
       (.I(sw[12]),
        .O(sw_IBUF[12]));
  IBUF \sw_IBUF[1]_inst 
       (.I(sw[1]),
        .O(sw_IBUF[1]));
  IBUF \sw_IBUF[2]_inst 
       (.I(sw[2]),
        .O(sw_IBUF[2]));
  IBUF \sw_IBUF[3]_inst 
       (.I(sw[3]),
        .O(sw_IBUF[3]));
  IBUF \sw_IBUF[4]_inst 
       (.I(sw[4]),
        .O(sw_IBUF[4]));
  IBUF \sw_IBUF[5]_inst 
       (.I(sw[5]),
        .O(sw_IBUF[5]));
  IBUF \sw_IBUF[6]_inst 
       (.I(sw[6]),
        .O(sw_IBUF[6]));
  IBUF \sw_IBUF[7]_inst 
       (.I(sw[7]),
        .O(sw_IBUF[7]));
  IBUF \sw_IBUF[8]_inst 
       (.I(sw[8]),
        .O(sw_IBUF[8]));
  IBUF \sw_IBUF[9]_inst 
       (.I(sw[9]),
        .O(sw_IBUF[9]));
endmodule

module seven_segment
   (data,
    segment);
  input [3:0]data;
  output [6:0]segment;

  wire [3:0]data;
  wire [6:0]segment;

  (* BOX_TYPE = "PRIMITIVE" *) 
  LUT4 #(
    .INIT(16'hD004)) 
    seg2
       (.I0(data[0]),
        .I1(data[1]),
        .I2(data[2]),
        .I3(data[3]),
        .O(segment[2]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  LUT4 #(
    .INIT(16'h8492)) 
    seg3
       (.I0(data[0]),
        .I1(data[1]),
        .I2(data[2]),
        .I3(data[3]),
        .O(segment[3]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  LUT4 #(
    .INIT(16'h02BA)) 
    seg4
       (.I0(data[0]),
        .I1(data[1]),
        .I2(data[2]),
        .I3(data[3]),
        .O(segment[4]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  LUT4 #(
    .INIT(16'h208E)) 
    seg5
       (.I0(data[0]),
        .I1(data[1]),
        .I2(data[2]),
        .I3(data[3]),
        .O(segment[5]));
  (* BOX_TYPE = "PRIMITIVE" *) 
  LUT4 #(
    .INIT(16'h1083)) 
    seg6
       (.I0(data[0]),
        .I1(data[1]),
        .I2(data[2]),
        .I3(data[3]),
        .O(segment[6]));
  (* SOFT_HLUTNM = "soft_lutpair4" *) 
  LUT4 #(
    .INIT(16'h2806)) 
    \segment[0]_INST_0 
       (.I0(data[0]),
        .I1(data[2]),
        .I2(data[1]),
        .I3(data[3]),
        .O(segment[0]));
  (* SOFT_HLUTNM = "soft_lutpair4" *) 
  LUT4 #(
    .INIT(16'hD680)) 
    \segment[1]_INST_0 
       (.I0(data[0]),
        .I1(data[1]),
        .I2(data[3]),
        .I3(data[2]),
        .O(segment[1]));
endmodule
///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2016 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 2017.1
//  \   \         Description : Xilinx Unified Simulation Library Component
//  /   /                  D Flip-Flop with Clock Enable and Asynchronous Clear
// /___/   /\     Filename : FDCE.v
// \   \  /  \
//  \___\/\___\
//
// Revision:
//    08/24/10 - Initial version.
//    10/20/10 - remove unused pin line from table.
//    11/01/11 - Disable timing check when set reset active (CR632017)
//    12/08/11 - add MSGON and XON attributes (CR636891)
//    01/16/12 - 640813 - add MSGON and XON functionality
//    04/16/13 - PR683925 - add invertible pin support.
// End Revision

`timescale  1 ps / 1 ps

`celldefine 

module FDCE #(
  `ifdef XIL_TIMING
  parameter LOC = "UNPLACED",
  parameter MSGON = "TRUE",
  parameter XON = "TRUE",
  `endif
  parameter [0:0] INIT = 1'b0,
  parameter [0:0] IS_CLR_INVERTED = 1'b0,
  parameter [0:0] IS_C_INVERTED = 1'b0,
  parameter [0:0] IS_D_INVERTED = 1'b0
)(
  output Q,
  
  input C,
  input CE,
  input CLR,
  input D
);

    reg [0:0] IS_CLR_INVERTED_REG = IS_CLR_INVERTED;
    reg [0:0] IS_C_INVERTED_REG = IS_C_INVERTED;
    reg [0:0] IS_D_INVERTED_REG = IS_D_INVERTED;
    
    tri0 glblGSR = glbl.GSR;

`ifdef XIL_TIMING
    wire D_dly, C_dly, CE_dly;
    wire CLR_dly;
`endif

    wire CLR_in;

`ifdef XIL_TIMING
    assign CLR_in = (CLR_dly ^ IS_CLR_INVERTED_REG) && (CLR !== 1'bz);
`else
    assign CLR_in = (CLR ^ IS_CLR_INVERTED_REG) && (CLR !== 1'bz);
`endif

// begin behavioral model

  reg Q_out;

  assign #100 Q = Q_out;

    always @(glblGSR or CLR_in)
      if (glblGSR) 
        assign Q_out = INIT;
      else if (CLR_in === 1'b1) 
        assign Q_out = 1'b0;
      else if (CLR_in === 1'bx) 
        assign Q_out = 1'bx;
      else
        deassign Q_out;

`ifdef XIL_TIMING
generate
if (IS_C_INVERTED == 1'b0) begin : generate_block1
  always @(posedge C_dly or posedge CLR_in)
    if (CLR_in || (CLR === 1'bx && Q_out == 1'b0))
      Q_out <= 1'b0;
    else if (CE_dly || (CE === 1'bz) || ((CE === 1'bx) && (Q_out == (D_dly ^ IS_D_INVERTED_REG))))
      Q_out <= D_dly ^ IS_D_INVERTED_REG;
end else begin : generate_block1
  always @(negedge C_dly or posedge CLR_in)
    if (CLR_in || (CLR === 1'bx && Q_out == 1'b0))
      Q_out <= 1'b0;
    else if (CE_dly || (CE === 1'bz) || ((CE === 1'bx) && (Q_out == (D_dly ^ IS_D_INVERTED_REG))))
      Q_out <= D_dly ^ IS_D_INVERTED_REG;
end
endgenerate
`else
generate
if (IS_C_INVERTED == 1'b0) begin : generate_block1
  always @(posedge C or posedge CLR_in)
    if (CLR_in || (CLR === 1'bx && Q_out == 1'b0))
      Q_out <= 1'b0;
    else if (CE || (CE === 1'bz) || ((CE === 1'bx) && (Q_out == (D ^ IS_D_INVERTED_REG))))
      Q_out <= D ^ IS_D_INVERTED_REG;
end else begin : generate_block1
  always @(negedge C or posedge CLR_in)
    if (CLR_in || (CLR === 1'bx && Q_out == 1'b0))
      Q_out <= 1'b0;
    else if (CE || (CE === 1'bz) || ((CE === 1'bx) && (Q_out == (D ^ IS_D_INVERTED_REG))))
      Q_out <= D ^ IS_D_INVERTED_REG;
end
endgenerate
`endif

`ifdef XIL_TIMING
    reg notifier;
    wire notifier1;
`endif

`ifdef XIL_TIMING
    wire ngsr, in_out;
    wire nrst;
    wire in_clk_enable, in_clk_enable_p, in_clk_enable_n;
    wire ce_clk_enable, ce_clk_enable_p, ce_clk_enable_n;
    reg init_enable = 1'b1;
    wire rst_clk_enable, rst_clk_enable_p, rst_clk_enable_n;
`endif

`ifdef XIL_TIMING
    not (ngsr, glblGSR);
    xor (in_out, D_dly, IS_D_INVERTED_REG, Q_out);
    not (nrst, (CLR_dly ^ IS_CLR_INVERTED_REG) && (CLR !== 1'bz));

    and (in_clk_enable, ngsr, nrst, CE || (CE === 1'bz));
    and (ce_clk_enable, ngsr, nrst, in_out);
    and (rst_clk_enable, ngsr, CE || (CE === 1'bz), D ^ IS_D_INVERTED_REG);
    always @(negedge nrst) init_enable = (MSGON =="TRUE") && ~glblGSR && (Q_out ^ INIT);

    assign notifier1 = (XON == "FALSE") ?  1'bx : notifier;
    assign ce_clk_enable_n = (MSGON =="TRUE") && ce_clk_enable && (IS_C_INVERTED == 1'b1);
    assign in_clk_enable_n = (MSGON =="TRUE") && in_clk_enable && (IS_C_INVERTED == 1'b1);
    assign rst_clk_enable_n = (MSGON =="TRUE") && rst_clk_enable && (IS_C_INVERTED == 1'b1);
    assign ce_clk_enable_p = (MSGON =="TRUE") && ce_clk_enable && (IS_C_INVERTED == 1'b0);
    assign in_clk_enable_p = (MSGON =="TRUE") && in_clk_enable && (IS_C_INVERTED == 1'b0);
    assign rst_clk_enable_p = (MSGON =="TRUE") && rst_clk_enable && (IS_C_INVERTED == 1'b0);
`endif

// end behavioral model

`ifdef XIL_TIMING
  specify
  (C => Q) = (100:100:100, 100:100:100);
  (negedge CLR => (Q +: 0)) = (0:0:0, 0:0:0);
  (posedge CLR => (Q +: 0)) = (0:0:0, 0:0:0);
  (CLR => Q) = (0:0:0, 0:0:0);
  $period (negedge C &&& CE, 0:0:0, notifier);
  $period (posedge C &&& CE, 0:0:0, notifier);
  $recrem (negedge CLR, negedge C, 0:0:0, 0:0:0, notifier,rst_clk_enable_n,rst_clk_enable_n,CLR_dly, C_dly);
  $recrem (negedge CLR, posedge C, 0:0:0, 0:0:0, notifier,rst_clk_enable_p,rst_clk_enable_p,CLR_dly, C_dly);
  $recrem (posedge CLR, negedge C, 0:0:0, 0:0:0, notifier,rst_clk_enable_n,rst_clk_enable_n,CLR_dly, C_dly);
  $recrem (posedge CLR, posedge C, 0:0:0, 0:0:0, notifier,rst_clk_enable_p,rst_clk_enable_p,CLR_dly, C_dly);
  $setuphold (negedge C, negedge CE, 0:0:0, 0:0:0, notifier,ce_clk_enable_n,ce_clk_enable_n,C_dly,CE_dly);
  $setuphold (negedge C, negedge D, 0:0:0, 0:0:0, notifier,in_clk_enable_n,in_clk_enable_n,C_dly,D_dly);
  $setuphold (negedge C, posedge CE, 0:0:0, 0:0:0, notifier,ce_clk_enable_n,ce_clk_enable_n,C_dly,CE_dly);
  $setuphold (negedge C, posedge D, 0:0:0, 0:0:0, notifier,in_clk_enable_n,in_clk_enable_n,C_dly,D_dly);
  $setuphold (posedge C, negedge CE, 0:0:0, 0:0:0, notifier,ce_clk_enable_p,ce_clk_enable_p,C_dly,CE_dly);
  $setuphold (posedge C, negedge D, 0:0:0, 0:0:0, notifier,in_clk_enable_p,in_clk_enable_p,C_dly,D_dly);
  $setuphold (posedge C, posedge CE, 0:0:0, 0:0:0, notifier,ce_clk_enable_p,ce_clk_enable_p,C_dly,CE_dly);
  $setuphold (posedge C, posedge D, 0:0:0, 0:0:0, notifier,in_clk_enable_p,in_clk_enable_p,C_dly,D_dly);
  $width (negedge C &&& CE, 0:0:0, 0, notifier);
  $width (negedge CLR &&& init_enable, 0:0:0, 0, notifier);
  $width (posedge C &&& CE, 0:0:0, 0, notifier);
  $width (posedge CLR &&& init_enable, 0:0:0, 0, notifier);
  specparam PATHPULSE$ = 0;
  endspecify
`endif
endmodule

`endcelldefine

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2016 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor      : Xilinx
// \   \   \/     Version     : 2017.1
//  \   \         Description : Xilinx Unified Simulation Library Component
//  /   /                  5-Bit Look-Up Table
// /___/   /\     Filename : LUT5.v
// \   \  /  \
//  \___\/\___\
//
///////////////////////////////////////////////////////////////////////////////
//  Revision:
//    03/23/04 - Initial version.
//    02/04/05 - Replace primitive with function; Remove buf.
//    01/07/06 - 222733 - Add LOC Parameter
//    06/04/07 - Add wire declaration to internal signal.
//    12/13/11 - 524859 - Added `celldefine and `endcelldefine
//    09/12/16 - ANSI ports, speed improvements
//  End Revision:
///////////////////////////////////////////////////////////////////////////////

`timescale 1 ps/1 ps

`celldefine

module LUT5 #(
`ifdef XIL_TIMING
  parameter LOC = "UNPLACED",
`endif
  parameter [31:0] INIT = 32'h00000000
)(
  output O,

  input I0,
  input I1,
  input I2,
  input I3,
  input I4
);

// define constants
  localparam MODULE_NAME = "LUT5";

  reg trig_attr = 1'b0;
// include dynamic registers - XILINX test only
`ifdef XIL_DR
  `include "LUT5_dr.v"
`else
  reg [31:0] INIT_REG = INIT;
`endif

// begin behavioral model

  reg O_out;

  assign O = O_out;

  function lut_mux4_f;
  input [3:0] d;
  input [1:0] s;
  begin
    if (((s[1]^s[0]) === 1'b1) || ((s[1]^s[0]) === 1'b0))
      lut_mux4_f = d[s];
    else if ( ~(|d) || &d)
      lut_mux4_f = d[0];
    else if (((s[0] === 1'b1) || (s[0] === 1'b0)) && (d[{1'b0,s[0]}] === d[{1'b1,s[0]}]))
      lut_mux4_f = d[{1'b0,s[0]}];
    else if (((s[1] === 1'b1) || (s[1] === 1'b0)) && (d[{s[1],1'b0}] === d[{s[1],1'b1}]))
      lut_mux4_f = d[{s[1],1'b0}];
    else
      lut_mux4_f = 1'bx;
  end
  endfunction

  function lut_mux8_f;
  input [7:0] d;
  input [2:0] s;
  begin
    if (((s[2]^s[1]^s[0]) === 1'b1) || ((s[2]^s[1]^s[0]) === 1'b0))
      lut_mux8_f = d[s];
    else if ( ~(|d) || &d)
      lut_mux8_f = d[0];
    else if ((((s[1]^s[0]) === 1'b1) || ((s[1]^s[0]) === 1'b0)) &&
             (d[{1'b0,s[1:0]}] === d[{1'b1,s[1:0]}]))
      lut_mux8_f = d[{1'b0,s[1:0]}];
    else if ((((s[2]^s[0]) === 1'b1) || ((s[2]^s[0]) === 1'b0)) &&
             (d[{s[2],1'b0,s[0]}] === d[{s[2],1'b1,s[0]}]))
      lut_mux8_f = d[{s[2],1'b0,s[0]}];
    else if ((((s[2]^s[1]) === 1'b1) || ((s[2]^s[1]) === 1'b0)) &&
             (d[{s[2],s[1],1'b0}] === d[{s[2],s[1],1'b1}]))
      lut_mux8_f = d[{s[2:1],1'b0}];
    else if (((s[0] === 1'b1) || (s[0] === 1'b0)) &&
             (d[{1'b0,1'b0,s[0]}] === d[{1'b0,1'b1,s[0]}]) &&
             (d[{1'b0,1'b0,s[0]}] === d[{1'b1,1'b0,s[0]}]) &&
             (d[{1'b0,1'b0,s[0]}] === d[{1'b1,1'b1,s[0]}]))
      lut_mux8_f = d[{1'b0,1'b0,s[0]}];
    else if (((s[1] === 1'b1) || (s[1] === 1'b0)) &&
             (d[{1'b0,s[1],1'b0}] === d[{1'b0,s[1],1'b1}]) &&
             (d[{1'b0,s[1],1'b0}] === d[{1'b1,s[1],1'b0}]) &&
             (d[{1'b0,s[1],1'b0}] === d[{1'b1,s[1],1'b1}]))
      lut_mux8_f = d[{1'b0,s[1],1'b0}];
    else if (((s[2] === 1'b1) || (s[2] === 1'b0)) &&
             (d[{s[2],1'b0,1'b0}] === d[{s[2],1'b0,1'b1}]) &&
             (d[{s[2],1'b0,1'b0}] === d[{s[2],1'b1,1'b0}]) &&
             (d[{s[2],1'b0,1'b0}] === d[{s[2],1'b1,1'b1}]))
      lut_mux8_f = d[{s[2],1'b0,1'b0}];
    else
      lut_mux8_f = 1'bx;
  end
  endfunction

 always @(I0 or I1 or I2 or I3 or I4)  begin
   if ( (I0 ^ I1  ^ I2 ^ I3 ^ I4) === 1'b0 || (I0 ^ I1  ^ I2 ^ I3 ^ I4) === 1'b1)
     O_out = INIT_REG[{I4, I3, I2, I1, I0}];
   else if ( ~(|INIT_REG) || &INIT_REG )
     O_out = INIT_REG[0];
   else
     O_out = lut_mux4_f ({lut_mux8_f (INIT_REG[31:24], {I2, I1, I0}),
                      lut_mux8_f (INIT_REG[23:16], {I2, I1, I0}),
                      lut_mux8_f ( INIT_REG[15:8], {I2, I1, I0}),
                      lut_mux8_f (  INIT_REG[7:0], {I2, I1, I0})}, {I4, I3});
  end

// end behavioral model

`ifdef XIL_TIMING
  specify
	(I0 => O) = (0:0:0, 0:0:0);
	(I1 => O) = (0:0:0, 0:0:0);
	(I2 => O) = (0:0:0, 0:0:0);
	(I3 => O) = (0:0:0, 0:0:0);
	(I4 => O) = (0:0:0, 0:0:0);
	specparam PATHPULSE$ = 0;
  endspecify
`endif

endmodule

`endcelldefine

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2009 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 10.1
//  \   \         Description : Xilinx Functional Simulation Library Component
//  /   /                  2-to-1 Lookup Table Multiplexer with General Output
// /___/   /\     Filename : MUXF7.v
// \   \  /  \    Timestamp : Thu Mar 25 16:42:55 PST 2004
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    02/04/05 - Rev 0.0.1 Remove input/output bufs; Remove unnessasary begin/end;
//    05/10/07 - When input same, output same for any sel value. (CR434611).
//    08/23/07 - User block statement (CR446704).
//    12/13/11 - Added `celldefine and `endcelldefine (CR 524859).
// End Revision

`timescale  1 ps / 1 ps

`celldefine

module MUXF7 (O, I0, I1, S);


`ifdef XIL_TIMING

    parameter LOC = "UNPLACED";

`endif

    
    output O;
    input I0, I1, S;

    reg O_out;

    always @(I0 or I1 or S) 
	if (S)
	    O_out = I1;
	else
	    O_out = I0;

    assign O = O_out;
    
`ifdef XIL_TIMING

    specify
                                                                                 
        (I0 => O) = (0:0:0, 0:0:0);
        (I1 => O) = (0:0:0, 0:0:0);
	(S => O) = (0:0:0, 0:0:0);
        specparam PATHPULSE$ = 0;
                                                                                 
    endspecify

`endif
    
endmodule

`endcelldefine


///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2004 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 10.1
//  \   \         Description : Xilinx Functional Simulation Library Component
//  /   /                  Output Buffer
// /___/   /\     Filename : OBUF.v
// \   \  /  \    Timestamp : Thu Mar 25 16:42:59 PST 2004
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    02/22/06 - CR#226003 - Added integer, real parameter type
//    05/23/07 - Changed timescale to 1 ps / 1 ps.

`timescale  1 ps / 1 ps


`celldefine

module OBUF (O, I);

    parameter CAPACITANCE = "DONT_CARE";
    parameter integer DRIVE = 12;
    parameter IOSTANDARD = "DEFAULT";

`ifdef XIL_TIMING

    parameter LOC = " UNPLACED";

`endif

    parameter SLEW = "SLOW";
   
    output O;

    input  I;

    tri0 GTS = glbl.GTS;

    bufif0 B1 (O, I, GTS);

    initial begin
	
        case (CAPACITANCE)

            "LOW", "NORMAL", "DONT_CARE" : ;
            default : begin
                          $display("Attribute Syntax Error : The attribute CAPACITANCE on OBUF instance %m is set to %s.  Legal values for this attribute are DONT_CARE, LOW or NORMAL.", CAPACITANCE);
                          #1 $finish;
                      end

        endcase

    end

    
`ifdef XIL_TIMING
    
    specify
        (I => O) = (0:0:0, 0:0:0);
        specparam PATHPULSE$ = 0;
    endspecify

`endif

    
endmodule

`endcelldefine





///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2016 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor      : Xilinx
// \   \   \/     Version     : 2017.1
//  \   \         Description : Xilinx Unified Simulation Library Component
//  /   /                  2-Bit Look-Up Table
// /___/   /\     Filename : LUT2.v
// \   \  /  \
//  \___\/\___\
//
///////////////////////////////////////////////////////////////////////////////
//  Revision:
//    03/23/04 - Initial version.
//    03/11/05 - Add LOC Parameter
//    12/13/11 - 524859 - Added `celldefine and `endcelldefine
//    09/12/16 - ANSI ports, speed improvements
//  End Revision:
///////////////////////////////////////////////////////////////////////////////

`timescale 1 ps/1 ps

`celldefine

module LUT2 #(
`ifdef XIL_TIMING
  parameter LOC = "UNPLACED",
`endif
  parameter [3:0] INIT = 4'h0
)(
  output O,

  input I0,
  input I1
);

// define constants
  localparam MODULE_NAME = "LUT2";

  reg trig_attr = 1'b0;
// include dynamic registers - XILINX test only
`ifdef XIL_DR
  `include "LUT2_dr.v"
`else
  reg [3:0] INIT_REG = INIT;
`endif

  x_lut2_mux4 (O, INIT_REG[3], INIT_REG[2], INIT_REG[1], INIT_REG[0], I1, I0);

`ifdef XIL_TIMING
  specify
	(I0 => O) = (0:0:0, 0:0:0);
	(I1 => O) = (0:0:0, 0:0:0);
	specparam PATHPULSE$ = 0;
  endspecify
`endif

endmodule

`endcelldefine

primitive x_lut2_mux4 (o, d3, d2, d1, d0, s1, s0);

  output o;
  input d3, d2, d1, d0;
  input s1, s0;

  table

    // d3  d2  d1  d0  s1  s0 : o;

       ?   ?   ?   1   0   0  : 1;
       ?   ?   ?   0   0   0  : 0;
       ?   ?   1   ?   0   1  : 1;
       ?   ?   0   ?   0   1  : 0;
       ?   1   ?   ?   1   0  : 1;
       ?   0   ?   ?   1   0  : 0;
       1   ?   ?   ?   1   1  : 1;
       0   ?   ?   ?   1   1  : 0;

       ?   ?   0   0   0   x  : 0;
       ?   ?   1   1   0   x  : 1;
       0   0   ?   ?   1   x  : 0;
       1   1   ?   ?   1   x  : 1;

       ?   0   ?   0   x   0  : 0;
       ?   1   ?   1   x   0  : 1;
       0   ?   0   ?   x   1  : 0;
       1   ?   1   ?   x   1  : 1;

       0   0   0   0   x   x  : 0;
       1   1   1   1   x   x  : 1;

  endtable

endprimitive

///////////////////////////////////////////////////////////////////////////////
//  Copyright (c) 1995/2018 Xilinx, Inc.
//  All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /     Vendor      : Xilinx
// \   \   \/      Version     : 2018.3
//  \   \          Description : Xilinx Unified Simulation Library Component
//  /   /                        General Clock Buffer
// /___/   /\      Filename    : BUFG.v
// \   \  /  \
//  \___\/\___\
//
///////////////////////////////////////////////////////////////////////////////
//  Revision:
//    03/23/04 - Initial version.
//    05/23/07 - Changed timescale to 1 ps / 1 ps.
//    12/13/11 - 524859 - Added `celldefine and `endcelldefine
//  End Revision:
///////////////////////////////////////////////////////////////////////////////

`timescale 1 ps / 1 ps

`celldefine

module BUFG
`ifdef XIL_TIMING
#(
  parameter LOC = "UNPLACED"
)
`endif
(
  output O,

  input I
);
  
// define constants
  localparam MODULE_NAME = "BUFG";

`ifdef XIL_XECLIB
  reg glblGSR = 1'b0;
`else
  tri0 glblGSR = glbl.GSR;
`endif

`ifdef XIL_TIMING
  reg notifier;
`endif

// begin behavioral model

    buf B1 (O, I);

// end behavioral model

`ifndef XIL_XECLIB
`ifdef XIL_TIMING
  specify
    (I => O) = (0:0:0, 0:0:0);
    $period (negedge I, 0:0:0, notifier);
    $period (posedge I, 0:0:0, notifier);
    specparam PATHPULSE$ = 0;
  endspecify
`endif
`endif
endmodule

`endcelldefine

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2016 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor      : Xilinx
// \   \   \/     Version     : 2017.1
//  \   \         Description : Xilinx Unified Simulation Library Component
//  /   /                  6-Bit Look-Up Table
// /___/   /\     Filename : LUT6.v
// \   \  /  \
//  \___\/\___\
//
///////////////////////////////////////////////////////////////////////////////
//  Revision:
//    03/23/04 - Initial version.
//    02/04/05 - Replace primitive with function; Remove buf.
//    01/07/06 - 222733 - Add LOC Parameter
//    06/04/07 - Add wire declaration to internal signal.
//    12/13/11 - 524859 - Added `celldefine and `endcelldefine
//    09/12/16 - ANSI ports, speed improvements
//  End Revision:
///////////////////////////////////////////////////////////////////////////////

`timescale 1 ps/1 ps

`celldefine

module LUT6 #(
`ifdef XIL_TIMING
  parameter LOC = "UNPLACED",
`endif
  parameter [63:0] INIT = 64'h0000000000000000
)(
  output O,

  input I0,
  input I1,
  input I2,
  input I3,
  input I4,
  input I5
);

// define constants
  localparam MODULE_NAME = "LUT6";

  reg trig_attr = 1'b0;
// include dynamic registers - XILINX test only
`ifdef XIL_DR
  `include "LUT6_dr.v"
`else
  reg [63:0] INIT_REG = INIT;
`endif

// begin behavioral model

  reg O_out;

  assign O = O_out;

  function lut_mux8_f;
  input [7:0] d;
  input [2:0] s;
  begin
    if (((s[2]^s[1]^s[0]) === 1'b1) || ((s[2]^s[1]^s[0]) === 1'b0))
      lut_mux8_f = d[s];
    else if ( ~(|d) || &d)
      lut_mux8_f = d[0];
    else if ((((s[1]^s[0]) === 1'b1) || ((s[1]^s[0]) === 1'b0)) &&
             (d[{1'b0,s[1:0]}] === d[{1'b1,s[1:0]}]))
      lut_mux8_f = d[{1'b0,s[1:0]}];
    else if ((((s[2]^s[0]) === 1'b1) || ((s[2]^s[0]) === 1'b0)) &&
             (d[{s[2],1'b0,s[0]}] === d[{s[2],1'b1,s[0]}]))
      lut_mux8_f = d[{s[2],1'b0,s[0]}];
    else if ((((s[2]^s[1]) === 1'b1) || ((s[2]^s[1]) === 1'b0)) &&
             (d[{s[2],s[1],1'b0}] === d[{s[2],s[1],1'b1}]))
      lut_mux8_f = d[{s[2:1],1'b0}];
    else if (((s[0] === 1'b1) || (s[0] === 1'b0)) &&
             (d[{1'b0,1'b0,s[0]}] === d[{1'b0,1'b1,s[0]}]) &&
             (d[{1'b0,1'b0,s[0]}] === d[{1'b1,1'b0,s[0]}]) &&
             (d[{1'b0,1'b0,s[0]}] === d[{1'b1,1'b1,s[0]}]))
      lut_mux8_f = d[{1'b0,1'b0,s[0]}];
    else if (((s[1] === 1'b1) || (s[1] === 1'b0)) &&
             (d[{1'b0,s[1],1'b0}] === d[{1'b0,s[1],1'b1}]) &&
             (d[{1'b0,s[1],1'b0}] === d[{1'b1,s[1],1'b0}]) &&
             (d[{1'b0,s[1],1'b0}] === d[{1'b1,s[1],1'b1}]))
      lut_mux8_f = d[{1'b0,s[1],1'b0}];
    else if (((s[2] === 1'b1) || (s[2] === 1'b0)) &&
             (d[{s[2],1'b0,1'b0}] === d[{s[2],1'b0,1'b1}]) &&
             (d[{s[2],1'b0,1'b0}] === d[{s[2],1'b1,1'b0}]) &&
             (d[{s[2],1'b0,1'b0}] === d[{s[2],1'b1,1'b1}]))
      lut_mux8_f = d[{s[2],1'b0,1'b0}];
    else
      lut_mux8_f = 1'bx;
  end
  endfunction

 always @(I0 or I1 or I2 or I3 or I4 or I5)  begin
   if ( (I0 ^ I1  ^ I2 ^ I3 ^ I4 ^ I5) === 1'b0 || (I0 ^ I1  ^ I2 ^ I3 ^ I4 ^ I5) === 1'b1)
     O_out = INIT_REG[{I5, I4, I3, I2, I1, I0}];
   else if ( ~(|INIT_REG) || &INIT_REG )
     O_out = INIT_REG[0];
   else
     O_out = lut_mux8_f ({lut_mux8_f (INIT_REG[63:56], {I2, I1, I0}),
                      lut_mux8_f (INIT_REG[55:48], {I2, I1, I0}),
                      lut_mux8_f (INIT_REG[47:40], {I2, I1, I0}),
                      lut_mux8_f (INIT_REG[39:32], {I2, I1, I0}),
                      lut_mux8_f (INIT_REG[31:24], {I2, I1, I0}),
                      lut_mux8_f (INIT_REG[23:16], {I2, I1, I0}),
                      lut_mux8_f ( INIT_REG[15:8], {I2, I1, I0}),
                      lut_mux8_f (  INIT_REG[7:0], {I2, I1, I0})}, {I5, I4, I3});
 end

// end behavioral model

`ifdef XIL_TIMING
  specify
	(I0 => O) = (0:0:0, 0:0:0);
	(I1 => O) = (0:0:0, 0:0:0);
	(I2 => O) = (0:0:0, 0:0:0);
	(I3 => O) = (0:0:0, 0:0:0);
	(I4 => O) = (0:0:0, 0:0:0);
	(I5 => O) = (0:0:0, 0:0:0);
	specparam PATHPULSE$ = 0;
  endspecify
`endif

endmodule

`endcelldefine

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2016 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor      : Xilinx
// \   \   \/     Version     : 2017.1
//  \   \         Description : Xilinx Unified Simulation Library Component
//  /   /                  4-Bit Look-Up Table
// /___/   /\     Filename : LUT4.v
// \   \  /  \
//  \___\/\___\
//
///////////////////////////////////////////////////////////////////////////////
//  Revision:
//    03/23/04 - Initial version.
//    02/04/05 - Replace primitive with function; Remove buf.
//    03/11/05 - Add LOC Parameter
//    06/04/07 - Add wire declaration to internal signal.
//    12/13/11 - 524859 - Added `celldefine and `endcelldefine
//    09/12/16 - ANSI ports, speed improvements
//  End Revision:
///////////////////////////////////////////////////////////////////////////////

`timescale 1 ps/1 ps

`celldefine

module LUT4 #(
`ifdef XIL_TIMING
  parameter LOC = "UNPLACED",
`endif
  parameter [15:0] INIT = 16'h0000
)(
  output O,

  input I0,
  input I1,
  input I2,
  input I3
);

// define constants
  localparam MODULE_NAME = "LUT4";

  reg trig_attr = 1'b0;
// include dynamic registers - XILINX test only
`ifdef XIL_DR
  `include "LUT4_dr.v"
`else
  reg [15:0] INIT_REG = INIT;
`endif

// begin behavioral model

  reg O_out;

  assign O = O_out;

  function lut_mux4_f;
  input [3:0] d;
  input [1:0] s;
  begin
    if (((s[1]^s[0]) === 1'b1) || ((s[1]^s[0]) === 1'b0))
      lut_mux4_f = d[s];
    else if ( ~(|d) || &d)
      lut_mux4_f = d[0];
    else if (((s[0] === 1'b1) || (s[0] === 1'b0)) && (d[{1'b0,s[0]}] === d[{1'b1,s[0]}]))
      lut_mux4_f = d[{1'b0,s[0]}];
    else if (((s[1] === 1'b1) || (s[1] === 1'b0)) && (d[{s[1],1'b0}] === d[{s[1],1'b1}]))
      lut_mux4_f = d[{s[1],1'b0}];
    else
      lut_mux4_f = 1'bx;
  end
  endfunction

 always @(I0 or I1 or I2 or I3)  begin
   if ( (I0 ^ I1  ^ I2 ^ I3) === 1'b0 || (I0 ^ I1  ^ I2 ^ I3) === 1'b1)
    O_out = INIT_REG[{I3, I2, I1, I0}];
   else if ( ~(|INIT_REG) || &INIT_REG )
    O_out = INIT_REG[0];
   else
    O_out = lut_mux4_f ({lut_mux4_f (INIT_REG[15:12], {I1, I0}),
                     lut_mux4_f ( INIT_REG[11:8], {I1, I0}),
                     lut_mux4_f (  INIT_REG[7:4], {I1, I0}),
                     lut_mux4_f (  INIT_REG[3:0], {I1, I0})}, {I3, I2});
  end

// end behavioral model

`ifdef XIL_TIMING
  specify
	(I0 => O) = (0:0:0, 0:0:0);
	(I1 => O) = (0:0:0, 0:0:0);
	(I2 => O) = (0:0:0, 0:0:0);
	(I3 => O) = (0:0:0, 0:0:0);
	specparam PATHPULSE$ = 0;
  endspecify
`endif

endmodule

`endcelldefine

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2004 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 10.1
//  \   \         Description : Xilinx Functional Simulation Library Component
//  /   /                  Input Buffer
// /___/   /\     Filename : IBUF.v
// \   \  /  \    Timestamp : Thu Mar 25 16:42:23 PST 2004
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    05/23/07 - Changed timescale to 1 ps / 1 ps.
//    07/16/08 - Added IBUF_LOW_PWR attribute.
//    04/22/09 - CR 519127 - Changed IBUF_LOW_PWR default to TRUE.
//    12/13/11 - Added `celldefine and `endcelldefine (CR 524859).
//    10/22/14 - Added #1 to $finish (CR 808642).
// End Revision

`timescale  1 ps / 1 ps


`celldefine

module IBUF (O, I);

    parameter CAPACITANCE = "DONT_CARE";
    parameter IBUF_DELAY_VALUE = "0";
    parameter IBUF_LOW_PWR = "TRUE";
    parameter IFD_DELAY_VALUE = "AUTO";
    parameter IOSTANDARD = "DEFAULT";

`ifdef XIL_TIMING

    parameter LOC = " UNPLACED";

`endif

    
    output O;
    input  I;

    buf B1 (O, I);
    
    
    initial begin
	
        case (CAPACITANCE)

            "LOW", "NORMAL", "DONT_CARE" : ;
            default : begin
                          $display("Attribute Syntax Error : The attribute CAPACITANCE on IBUF instance %m is set to %s.  Legal values for this attribute are DONT_CARE, LOW or NORMAL.", CAPACITANCE);
                          #1 $finish;
                      end

        endcase


	case (IBUF_DELAY_VALUE)

            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16" : ;
            default : begin
                          $display("Attribute Syntax Error : The attribute IBUF_DELAY_VALUE on IBUF instance %m is set to %s.  Legal values for this attribute are 0, 1, 2, ... or 16.", IBUF_DELAY_VALUE);
                          #1 $finish;
                      end

        endcase

        case (IBUF_LOW_PWR)

            "FALSE", "TRUE" : ;
            default : begin
                          $display("Attribute Syntax Error : The attribute IBUF_LOW_PWR on IBUF instance %m is set to %s.  Legal values for this attribute are TRUE or FALSE.", IBUF_LOW_PWR);
                          #1 $finish;
                      end

        endcase


	case (IFD_DELAY_VALUE)

            "AUTO", "0", "1", "2", "3", "4", "5", "6", "7", "8" : ;
            default : begin
                          $display("Attribute Syntax Error : The attribute IFD_DELAY_VALUE on IBUF instance %m is set to %s.  Legal values for this attribute are AUTO, 0, 1, 2, ... or 8.", IFD_DELAY_VALUE);
                          #1 $finish;
                      end

	endcase
	
    end


`ifdef XIL_TIMING
    
    specify
        (I => O) = (0:0:0, 0:0:0);
        specparam PATHPULSE$ = 0;
    endspecify
    
`endif

    
endmodule

`endcelldefine


///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2009 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 10.1
//  \   \         Description : Xilinx Functional Simulation Library Component
//  /   /                  VCC Connection
// /___/   /\     Filename : VCC.v
// \   \  /  \    Timestamp : Thu Mar 25 16:43:41 PST 2004
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    05/23/07 - Changed timescale to 1 ps / 1 ps.
//    12/13/11 - Added `celldefine and `endcelldefine (CR 524859).
// End Revision

`timescale  1 ps / 1 ps


`celldefine

module VCC(P);


`ifdef XIL_TIMING

    parameter LOC = "UNPLACED";

`endif


    output P;

    assign P = 1'b1;

endmodule

`endcelldefine


///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2009 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 10.1
//  \   \         Description : Xilinx Functional Simulation Library Component
//  /   /                  GND Connection
// /___/   /\     Filename : GND.v
// \   \  /  \    Timestamp : Thu Mar 25 16:42:19 PST 2004
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    05/23/07 - Changed timescale to 1 ps / 1 ps.

`timescale  1 ps / 1 ps


`celldefine

module GND(G);


`ifdef XIL_TIMING

    parameter LOC = "UNPLACED";

`endif

    output G;

    assign G = 1'b0;

endmodule

`endcelldefine


