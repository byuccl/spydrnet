import os
import spydrnet as sdn

base_dir = os.path.dirname(os.path.abspath(sdn.__file__))
base_file_path = os.path.join(base_dir, 'support_files', 'architecture_libraries')

XILINX_7SERIES = os.path.join(base_file_path, "xilinx_7series.v.zip")
F4PGA_XILINX_7SERIES = os.path.join(base_file_path, "f4pga_xilinx_7series.v.zip")
LATTICE_LIFCL = os.path.join(base_file_path, "lifcl.v.zip")
YOSYS_CELLS = os.path.join(base_file_path, "yosys_internal_cells.v.zip")