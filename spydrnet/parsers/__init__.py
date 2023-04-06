import os
import zipfile
import tempfile

"""
Init for Spydrnet. The functions below can be called directly

"""


def parse(filename, architecture=None, remove_space=False):
    """
    The parse function is able to parse an EDIF (.edf) file, a Verilog file (.v), or an EBLIF file (.eblif).

    This functions also supports the parsing of .zip files. Such as the ones in support_files folder

    Returns
    -------
    Netlist
        The netlist that comes as the result of the parsing of the file if the file was parsed successfully

    Examples
    --------

    >>> import spydrnet as sdn
    >>> netlist = sdn.parse('<netlist_filename>.edf')

    Or we can parse a verilog file

    >>> netlist = sdn.parse('<netlist_filename>.v')

    Or a zip file that contains the edif or verilog file

    >>> netlist = sdn.parse('4bitadder.edf.zip')

    The same applies for EBLIF files
    """
    basename_less_final_extension = os.path.splitext(
        os.path.basename(filename))[0]
    extension = get_lowercase_extension(filename)
    if extension == ".zip":
        assert zipfile.is_zipfile(filename), \
            "Input filename {} with extension .zip is not a zip file.".format(
                basename_less_final_extension)
        with tempfile.TemporaryDirectory() as tempdirname:
            with zipfile.ZipFile(filename) as zip:
                files = zip.namelist()
                assert len(files) == 1 and files[0] == basename_less_final_extension, \
                    "Only single file archives allowed with a file whose name matches the name of the archive"
                zip.extract(basename_less_final_extension, tempdirname)
                filename = os.path.join(
                    tempdirname, basename_less_final_extension)
                return _parse(filename)
    return _parse(filename, architecture, remove_space)


def _parse(filename, architecture=None, remove_space=False):
    extension = get_lowercase_extension(filename)
    if extension in [".edf", ".edif", ".edn"]:
        from spydrnet.parsers.edif.parser import EdifParser
        parser = EdifParser.from_filename(filename)
    elif extension in [".v", ".vh", ".vm"]:
        from spydrnet.parsers.verilog.parser import VerilogParser
        parser = VerilogParser.from_filename(filename)
    elif extension in [".eblif",".blif"]:
        from spydrnet.parsers.eblif.eblif_parser import EBLIFParser
        parser = EBLIFParser.from_filename(filename)
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
    parser.parse()
    
    if remove_space:
        from spydrnet.util.remove_space import removing_space
        removing_space(parser.netlist)

    if architecture:
        read_primitive_library(architecture, parser.netlist)
        if extension in [".eblif",".blif"]:
            set_eblif_names(parser.netlist)
    return parser.netlist


def get_lowercase_extension(filename):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    return extension_lower

def read_primitive_library(architecture, netlist):
    from spydrnet.parsers.primitive_library_reader import PrimitiveLibraryReader
    reader = PrimitiveLibraryReader(architecture, netlist)
    reader.run()

def set_eblif_names(netlist):
    from spydrnet.parsers.eblif.eblif_parser import EBLIFParser
    eblif_parser = EBLIFParser()
    eblif_parser.netlist = netlist
    eblif_parser.set_subcircuit_names_by_convention()