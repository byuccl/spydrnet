from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif

filename = r"fourBitCounter_test.edf"

# parse
parser = EdifParser.from_filename(filename)
parser.parse()
ir = parser.netlist

# compose
composer = ComposeEdif()
composer.run(ir, "fourBitCounter_composed.edf")
