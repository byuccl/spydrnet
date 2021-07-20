import os
import zipfile
import tempfile

"""
Init for Spydrnet. the funcitons below can be called directly

"""


def parse(filename):
    """
    The parse function is able to parse either a EDIF (.edf) file or a Verilog file (.v)

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
    return _parse(filename)


def _parse(filename):
    extension = get_lowercase_extension(filename)
    if extension in [".edf", ".edif", ".edn"]:
        from spydrnet.parsers.edif.parser import EdifParser
        parser = EdifParser.from_filename(filename)
    elif extension in [".v", ".vh"]:
        from spydrnet.parsers.verilog.parser import VerilogParser
        parser = VerilogParser.from_filename(filename)
    else:
        raise RuntimeError("Extension {} not recognized.".format(extension))
    parser.parse()
    return parser.netlist


def get_lowercase_extension(filename):
    extension = os.path.splitext(filename)[1]
    extension_lower = extension.lower()
    return extension_lower
