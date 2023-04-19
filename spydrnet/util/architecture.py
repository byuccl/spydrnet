import os
import spydrnet as sdn
from pathlib import Path

base_dir = Path(Path(sdn.__file__).absolute()).parent
base_file_path = Path(base_dir, 'support_files', 'architecture_libraries')

XILINX_7SERIES = os.path.join(base_file_path, "xilinx_7series.v.zip")
# XILINX_7SERIES = Path(base_file_path, "xilinx_7series.v.zip") # UnicodeDecodeError
F4PGA_XILINX_7SERIES = os.path.join(base_file_path, "f4pga_xilinx_7series.v.zip")
LATTICE_LIFCL = os.path.join(base_file_path, "lifcl.v.zip")
YOSYS_CELLS = os.path.join(base_file_path, "yosys_internal_cells.v.zip")