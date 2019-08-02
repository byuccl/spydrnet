import json
import argparse

import spydrnet.analyze.analyze as analyze
import spydrnet.analyze.fannout_voter_selection as voter_section
import spydrnet.utility.utility as util

from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
from spydrnet.utility.Uniqueifier import Uniquifier
from spydrnet.transform.TMR import TMR
from spydrnet.graph.Graph_Builder import GraphBuilder

parser = argparse.ArgumentParser(description='SpyDrNet')
parser.add_argument('--netlist', '-n', type=str, required=True, help='Path to netlist file')
parser.add_argument('--config', '-c', type=str, required=True, help='Path to config file')

args = parser.parse_args()
config_file = args.config
netlist_file = args.netlist

print("Reading config file")
f = open(config_file, 'r')
test = f.read()
config = json.loads(test)

print("Parsing EDIF file")
parser = EdifParser.from_filename(netlist_file)
parser.parse()
ir = parser.netlist

print("Making definitions unique")
uniqueifier = Uniquifier()
uniqueifier.run(ir)
# Determine triplicate targets
print("Determining cells to triplicate")
cell_target = None
cell_target = analyze.determine_cells_to_replicate(ir, config)
# Determine voter locations
print("Determine where to place partition voters")
builder = GraphBuilder()
builder.build_graph(ir)
voter_section.D = builder.ir_graph
voter_section.perform_feedback_cut()
nets_to_cut = voter_section.keyPointsToCut



voter_target = list()
for instance in nets_to_cut:
    for inner_pin, outer_pin in instance.outer_pins.items():
        if inner_pin.port.direction.name == "OUT":
            voter_target.append(outer_pin.wire.cable['EDIF.identifier'])

analyze.determine_other_voters(ir, cell_target, voter_target)

print("Applying TMR")
tmr = TMR()
tmr.run(cell_target, voter_target, ir)

print("Determine reduction voter locations")
# voter_target = analyze.determine_reduction_location(ir, cell_target)
print("Placing reduction voters")
# tmr.run(None, voter_target, ir)

print("Writing out EDIF file")
composer = ComposeEdif()
composer.run(ir)
