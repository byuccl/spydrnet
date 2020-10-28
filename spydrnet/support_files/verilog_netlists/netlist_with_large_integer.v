// Copyright 1986-2018 Xilinx, Inc. All Rights Reserved.
// --------------------------------------------------------------------------------
// Tool Version: Vivado v.2018.3 (win64) Build 2405991 Thu Dec  6 23:38:27 MST 2018
// Date        : Mon Feb  3 13:45:17 2020
// Host        : CB461-EE10461 running 64-bit major release  (build 9200)
// Command     : write_verilog -file C:/Users/mbjerreg/verilog/netlist_with_large_integer.v -include_xilinx_libs
// Design      : carryAdd8
// Purpose     : This is a Verilog netlist of the current design or from a specific cell of the design. The output is an
//               IEEE 1364-2001 compliant Verilog HDL file that contains netlist information obtained from the input
//               design files.
// Device      : xc7a100tcsg324-1
// --------------------------------------------------------------------------------
`timescale 1 ps / 1 ps

(* STRUCTURAL_NETLIST = "yes" *)
module carryAdd8
   (.a({\a[7] ,\a[6] ,\a[5] ,\a[4] ,\a[3] ,\a[2] ,\a[1] ,\a[0] }),
    .b({\b[7] ,\b[6] ,\b[5] ,\b[4] ,\b[3] ,\b[2] ,\b[1] ,\b[0] }),
    .cin({\cin[7] ,\cin[6] ,\cin[5] ,\cin[4] ,\cin[3] ,\cin[2] ,\cin[1] ,\cin[0] }),
    cout,
    .s({\s[7] ,\s[6] ,\s[5] ,\s[4] ,\s[3] ,\s[2] ,\s[1] ,\s[0] }));
  output cout;
  input \a[0] ;
  input \a[1] ;
  input \a[2] ;
  input \a[3] ;
  input \a[4] ;
  input \a[5] ;
  input \a[6] ;
  input \a[7] ;
  input \b[0] ;
  input \b[1] ;
  input \b[2] ;
  input \b[3] ;
  input \b[4] ;
  input \b[5] ;
  input \b[6] ;
  input \b[7] ;
  input \cin[0] ;
  input \cin[1] ;
  input \cin[2] ;
  input \cin[3] ;
  input \cin[4] ;
  input \cin[5] ;
  input \cin[6] ;
  input \cin[7] ;
  output \s[0] ;
  output \s[1] ;
  output \s[2] ;
  output \s[3] ;
  output \s[4] ;
  output \s[5] ;
  output \s[6] ;
  output \s[7] ;

  wire \$abc$240$n36 ;
  wire \$abc$240$n37 ;
  wire \$abc$240$n38 ;
  wire \$abc$240$n39 ;
  wire \$abc$240$n40 ;
  wire \$abc$240$n41 ;
  wire \$abc$240$n42 ;
  wire \$abc$240$n43 ;
  wire \$abc$240$n44 ;
  wire \$abc$240$n45 ;
  wire \$abc$240$n46 ;
  wire \$abc$240$n47 ;
  wire \$abc$240$n48 ;
  wire \$abc$240$n49 ;
  wire \$abc$240$n50 ;
  wire \a[0] ;
  wire \a[1] ;
  wire \a[2] ;
  wire \a[3] ;
  wire \a[4] ;
  wire \a[5] ;
  wire \a[6] ;
  wire \a[7] ;
  wire [7:0]a_IBUF;
  wire \b[0] ;
  wire \b[1] ;
  wire \b[2] ;
  wire \b[3] ;
  wire \b[4] ;
  wire \b[5] ;
  wire \b[6] ;
  wire \b[7] ;
  wire [7:0]b_IBUF;
  wire \cin[0] ;
  wire \cin[1] ;
  wire \cin[2] ;
  wire \cin[3] ;
  wire \cin[4] ;
  wire \cin[5] ;
  wire \cin[6] ;
  wire \cin[7] ;
  wire [7:0]cin_IBUF;
  wire cout;
  wire cout_OBUF;
  wire \s[0] ;
  wire \s[1] ;
  wire \s[2] ;
  wire \s[3] ;
  wire \s[4] ;
  wire \s[5] ;
  wire \s[6] ;
  wire \s[7] ;
  wire [7:0]s_OBUF;

  LUT5 #(
    .INIT(32'h7FFFFFFF)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$241 
       (.I0(\$abc$240$n36 ),
        .I1(\$abc$240$n50 ),
        .I2(a_IBUF[7]),
        .I3(b_IBUF[7]),
        .I4(cin_IBUF[7]),
        .O(cout_OBUF));
  LUT6 #(
    .INIT(64'h0000FF005700FF57)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$242 
       (.I0(\$abc$240$n46 ),
        .I1(\$abc$240$n39 ),
        .I2(\$abc$240$n49 ),
        .I3(\$abc$240$n47 ),
        .I4(\$abc$240$n48 ),
        .I5(\$abc$240$n37 ),
        .O(\$abc$240$n36 ));
  LUT4 #(
    .INIT(16'h4114)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$243 
       (.I0(\$abc$240$n38 ),
        .I1(a_IBUF[5]),
        .I2(b_IBUF[5]),
        .I3(cin_IBUF[5]),
        .O(\$abc$240$n37 ));
  LUT3 #(
    .INIT(8'h17)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$244 
       (.I0(a_IBUF[4]),
        .I1(b_IBUF[4]),
        .I2(cin_IBUF[4]),
        .O(\$abc$240$n38 ));
  LUT6 #(
    .INIT(64'hEAFF00EA00000000)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$245 
       (.I0(\$abc$240$n42 ),
        .I1(\$abc$240$n43 ),
        .I2(\$abc$240$n44 ),
        .I3(\$abc$240$n40 ),
        .I4(\$abc$240$n41 ),
        .I5(\$abc$240$n45 ),
        .O(\$abc$240$n39 ));
  LUT3 #(
    .INIT(8'h17)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$246 
       (.I0(a_IBUF[2]),
        .I1(b_IBUF[2]),
        .I2(cin_IBUF[2]),
        .O(\$abc$240$n40 ));
  LUT3 #(
    .INIT(8'h96)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$247 
       (.I0(a_IBUF[3]),
        .I1(b_IBUF[3]),
        .I2(cin_IBUF[3]),
        .O(\$abc$240$n41 ));
  LUT6 #(
    .INIT(64'hE80000E800E8E800)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$248 
       (.I0(a_IBUF[1]),
        .I1(b_IBUF[1]),
        .I2(cin_IBUF[1]),
        .I3(a_IBUF[2]),
        .I4(b_IBUF[2]),
        .I5(cin_IBUF[2]),
        .O(\$abc$240$n42 ));
  LUT6 #(
    .INIT(64'hE80000E800E8E800)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$249 
       (.I0(a_IBUF[0]),
        .I1(b_IBUF[0]),
        .I2(cin_IBUF[0]),
        .I3(a_IBUF[1]),
        .I4(b_IBUF[1]),
        .I5(cin_IBUF[1]),
        .O(\$abc$240$n43 ));
  LUT6 #(
    .INIT(64'h17E8E817E81717E8)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$250 
       (.I0(a_IBUF[1]),
        .I1(b_IBUF[1]),
        .I2(cin_IBUF[1]),
        .I3(a_IBUF[2]),
        .I4(b_IBUF[2]),
        .I5(cin_IBUF[2]),
        .O(\$abc$240$n44 ));
  LUT6 #(
    .INIT(64'h17E8E817E81717E8)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$251 
       (.I0(a_IBUF[3]),
        .I1(b_IBUF[3]),
        .I2(cin_IBUF[3]),
        .I3(a_IBUF[4]),
        .I4(b_IBUF[4]),
        .I5(cin_IBUF[4]),
        .O(\$abc$240$n45 ));
  LUT4 #(
    .INIT(16'h9669)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$252 
       (.I0(\$abc$240$n38 ),
        .I1(a_IBUF[5]),
        .I2(b_IBUF[5]),
        .I3(cin_IBUF[5]),
        .O(\$abc$240$n46 ));
  LUT3 #(
    .INIT(8'h17)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$253 
       (.I0(a_IBUF[5]),
        .I1(b_IBUF[5]),
        .I2(cin_IBUF[5]),
        .O(\$abc$240$n47 ));
  LUT3 #(
    .INIT(8'h96)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$254 
       (.I0(a_IBUF[6]),
        .I1(b_IBUF[6]),
        .I2(cin_IBUF[6]),
        .O(\$abc$240$n48 ));
  LUT6 #(
    .INIT(64'hE80000E800E8E800)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$255 
       (.I0(a_IBUF[3]),
        .I1(b_IBUF[3]),
        .I2(cin_IBUF[3]),
        .I3(a_IBUF[4]),
        .I4(b_IBUF[4]),
        .I5(cin_IBUF[4]),
        .O(\$abc$240$n49 ));
  LUT3 #(
    .INIT(8'h17)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$256 
       (.I0(a_IBUF[6]),
        .I1(b_IBUF[6]),
        .I2(cin_IBUF[6]),
        .O(\$abc$240$n50 ));
  LUT5 #(
    .INIT(32'h7FFFFFFF)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$257 
       (.I0(\$abc$240$n36 ),
        .I1(\$abc$240$n50 ),
        .I2(a_IBUF[7]),
        .I3(b_IBUF[7]),
        .I4(cin_IBUF[7]),
        .O(s_OBUF[7]));
  LUT6 #(
    .INIT(64'h001FFFE0FFE0001F)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$258 
       (.I0(\$abc$240$n39 ),
        .I1(\$abc$240$n49 ),
        .I2(\$abc$240$n46 ),
        .I3(\$abc$240$n37 ),
        .I4(\$abc$240$n47 ),
        .I5(\$abc$240$n48 ),
        .O(s_OBUF[6]));
  LUT3 #(
    .INIT(8'h1E)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$259 
       (.I0(\$abc$240$n39 ),
        .I1(\$abc$240$n49 ),
        .I2(\$abc$240$n46 ),
        .O(s_OBUF[5]));
  LUT6 #(
    .INIT(64'h00F070F7FF0F8F08)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$260 
       (.I0(\$abc$240$n43 ),
        .I1(\$abc$240$n44 ),
        .I2(\$abc$240$n40 ),
        .I3(\$abc$240$n41 ),
        .I4(\$abc$240$n42 ),
        .I5(\$abc$240$n45 ),
        .O(s_OBUF[4]));
  LUT5 #(
    .INIT(32'h07F8F807)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$261 
       (.I0(\$abc$240$n43 ),
        .I1(\$abc$240$n44 ),
        .I2(\$abc$240$n42 ),
        .I3(\$abc$240$n40 ),
        .I4(\$abc$240$n41 ),
        .O(s_OBUF[3]));
  LUT2 #(
    .INIT(4'h6)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$262 
       (.I0(\$abc$240$n43 ),
        .I1(\$abc$240$n44 ),
        .O(s_OBUF[2]));
  LUT6 #(
    .INIT(64'h17E8E817E81717E8)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$263 
       (.I0(a_IBUF[0]),
        .I1(b_IBUF[0]),
        .I2(cin_IBUF[0]),
        .I3(a_IBUF[1]),
        .I4(b_IBUF[1]),
        .I5(cin_IBUF[1]),
        .O(s_OBUF[1]));
  LUT3 #(
    .INIT(8'h96)) 
    \$abc$240$auto$blifparse.cc:465:parse_blif$264 
       (.I0(a_IBUF[0]),
        .I1(b_IBUF[0]),
        .I2(cin_IBUF[0]),
        .O(s_OBUF[0]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \a[0]_IBUF_inst 
       (.I(\a[0] ),
        .O(a_IBUF[7]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \a[1]_IBUF_inst 
       (.I(\a[1] ),
        .O(a_IBUF[6]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \a[2]_IBUF_inst 
       (.I(\a[2] ),
        .O(a_IBUF[5]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \a[3]_IBUF_inst 
       (.I(\a[3] ),
        .O(a_IBUF[4]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \a[4]_IBUF_inst 
       (.I(\a[4] ),
        .O(a_IBUF[3]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \a[5]_IBUF_inst 
       (.I(\a[5] ),
        .O(a_IBUF[2]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \a[6]_IBUF_inst 
       (.I(\a[6] ),
        .O(a_IBUF[1]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \a[7]_IBUF_inst 
       (.I(\a[7] ),
        .O(a_IBUF[0]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \b[0]_IBUF_inst 
       (.I(\b[0] ),
        .O(b_IBUF[7]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \b[1]_IBUF_inst 
       (.I(\b[1] ),
        .O(b_IBUF[6]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \b[2]_IBUF_inst 
       (.I(\b[2] ),
        .O(b_IBUF[5]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \b[3]_IBUF_inst 
       (.I(\b[3] ),
        .O(b_IBUF[4]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \b[4]_IBUF_inst 
       (.I(\b[4] ),
        .O(b_IBUF[3]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \b[5]_IBUF_inst 
       (.I(\b[5] ),
        .O(b_IBUF[2]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \b[6]_IBUF_inst 
       (.I(\b[6] ),
        .O(b_IBUF[1]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \b[7]_IBUF_inst 
       (.I(\b[7] ),
        .O(b_IBUF[0]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \cin[0]_IBUF_inst 
       (.I(\cin[0] ),
        .O(cin_IBUF[7]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \cin[1]_IBUF_inst 
       (.I(\cin[1] ),
        .O(cin_IBUF[6]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \cin[2]_IBUF_inst 
       (.I(\cin[2] ),
        .O(cin_IBUF[5]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \cin[3]_IBUF_inst 
       (.I(\cin[3] ),
        .O(cin_IBUF[4]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \cin[4]_IBUF_inst 
       (.I(\cin[4] ),
        .O(cin_IBUF[3]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \cin[5]_IBUF_inst 
       (.I(\cin[5] ),
        .O(cin_IBUF[2]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \cin[6]_IBUF_inst 
       (.I(\cin[6] ),
        .O(cin_IBUF[1]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  IBUF \cin[7]_IBUF_inst 
       (.I(\cin[7] ),
        .O(cin_IBUF[0]));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF cout_OBUF_inst
       (.I(cout_OBUF),
        .O(cout));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF \s[0]_OBUF_inst 
       (.I(s_OBUF[7]),
        .O(\s[0] ));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF \s[1]_OBUF_inst 
       (.I(s_OBUF[6]),
        .O(\s[1] ));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF \s[2]_OBUF_inst 
       (.I(s_OBUF[5]),
        .O(\s[2] ));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF \s[3]_OBUF_inst 
       (.I(s_OBUF[4]),
        .O(\s[3] ));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF \s[4]_OBUF_inst 
       (.I(s_OBUF[3]),
        .O(\s[4] ));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF \s[5]_OBUF_inst 
       (.I(s_OBUF[2]),
        .O(\s[5] ));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF \s[6]_OBUF_inst 
       (.I(s_OBUF[1]),
        .O(\s[6] ));
  (* OPT_INSERTED *) 
  (* OPT_MODIFIED = "MLO " *) 
  OBUF \s[7]_OBUF_inst 
       (.I(s_OBUF[0]),
        .O(\s[7] ));
endmodule
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

