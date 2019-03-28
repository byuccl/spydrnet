from spydrnet.parsers.edif.parser import EdifParser

edif_parser = EdifParser.from_filename(r"data\json_edif\temp.edf")
edif_parser.parse()
print(edif_parser.netlist)
