import spydrnet as sdn
from pathlib import Path

base_dir = Path(Path(sdn.__file__).absolute()).parent
base_file_path = Path(base_dir, 'support_files', 'architecture_libraries')

XILINX_7SERIES = Path(base_file_path).joinpath("xilinx_7series.v.zip")
F4PGA_XILINX_7SERIES = Path(base_file_path).joinpath("f4pga_xilinx_7series.v.zip")
LATTICE_LIFCL = Path(base_file_path).joinpath("lifcl.v.zip")
YOSYS_CELLS = Path(base_file_path).joinpath("yosys_internal_cells.v.zip")