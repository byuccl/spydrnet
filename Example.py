from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
import json

print("Parsing Edif.........")
edif_parser = EdifParser.from_filename(r"data/json_edif/temp.edf")
edif_parser.parse()
#print(edif_parser.netlist)
print("Success")
print("Exporting IR.........")
print("Skipped")
print("Composing Edif.......")
ComposeEdif().run(edif_parser.netlist, "run_through.edf")
print("Success")

