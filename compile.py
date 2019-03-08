from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("spydrnet.parsers.edif.tokenizer",  ["spydrnet/parsers/edif/tokenizer.py"]),
#    Extension("spydrnet.parsers.edif.parser", ["spydrnet/parsers/edif/parser.py"])
#   ... all your modules that need be compiled ...
]
setup(
    name = 'spydrnet',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)