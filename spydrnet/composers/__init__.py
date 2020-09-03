import os


def compose(netlist, filename):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    if extension_lower in {".edf", ".edif"}:
        from spydrnet.composers.edif.composer import ComposeEdif
        composer = ComposeEdif()
        composer.run(netlist, filename)
    elif extension_lower in [".v", ".vh"]:
        from spydrnet.composers.verilog.composer import Composer
        composer = Composer()
        composer.run(netlist, file_out = filename)
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
