from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif

filename = r"fourBitCounter_test.edf"

# parse
# parser = EdifParser.from_filename(filename)
# parser.parse()
# ir = parser.netlist

# compose
# composer = ComposeEdif()
# composer.run(ir, "fourBitCounter_composed.edf")


class Composer:

    def __init__(self, filename=None, outfilename=None):
        if filename is None:
            raise Exception('filename cannot be None')
        elif outfilename is None:
            raise Exception('outfileName cannot be none')
        self.filename = filename
        self.outfilename = outfilename

    def run(self):
        print("reading netlist")
        parser = EdifParser.from_filename(self.filename)
        parser.parse()
        ir = parser.netlist

        print("writing netlist")
        composer = ComposeEdif()
        composer.run(ir, self.outfilename)

if __name__ == '__main__':
    composer = Composer("leon3mp_hierarchical.edf", "leon3mp_hierarchical_composed.edf")
    composer.run()
