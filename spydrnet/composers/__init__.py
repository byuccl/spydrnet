import os


def compose(netlist, filename, definition_list=[], write_blackbox=True):
    """To compose a file into a netlist format"""
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    if extension_lower in {".edf", ".edif"}:
        from spydrnet.composers.edif.composer import ComposeEdif
        composer = ComposeEdif()
        if netlist.name is None:
            raise Exception("netlist.name undefined")
        composer.run(netlist, filename)
    elif extension_lower in [".v", ".vh"]:
        from spydrnet.composers.verilog.composer import Composer
        composer = Composer(definition_list, write_blackbox)
        composer.run(netlist, file_out=filename)
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
