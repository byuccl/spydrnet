import unittest
import spydrnet as sdn
from spydrnet.composers.edif.composer import ComposeEdif


class TestTopologicalSort(unittest.TestCase):

    def test_top_sort(self):
        ce = ComposeEdif()
        def library_dependence(library):
            depend_set = set()
            for definition in library.definitions:
                # print("library: " + library.name)
                for child in definition.children:
                    # print("contains: " + child.name)
                    if child.reference.library != library:
                        # print("which instances definition " + child.reference.name)
                        # print("which depends on " + child.reference.library.name)
                        depend_set.add(child.reference.library)
            # print("DEPENDENCY LIST RETURNED")
            # for lib_dep in depend_set:
            #     print(lib_dep.name)
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

        lib_c = netlist.create_library()
        lib_c.name = "lib_c"
        definition_c = lib_c.create_definition()
        definition_c.name = "def_c"

        instance_c1 = definition_c.create_child()
        instance_c1.name = "relies_on_a"
        instance_c1.reference = definition_a
        instance_c2 = definition_c.create_child()
        instance_c2.name = "relies_on_b"
        instance_c2.reference = definition_b

        libraries = ce._topological_sort(netlist.libraries, library_dependence)

        print("should be a, b, c")
        for lib in libraries:
            print(lib.name)

        print("dependencies")
        for lib in libraries:
            print(lib.name, end = "")
            print(" relies on")
            for l in library_dependence(lib):
                print("\t" + l.name)

        for l in libraries:
            assert l in netlist.libraries

        for l in netlist.libraries:
            assert l in libraries

        found_libraries = set()
        for l in libraries:
            found_libraries.add(l)
            for l_dep in library_dependence(l):
                assert l_dep in found_libraries