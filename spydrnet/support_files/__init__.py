import os
import glob

supportfile_dir = os.path.abspath(os.path.dirname(__file__))

temp = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'EDIF_files', '*.edf')
_temp_edif_files = glob.glob(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'EDIF_files', '*.edf'))
edif_files = dict()
for file in _temp_edif_files:
    test = os.path.split(file)
    edif_files[test[1]] = file
print()
