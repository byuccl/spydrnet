import sys

from spydrnet.compare.compare_netlists import Comparer
from spydrnet.compare.compose_netlist import Composer

def run(file_name):
    file_parts = file_name.split('.')
    out_file_name = file_parts[0] + '_composed.' + file_parts[1]
    composer = Composer(file_name, out_file_name)
    composer.run()
    comparer = Comparer(file_name, out_file_name)
    comparer.run()

if __name__ == '__main__':
    if len(sys.argv) != 2:
         sys.exit("This script requires an filename as an argument")
    run(sys.argv[1])
