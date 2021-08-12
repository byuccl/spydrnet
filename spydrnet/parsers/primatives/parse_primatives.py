#Parse primative library files from various vendors.
#Copyright 2019 BYU Configurable Computing Lab
#Author Dallin Skouson
#See the license that accompanies SpyDrNet tools for more information
#
#Currently implemented vendors:
#Xilinx vivado tested with and designed for files from Vivado/2019.1/data/verilog/src/xeclib (other versions should hopefully work)
#
#Future capabilities
#accept files from other locations for Xilinx
#support intel/altera devices.
#support for other vendors

import os
import spydrnet as SpyDrNet

VERBOSE = True

class PrimativeParser:
    '''
    Parses primative libraries for use with the tools

    This class is a standalone class as of the first release. 
    Hopefully the xilinx part of this parser can be combined with the structural verilog parser so that they can share code

    Extracts the ports, parameters, and names of primatives
    The primative libraries can be found in the following location
    Xilinx Vivado:
    Vivado/2019.1/data/verilog/src/xeclib
    '''

    def vivado_parse_xeclib(self, xeclib_directory):
        '''
        parse each file in the xeclib_directory
        parameters:
            xeclib_directory - The directory where the primatives can be found
        returns:
            Library that contains all the primatives and is orphaned from any netlist.
        '''
        for v_file in os.listdir(xeclib_directory):
            self._vivado_parse_file(xeclib_directory + "/" + v_file)

    def _vivado_parse_file(self, verilog_file):
        '''
        parse the verilog file
        parameters:
            a verilog file to parse
        returns:
            Definition created from the verilog file
        '''
        if not verilog_file.endswith('.v'):
           print("File " + verilog_file + " in directory does not end with the proper extension") 
        with open(verilog_file) as vf:
            self._vivado_parse(vf)

    def _vivado_parse(self, stream):
        parameters = {}
        inputs = {}
        outputs = {}
        inouts = {}
        name = ''
        for statement in stream:
            statement = statement.rstrip()
            if statement.endswith(';') or statement.endswith(','):
                statement = statement[:-1]
            statement = statement.split()
            if len(statement) == 0:
                continue
            elif statement[0] == 'parameter':
                pass
            elif statement[0] == 'module':
                name = statement[1] #this is lazy but I think it might work with all the xilinx verilog files for now....
            elif statement[0] == 'input':
                self._vivado_get_port_info(statement, inputs)
            elif statement[0] == 'output':
                self._vivado_get_port_info(statement, outputs)
            elif statement[0] == 'inout':
                self._vivado_get_port_info(statement, inouts)
            else:
                pass

        if(VERBOSE):
            print("\nModule " + name)
            print("Inputs:")
            print(inputs)
            print("Outputs:")
            print(outputs)
            print("Inouts:")
            print(inouts)

        definition = self._vivado_create_definition(name, parameters, inputs, outputs, inouts)
        return definition

    def _vivado_get_port_info(self, line, port_container):
        if line[1][0] == '[':
            direction = line[1]
            direction = direction[1:-1]
            from_to = direction.split(":")
            from_to[0] = int(from_to[0])
            from_to[1] = int(from_to[1])
            for i in range(2,len(line)):
                port_container[line[i]] = from_to
        else:
            for i in range(1,len(line)):
                port_container[line[i]] = ''
    
    def _vivado_create_definition(self, name, parameters, inputs, outputs, inouts):
        definition = SpyDrNet.create_definition()
        for i, val in inputs.items():
            definition.add_port(self._create_port(i,val,SpyDrNet.Port.Direction.IN))
        for o, val in outputs.items():
            definition.add_port(self._create_port(o,val,SpyDrNet.Port.Direction.OUT))
        for io, val in inouts.items():
            definition.add_port(self._create_port(io,val,SpyDrNet.Port.Direction.INOUT))
        return definition
        
    def _create_port(self, name, indicies, direction):
        port = SpyDrNet.create_port(name = name)
        port.set_direction(direction)
        if indicies != '':
            port.initialize_pins_in_range(indicies[0],indicies[1])
        return port

if __name__ == "__main__":
    parse = PrimativeParser()
    parse.vivado_parse_xeclib("/home/dallin/Documents/byuccl/xeclib")