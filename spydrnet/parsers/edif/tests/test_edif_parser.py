import unittest
import spydrnet as sdn

from spydrnet.parsers.edif.parser import EdifParser
from spydrnet import base_dir

class TestEdifTokenizer(unittest.TestCase):
    def test_multi_bit_add_out_of_order(self):
        definition = sdn.Definition()
        cable0 = sdn.Cable()
        cable0.name = "net[0]"
        cable0["EDIF.identifier"] = "net_0_"
        cable1 = sdn.Cable()
        cable1.name = "net[1]"
        cable1["EDIF.identifier"] = "net_1_"
        cable2 = sdn.Cable()
        cable2.name = "net[2]"
        cable2["EDIF.identifier"] = "net_2_"

        cable0.create_wire()
        cable1.create_wire()
        cable2.create_wire()
        
        p0 = sdn.InnerPin()
        p1 = sdn.InnerPin()
        p2 = sdn.InnerPin()

        cable1.wires[0].connect_pin(p0)
        cable1.wires[0].connect_pin(p1)
        cable1.wires[0].connect_pin(p2)

        ep = EdifParser()
        ep.multibit_add_cable(definition, cable0)
        ep.multibit_add_cable(definition, cable2)
        ep.multibit_add_cable(definition, cable1)

        assert len(definition.cables) == 1
        assert len (definition.cables[0].wires) == 3
        assert len(definition.cables[0].wires[0].pins) == 0
        assert len(definition.cables[0].wires[1].pins) == 3
        assert len(definition.cables[0].wires[2].pins) == 0
        assert p0 in definition.cables[0].wires[1].pins
        assert p1 in definition.cables[0].wires[1].pins
        assert p2 in definition.cables[0].wires[1].pins
            