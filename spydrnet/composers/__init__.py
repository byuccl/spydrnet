import os


def compose(netlist, filename):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    if extension_lower in {".edf", ".edif"}:
        from spydrnet.composers.edif.composer import ComposeEdif
        composer = ComposeEdif()
        composer.run(netlist, filename)
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
