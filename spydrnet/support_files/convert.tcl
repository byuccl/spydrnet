# Vivado EDIF conversion scripts
#
# This file provide examples of how EDIF files can be converted to Verilog or 
# VHDL using Vivado.
#
# The EDIF files in the folder `EDIF_netlists` were used with "Method 1" below 
# to generate the netlists in the `verilog_netlists` folder.
# 
# It was observed that METAX elements in EDIF were preventing files from being
# read into Vivado. The simple work around used was to sanitize the EDIF file 
# using Python or a Unix sed command. In Python, something like this.
# 
# with open(input_filename) as fh_in, open(output_filename) as fh_out:
#     for line in fh_in:
#         if "(metax" not in line:
#             fh_out.write(line)
#
#
# #### Method 1 ####
# set file fourBitCounter.edf
# set module fourBitCounter
# 
# set files [glob *.edf]	;
# foreach file $files {	;
#     set dot [expr [string length $file] - 5]
#     set module [string range $file 0 $dot]
#     puts "*******************************************"
#     put $module
#     add_files $file
#     set_property top $module [current_fileset]
#     link_design -name netlist_1
#     write_verilog -file [pwd]/$module.v -include_xilinx_libs -force
#     write_vhdl -file [pwd]/$module.vhd -include_xilinx_libs -force
#     close_design
#     remove_file $file
# }
#
# #### Method 2 ####
# set_property design_mode GateLvl [current_fileset]
# set_property edif_top_file <filename.edf> [current_fileset]
# link_design -mode out_of_context -part <partnumber>
# write_verilog -mode funcsim <outputFilename.v>