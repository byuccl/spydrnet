from spydrnet.ir import *

import os

current_design = None

designs = list()

def create_design():
    global current_design
    new_design = Design()
    designs.append(new_design)
    current_design = new_design
    
def parse(filename):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    if extension_lower in [".edf", ".edif"]:
        from spydrnet.parsers.edif.parser import EdifParser
        parser = EdifParser.from_filename(filename)
        parser.parse()
        current_design.netlist = parser.netlist
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
        
    