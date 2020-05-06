import unittest
import spydrnet as sdn
# from spydrnet.parsers.verilog.VerilogParser import verilogParser


class TestVerilogParser(unittest.TestCase):
    pass
    # def test_simple(self):
    #     f = open('simpleVerilog.v', 'r')
    #     s = f.read()
    #     f.close()
    #     parser = verilogParser()
    #     result = parser.parse(s)
    #     library = result.libraries[0]
    #     self.assertEqual(len(library.definitions), 1)
    #     definition = library.definitions[0]
    #     self.assertEqual(definition.name, 'foo')
    #     self.assertEqual(len(definition.ports), 1)
    #     port = definition.ports[0]
    #     self.assertEqual(port.name, 'a')
    #     self.assertEqual(port.direction, sdn.IN)
    #     self.assertEqual(len(port.pins), 1)
    #     self.assertEqual(len(definition.cables), 1)
    #     cable = definition.cables[0]
    #     self.assertEqual(cable.name, 'a')
    #     self.assertEqual(len(cable.wires), 1)

    # def test_port_direction_1(self):
    #     f = open('portDirection1.v', 'r')
    #     s = f.read()
    #     f.close()
    #     parser = verilogParser()
    #     result = parser.parse(s)
    #     definition = result.libraries[0].definitions[0]
    #     self.assertEqual(len(definition.ports), 6)
    #     ports = definition.ports
    #     port = ports[0]
    #     self.assertEqual(port.direction, sdn.IN)
    #     port = ports[1]
    #     self.assertEqual(port.direction, sdn.IN)
    #     port = ports[2]
    #     self.assertEqual(port.direction, sdn.INOUT)
    #     port = ports[3]
    #     self.assertEqual(port.direction, sdn.INOUT)
    #     port = ports[4]
    #     self.assertEqual(port.direction, sdn.OUT)
    #     port = ports[5]
    #     self.assertEqual(port.direction, sdn.OUT)

    # def test_port_direction_1(self):
    #     f = open('portDirection2.v', 'r')
    #     s = f.read()
    #     f.close()
    #     parser = verilogParser()
    #     result = parser.parse(s)
    #     definition = result.libraries[0].definitions[0]
    #     self.assertEqual(len(definition.ports), 6)
    #     ports = definition.ports
    #     port = ports[0]
    #     self.assertEqual(port.direction, sdn.IN)
    #     port = ports[1]
    #     self.assertEqual(port.direction, sdn.IN)
    #     port = ports[2]
    #     self.assertEqual(port.direction, sdn.INOUT)
    #     port = ports[3]
    #     self.assertEqual(port.direction, sdn.INOUT)
    #     port = ports[4]
    #     self.assertEqual(port.direction, sdn.OUT)
    #     port = ports[5]
    #     self.assertEqual(port.direction, sdn.OUT)


if __name__ == '__main__':
    unittest.main()
