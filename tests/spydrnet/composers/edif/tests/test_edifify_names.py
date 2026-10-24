import unittest
import tempfile
from pathlib import Path
import spydrnet as sdn
from spydrnet.composers.edif.edifify_names import EdififyNames


class TestEdififyNames(unittest.TestCase):
    def test_case_collisions_roundtrip_preserves_names_and_connections(self):
        for stored_identifier in (False, True):
            with self.subTest(stored_identifier=stored_identifier):
                netlist = sdn.Netlist(name="roundtrip")
                library = netlist.create_library(name="work")
                leaf = library.create_definition(name="leaf")
                leaf_port = leaf.create_port(name="I", direction=sdn.IN)
                leaf_port.create_pin()
                top = library.create_definition(name="top")
                top_instance = sdn.Instance(name="top_instance")
                top_instance.reference = top
                netlist.top_instance = top_instance
                names = (
                    ("original", "mixed", "MIXED_SDN_1_")
                    if stored_identifier
                    else ("Mixed", "mixed", "MIXED_SDN_1_")
                )
                for index, name in enumerate(names):
                    port = top.create_port(name=name, direction=sdn.IN)
                    cable = top.create_cable(name=name)
                    instance = top.create_child(name=name, reference=leaf)
                    if stored_identifier and index == 0:
                        for element in (port, cable, instance):
                            element["EDIF.identifier"] = "MiXeD"
                    wire = cable.create_wire()
                    wire.connect_pin(port.create_pin())
                    wire.connect_pin(instance.pins[leaf_port.pins[0]])

                with tempfile.TemporaryDirectory() as directory:
                    filename = str(Path(directory) / "case_collisions.edf")
                    sdn.compose(netlist, filename)
                    for objects in (top.ports, top.cables, top.children):
                        identifiers = [
                            element["EDIF.identifier"].lower() for element in objects
                        ]
                        self.assertEqual(len(set(identifiers)), 3)
                    parsed = sdn.parse(filename)

                parsed_top = parsed.top_instance.reference
                for objects in (
                    parsed_top.ports,
                    parsed_top.cables,
                    parsed_top.children,
                ):
                    self.assertEqual({element.name for element in objects}, set(names))
                    identifiers = [
                        element["EDIF.identifier"].lower() for element in objects
                    ]
                    self.assertEqual(len(set(identifiers)), 3)
                parsed_ports = {port.name: port for port in parsed_top.ports}
                parsed_cables = {cable.name: cable for cable in parsed_top.cables}
                parsed_children = {child.name: child for child in parsed_top.children}
                for name in names:
                    wire = parsed_cables[name].wires[0]
                    self.assertIs(parsed_ports[name].pins[0].wire, wire)
                    child = parsed_children[name]
                    self.assertEqual(child.reference.name, "leaf")
                    self.assertEqual(len(child.pins), 1)
                    self.assertIs(next(iter(child.pins.values())).wire, wire)
                    self.assertEqual(len(wire.pins), 2)

    def test_simple_conversion(self):
        ed = EdififyNames()
        l = []
        i = sdn.Instance()
        i.name = "name"
        l = [i]
        assert ed.make_valid(i, l) == "name"

    def test_invalid_name(self):
        ed = EdififyNames()
        l = []
        i = sdn.Instance()
        i.name = "*this_is+an$*`id[0:3]"
        l = [i]
        assert ed.make_valid(i, l) == "&_this_is_an___id_0_3_"

    def test_duplicate_name(self):
        ed = EdififyNames()
        l = []
        i = sdn.Instance()
        i.name = "name"
        i2 = sdn.Instance()
        i2.name = "name"
        l = [i, i2]
        assert ed.make_valid(i2, l) == "name_sdn_1_"

    def test_duplicate_name_is_case_insensitive(self):
        ed = EdififyNames()
        existing = sdn.Instance()
        existing.name = "Name"
        duplicate = sdn.Instance()
        duplicate.name = "name"

        assert ed.make_valid(duplicate, [existing, duplicate]) == "name_sdn_1_"

    def test_duplicate_edif_identifier_is_case_insensitive(self):
        ed = EdififyNames()
        existing = sdn.Instance()
        existing.name = "original_name"
        existing["EDIF.identifier"] = "Name"
        duplicate = sdn.Instance()
        duplicate.name = "name"

        assert ed.make_valid(duplicate, [existing, duplicate]) == "name_sdn_1_"

    def test_case_insensitive_suffix_conflict_increments(self):
        ed = EdififyNames()
        existing = sdn.Instance()
        existing.name = "NAME"
        existing_suffix = sdn.Instance()
        existing_suffix.name = "NAME_SDN_1_"
        duplicate = sdn.Instance()
        duplicate.name = "name"

        objects = [existing, existing_suffix, duplicate]
        assert ed.make_valid(duplicate, objects) == "name_sdn_2_"

    def test_duplicate_number_increment(self):
        ed = EdififyNames()
        l = []
        i = sdn.Instance()
        i.name = "name"
        i_duplicate = sdn.Instance()
        i_duplicate.name = "name"
        i2 = sdn.Instance()
        i2.name = "name_sdn_1_"
        l = [i, i2, i_duplicate]
        assert ed.make_valid(i_duplicate, l) == "name_sdn_2_"

    def test_length(self):
        ed = EdififyNames()
        l = []
        test_str = ""
        answer_str = ""
        for _ in range(ed.name_length_target + 5):
            test_str = test_str + "a"
        for _ in range(ed.name_length_target):
            answer_str = answer_str + "a"
        i = sdn.Instance()
        i.name = test_str
        l = [i]
        assert ed.make_valid(i, l) == answer_str

    def test_length_2(self):
        ed = EdififyNames()
        l = []
        test_str = "$"
        answer_str = "&_"
        for _ in range(ed.name_length_target + 5):
            test_str = test_str + "a"
        for _ in range(ed.name_length_target - 2):
            answer_str = answer_str + "a"
        i = sdn.Instance()
        i.name = test_str
        l = [i]
        assert ed.make_valid(i, l) == answer_str

    def test_length_3(self):
        ed = EdififyNames()
        l = []

        instance_1 = sdn.Instance()
        name_1 = "&_"
        for _ in range(ed.name_length_target - 2):
            name_1 = name_1 + "a"
        instance_1.name = name_1

        instance_2 = sdn.Instance()

        name_2 = "&_"
        for _ in range(ed.name_length_target - 9):
            name_2 = name_2 + "a"
        name_2 = name_2 + "_sdn_1_"
        instance_2.name = name_2

        test_str = "$"
        answer_str = "&_"
        for _ in range(ed.name_length_target + 5):
            test_str = test_str + "a"
        for _ in range(ed.name_length_target - 9):
            answer_str = answer_str + "a"

        answer_str = answer_str + "_sdn_2_"

        instance_3 = sdn.Instance()
        instance_3.name = test_str

        l = [instance_1, instance_2, instance_3]

        assert ed.make_valid(instance_3, l) == answer_str
