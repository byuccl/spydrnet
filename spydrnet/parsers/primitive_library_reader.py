import spydrnet as sdn
from spydrnet.ir import Library
from spydrnet.parsers.verilog.parser import VerilogParser
import spydrnet.parsers.verilog.verilog_tokens as vt

MODULE = "module"
END_MODULE = "endmodule"
INPUT = "input"
OUTPUT = "output"
PARAMETER = "parameter"

class PrimitiveLibraryReader():
    """
    A class to extract primitive port information from a Verilog file and insert it into the netlist. The input file is parsed using the Verilog Parser and if any module information is found for a definition in the given netlist, the port information (i.e. directions) is added.

    parameters
    ----------
    architecture - the targeted architecture. Must be a type from spydrnet.util.architecture
    netlist - the current netlist
    """

    def __init__(self, architecture, netlist):
        self.input_file = architecture
        self.netlist = netlist
        self.netlist_defs = dict()
        self.parsed_defs = dict()
        self.parser = None
    
    def run(self):
        self.initialize()
        while(self.parser.tokenizer.has_next()):
            self.get_past_comments()
            self.parser.parse_primitive()
            definition = self.parser.current_definition
            self.parsed_defs[definition.name] = definition
        cnt = self.insert_info()
        print("Found information for %d definitions" % cnt)
    
    def initialize(self):
        self.parser = VerilogParser.from_filename(self.input_file)
        self.parser.initialize_tokenizer()
        self.parser.current_library = Library()
        self.create_defintiion_dict()

    def get_past_comments(self):
        token = self.parser.peek_token()
        while(token != vt.MODULE and token != vt.PRIMITIVE):
            # print(token)
            self.parser.next_token()
            token = self.parser.peek_token()

    def create_defintiion_dict(self):
        for definition in self.netlist.get_definitions():
            self.netlist_defs[definition.name] = definition

    def insert_info(self):
        cnt = 0
        for def_name, definition in self.netlist_defs.items():
            if def_name in self.parsed_defs.keys():
                match = self.parsed_defs[def_name]
                port_dict = self.create_port_dict(match)
                # print(definition.name + " " + str(port_dict))
                for port in definition.get_ports():
                    port.direction = port_dict[port.name]
                cnt+=1
        return cnt

    def create_port_dict(self, definition):
        port_dict = dict()
        for port in definition.get_ports():
            port_dict[port.name] = port.direction
            # print(port.name + " has direction " + str(port.direction))
        return port_dict