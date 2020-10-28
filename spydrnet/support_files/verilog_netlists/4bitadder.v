// Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2018.3 (win64) Build 2405991 Thu Dec  6 23:38:27 MST 2018
// Date        : Mon Feb  3 13:26:57 2020
// Host        : CB461-EE10461 running 64-bit major release  (build 9200)
// Command     : write_verilog -file C:/Users/mbjerreg/verilog/4bitadder.v -include_xilinx_libs
// Design      : adder
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xc7a100tcsg324-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* STRUCTURAL_NETLIST = "yes" *)
module adder
   (data1,
    data2,
    answer,
    clk,
    reset,
    enable);
  input [3:0]data1;
  input [3:0]data2;
  output [3:0]answer;
  input clk;
  input reset;
  input enable;

  wire \^GND ;
  wire GND_2;
  wire VCC_1;
  wire [3:0]answer;
  wire [3:0]answer1;
  wire [3:0]answer2;
  wire [3:0]answer_1;
  wire clk;
  wire clk_c;
  wire [3:0]data1;
  wire [3:0]data11;
  wire [3:0]data11r;
  wire [3:0]data12;
  wire [3:0]data12r;
  wire [3:0]data1_c;
  wire [3:0]data2;
  wire [3:0]data21;
  wire [3:0]data21r;
  wire [3:0]data22;
  wire [3:0]data22r;
  wire [3:0]data2_c;
  wire [3:0]ddata1;
  wire [3:0]ddata2;
  wire \^dlyctrl ;
  wire enable;
  wire enable_c;
  wire reset;
  wire reset_c;
  wire \^reset_c_i ;
  wire \^un2_answer2_axb0 ;
  wire \^un2_answer2_axbxc1 ;
  wire \^un2_answer2_axbxc2 ;
  wire \^un2_answer2_axbxc3 ;
  wire \^un2_answer2_axbxc3_1 ;
  wire \^un2_answer2_p4 ;
  wire \^un3_answer1_axb0 ;
  wire \^un3_answer1_axbxc1 ;
  wire \^un3_answer1_axbxc2 ;
  wire \^un3_answer1_axbxc3 ;
  wire \^un3_answer1_axbxc3_1 ;
  wire \^un3_answer1_p4 ;

  GND GND
       (.G(\^GND ));
  GND GND_1
       (.G(GND_2));
  VCC VCC
       (.P(VCC_1));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \answer1[0] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(\^un3_answer1_axb0 ),
        .Q(answer1[0]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \answer1[1] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(\^un3_answer1_axbxc1 ),
        .Q(answer1[1]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \answer1[2] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(\^un3_answer1_axbxc2 ),
        .Q(answer1[2]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \answer1[3] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(\^un3_answer1_axbxc3 ),
        .Q(answer1[3]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \answer2[0] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(\^un2_answer2_axb0 ),
        .Q(answer2[0]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \answer2[1] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(\^un2_answer2_axbxc1 ),
        .Q(answer2[1]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \answer2[2] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(\^un2_answer2_axbxc2 ),
        .Q(answer2[2]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \answer2[3] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(\^un2_answer2_axbxc3 ),
        .Q(answer2[3]));
  (* OPT_MODIFIED = "MLO " *) 
  (* __SRVAL = "FALSE" *) 
  ODDR #(
    .INIT(1'b0)) 
    \answer_gen.0.U_ODDR 
       (.C(clk_c),
        .CE(enable_c),
        .D1(answer1[0]),
        .D2(answer2[0]),
        .Q(answer_1[0]),
        .R(reset_c));
  (* OPT_MODIFIED = "MLO " *) 
  (* __SRVAL = "FALSE" *) 
  ODDR #(
    .INIT(1'b0)) 
    \answer_gen.1.U_ODDR 
       (.C(clk_c),
        .CE(enable_c),
        .D1(answer1[1]),
        .D2(answer2[1]),
        .Q(answer_1[1]),
        .R(reset_c));
  (* OPT_MODIFIED = "MLO " *) 
  (* __SRVAL = "FALSE" *) 
  ODDR #(
    .INIT(1'b0)) 
    \answer_gen.2.U_ODDR 
       (.C(clk_c),
        .CE(enable_c),
        .D1(answer1[2]),
        .D2(answer2[2]),
        .Q(answer_1[2]),
        .R(reset_c));
  (* OPT_MODIFIED = "MLO " *) 
  (* __SRVAL = "FALSE" *) 
  ODDR #(
    .INIT(1'b0)) 
    \answer_gen.3.U_ODDR 
       (.C(clk_c),
        .CE(enable_c),
        .D1(answer1[3]),
        .D2(answer2[3]),
        .Q(answer_1[3]),
        .R(reset_c));
  OBUF \answer_obuf[0] 
       (.I(answer_1[0]),
        .O(answer[0]));
  OBUF \answer_obuf[1] 
       (.I(answer_1[1]),
        .O(answer[1]));
  OBUF \answer_obuf[2] 
       (.I(answer_1[2]),
        .O(answer[2]));
  OBUF \answer_obuf[3] 
       (.I(answer_1[3]),
        .O(answer[3]));
  (* XILINX_REPORT_XFORM = "BUFGP" *) 
  BUFGP clk_ibuf
       (.I(clk),
        .O(clk_c));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data11r[0] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data11[0]),
        .Q(data11r[0]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data11r[1] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data11[1]),
        .Q(data11r[1]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data11r[2] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data11[2]),
        .Q(data11r[2]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data11r[3] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data11[3]),
        .Q(data11r[3]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data12r[0] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data12[0]),
        .Q(data12r[0]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data12r[1] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data12[1]),
        .Q(data12r[1]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data12r[2] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data12[2]),
        .Q(data12r[2]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data12r[3] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data12[3]),
        .Q(data12r[3]));
  IBUF \data1_ibuf[0] 
       (.I(data1[0]),
        .O(data1_c[0]));
  IBUF \data1_ibuf[1] 
       (.I(data1[1]),
        .O(data1_c[1]));
  IBUF \data1_ibuf[2] 
       (.I(data1[2]),
        .O(data1_c[2]));
  IBUF \data1_ibuf[3] 
       (.I(data1[3]),
        .O(data1_c[3]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data21r[0] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data21[0]),
        .Q(data21r[0]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data21r[1] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data21[1]),
        .Q(data21r[1]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data21r[2] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data21[2]),
        .Q(data21r[2]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data21r[3] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data21[3]),
        .Q(data21r[3]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data22r[0] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data22[0]),
        .Q(data22r[0]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data22r[1] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data22[1]),
        .Q(data22r[1]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data22r[2] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data22[2]),
        .Q(data22r[2]));
  (* XILINX_LEGACY_PRIM = "FDC" *) 
  (* XILINX_REPORT_XFORM = "FDC" *) 
  FDCE #(
    .INIT(1'b0)) 
    \data22r[3] 
       (.C(clk_c),
        .CE(VCC_1),
        .CLR(\^reset_c_i ),
        .D(data22[3]),
        .Q(data22r[3]));
  IBUF \data2_ibuf[0] 
       (.I(data2[0]),
        .O(data2_c[0]));
  IBUF \data2_ibuf[1] 
       (.I(data2[1]),
        .O(data2_c[1]));
  IBUF \data2_ibuf[2] 
       (.I(data2[2]),
        .O(data2_c[2]));
  IBUF \data2_ibuf[3] 
       (.I(data2[3]),
        .O(data2_c[3]));
  (* XILINX_LEGACY_PRIM = "IDELAY" *) 
  (* XILINX_REPORT_XFORM = "IDELAY" *) 
  (* XILINX_TRANSFORM_PINMAP = "O:DATAOUT I:IDATAIN RST:LD" *) 
  IDELAYE2 #(
    .CINVCTRL_SEL("FALSE"),
    .DELAY_SRC("IDATAIN"),
    .HIGH_PERFORMANCE_MODE("TRUE"),
    .IDELAY_TYPE("FIXED"),
    .IDELAY_VALUE(0),
    .REFCLK_FREQUENCY(200.000000),
    .SIGNAL_PATTERN("DATA")) 
    \ddata_gen.0.UD1 
       (.C(\^GND ),
        .CE(\^GND ),
        .CINVCTRL(GND_2),
        .DATAIN(VCC_1),
        .DATAOUT(ddata1[0]),
        .IDATAIN(data1_c[0]),
        .INC(\^GND ),
        .LD(\^GND ),
        .LDPIPEEN(GND_2),
        .REGRST(GND_2));
  (* XILINX_LEGACY_PRIM = "IDELAY" *) 
  (* XILINX_REPORT_XFORM = "IDELAY" *) 
  (* XILINX_TRANSFORM_PINMAP = "O:DATAOUT I:IDATAIN RST:LD" *) 
  IDELAYE2 #(
    .CINVCTRL_SEL("FALSE"),
    .DELAY_SRC("IDATAIN"),
    .HIGH_PERFORMANCE_MODE("TRUE"),
    .IDELAY_TYPE("FIXED"),
    .IDELAY_VALUE(0),
    .REFCLK_FREQUENCY(200.000000),
    .SIGNAL_PATTERN("DATA")) 
    \ddata_gen.0.UD2 
       (.C(\^GND ),
        .CE(\^GND ),
        .CINVCTRL(GND_2),
        .DATAIN(VCC_1),
        .DATAOUT(ddata2[0]),
        .IDATAIN(data2_c[0]),
        .INC(\^GND ),
        .LD(\^GND ),
        .LDPIPEEN(GND_2),
        .REGRST(GND_2));
  (* XILINX_LEGACY_PRIM = "IDELAY" *) 
  (* XILINX_REPORT_XFORM = "IDELAY" *) 
  (* XILINX_TRANSFORM_PINMAP = "O:DATAOUT I:IDATAIN RST:LD" *) 
  IDELAYE2 #(
    .CINVCTRL_SEL("FALSE"),
    .DELAY_SRC("IDATAIN"),
    .HIGH_PERFORMANCE_MODE("TRUE"),
    .IDELAY_TYPE("FIXED"),
    .IDELAY_VALUE(0),
    .REFCLK_FREQUENCY(200.000000),
    .SIGNAL_PATTERN("DATA")) 
    \ddata_gen.1.UD1 
       (.C(\^GND ),
        .CE(\^GND ),
        .CINVCTRL(GND_2),
        .DATAIN(VCC_1),
        .DATAOUT(ddata1[1]),
        .IDATAIN(data1_c[1]),
        .INC(\^GND ),
        .LD(\^GND ),
        .LDPIPEEN(GND_2),
        .REGRST(GND_2));
  (* XILINX_LEGACY_PRIM = "IDELAY" *) 
  (* XILINX_REPORT_XFORM = "IDELAY" *) 
  (* XILINX_TRANSFORM_PINMAP = "O:DATAOUT I:IDATAIN RST:LD" *) 
  IDELAYE2 #(
    .CINVCTRL_SEL("FALSE"),
    .DELAY_SRC("IDATAIN"),
    .HIGH_PERFORMANCE_MODE("TRUE"),
    .IDELAY_TYPE("FIXED"),
    .IDELAY_VALUE(0),
    .REFCLK_FREQUENCY(200.000000),
    .SIGNAL_PATTERN("DATA")) 
    \ddata_gen.1.UD2 
       (.C(\^GND ),
        .CE(\^GND ),
        .CINVCTRL(GND_2),
        .DATAIN(VCC_1),
        .DATAOUT(ddata2[1]),
        .IDATAIN(data2_c[1]),
        .INC(\^GND ),
        .LD(\^GND ),
        .LDPIPEEN(GND_2),
        .REGRST(GND_2));
  (* XILINX_LEGACY_PRIM = "IDELAY" *) 
  (* XILINX_REPORT_XFORM = "IDELAY" *) 
  (* XILINX_TRANSFORM_PINMAP = "O:DATAOUT I:IDATAIN RST:LD" *) 
  IDELAYE2 #(
    .CINVCTRL_SEL("FALSE"),
    .DELAY_SRC("IDATAIN"),
    .HIGH_PERFORMANCE_MODE("TRUE"),
    .IDELAY_TYPE("FIXED"),
    .IDELAY_VALUE(0),
    .REFCLK_FREQUENCY(200.000000),
    .SIGNAL_PATTERN("DATA")) 
    \ddata_gen.2.UD1 
       (.C(\^GND ),
        .CE(\^GND ),
        .CINVCTRL(GND_2),
        .DATAIN(VCC_1),
        .DATAOUT(ddata1[2]),
        .IDATAIN(data1_c[2]),
        .INC(\^GND ),
        .LD(\^GND ),
        .LDPIPEEN(GND_2),
        .REGRST(GND_2));
  (* XILINX_LEGACY_PRIM = "IDELAY" *) 
  (* XILINX_REPORT_XFORM = "IDELAY" *) 
  (* XILINX_TRANSFORM_PINMAP = "O:DATAOUT I:IDATAIN RST:LD" *) 
  IDELAYE2 #(
    .CINVCTRL_SEL("FALSE"),
    .DELAY_SRC("IDATAIN"),
    .HIGH_PERFORMANCE_MODE("TRUE"),
    .IDELAY_TYPE("FIXED"),
    .IDELAY_VALUE(0),
    .REFCLK_FREQUENCY(200.000000),
    .SIGNAL_PATTERN("DATA")) 
    \ddata_gen.2.UD2 
       (.C(\^GND ),
        .CE(\^GND ),
        .CINVCTRL(GND_2),
        .DATAIN(VCC_1),
        .DATAOUT(ddata2[2]),
        .IDATAIN(data2_c[2]),
        .INC(\^GND ),
        .LD(\^GND ),
        .LDPIPEEN(GND_2),
        .REGRST(GND_2));
  (* XILINX_LEGACY_PRIM = "IDELAY" *) 
  (* XILINX_REPORT_XFORM = "IDELAY" *) 
  (* XILINX_TRANSFORM_PINMAP = "O:DATAOUT I:IDATAIN RST:LD" *) 
  IDELAYE2 #(
    .CINVCTRL_SEL("FALSE"),
    .DELAY_SRC("IDATAIN"),
    .HIGH_PERFORMANCE_MODE("TRUE"),
    .IDELAY_TYPE("FIXED"),
    .IDELAY_VALUE(0),
    .REFCLK_FREQUENCY(200.000000),
    .SIGNAL_PATTERN("DATA")) 
    \ddata_gen.3.UD1 
       (.C(\^GND ),
        .CE(\^GND ),
        .CINVCTRL(GND_2),
        .DATAIN(VCC_1),
        .DATAOUT(ddata1[3]),
        .IDATAIN(data1_c[3]),
        .INC(\^GND ),
        .LD(\^GND ),
        .LDPIPEEN(GND_2),
        .REGRST(GND_2));
  (* XILINX_LEGACY_PRIM = "IDELAY" *) 
  (* XILINX_REPORT_XFORM = "IDELAY" *) 
  (* XILINX_TRANSFORM_PINMAP = "O:DATAOUT I:IDATAIN RST:LD" *) 
  IDELAYE2 #(
    .CINVCTRL_SEL("FALSE"),
    .DELAY_SRC("IDATAIN"),
    .HIGH_PERFORMANCE_MODE("TRUE"),
    .IDELAY_TYPE("FIXED"),
    .IDELAY_VALUE(0),
    .REFCLK_FREQUENCY(200.000000),
    .SIGNAL_PATTERN("DATA")) 
    \ddata_gen.3.UD2 
       (.C(\^GND ),
        .CE(\^GND ),
        .CINVCTRL(GND_2),
        .DATAIN(VCC_1),
        .DATAOUT(ddata2[3]),
        .IDATAIN(data2_c[3]),
        .INC(\^GND ),
        .LD(\^GND ),
        .LDPIPEEN(GND_2),
        .REGRST(GND_2));
  (* __SRVAL = "FALSE" *) 
  IDDR \ddr_data_gen.0.U1_IDDR 
       (.C(clk_c),
        .CE(enable_c),
        .D(ddata1[0]),
        .Q1(data11[0]),
        .Q2(data12[0]),
        .R(reset_c),
        .S(\^GND ));
  (* __SRVAL = "FALSE" *) 
  IDDR \ddr_data_gen.0.U2_IDDR 
       (.C(clk_c),
        .CE(enable_c),
        .D(ddata2[0]),
        .Q1(data21[0]),
        .Q2(data22[0]),
        .R(reset_c),
        .S(\^GND ));
  (* __SRVAL = "FALSE" *) 
  IDDR \ddr_data_gen.1.U1_IDDR 
       (.C(clk_c),
        .CE(enable_c),
        .D(ddata1[1]),
        .Q1(data11[1]),
        .Q2(data12[1]),
        .R(reset_c),
        .S(\^GND ));
  (* __SRVAL = "FALSE" *) 
  IDDR \ddr_data_gen.1.U2_IDDR 
       (.C(clk_c),
        .CE(enable_c),
        .D(ddata2[1]),
        .Q1(data21[1]),
        .Q2(data22[1]),
        .R(reset_c),
        .S(\^GND ));
  (* __SRVAL = "FALSE" *) 
  IDDR \ddr_data_gen.2.U1_IDDR 
       (.C(clk_c),
        .CE(enable_c),
        .D(ddata1[2]),
        .Q1(data11[2]),
        .Q2(data12[2]),
        .R(reset_c),
        .S(\^GND ));
  (* __SRVAL = "FALSE" *) 
  IDDR \ddr_data_gen.2.U2_IDDR 
       (.C(clk_c),
        .CE(enable_c),
        .D(ddata2[2]),
        .Q1(data21[2]),
        .Q2(data22[2]),
        .R(reset_c),
        .S(\^GND ));
  (* __SRVAL = "FALSE" *) 
  IDDR \ddr_data_gen.3.U1_IDDR 
       (.C(clk_c),
        .CE(enable_c),
        .D(ddata1[3]),
        .Q1(data11[3]),
        .Q2(data12[3]),
        .R(reset_c),
        .S(\^GND ));
  (* __SRVAL = "FALSE" *) 
  IDDR \ddr_data_gen.3.U2_IDDR 
       (.C(clk_c),
        .CE(enable_c),
        .D(ddata2[3]),
        .Q1(data21[3]),
        .Q2(data22[3]),
        .R(reset_c),
        .S(\^GND ));
  IDELAYCTRL dlyctrl
       (.RDY(\^dlyctrl ),
        .REFCLK(clk_c),
        .RST(reset_c));
  IBUF enable_ibuf
       (.I(enable),
        .O(enable_c));
  (* XILINX_LEGACY_PRIM = "INV" *) 
  (* XILINX_REPORT_XFORM = "INV" *) 
  (* XILINX_TRANSFORM_PINMAP = "I:I0" *) 
  LUT1 #(
    .INIT(2'h1)) 
    reset_c_i
       (.I0(reset_c),
        .O(\^reset_c_i ));
  IBUF reset_ibuf
       (.I(reset),
        .O(reset_c));
  (* XILINX_LEGACY_PRIM = "LUT2_L" *) 
  (* XILINX_REPORT_XFORM = "LUT2_L" *) 
  (* XILINX_TRANSFORM_PINMAP = "LO:O" *) 
  LUT2 #(
    .INIT(4'h6)) 
    un2_answer2_axb0
       (.I0(data12r[0]),
        .I1(data22r[0]),
        .O(\^un2_answer2_axb0 ));
  (* XILINX_LEGACY_PRIM = "LUT4_L" *) 
  (* XILINX_REPORT_XFORM = "LUT4_L" *) 
  (* XILINX_TRANSFORM_PINMAP = "LO:O" *) 
  LUT4 #(
    .INIT(16'h936C)) 
    un2_answer2_axbxc1
       (.I0(data12r[0]),
        .I1(data12r[1]),
        .I2(data22r[0]),
        .I3(data22r[1]),
        .O(\^un2_answer2_axbxc1 ));
  (* XILINX_LEGACY_PRIM = "LUT3_L" *) 
  (* XILINX_REPORT_XFORM = "LUT3_L" *) 
  (* XILINX_TRANSFORM_PINMAP = "LO:O" *) 
  LUT3 #(
    .INIT(8'h96)) 
    un2_answer2_axbxc2
       (.I0(data12r[2]),
        .I1(data22r[2]),
        .I2(\^un2_answer2_p4 ),
        .O(\^un2_answer2_axbxc2 ));
  (* XILINX_LEGACY_PRIM = "LUT4_L" *) 
  (* XILINX_REPORT_XFORM = "LUT4_L" *) 
  (* XILINX_TRANSFORM_PINMAP = "LO:O" *) 
  LUT4 #(
    .INIT(16'h1E78)) 
    un2_answer2_axbxc3
       (.I0(data12r[2]),
        .I1(data22r[2]),
        .I2(\^un2_answer2_axbxc3_1 ),
        .I3(\^un2_answer2_p4 ),
        .O(\^un2_answer2_axbxc3 ));
  LUT2 #(
    .INIT(4'h6)) 
    un2_answer2_axbxc3_1
       (.I0(data12r[3]),
        .I1(data22r[3]),
        .O(\^un2_answer2_axbxc3_1 ));
  LUT4 #(
    .INIT(16'hEC80)) 
    un2_answer2_p4
       (.I0(data12r[0]),
        .I1(data12r[1]),
        .I2(data22r[0]),
        .I3(data22r[1]),
        .O(\^un2_answer2_p4 ));
  (* XILINX_LEGACY_PRIM = "LUT2_L" *) 
  (* XILINX_REPORT_XFORM = "LUT2_L" *) 
  (* XILINX_TRANSFORM_PINMAP = "LO:O" *) 
  LUT2 #(
    .INIT(4'h6)) 
    un3_answer1_axb0
       (.I0(data11r[0]),
        .I1(data21r[0]),
        .O(\^un3_answer1_axb0 ));
  (* XILINX_LEGACY_PRIM = "LUT4_L" *) 
  (* XILINX_REPORT_XFORM = "LUT4_L" *) 
  (* XILINX_TRANSFORM_PINMAP = "LO:O" *) 
  LUT4 #(
    .INIT(16'h936C)) 
    un3_answer1_axbxc1
       (.I0(data11r[0]),
        .I1(data11r[1]),
        .I2(data21r[0]),
        .I3(data21r[1]),
        .O(\^un3_answer1_axbxc1 ));
  (* XILINX_LEGACY_PRIM = "LUT3_L" *) 
  (* XILINX_REPORT_XFORM = "LUT3_L" *) 
  (* XILINX_TRANSFORM_PINMAP = "LO:O" *) 
  LUT3 #(
    .INIT(8'h96)) 
    un3_answer1_axbxc2
       (.I0(data11r[2]),
        .I1(data21r[2]),
        .I2(\^un3_answer1_p4 ),
        .O(\^un3_answer1_axbxc2 ));
  (* XILINX_LEGACY_PRIM = "LUT4_L" *) 
  (* XILINX_REPORT_XFORM = "LUT4_L" *) 
  (* XILINX_TRANSFORM_PINMAP = "LO:O" *) 
  LUT4 #(
    .INIT(16'h1E78)) 
    un3_answer1_axbxc3
       (.I0(data11r[2]),
        .I1(data21r[2]),
        .I2(\^un3_answer1_axbxc3_1 ),
        .I3(\^un3_answer1_p4 ),
        .O(\^un3_answer1_axbxc3 ));
  LUT2 #(
    .INIT(4'h6)) 
    un3_answer1_axbxc3_1
       (.I0(data11r[3]),
        .I1(data21r[3]),
        .O(\^un3_answer1_axbxc3_1 ));
  LUT4 #(
    .INIT(16'hEC80)) 
    un3_answer1_p4
       (.I0(data11r[0]),
        .I1(data11r[1]),
        .I2(data21r[0]),
        .I3(data21r[1]),
        .O(\^un3_answer1_p4 ));
endmodule
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
// Copyright (c) 1995/2015 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor      : Xilinx
// \   \   \/     Version     : 2015.3
//  \   \         Description : Xilinx Unified Simulation Library Component
//  /   /                       IDELAYE3/ODELAYE3 Tap Delay Value Control
// /___/   /\     Filename    : IDELAYCTRL.v
// \   \  /  \
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    03/11/05 - Added LOC parameter and initialized outpus.
//    04/10/07 - CR 436682 fix, disable activity when rst is high
//    12/13/11 - Added `celldefine and `endcelldefine (CR 524859).
//    06/01/15 - 850338 - Added SIM_DEVICE and warning
// End Revision

`timescale 1 ps / 1 ps 

`celldefine

module IDELAYCTRL #(
`ifdef XIL_TIMING
  parameter LOC = "UNPLACED",
`endif
  parameter SIM_DEVICE = "7SERIES"
)(
  output RDY,

  input REFCLK,
  input RST
);

// define constants
  localparam MODULE_NAME = "IDELAYCTRL";

// Parameter encodings and registers
  localparam SIM_DEVICE_7SERIES = 0;
  localparam SIM_DEVICE_ULTRASCALE = 1;

  reg trig_attr = 1'b0;
// include dynamic registers - XILINX test only
//`ifdef XIL_DR
//  `include "IDELAYCTRL_dr.v"
//`else
  localparam [80:1] SIM_DEVICE_REG = SIM_DEVICE;
//`endif

`ifdef XIL_ATTR_TEST
  reg attr_test = 1'b1;
`else
  reg attr_test = 1'b0;
`endif
  reg attr_err = 1'b0;

  reg RDY_out = 0;

  wire REFCLK_in;
  wire RST_in;

`ifdef XIL_TIMING
  wire REFCLK_delay;
  wire RST_delay;
`endif

  assign RDY = RDY_out;

`ifdef XIL_TIMING
  assign REFCLK_in = REFCLK_delay;
  assign RST_in = RST_delay;
`else
  assign REFCLK_in = REFCLK;
  assign RST_in = RST;
`endif

    time clock_edge;
    reg [63:0] period;
    reg clock_low, clock_high;
    reg clock_posedge, clock_negedge;
    reg lost;
    reg msg_flag = 1'b0;


  initial begin
    #1;
    trig_attr = ~trig_attr;
  end
  
  always @ (trig_attr) begin
    #1;
    if ((attr_test == 1'b1) ||
        ((SIM_DEVICE_REG != "7SERIES") &&
         (SIM_DEVICE_REG != "ULTRASCALE"))) begin
      $display("Error: [Unisim %s-104] SIM_DEVICE attribute is set to %s.  Legal values for this attribute are 7SERIES or ULTRASCALE. Instance: %m", MODULE_NAME, SIM_DEVICE_REG);
      attr_err = 1'b1;
    end
    
    if (attr_err == 1'b1) #1 $finish;
  end


    always @(RST_in, lost) begin

   if (RST_in == 1'b1) begin
     RDY_out <= 1'b0;
   end else if (lost == 1)
     RDY_out <= 1'b0;
   else if (RST_in == 1'b0 && lost == 0)
     RDY_out <= 1'b1;
    end
   
   always @(posedge RST_in) begin
     if (SIM_DEVICE_REG == "ULTRASCALE" && msg_flag == 1'b0) begin 
       $display("Info: [Unisim %s-1] RST simulation behaviour for SIM_DEVICE %s may not match hardware behaviour when I/ODELAY DELAY_FORMAT = TIME if SelectIO User Guide recommendation for I/ODELAY connections or reset sequence are not followed. For more information, refer to the Select IO Userguide. Instance: %m", MODULE_NAME, SIM_DEVICE_REG);
      msg_flag <= 1'b1;
     end
   end
    initial begin
   clock_edge <= 0;
   clock_high <= 0;
   clock_low <= 0;
   lost <= 1;
   period <= 0;
    end


    always @(posedge REFCLK_in) begin
      if(RST_in == 1'b0) begin
   clock_edge <= $time;
   if (period != 0 && (($time - clock_edge) <= (1.5 * period)))
       period <= $time - clock_edge;
   else if (period != 0 && (($time - clock_edge) > (1.5 * period)))
       period <= 0;
   else if ((period == 0) && (clock_edge != 0))
       period <= $time - clock_edge;
      end
    end
    
    always @(posedge REFCLK_in) begin
   clock_low <= 1'b0;
   clock_high <= 1'b1;
   if (period != 0)
       lost <= 1'b0;
   clock_posedge <= 1'b0;
   #((period * 9.1) / 10)
   if ((clock_low != 1'b1) && (clock_posedge != 1'b1))
       lost <= 1;
    end
    
    always @(posedge REFCLK_in) begin
   clock_negedge <= 1'b1;
    end
    
    always @(negedge REFCLK_in) begin
   clock_posedge <= 1'b1;
    end
    
    always @(negedge REFCLK_in) begin
   clock_high  <= 1'b0;
   clock_low   <= 1'b1;
   if (period != 0)
       lost <= 1'b0;
   clock_negedge <= 1'b0;
   #((period * 9.1) / 10)
   if ((clock_high != 1'b1) && (clock_negedge != 1'b1))
       lost <= 1;
    end

//*** Timing Checks Start here
`ifdef XIL_TIMING
  reg notifier;
`endif

  specify
  (RST => RDY) = (0:0:0, 0:0:0);
  (posedge RST => (RDY +: 0)) = (0:0:0, 0:0:0);
  (REFCLK => RDY) = (100:100:100, 100:100:100);
`ifdef XIL_TIMING
    $period (negedge REFCLK, 0:0:0, notifier);
    $period (posedge REFCLK, 0:0:0, notifier);
    $recrem (negedge RST, posedge REFCLK, 0:0:0, 0:0:0, notifier, , , RST_delay, REFCLK_delay);
    $recrem (posedge RST, posedge REFCLK, 0:0:0, 0:0:0, notifier, , , RST_delay, REFCLK_delay);
    $width (negedge REFCLK, 0:0:0, 0, notifier);
    $width (negedge RST, 0:0:0, 0, notifier);
    $width (posedge REFCLK, 0:0:0, 0, notifier);
    $width (posedge RST, 0:0:0, 0, notifier);
`endif
    specparam PATHPULSE$ = 0;
  endspecify

endmodule

`endcelldefine

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2005 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 8.1i (I.13)
//  \   \         Description : Xilinx Timing Simulation Library Component
//  /   /                  Dual Data Rate Input D Flip-Flop
// /___/   /\     Filename : IDDR.v
// \   \  /  \    Timestamp : Thu Mar 11 16:44:06 PST 2005
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    03/11/05 - Added LOC parameter, removed GSR ports and initialized outpus.
//    12/20/05 - Fixed setup and hold checks.
//    04/28/06 - Added c_in into the sensitivity list (CR 219840).
//    05/29/07 - Added wire declaration for internal signals
//    04/16/08 - CR 468871 Negative SetupHold fix
//    05/06/08 - CR 455447 add XON MSGON property to support async reg
//    12/03/08 - CR 498674 added pulldown on R/S.
//    12/13/11 - Added `celldefine and `endcelldefine (CR 524859).
//    08/23/13 - PR683925 - add invertible pin support.
//    10/22/14 - Added #1 to $finish (CR 808642).
// End Revision

`timescale  1 ps / 1 ps

`celldefine

module IDDR (Q1, Q2, C, CE, D, R, S);
    
    output Q1;
    output Q2;
    
    input C;
    input CE;
    input D;
    input R;
    input S;

    parameter DDR_CLK_EDGE = "OPPOSITE_EDGE";    
    parameter INIT_Q1 = 1'b0;
    parameter INIT_Q2 = 1'b0;
    parameter [0:0] IS_C_INVERTED = 1'b0;
    parameter [0:0] IS_D_INVERTED = 1'b0;
    parameter SRTYPE = "SYNC";

`ifdef XIL_TIMING

    parameter LOC = "UNPLACED";
    parameter MSGON = "TRUE";
    parameter XON = "TRUE";

`endif



    pulldown P1 (R);
    pulldown P2 (S);

    reg q1_out = INIT_Q1, q2_out = INIT_Q2;
    reg q1_out_int, q2_out_int;
    reg q1_out_pipelined, q2_out_same_edge_int;
    reg notifier, notifier1, notifier2;
    wire notifier1x, notifier2x;

    wire c_in,delay_c;
    wire ce_in,delay_ce;
    wire d_in,delay_d;
    wire gsr_in;
    wire r_in,delay_r;
    wire s_in,delay_s;
    
    tri0 GSR = glbl.GSR;
    
    assign gsr_in = GSR;
    assign Q1 = q1_out;
    assign Q2 = q2_out;
    
    wire nr, ns, ngsr;
    wire ce_c_enable, d_c_enable, r_c_enable, s_c_enable;
    wire ce_c_enable1, d_c_enable1, r_c_enable1, s_c_enable1;
    not (nr, R);
    not (ns, S);
    not (ngsr, GSR);

    and (ce_c_enable, ngsr, nr, ns);
    and (d_c_enable, ngsr, nr, ns, CE);
    and (s_c_enable, ngsr, nr);


`ifdef XIL_TIMING

    assign notifier1x = (XON == "FALSE") ?  1'bx : notifier1;
    assign notifier2x = (XON == "FALSE") ?  1'bx : notifier2;

    assign ce_c_enable1 = (MSGON =="FALSE") ? 1'b0 : ce_c_enable;
    assign d_c_enable1 = (MSGON =="FALSE") ? 1'b0 : d_c_enable;
    assign r_c_enable1 = (MSGON =="FALSE") ? 1'b0 : ngsr;
    assign s_c_enable1 = (MSGON =="FALSE") ? 1'b0 : s_c_enable;

`endif

    
    initial begin

   if ((INIT_Q1 != 0) && (INIT_Q1 != 1)) begin
       $display("Attribute Syntax Error : The attribute INIT_Q1 on IDDR instance %m is set to %d.  Legal values for this attribute are 0 or 1.", INIT_Q1);
       #1 $finish;
   end
   
       if ((INIT_Q2 != 0) && (INIT_Q2 != 1)) begin
       $display("Attribute Syntax Error : The attribute INIT_Q1 on IDDR instance %m is set to %d.  Legal values for this attribute are 0 or 1.", INIT_Q2);
       #1 $finish;
   end

       if ((DDR_CLK_EDGE != "OPPOSITE_EDGE") && (DDR_CLK_EDGE != "SAME_EDGE") && (DDR_CLK_EDGE != "SAME_EDGE_PIPELINED")) begin
       $display("Attribute Syntax Error : The attribute DDR_CLK_EDGE on IDDR instance %m is set to %s.  Legal values for this attribute are OPPOSITE_EDGE, SAME_EDGE or SAME_EDGE_PIPELINED.", DDR_CLK_EDGE);
       #1 $finish;
   end
   
   if ((SRTYPE != "ASYNC") && (SRTYPE != "SYNC")) begin
       $display("Attribute Syntax Error : The attribute SRTYPE on IDDR instance %m is set to %s.  Legal values for this attribute are ASYNC or SYNC.", SRTYPE);
       #1 $finish;
   end

    end // initial begin
    
         
    always @(gsr_in or r_in or s_in) begin
   if (gsr_in == 1'b1) begin
       assign q1_out_int = INIT_Q1;
       assign q1_out_pipelined = INIT_Q1;
       assign q2_out_same_edge_int = INIT_Q2;
       assign q2_out_int = INIT_Q2;
   end
   else if (gsr_in == 1'b0) begin
       if (r_in == 1'b1 && SRTYPE == "ASYNC") begin
      assign q1_out_int = 1'b0;
      assign q1_out_pipelined = 1'b0;
      assign q2_out_same_edge_int = 1'b0;
      assign q2_out_int = 1'b0;
       end
            else if (r_in == 1'b0 && s_in == 1'b1 && SRTYPE == "ASYNC") begin
      assign q1_out_int = 1'b1;
      assign q1_out_pipelined = 1'b1;
      assign q2_out_same_edge_int = 1'b1;
      assign q2_out_int = 1'b1;
       end
       else if ((r_in == 1'b1 || s_in == 1'b1) && SRTYPE == "SYNC") begin
      deassign q1_out_int;
      deassign q1_out_pipelined;
      deassign q2_out_same_edge_int;
      deassign q2_out_int;
       end       
       else if (r_in == 1'b0 && s_in == 1'b0) begin
      deassign q1_out_int;
      deassign q1_out_pipelined;
      deassign q2_out_same_edge_int;
      deassign q2_out_int;
       end
   end // if (gsr_in == 1'b0)
    end // always @ (gsr_in or r_in or s_in)
    
       
    always @(posedge c_in) begin
    if (r_in == 1'b1) begin
       q1_out_int <= 1'b0;
       q1_out_pipelined <= 1'b0;
       q2_out_same_edge_int <= 1'b0;
   end
   else if (r_in == 1'b0 && s_in == 1'b1) begin
       q1_out_int <= 1'b1;
       q1_out_pipelined <= 1'b1;
       q2_out_same_edge_int <= 1'b1;
   end
   else if (ce_in == 1'b1 && r_in == 1'b0 && s_in == 1'b0) begin
            q1_out_int <= d_in;
       q1_out_pipelined <= q1_out_int;
       q2_out_same_edge_int <= q2_out_int;
   end
    end // always @ (posedge c_in)
    
   
    always @(negedge c_in) begin
   if (r_in == 1'b1)
       q2_out_int <= 1'b0;
   else if (r_in == 1'b0 && s_in == 1'b1)
       q2_out_int <= 1'b1;
   else if (ce_in == 1'b1 && r_in == 1'b0 && s_in == 1'b0)
       q2_out_int <= d_in;
    end
    
    
    always @(c_in or q1_out_int or q2_out_int or q2_out_same_edge_int or q1_out_pipelined) begin
   case (DDR_CLK_EDGE)
       "OPPOSITE_EDGE" : begin
                        q1_out <= q1_out_int;
                        q2_out <= q2_out_int;
                         end
       "SAME_EDGE" : begin
                         q1_out <= q1_out_int;
                         q2_out <= q2_out_same_edge_int;
                     end
       "SAME_EDGE_PIPELINED" : begin
                              q1_out <= q1_out_pipelined;
                                     q2_out <= q2_out_same_edge_int;
                               end
       default : begin
                       $display("Attribute Syntax Error : The attribute DDR_CLK_EDGE on IDDR instance %m is set to %s.  Legal values for this attribute are OPPOSITE_EDGE, SAME_EDGE or SAME_EDGE_PIPELINED.", DDR_CLK_EDGE);
                $finish;
       end
   endcase // case(DDR_CLK_EDGE)
    end // always @ (q1_out_int or q2_out_int or q2_out_same_edge_int or q1_out_pipelined or q2_out_pipelined)
    

`ifndef XIL_TIMING

    assign delay_c =  C;
    assign delay_ce = CE;
    assign delay_d =  D;
    assign delay_r = R;
    assign delay_s = S;

`endif
    assign c_in = IS_C_INVERTED ^ delay_c;
    assign ce_in = delay_ce;
    assign d_in = IS_D_INVERTED ^ delay_d;
    assign r_in = delay_r;
    assign s_in = delay_s;
 
    
//*** Timing Checks Start here

`ifdef XIL_TIMING
    
    always @(notifier or notifier1x) begin
   q1_out <= 1'bx;
    end
    
    always @(notifier or notifier2x) begin
   q2_out <= 1'bx;
    end

`endif
    
`ifdef XIL_TIMING
   wire c_en_n;
   wire c_en_p;
   wire ce_c_enable1_n,d_c_enable1_n,r_c_enable1_n,s_c_enable1_n;
   wire ce_c_enable1_p,d_c_enable1_p,r_c_enable1_p,s_c_enable1_p;
   assign c_en_n = IS_C_INVERTED;
   assign c_en_p = ~IS_C_INVERTED;
   assign ce_c_enable1_n = ce_c_enable1 && c_en_n;
   assign ce_c_enable1_p = ce_c_enable1 && c_en_p;
   assign d_c_enable1_n = d_c_enable1 && c_en_n;
   assign d_c_enable1_p = d_c_enable1 && c_en_p;
   assign r_c_enable1_n = r_c_enable1 && c_en_n;
   assign r_c_enable1_p = r_c_enable1 && c_en_p;
   assign s_c_enable1_p = s_c_enable1 && c_en_p;
   assign s_c_enable1_n = s_c_enable1 && c_en_n;
`endif

    specify
   
   (C => Q1) = (100:100:100, 100:100:100);
   (C => Q2) = (100:100:100, 100:100:100);
   (posedge R => (Q1 +: 0)) = (0:0:0, 0:0:0);
   (posedge R => (Q2 +: 0)) = (0:0:0, 0:0:0);
   (posedge S => (Q1 +: 0)) = (0:0:0, 0:0:0);
   (posedge S => (Q2 +: 0)) = (0:0:0, 0:0:0);
`ifdef XIL_TIMING
    (R => Q1) = (0:0:0, 0:0:0);
   (R => Q2) = (0:0:0, 0:0:0);
   (S => Q1) = (0:0:0, 0:0:0);
   (S => Q2) = (0:0:0, 0:0:0);

   $period (negedge C, 0:0:0, notifier);
   $period (posedge C, 0:0:0, notifier);
   $recrem (negedge R, negedge C, 0:0:0, 0:0:0, notifier2, c_en_n, c_en_n);
   $recrem (negedge R, posedge C, 0:0:0, 0:0:0, notifier1, c_en_p, c_en_p);
   $recrem (negedge S, negedge C, 0:0:0, 0:0:0, notifier2, c_en_n, c_en_n);
   $recrem (negedge S, posedge C, 0:0:0, 0:0:0, notifier1, c_en_p, c_en_p);
   $recrem ( posedge R, negedge C, 0:0:0, 0:0:0, notifier2, c_en_n, c_en_n);
   $recrem ( posedge R, posedge C, 0:0:0, 0:0:0, notifier1, c_en_p, c_en_p);
   $recrem ( posedge S, negedge C, 0:0:0, 0:0:0, notifier2, c_en_n, c_en_n);
   $recrem ( posedge S, posedge C, 0:0:0, 0:0:0, notifier1, c_en_p, c_en_p);
   $setuphold (negedge C, negedge CE &&& (ce_c_enable1_n!=0), 0:0:0, 0:0:0, notifier2, , , delay_c, delay_ce);
   $setuphold (negedge C, negedge D  &&& (d_c_enable1_n!=0),  0:0:0, 0:0:0, notifier2, , , delay_c, delay_d);
   $setuphold (negedge C, negedge R  &&& (r_c_enable1_n!=0),  0:0:0, 0:0:0, notifier2, , , delay_c, delay_r);
   $setuphold (negedge C, negedge S  &&& (s_c_enable1_n!=0),  0:0:0, 0:0:0, notifier2, , , delay_c, delay_s);
   $setuphold (negedge C, posedge CE &&& (ce_c_enable1_n!=0), 0:0:0, 0:0:0, notifier2, , , delay_c, delay_ce);
   $setuphold (negedge C, posedge D  &&& (d_c_enable1_n!=0),  0:0:0, 0:0:0, notifier2, , , delay_c, delay_d);
   $setuphold (negedge C, posedge R  &&& (r_c_enable1_n!=0),  0:0:0, 0:0:0, notifier2, , , delay_c, delay_r);
   $setuphold (negedge C, posedge S  &&& (s_c_enable1_n!=0),  0:0:0, 0:0:0, notifier2, , , delay_c, delay_s);
   $setuphold (posedge C, negedge CE &&& (ce_c_enable1_p!=0), 0:0:0, 0:0:0, notifier1, , , delay_c, delay_ce);
   $setuphold (posedge C, negedge D  &&& (d_c_enable1_p!=0),  0:0:0, 0:0:0, notifier1, , , delay_c, delay_d);
   $setuphold (posedge C, negedge R  &&& (r_c_enable1_p!=0),  0:0:0, 0:0:0, notifier1, , , delay_c, delay_r);
   $setuphold (posedge C, negedge S  &&& (s_c_enable1_p!=0),  0:0:0, 0:0:0, notifier1, , , delay_c, delay_s);
   $setuphold (posedge C, posedge CE &&& (ce_c_enable1_p!=0), 0:0:0, 0:0:0, notifier1, , , delay_c, delay_ce);
   $setuphold (posedge C, posedge D  &&& (d_c_enable1_p!=0),  0:0:0, 0:0:0, notifier1, , , delay_c, delay_d);
   $setuphold (posedge C, posedge R  &&& (r_c_enable1_p!=0),  0:0:0, 0:0:0, notifier1, , , delay_c, delay_r);
   $setuphold (posedge C, posedge S  &&& (s_c_enable1_p!=0),  0:0:0, 0:0:0, notifier1, , , delay_c, delay_s);
   $width (negedge C, 0:0:0, 0, notifier);
   $width (negedge R, 0:0:0, 0, notifier);
   $width (negedge S, 0:0:0, 0, notifier);
   $width (posedge C, 0:0:0, 0, notifier);
   $width (posedge R, 0:0:0, 0, notifier);
   $width (posedge S, 0:0:0, 0, notifier);

`endif

   specparam PATHPULSE$ = 0;
   
    endspecify


endmodule // IDDR

`endcelldefine


///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2005 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 10.1
//  \   \         Description : Xilinx Unified Simulation Library Component
//  /   /                  Dual Data Rate Output D Flip-Flop
// /___/   /\     Filename : ODDR.v
// \   \  /  \    
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    03/11/05 - Added LOC parameter, removed GSR ports and initialized outputs.
//    05/29/07 - Added wire declaration for internal signals
//    04/17/08 - CR 468871 Negative SetupHold fix
//    05/12/08 - CR 455447 add XON MSGON property to support async reg
//    12/03/08 - CR 498674 added pulldown on R/S.
//    07/28/09 - CR 527698 According to holistic, CE has to be high for both rise/fall CLK
//             - If CE is low on the rising edge, it has an effect of no change in the falling CLK.
//    06/23/10 - CR 566394 Removed extra recrem checks
//    12/13/11 - Added `celldefine and `endcelldefine (CR 524859).
//    04/13/12 - CR 591320 fixed SU/H checks in OPPOSITE edge mode.
//    10/22/14 - Added #1 to $finish (CR 808642).
// End Revision

`timescale 1 ps / 1 ps

`celldefine

module ODDR (Q, C, CE, D1, D2, R, S);
    
    output Q;
    
    input C;
    input CE;
    input D1;
    input D2;    
    input R;
    input S;

    parameter DDR_CLK_EDGE = "OPPOSITE_EDGE";    
    parameter INIT = 1'b0;
    parameter [0:0] IS_C_INVERTED = 1'b0;
    parameter [0:0] IS_D1_INVERTED = 1'b0;
    parameter [0:0] IS_D2_INVERTED = 1'b0;

    parameter SRTYPE = "SYNC";
`ifdef XIL_TIMING
    parameter LOC = "UNPLACED";
    parameter MSGON = "TRUE";
    parameter XON = "TRUE";
`endif

    localparam MODULE_NAME = "ODDR";

    pulldown P1 (R);
    pulldown P2 (S);

    reg q_out = INIT, qd2_posedge_int;    
`ifdef XIL_TIMING
    reg notifier;
    wire notifierx;
`endif
    tri0 GSR = glbl.GSR;
    
    wire c_in,delay_c;
    wire ce_in,delay_ce;
    wire d1_in,delay_d1;
    wire d2_in,delay_d2;
    wire gsr_in;
    wire r_in,delay_r;
    wire s_in,delay_s;

    assign gsr_in = GSR;
    assign Q = q_out;

`ifdef XIL_TIMING
   
    wire nr, ns, ngsr;
    wire ce_c_enable, d_c_enable, r_c_enable, s_c_enable; 
    wire ce_c_enable1, d1_c_enable1, d2_c_enable1, d2_c_enable2, r_c_enable1, s_c_enable1;

    not (nr, R);
    not (ns, S);
    not (ngsr, GSR);

    and (ce_c_enable, ngsr, nr, ns);
    and (d_c_enable, ngsr, nr, ns, CE);
    and (s_c_enable, ngsr, nr);

    assign notifierx = (XON == "FALSE") ?  1'bx : notifier;

    assign ce_c_enable1 = (MSGON =="FALSE") ? 1'b0 : ce_c_enable;
    assign d1_c_enable1 = (MSGON =="FALSE") ? 1'b0 : d_c_enable;
    assign d2_c_enable1 = ((MSGON =="FALSE") && (DDR_CLK_EDGE == "OPPOSITE_EDGE")) ? 1'b0 : d_c_enable; // SAME_EDGE case, D2 to posedge C
    assign d2_c_enable2 = ((MSGON =="FALSE") && (DDR_CLK_EDGE == "SAME_EDGE")) ? 1'b0 : d_c_enable; // OPPOSITE_EDGE case, D2 to negedge C
    assign r_c_enable1 = (MSGON =="FALSE") ? 1'b0 : ngsr;
    assign s_c_enable1 = (MSGON =="FALSE") ? 1'b0 : s_c_enable;

`endif

    initial begin

   if ((INIT != 0) && (INIT != 1)) begin
       $display("Attribute Syntax Error : The attribute INIT on %s instance %m is set to %d.  Legal values for this attribute are 0 or 1.", MODULE_NAME, INIT);
       #1 $finish;
   end
   
       if ((DDR_CLK_EDGE != "OPPOSITE_EDGE") && (DDR_CLK_EDGE != "SAME_EDGE")) begin
       $display("Attribute Syntax Error : The attribute DDR_CLK_EDGE on %s instance %m is set to %s.  Legal values for this attribute are OPPOSITE_EDGE or SAME_EDGE.", MODULE_NAME, DDR_CLK_EDGE);
       #1 $finish;
   end
   
   if ((SRTYPE != "ASYNC") && (SRTYPE != "SYNC")) begin
       $display("Attribute Syntax Error : The attribute SRTYPE on %s instance %m is set to %s.  Legal values for this attribute are ASYNC or SYNC.", MODULE_NAME, SRTYPE);
       #1 $finish;
   end

    end // initial begin
    

    always @(gsr_in or r_in or s_in) begin
   if (gsr_in == 1'b1) begin
       assign q_out = INIT;
       assign qd2_posedge_int = INIT;
   end
   else if (gsr_in == 1'b0) begin
       if (r_in == 1'b1 && SRTYPE == "ASYNC") begin
      assign q_out = 1'b0;
      assign qd2_posedge_int = 1'b0;
       end
       else if (r_in == 1'b0 && s_in == 1'b1 && SRTYPE == "ASYNC") begin
      assign q_out = 1'b1;
      assign qd2_posedge_int = 1'b1;
       end
       else if ((r_in == 1'b1 || s_in == 1'b1) && SRTYPE == "SYNC") begin
      deassign q_out;
      deassign qd2_posedge_int;
       end       
       else if (r_in == 1'b0 && s_in == 1'b0) begin
      deassign q_out;
      deassign qd2_posedge_int;
       end
   end // if (gsr_in == 1'b0)
    end // always @ (gsr_in or r_in or s_in)

       
    always @(posedge c_in) begin
    if (r_in == 1'b1) begin
       q_out <= 1'b0;
       qd2_posedge_int <= 1'b0;
   end
   else if (r_in == 1'b0 && s_in == 1'b1) begin
       q_out <= 1'b1;
       qd2_posedge_int <= 1'b1;
   end
   else if (ce_in == 1'b1 && r_in == 1'b0 && s_in == 1'b0) begin
       q_out <= d1_in;
       qd2_posedge_int <= d2_in;
   end
// CR 527698 
   else if (ce_in == 1'b0 && r_in == 1'b0 && s_in == 1'b0) begin
       qd2_posedge_int <= q_out;
   end
    end // always @ (posedge c_in)
    
   
    always @(negedge c_in) begin
   if (r_in == 1'b1)
       q_out <= 1'b0;
   else if (r_in == 1'b0 && s_in == 1'b1)
       q_out <= 1'b1;
   else if (ce_in == 1'b1 && r_in == 1'b0 && s_in == 1'b0) begin
       if (DDR_CLK_EDGE == "SAME_EDGE")
      q_out <= qd2_posedge_int;
       else if (DDR_CLK_EDGE == "OPPOSITE_EDGE")
      q_out <= d2_in;
   end
    end // always @ (negedge c_in)

`ifndef XIL_TIMING

    assign delay_c = C;
    assign delay_ce = CE;
    assign delay_d1 =  D1;
    assign delay_d2 =  D2;
    assign delay_r = R;
    assign delay_s = S;

`endif
    assign c_in = IS_C_INVERTED ^ delay_c;
    assign ce_in = delay_ce;
    assign d1_in = IS_D1_INVERTED ^ delay_d1;
    assign d2_in = IS_D2_INVERTED ^ delay_d2;
    assign r_in = delay_r;
    assign s_in = delay_s;


//*** Timing Checks Start here

`ifdef XIL_TIMING

   wire c_en_n;
   wire c_en_p;
   wire ce_c_enable1_n,d1_c_enable1_n,d2_c_enable2_n,r_c_enable1_n,s_c_enable1_n;
   wire ce_c_enable1_p,d1_c_enable1_p,d2_c_enable2_p,r_c_enable1_p,s_c_enable1_p;
   assign c_en_n = IS_C_INVERTED;
   assign c_en_p = ~IS_C_INVERTED;
   assign ce_c_enable1_n = ce_c_enable1 && c_en_n;
   assign ce_c_enable1_p = ce_c_enable1 && c_en_p;
   assign d1_c_enable1_n = d1_c_enable1 && c_en_n;
   assign d1_c_enable1_p = d1_c_enable1 && c_en_p;
   assign d2_c_enable2_n = d2_c_enable2 && c_en_n;
   assign d2_c_enable2_p = d2_c_enable2 && c_en_p;
   assign r_c_enable1_n = r_c_enable1 && c_en_n;
   assign r_c_enable1_p = r_c_enable1 && c_en_p;
   assign s_c_enable1_p = s_c_enable1 && c_en_p;
   assign s_c_enable1_n = s_c_enable1 && c_en_n;

    always @(notifierx) begin
   q_out <= 1'bx;
    end

`endif

   specify

   (C => Q) = (100:100:100, 100:100:100);
    (posedge R => (Q +: 0)) = (0:0:0, 0:0:0);
    (posedge S => (Q +: 0)) = (0:0:0, 0:0:0);

`ifdef XIL_TIMING
   (R => Q) = (0:0:0, 0:0:0);
   (S => Q) = (0:0:0, 0:0:0);
   
   $period (negedge C, 0:0:0, notifier);
   $period (posedge C, 0:0:0, notifier);
   $recrem (negedge R, negedge C, 0:0:0, 0:0:0, notifier,c_en_n,c_en_n);
   $recrem (negedge R, posedge C, 0:0:0, 0:0:0, notifier,c_en_p,c_en_p);
   $recrem (negedge S, negedge C, 0:0:0, 0:0:0, notifier,c_en_n,c_en_n);
   $recrem (negedge S, posedge C, 0:0:0, 0:0:0, notifier,c_en_p,c_en_p);
   $recrem ( posedge R, negedge C, 0:0:0, 0:0:0, notifier,c_en_n,c_en_n);
   $recrem ( posedge R, posedge C, 0:0:0, 0:0:0, notifier,c_en_p,c_en_p);
   $recrem ( posedge S, negedge C, 0:0:0, 0:0:0, notifier,c_en_n,c_en_n);
   $recrem ( posedge S, posedge C, 0:0:0, 0:0:0, notifier,c_en_p,c_en_p);
   $setuphold (negedge C, negedge CE &&& (ce_c_enable1_n!=0), 0:0:0, 0:0:0, notifier, , , delay_c, delay_ce);
   $setuphold (negedge C, negedge D1 &&& (d1_c_enable1_n!=0),  0:0:0, 0:0:0, notifier, , , delay_c, delay_d1);
   $setuphold (negedge C, negedge D2 &&& (d2_c_enable2_n!=0),  0:0:0, 0:0:0, notifier, , , delay_c, delay_d2);
   $setuphold (negedge C, negedge R  &&& (r_c_enable1_n!=0),  0:0:0, 0:0:0,  notifier, , , delay_c, delay_r);
   $setuphold (negedge C, negedge S  &&& (r_c_enable1_n!=0),  0:0:0, 0:0:0,  notifier, , , delay_c, delay_s);
   $setuphold (negedge C, posedge CE &&& (ce_c_enable1_n!=0), 0:0:0, 0:0:0, notifier, , , delay_c, delay_ce);
   $setuphold (negedge C, posedge D1 &&& (d1_c_enable1_n!=0),  0:0:0, 0:0:0, notifier, , , delay_c, delay_d1);
   $setuphold (negedge C, posedge D2 &&& (d2_c_enable2_n!=0),  0:0:0, 0:0:0, notifier, , , delay_c, delay_d2);
   $setuphold (negedge C, posedge R  &&& (r_c_enable1_n!=0),  0:0:0, 0:0:0,  notifier, , , delay_c, delay_r);
   $setuphold (negedge C, posedge S  &&& (r_c_enable1_n!=0),  0:0:0, 0:0:0,  notifier, , , delay_c, delay_s);
   $setuphold (posedge C, negedge CE &&& (ce_c_enable1_p!=0), 0:0:0, 0:0:0, notifier, , , delay_c, delay_ce);
   $setuphold (posedge C, negedge D1 &&& (d1_c_enable1_p!=0),  0:0:0, 0:0:0, notifier, , , delay_c, delay_d1);
   $setuphold (posedge C, negedge D2 &&& (d2_c_enable2_p!=0),  0:0:0, 0:0:0, notifier, , , delay_c, delay_d2);
   $setuphold (posedge C, negedge R  &&& (r_c_enable1_p!=0),  0:0:0, 0:0:0,  notifier, , , delay_c, delay_r);
   $setuphold (posedge C, negedge S  &&& (r_c_enable1_p!=0),  0:0:0, 0:0:0,  notifier, , , delay_c, delay_s);
   $setuphold (posedge C, posedge CE &&& (ce_c_enable1_p!=0), 0:0:0, 0:0:0, notifier, , , delay_c, delay_ce);
   $setuphold (posedge C, posedge D1 &&& (d1_c_enable1_p!=0),  0:0:0, 0:0:0, notifier, , , delay_c, delay_d1);
   $setuphold (posedge C, posedge D2 &&& (d2_c_enable2_p!=0),  0:0:0, 0:0:0, notifier, , , delay_c, delay_d2);
   $setuphold (posedge C, posedge R  &&& (r_c_enable1_p!=0),  0:0:0, 0:0:0,  notifier, , , delay_c, delay_r);
   $setuphold (posedge C, posedge S  &&& (r_c_enable1_p!=0),  0:0:0, 0:0:0,  notifier, , , delay_c, delay_s);
   $width (negedge C, 0:0:0, 0, notifier);
   $width (negedge R, 0:0:0, 0, notifier);
   $width (negedge S, 0:0:0, 0, notifier);
   $width (posedge C, 0:0:0, 0, notifier);
   $width (posedge R, 0:0:0, 0, notifier);
   $width (posedge S, 0:0:0, 0, notifier);

`endif
   specparam PATHPULSE$ = 0;
   
   endspecify

endmodule // ODDR

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
//  /   /                  1-Bit Look-Up Table
// /___/   /\     Filename : LUT1.v
// \   \  /  \
//  \___\/\___\
//
///////////////////////////////////////////////////////////////////////////////
//  Revision:
//    05/12/11 - Initial version.
//    12/13/11 - 524859 - Added `celldefine and `endcelldefine
//    09/12/16 - ANSI ports, speed improvements
//  End Revision:
///////////////////////////////////////////////////////////////////////////////

`timescale 1 ps/1 ps

`celldefine

module LUT1 #(
`ifdef XIL_TIMING
  parameter LOC = "UNPLACED",
`endif
  parameter [1:0] INIT = 2'h0
)(
  output O,

  input I0
);

// define constants
  localparam MODULE_NAME = "LUT1";

  reg trig_attr = 1'b0;
// include dynamic registers - XILINX test only
`ifdef XIL_DR
  `include "LUT1_dr.v"
`else
  reg [1:0] INIT_REG = INIT;
`endif

  x_lut1_mux2 (O, INIT_REG[1], INIT_REG[0], I0);

`ifdef XIL_TIMING
  specify
	(I0 => O) = (0:0:0, 0:0:0);
	specparam PATHPULSE$ = 0;
  endspecify
`endif

endmodule

`endcelldefine

primitive x_lut1_mux2 (o, d1, d0, s0);

  output o;
  input  d1, d0;
  input  s0;

  table

    //         d1  d0      s0 : o;

               ?   1       0  : 1;
               ?   0       0  : 0;
               1   ?       1  : 1;
               0   ?       1  : 0;

               0   0       x  : 0;
               1   1       x  : 1;

  endtable

endprimitive

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
//  /   /                  Primary Global Buffer for Driving Clocks or Long Lines
// /___/   /\     Filename : BUFGP.v
// \   \  /  \    Timestamp : Thu Mar 25 16:42:14 PST 2004
//  \___\/\___\
//
// Revision:
//    03/23/04 - Initial version.
//    05/23/07 - Changed timescale to 1 ps / 1 ps.
//    12/13/11 - Added `celldefine and `endcelldefine (CR 524859).
// End Revision

`timescale  1 ps / 1 ps


`celldefine

module BUFGP (O, I);


`ifdef XIL_TIMING

    parameter LOC = " UNPLACED";

`endif


    output O;
    input  I;

    buf B1 (O, I);

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
//  /   /                  3-Bit Look-Up Table
// /___/   /\     Filename : LUT3.v
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

module LUT3 #(
`ifdef XIL_TIMING
  parameter LOC = "UNPLACED",
`endif
  parameter [7:0] INIT = 8'h00
)(
  output O,

  input I0,
  input I1,
  input I2
);

// define constants
  localparam MODULE_NAME = "LUT3";

  reg trig_attr = 1'b0;
// include dynamic registers - XILINX test only
`ifdef XIL_DR
  `include "LUT3_dr.v"
`else
  reg [7:0] INIT_REG = INIT;
`endif

  x_lut3_mux8 (O, INIT_REG[7], INIT_REG[6], INIT_REG[5], INIT_REG[4], INIT_REG[3], INIT_REG[2], INIT_REG[1], INIT_REG[0], I2, I1, I0);

`ifdef XIL_TIMING
  specify
	(I0 => O) = (0:0:0, 0:0:0);
	(I1 => O) = (0:0:0, 0:0:0);
	(I2 => O) = (0:0:0, 0:0:0);
	specparam PATHPULSE$ = 0;
  endspecify
`endif

endmodule

`endcelldefine

primitive x_lut3_mux8 (o, d7, d6, d5, d4, d3, d2, d1, d0, s2, s1, s0);

  output o;
  input d7, d6, d5, d4, d3, d2, d1, d0;
  input s2, s1, s0;

  table

    // d7  d6  d5  d4  d3  d2  d1  d0  s2  s1  s0 : o;

       ?   ?   ?   ?   ?   ?   ?   1   0   0   0  : 1;
       ?   ?   ?   ?   ?   ?   ?   0   0   0   0  : 0;
       ?   ?   ?   ?   ?   ?   1   ?   0   0   1  : 1;
       ?   ?   ?   ?   ?   ?   0   ?   0   0   1  : 0;
       ?   ?   ?   ?   ?   1   ?   ?   0   1   0  : 1;
       ?   ?   ?   ?   ?   0   ?   ?   0   1   0  : 0;
       ?   ?   ?   ?   1   ?   ?   ?   0   1   1  : 1;
       ?   ?   ?   ?   0   ?   ?   ?   0   1   1  : 0;
       ?   ?   ?   1   ?   ?   ?   ?   1   0   0  : 1;
       ?   ?   ?   0   ?   ?   ?   ?   1   0   0  : 0;
       ?   ?   1   ?   ?   ?   ?   ?   1   0   1  : 1;
       ?   ?   0   ?   ?   ?   ?   ?   1   0   1  : 0;
       ?   1   ?   ?   ?   ?   ?   ?   1   1   0  : 1;
       ?   0   ?   ?   ?   ?   ?   ?   1   1   0  : 0;
       1   ?   ?   ?   ?   ?   ?   ?   1   1   1  : 1;
       0   ?   ?   ?   ?   ?   ?   ?   1   1   1  : 0;

       ?   ?   ?   ?   ?   ?   0   0   0   0   x  : 0;
       ?   ?   ?   ?   ?   ?   1   1   0   0   x  : 1;
       ?   ?   ?   ?   0   0   ?   ?   0   1   x  : 0;
       ?   ?   ?   ?   1   1   ?   ?   0   1   x  : 1;
       ?   ?   0   0   ?   ?   ?   ?   1   0   x  : 0;
       ?   ?   1   1   ?   ?   ?   ?   1   0   x  : 1;
       0   0   ?   ?   ?   ?   ?   ?   1   1   x  : 0;
       1   1   ?   ?   ?   ?   ?   ?   1   1   x  : 1;

       ?   ?   ?   ?   ?   0   ?   0   0   x   0  : 0;
       ?   ?   ?   ?   ?   1   ?   1   0   x   0  : 1;
       ?   ?   ?   ?   0   ?   0   ?   0   x   1  : 0;
       ?   ?   ?   ?   1   ?   1   ?   0   x   1  : 1;
       ?   0   ?   0   ?   ?   ?   ?   1   x   0  : 0;
       ?   1   ?   1   ?   ?   ?   ?   1   x   0  : 1;
       0   ?   0   ?   ?   ?   ?   ?   1   x   1  : 0;
       1   ?   1   ?   ?   ?   ?   ?   1   x   1  : 1;

       ?   ?   ?   0   ?   ?   ?   0   x   0   0  : 0;
       ?   ?   ?   1   ?   ?   ?   1   x   0   0  : 1;
       ?   ?   0   ?   ?   ?   0   ?   x   0   1  : 0;
       ?   ?   1   ?   ?   ?   1   ?   x   0   1  : 1;
       ?   0   ?   ?   ?   0   ?   ?   x   1   0  : 0;
       ?   1   ?   ?   ?   1   ?   ?   x   1   0  : 1;
       0   ?   ?   ?   0   ?   ?   ?   x   1   1  : 0;
       1   ?   ?   ?   1   ?   ?   ?   x   1   1  : 1;

       ?   ?   ?   ?   0   0   0   0   0   x   x  : 0;
       ?   ?   ?   ?   1   1   1   1   0   x   x  : 1;
       0   0   0   0   ?   ?   ?   ?   1   x   x  : 0;
       1   1   1   1   ?   ?   ?   ?   1   x   x  : 1;

       ?   ?   0   0   ?   ?   0   0   x   0   x  : 0;
       ?   ?   1   1   ?   ?   1   1   x   0   x  : 1;
       0   0   ?   ?   0   0   ?   ?   x   1   x  : 0;
       1   1   ?   ?   1   1   ?   ?   x   1   x  : 1;

       ?   0   ?   0   ?   0   ?   0   x   x   0  : 0;
       ?   1   ?   1   ?   1   ?   1   x   x   0  : 1;
       0   ?   0   ?   0   ?   0   ?   x   x   1  : 0;
       1   ?   1   ?   1   ?   1   ?   x   x   1  : 1;

       0   0   0   0   0   0   0   0   x   x   x  : 0;
       1   1   1   1   1   1   1   1   x   x   x  : 1;

  endtable

endprimitive

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


///////////////////////////////////////////////////////////////////////////////
// Copyright (c) 1995/2004 Xilinx, Inc.
// All Right Reserved.
///////////////////////////////////////////////////////////////////////////////
//   ____  ____
//  /   /\/   /
// /___/  \  /    Vendor : Xilinx
// \   \   \/     Version : 12.0
//  \   \         Description : Xilinx Functional and Timing Simulation Library Component
//  /   /                  Input Fixed or Variable Delay Element.
// /___/   /\     Filename : IDELAYE2.v
// \   \  /  \    Timestamp : Sat Sep 19 14:17:57 PDT 2009
//  \___\/\___\
//
// Revision:
//    09/19/09 - Initial version.
//    12/13/11 - Added `celldefine and `endcelldefine (CR 524859).
//    10/22/14 - Added #1 to $finish (CR 808642).
// End Revision

`timescale  1 ps / 1 ps

`celldefine

module IDELAYE2 (CNTVALUEOUT, DATAOUT, C, CE, CINVCTRL, CNTVALUEIN, DATAIN, IDATAIN, INC, LD, LDPIPEEN, REGRST);

    parameter CINVCTRL_SEL = "FALSE";
    parameter DELAY_SRC = "IDATAIN";
    parameter HIGH_PERFORMANCE_MODE    = "FALSE";
    parameter IDELAY_TYPE  = "FIXED";
    parameter integer IDELAY_VALUE = 0;
    parameter [0:0] IS_C_INVERTED = 1'b0;
    parameter [0:0] IS_DATAIN_INVERTED = 1'b0;
    parameter [0:0] IS_IDATAIN_INVERTED = 1'b0;
    parameter PIPE_SEL = "FALSE";
    parameter real REFCLK_FREQUENCY = 200.0;
    parameter SIGNAL_PATTERN    = "DATA";

`ifdef XIL_TIMING
    parameter LOC = "UNPLACED";
    parameter integer SIM_DELAY_D = 0;
    localparam DELAY_D = (IDELAY_TYPE == "VARIABLE") ? SIM_DELAY_D : 0;
`endif // ifdef XIL_TIMING

`ifndef XIL_TIMING
    integer DELAY_D=0;
`endif // ifndef XIL_TIMING

    output [4:0] CNTVALUEOUT;
    output DATAOUT;

    input C;
    input CE;
    input CINVCTRL;
    input [4:0] CNTVALUEIN;
    input DATAIN;
    input IDATAIN;
    input INC;
    input LD;
    input LDPIPEEN;
    input REGRST;


    tri0  GSR = glbl.GSR;
    real  CALC_TAPDELAY ; 
    real  INIT_DELAY;

//------------------- constants ------------------------------------

    localparam MAX_DELAY_COUNT = 31; 
    localparam MIN_DELAY_COUNT = 0; 

    localparam MAX_REFCLK_FREQUENCYL = 210.0;
    localparam MIN_REFCLK_FREQUENCYL = 190.0;

    localparam MAX_REFCLK_FREQUENCYH = 410.0;
    localparam MIN_REFCLK_FREQUENCYH = 290.0;


//------------------- variable declaration -------------------------

    integer idelay_count;
    integer CNTVALUEIN_INTEGER;
    reg [4:0] cntvalueout_pre;

    reg notifier;

    reg data_mux = 0;
    reg tap_out   = 0;
    reg DATAOUT_reg   = 0;

    wire delay_chain_0,  delay_chain_1,  delay_chain_2,  delay_chain_3,
         delay_chain_4,  delay_chain_5,  delay_chain_6,  delay_chain_7,
         delay_chain_8,  delay_chain_9,  delay_chain_10, delay_chain_11,
         delay_chain_12, delay_chain_13, delay_chain_14, delay_chain_15,
         delay_chain_16, delay_chain_17, delay_chain_18, delay_chain_19,
         delay_chain_20, delay_chain_21, delay_chain_22, delay_chain_23,
         delay_chain_24, delay_chain_25, delay_chain_26, delay_chain_27,
         delay_chain_28, delay_chain_29, delay_chain_30, delay_chain_31;

    reg  c_in;
    wire ce_in,delay_CE,delay_C;
    wire clkin_in;
    wire [4:0] cntvaluein_in,delay_CNTVALUEIN;
    wire datain_in,delay_DATAIN;
    wire gsr_in;
    wire idatain_in,delay_IDATAIN;
    wire inc_in,delay_INC;
    wire odatain_in;
    wire ld_in,delay_LD;
    wire t_in;
    wire cinvctrl_in,delay_CINVCTRL;
    wire ldpipeen_in,delay_LDPIPEEN;
    wire regrst_in,delay_REGRST;

    wire c_in_pre;

   reg [4:0] qcntvalueout_reg = 5'b0;
   reg [4:0] qcntvalueout_mux = 5'b0;


//----------------------------------------------------------------------
//-------------------------------  Output ------------------------------
//----------------------------------------------------------------------
// CR 587496
//    assign #INIT_DELAY DATAOUT = tap_out;
    always @(tap_out)
       DATAOUT_reg <= #INIT_DELAY tap_out;

    assign DATAOUT = DATAOUT_reg;

    assign CNTVALUEOUT = cntvalueout_pre;

`ifndef XIL_TIMING
//----------------------------------------------------------------------
//-------------------------------  Input -------------------------------
//----------------------------------------------------------------------
    assign delay_C = C;
    assign delay_CE = CE;
    assign delay_CNTVALUEIN = CNTVALUEIN;
    assign delay_INC = INC;
    assign delay_LD = LD;
    assign delay_LDPIPEEN = LDPIPEEN;
    assign delay_REGRST = REGRST;
`endif // ifndef XIL_TIMING
    assign delay_CINVCTRL = CINVCTRL;
    assign delay_DATAIN =  DATAIN;
    assign delay_IDATAIN =  IDATAIN;
    assign gsr_in = GSR;

    assign c_in_pre = delay_C ^ IS_C_INVERTED;
    assign ce_in = delay_CE;
    assign cntvaluein_in = delay_CNTVALUEIN;
    assign inc_in = delay_INC;
    assign ld_in = delay_LD;
    assign ldpipeen_in = delay_LDPIPEEN;
    assign regrst_in = delay_REGRST;
   assign cinvctrl_in = delay_CINVCTRL;
    assign datain_in = IS_DATAIN_INVERTED ^ delay_DATAIN;
    assign idatain_in = IS_IDATAIN_INVERTED ^ delay_IDATAIN;



//*** GLOBAL hidden GSR pin
    always @(gsr_in) begin
	if (gsr_in == 1'b1) begin
//   For simprims, the fixed/Default Delay values are taken from the sdf.
           // if (IDELAY_TYPE == "FIXED")
           //     assign idelay_count = 0;
           // else
           //     assign idelay_count = IDELAY_VALUE;
		case (IDELAY_TYPE)
                        "VAR_LOAD", "VAR_LOAD_PIPE": assign idelay_count = 0;
                        "FIXED", "VARIABLE" : assign idelay_count = IDELAY_VALUE;
                endcase
        end
	else if (gsr_in == 1'b0) begin
	    deassign idelay_count;
	end
    end


//------------------------------------------------------------
//---------------------   Initialization  --------------------
//------------------------------------------------------------

    initial begin

        //-------- CINVCTRL_SEL check

        case (CINVCTRL_SEL)
            "TRUE", "FALSE" : ;
            default : begin
               $display("Attribute Syntax Error : The attribute CINVCTRL_SEL on IDELAYE2 instance %m is set to %s.  Legal values for this attribute are TRUE or FALSE.",  CINVCTRL_SEL);
               #1 $finish;
            end
        endcase

        //-------- DELAY_SRC check

        if (DELAY_SRC != "DATAIN" && DELAY_SRC != "IDATAIN") begin
            $display("Attribute Syntax Error : The attribute DELAY_SRC on IDELAYE2 instance %m is set to %s.  Legal values for this attribute are DATAIN or IDATAIN", DELAY_SRC);
            #1 $finish;
        end



        //-------- HIGH_PERFORMANCE_MODE check

        case (HIGH_PERFORMANCE_MODE)
            "TRUE", "FALSE" : ;
            default : begin
               $display("Attribute Syntax Error : The attribute HIGH_PERFORMANCE_MODE on IDELAYE2 instance %m is set to %s.  Legal values for this attribute are TRUE or FALSE.",  HIGH_PERFORMANCE_MODE);
               #1 $finish;
            end
        endcase


        //-------- IDELAY_TYPE check

        if (IDELAY_TYPE != "FIXED" && IDELAY_TYPE != "VARIABLE" && IDELAY_TYPE != "VAR_LOAD" && IDELAY_TYPE != "VAR_LOAD_PIPE") begin

            $display("Attribute Syntax Error : The attribute IDELAY_TYPE on IDELAYE2 instance %m is set to %s.  Legal values for this attribute are FIXED, VARIABLE, VAR_LOAD or VAR_LOAD_PIPE", IDELAY_TYPE);
            #1 $finish;

        end


        //-------- IDELAY_VALUE check

        if (IDELAY_VALUE < MIN_DELAY_COUNT || IDELAY_VALUE > MAX_DELAY_COUNT) begin
            $display("Attribute Syntax Error : The attribute IDELAY_VALUE on IDELAYE2 instance %m is set to %d.  Legal values for this attribute are 0, 1, 2, 3, .... or 31", IDELAY_VALUE);
            #1 $finish;

        end

        //-------- PIPE_SEL check

        case (PIPE_SEL)
            "TRUE", "FALSE" : ;
            default : begin
               $display("Attribute Syntax Error : The attribute PIPE_SEL on IDELAYE2 instance %m is set to %s.  Legal values for this attribute are TRUE or FALSE.",  PIPE_SEL);
               #1 $finish;
            end
        endcase


        //-------- REFCLK_FREQUENCY check

        if ((REFCLK_FREQUENCY >= 190.0 && REFCLK_FREQUENCY <= 210.0) || 
	    (REFCLK_FREQUENCY >= 290.0 && REFCLK_FREQUENCY <= 310.0) || 
	    (REFCLK_FREQUENCY >=390.0 && REFCLK_FREQUENCY <= 410.0)) 
	      /*    */;
	else begin
            $display("Attribute Syntax Error : The attribute REFCLK_FREQUENCY on IDELAYE2 instance %m is set to %f.  Legal values for this attribute are either between 190.0 and 210.0, or between 290.0 and 310.0 or between 390.0 and 410.0", REFCLK_FREQUENCY);
            #1 $finish;
        end

        //-------- SIGNAL_PATTERN check

        case (SIGNAL_PATTERN)
            "CLOCK", "DATA" : ;
            default : begin
               $display("Attribute Syntax Error : The attribute SIGNAL_PATTERN on IDELAYE2 instance %m is set to %s.  Legal values for this attribute are DATA or CLOCK.",  SIGNAL_PATTERN);
               #1 $finish;
            end
        endcase


        //-------- CALC_TAPDELAY check

        INIT_DELAY = 600;

    end // initial begin

    // CALC_TAPDELAY value
    initial begin
        if ((REFCLK_FREQUENCY <= 410.0) && (REFCLK_FREQUENCY >= 390.0))
                begin
                        CALC_TAPDELAY = 39;
                end
        else if ((REFCLK_FREQUENCY <= 310.0) && (REFCLK_FREQUENCY >= 290.0))
	        begin
                        CALC_TAPDELAY = 52;
		end
	else
                begin
                        CALC_TAPDELAY = 78;
                end
    end

//----------------------------------------------------------------------
//------------------------ Dynamic clock inversion ---------------------
//----------------------------------------------------------------------

//    always @(c_in_pre or cinvctrl_in) begin
//        case (CINVCTRL_SEL)
//                "TRUE" : c_in = (cinvctrl_in ? ~c_in_pre : c_in_pre);
//                "FALSE" : c_in = c_in_pre;
//        endcase
//    end

   generate
      case (CINVCTRL_SEL)
         "TRUE"  : always @(c_in_pre or cinvctrl_in) c_in = (cinvctrl_in ? ~c_in_pre : c_in_pre);
         "FALSE" : always @(c_in_pre) c_in = c_in_pre;
      endcase
   endgenerate

//----------------------------------------------------------------------
//------------------------      CNTVALUEOUT        ---------------------
//----------------------------------------------------------------------
    always @(idelay_count) begin
//  Fixed CNTVALUEOUT for when in FIXED mode because of simprim. 
       if(IDELAY_TYPE != "FIXED")
           assign cntvalueout_pre = idelay_count;
       else
           assign cntvalueout_pre = IDELAY_VALUE;
    end

//----------------------------------------------------------------------
//--------------------------  CNTVALUEIN LOAD --------------------------
//----------------------------------------------------------------------
    always @(posedge c_in) begin
       if (regrst_in == 1'b1) 
              qcntvalueout_reg = 5'b0;
       else if (regrst_in == 1'b0 && ldpipeen_in == 1'b1) begin
              qcntvalueout_reg =  CNTVALUEIN_INTEGER;
       end 
    end  // always @(posedge c_in)

   generate
      case (PIPE_SEL)
         "TRUE"  : always @(qcntvalueout_reg) qcntvalueout_mux   <= qcntvalueout_reg;
         "FALSE" : always @(CNTVALUEIN_INTEGER) qcntvalueout_mux   <= CNTVALUEIN_INTEGER;
      endcase
    endgenerate

//----------------------------------------------------------------------
//--------------------------  IDELAY_COUNT  ----------------------------
//----------------------------------------------------------------------
    always @(posedge c_in) begin

        if (IDELAY_TYPE == "VARIABLE" | IDELAY_TYPE == "VAR_LOAD" | IDELAY_TYPE == "VAR_LOAD_PIPE") begin
            if (ld_in == 1'b1) begin
                case (IDELAY_TYPE)
                        "VARIABLE" : idelay_count = IDELAY_VALUE;
                        "VAR_LOAD", "VAR_LOAD_PIPE" : idelay_count = qcntvalueout_mux;
                endcase
            end
            else if (ld_in == 1'b0 && ce_in == 1'b1) begin
                if (inc_in == 1'b1) begin
                    case (IDELAY_TYPE)
                        "VARIABLE", "VAR_LOAD", "VAR_LOAD_PIPE" : begin
                                        if (idelay_count < MAX_DELAY_COUNT)
                                          idelay_count = idelay_count + 1;
                                        else if (idelay_count == MAX_DELAY_COUNT)
                                          idelay_count = MIN_DELAY_COUNT;
                                     end
                    endcase
                end
                else if (inc_in == 1'b0) begin
                    case (IDELAY_TYPE)
                        "VARIABLE", "VAR_LOAD", "VAR_LOAD_PIPE" : begin
                                        if (idelay_count >  MIN_DELAY_COUNT)
                                          idelay_count = idelay_count - 1;
                                        else if (idelay_count == MIN_DELAY_COUNT)
                                          idelay_count = MAX_DELAY_COUNT;
                                     end
                    endcase
                end
            end
        end //
    end // always @ (posedge c_in)
  
    always @(cntvaluein_in or gsr_in) begin
                case (cntvaluein_in)
                        5'b00000 : assign CNTVALUEIN_INTEGER = 0;
                        5'b00001 : assign CNTVALUEIN_INTEGER = 1;
                        5'b00010 : assign CNTVALUEIN_INTEGER = 2;
                        5'b00011 : assign CNTVALUEIN_INTEGER = 3;
                        5'b00100 : assign CNTVALUEIN_INTEGER = 4;
                        5'b00101 : assign CNTVALUEIN_INTEGER = 5;
                        5'b00110 : assign CNTVALUEIN_INTEGER = 6;
                        5'b00111 : assign CNTVALUEIN_INTEGER = 7;
                        5'b01000 : assign CNTVALUEIN_INTEGER = 8;
                        5'b01001 : assign CNTVALUEIN_INTEGER = 9;
                        5'b01010 : assign CNTVALUEIN_INTEGER = 10;
                        5'b01011 : assign CNTVALUEIN_INTEGER = 11;
                        5'b01100 : assign CNTVALUEIN_INTEGER = 12;
                        5'b01101 : assign CNTVALUEIN_INTEGER = 13;
                        5'b01110 : assign CNTVALUEIN_INTEGER = 14;
                        5'b01111 : assign CNTVALUEIN_INTEGER = 15;
                        5'b10000 : assign CNTVALUEIN_INTEGER = 16;
                        5'b10001 : assign CNTVALUEIN_INTEGER = 17;
                        5'b10010 : assign CNTVALUEIN_INTEGER = 18;
                        5'b10011 : assign CNTVALUEIN_INTEGER = 19;
                        5'b10100 : assign CNTVALUEIN_INTEGER = 20;
                        5'b10101 : assign CNTVALUEIN_INTEGER = 21;
                        5'b10110 : assign CNTVALUEIN_INTEGER = 22;
                        5'b10111 : assign CNTVALUEIN_INTEGER = 23;
                        5'b11000 : assign CNTVALUEIN_INTEGER = 24;
                        5'b11001 : assign CNTVALUEIN_INTEGER = 25;
                        5'b11010 : assign CNTVALUEIN_INTEGER = 26;
                        5'b11011 : assign CNTVALUEIN_INTEGER = 27;
                        5'b11100 : assign CNTVALUEIN_INTEGER = 28;
                        5'b11101 : assign CNTVALUEIN_INTEGER = 29;
                        5'b11110 : assign CNTVALUEIN_INTEGER = 30;
                        5'b11111 : assign CNTVALUEIN_INTEGER = 31;
                endcase
    end

 
//*********************************************************
//*** SELECT IDATA signal
//*********************************************************

    always @(datain_in or idatain_in) begin

        case (DELAY_SRC)

            "IDATAIN" : begin
                         data_mux <= idatain_in;
                        end
            "DATAIN" : begin
                         data_mux <= datain_in;
                       end
            default : begin
                          $display("Attribute Syntax Error : The attribute DELAY_SRC on X_IODELAYE2 instance %m is set to %s.  Legal values for this attribute are DATAIN or IDATAIN", DELAY_SRC);
                          $finish;
                      end

        endcase // case(DELAY_SRC)

    end // always @(datain_in or idatain_in)

//*********************************************************
//*** DELAY IDATA signal
//*********************************************************
    assign #(DELAY_D)     delay_chain_0  = data_mux;
    assign #CALC_TAPDELAY delay_chain_1  = delay_chain_0;
    assign #CALC_TAPDELAY delay_chain_2  = delay_chain_1;
    assign #CALC_TAPDELAY delay_chain_3  = delay_chain_2;
    assign #CALC_TAPDELAY delay_chain_4  = delay_chain_3;
    assign #CALC_TAPDELAY delay_chain_5  = delay_chain_4;
    assign #CALC_TAPDELAY delay_chain_6  = delay_chain_5;
    assign #CALC_TAPDELAY delay_chain_7  = delay_chain_6;
    assign #CALC_TAPDELAY delay_chain_8  = delay_chain_7;
    assign #CALC_TAPDELAY delay_chain_9  = delay_chain_8;
    assign #CALC_TAPDELAY delay_chain_10 = delay_chain_9;
    assign #CALC_TAPDELAY delay_chain_11 = delay_chain_10;
    assign #CALC_TAPDELAY delay_chain_12 = delay_chain_11;
    assign #CALC_TAPDELAY delay_chain_13 = delay_chain_12;
    assign #CALC_TAPDELAY delay_chain_14 = delay_chain_13;
    assign #CALC_TAPDELAY delay_chain_15 = delay_chain_14;
    assign #CALC_TAPDELAY delay_chain_16 = delay_chain_15;
    assign #CALC_TAPDELAY delay_chain_17 = delay_chain_16;
    assign #CALC_TAPDELAY delay_chain_18 = delay_chain_17;
    assign #CALC_TAPDELAY delay_chain_19 = delay_chain_18;
    assign #CALC_TAPDELAY delay_chain_20 = delay_chain_19;
    assign #CALC_TAPDELAY delay_chain_21 = delay_chain_20;
    assign #CALC_TAPDELAY delay_chain_22 = delay_chain_21;
    assign #CALC_TAPDELAY delay_chain_23 = delay_chain_22;
    assign #CALC_TAPDELAY delay_chain_24 = delay_chain_23;
    assign #CALC_TAPDELAY delay_chain_25 = delay_chain_24;
    assign #CALC_TAPDELAY delay_chain_26 = delay_chain_25;
    assign #CALC_TAPDELAY delay_chain_27 = delay_chain_26;
    assign #CALC_TAPDELAY delay_chain_28 = delay_chain_27;
    assign #CALC_TAPDELAY delay_chain_29 = delay_chain_28;
    assign #CALC_TAPDELAY delay_chain_30 = delay_chain_29;
    assign #CALC_TAPDELAY delay_chain_31 = delay_chain_30;

//*********************************************************
//*** assign delay
//*********************************************************
    always @(idelay_count) begin
        case (idelay_count)
            0:  assign tap_out = delay_chain_0;
            1:  assign tap_out = delay_chain_1;
            2:  assign tap_out = delay_chain_2;
            3:  assign tap_out = delay_chain_3;
            4:  assign tap_out = delay_chain_4;
            5:  assign tap_out = delay_chain_5;
            6:  assign tap_out = delay_chain_6;
            7:  assign tap_out = delay_chain_7;
            8:  assign tap_out = delay_chain_8;
            9:  assign tap_out = delay_chain_9;
            10: assign tap_out = delay_chain_10;
            11: assign tap_out = delay_chain_11;
            12: assign tap_out = delay_chain_12;
            13: assign tap_out = delay_chain_13;
            14: assign tap_out = delay_chain_14;
            15: assign tap_out = delay_chain_15;
            16: assign tap_out = delay_chain_16;
            17: assign tap_out = delay_chain_17;
            18: assign tap_out = delay_chain_18;
            19: assign tap_out = delay_chain_19;
            20: assign tap_out = delay_chain_20;
            21: assign tap_out = delay_chain_21;
            22: assign tap_out = delay_chain_22;
            23: assign tap_out = delay_chain_23;
            24: assign tap_out = delay_chain_24;
            25: assign tap_out = delay_chain_25;
            26: assign tap_out = delay_chain_26;
            27: assign tap_out = delay_chain_27;
            28: assign tap_out = delay_chain_28;
            29: assign tap_out = delay_chain_29;
            30: assign tap_out = delay_chain_30;
            31: assign tap_out = delay_chain_31;
            default:
                assign tap_out = delay_chain_0;
        endcase
    end // always @ (idelay_count)

`ifdef XIL_TIMING
   wire c_en_n;
   wire c_en_p;
   assign c_en_n = IS_C_INVERTED;
   assign c_en_p = ~IS_C_INVERTED;

   wire d_en;
   wire id_en;
   assign d_en = (idelay_count == 0) && (DELAY_SRC == "DATAIN");
   assign id_en = (idelay_count == 0) && (DELAY_SRC == "IDATAIN");
  
//*** Timing Checks Start here

    always @(notifier) begin
        tap_out <= 1'bx;
    end
`endif // ifdef XIL_TIMING


`ifdef XIL_TIMING
    specify

        ( C *> CNTVALUEOUT) = (0:0:0, 0:0:0);
        ( C => DATAOUT) = (0:0:0, 0:0:0);
        ( CINVCTRL *> CNTVALUEOUT) = (0:0:0, 0:0:0);
        ( CINVCTRL => DATAOUT) = (0:0:0, 0:0:0);
        if (d_en) ( DATAIN => DATAOUT) = (0:0:0, 0:0:0);
        if (id_en) ( IDATAIN => DATAOUT) = (0:0:0, 0:0:0);

        $period (negedge C, 0:0:0, notifier);
        $period (posedge C, 0:0:0, notifier);
 
        $setuphold (posedge C, posedge CE,  0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_CE);
        $setuphold (posedge C, negedge CE,  0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_CE);
        $setuphold (posedge C, posedge INC, 0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_INC);
        $setuphold (posedge C, negedge INC, 0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_INC);
        $setuphold (posedge C, posedge LD, 0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_LD);
        $setuphold (posedge C, negedge LD, 0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_LD);
        $setuphold (posedge C, posedge CNTVALUEIN, 0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_CNTVALUEIN);
        $setuphold (posedge C, negedge CNTVALUEIN, 0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_CNTVALUEIN);
        $setuphold (posedge C, posedge LDPIPEEN, 0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_LDPIPEEN);
        $setuphold (posedge C, negedge LDPIPEEN, 0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_LDPIPEEN);
        $setuphold (posedge C, posedge REGRST,  0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_REGRST);
        $setuphold (posedge C, negedge REGRST,  0:0:0, 0:0:0, notifier, c_en_p, c_en_p, delay_C, delay_REGRST);

        $setuphold (negedge C, posedge CE,  0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_CE);
        $setuphold (negedge C, negedge CE,  0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_CE);
        $setuphold (negedge C, posedge INC, 0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_INC);
        $setuphold (negedge C, negedge INC, 0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_INC);
        $setuphold (negedge C, posedge LD, 0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_LD);
        $setuphold (negedge C, negedge LD, 0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_LD);
        $setuphold (negedge C, posedge CNTVALUEIN, 0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_CNTVALUEIN);
        $setuphold (negedge C, negedge CNTVALUEIN, 0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_CNTVALUEIN);
        $setuphold (negedge C, posedge LDPIPEEN, 0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_LDPIPEEN);
        $setuphold (negedge C, negedge LDPIPEEN, 0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_LDPIPEEN);
        $setuphold (negedge C, posedge REGRST,  0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_REGRST);
        $setuphold (negedge C, negedge REGRST,  0:0:0, 0:0:0, notifier, c_en_n, c_en_n, delay_C, delay_REGRST);



        specparam PATHPULSE$ = 0;

    endspecify
`endif // ifdef XIL_TIMING

endmodule // IDELAYE2

`endcelldefine

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

