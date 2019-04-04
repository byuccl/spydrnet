from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif import ComposeEdif
from colorama import Fore
from colorama import Style

print("Parsing Edif......")
edif_parser = EdifParser.from_filename(r"data\json_edif\temp.edf")
edif_parser.parse()
#print(edif_parser.netlist)
#print(f"{Fore.GREEN}Success{Style.RESET_ALL}") could add color in linux
print("Success")
print("Composing Edif....")
ComposeEdif().run(edif_parser.netlist, "run_through.edf")
#print(f"{Fore.GREEN}Success{Style.RESET_ALL}") could add color in linux
print("Success")
print("ensure lisp level 0 for sanity check")

