import unittest
import spydrnet as sdn
from spydrnet.composers.edif.composer import ComposeEdif


class TestTopologicalSort(unittest.TestCase):

    def test_top_sort(self):
        ce = ComposeEdif()
        def library_dependence(library):
            depend_set = set()
            for definition in library.definitions:
                for child in definition.children:
                    if child.reference.library != library:
                        depend_set.add(child.reference.library)
            return depend_set

        netlist = sdn.Netlist()

        lib_a = netlist.create_library()
        lib_a.name = "lib_a"
        definition_a = lib_a.create_definition()
        definition_a.name = "def_a"

        lib_b = netlist.create_library()
        lib_b.name = "lib_b"
        definition_b = lib_b.create_definition()
        definition_b.name = "def_b"
        
        instance_b = definition_b.create_child()
        instance_b.name = "relies_on_lib_a"
        instance_b.reference = definition_a

        libraries = ce._topological_sort(netlist.libraries, library_dependence)

        for l in libraries:
            assert l in netlist.libraries

        for l in netlist.libraries:
            assert l in libraries