from spydrnet.ir import *

class Uniquifier:

    def __init__(self):
        self.num = 0

    def test(self, ir, definition_count, definition_to_instances):
        test = ir.libraries[-1].definitions[-1]
        self.trace(test, definition_count, definition_to_instances)
        for key, value in definition_count.items():
            print(key.__getitem__("EDIF.identifier"), "used", value, "times")


    def trace(self, definition, definition_count, definition_to_instances):
        for instance in definition.instances:
            to_skip = False
            for inner_pin, outer_pin in instance.outer_pins.items():
                if inner_pin.wire is None:
                    to_skip = True
                break
            if to_skip:
                continue
            if instance.definition not in definition_count:
                definition_count[instance.definition] = 1
                definition_to_instances[instance.definition] = [instance]
            else:
                definition_count[instance.definition] += 1
                definition_to_instances[instance.definition].append(instance)
            self.trace(instance.definition, definition_count, definition_to_instances)
        pass

    def run(self, ir):
        definition_count = dict()
        definition_copies = dict()
        definition_to_instances = dict()
        self.test(ir, definition_count, definition_to_instances)
        for key, value in definition_count.items():
                definition_copies[key] = self._make_definition_copy(key, value - 1)
        finished = True
        lest = 0
        wanted = None
        for key, value in definition_count.items():
            if value == 1:
                continue
            finished = False
            if lest == 0:
                lest = value
                wanted = key
            elif value < lest:
                lest = value
                wanted = key
        while not finished:
            while len(definition_copies[wanted]) > 0:
                definition = definition_copies[wanted].pop()
                instance = definition_to_instances[wanted].pop()
                instance.definition = definition
            print()
            definition_count = dict()
            definition_to_instances = dict()
            self.test(ir, definition_count, definition_to_instances)
            finished = True
            lest = 0
            wanted = None
            for key, value in definition_count.items():
                if value == 1:
                    continue
                finished = False
                if lest == 0:
                    lest = value
                    wanted = key
                elif value < lest:
                    lest = value
                    wanted = key
        for key, value in definition_copies.items():
            if len(value) != 0:
                raise Exception


    def _make_definition_copy(self, definition, num_of_copies):
        definition_copys = list()
        for x in range(num_of_copies):
            instance_map = dict()
            port_map = dict()
            definition_copy = Definition()
            save = ""
            for key, value in definition._metadata.items():
                definition_copy.__setitem__(key, value)
                if key == "EDIF.identifier":
                    save = value
            definition_copy.__setitem__("EDIF.identifier", save + "_" + str(x))
            for port in definition.ports:
                new_port = definition_copy.create_port()
                for key, value in port._metadata.items():
                    new_port.__setitem__(key, value)
                new_port.direction = port.direction
                new_port.initialize_pins(len(port.inner_pins))
                if hasattr(port, "is_array"):
                    new_port.is_array = port.is_array
                port_map[port] = new_port
            for instance in definition.instances:
                new_instance = definition_copy.create_instance()
                for key, value in instance._metadata.items():
                    new_instance.__setitem__(key, value)
                new_instance.definition = instance.definition
                for inner_pin, outer_pin in instance.outer_pins.items():
                    new_outer_pin = OuterPin()
                    new_outer_pin.inner_pin = inner_pin
                    new_outer_pin.instance = new_instance
                    new_instance.outer_pins[inner_pin] = new_outer_pin
                instance_map[instance] = new_instance
            for cable in definition.cables:
                new_cable = definition_copy.create_cable()
                for key, value in cable._metadata.items():
                    new_cable.__setitem__(key, value)
                for wire in cable.wires:
                    new_wire = new_cable.create_wire()
                    for pin in wire.pins:
                        if isinstance(pin, OuterPin):
                            test = instance_map[pin.instance]
                            test = test.outer_pins[pin.inner_pin]
                            new_wire.connect_pin(test)
                        else:
                            port = port_map[pin.port]
                            if hasattr(port, "is_array"):
                                for y in range(len(pin.port.inner_pins)):
                                    if pin is pin.port.inner_pins[y]:
                                        break
                                new_wire.connect_pin((port.inner_pins[y]))
                                pass
                            else:
                                new_wire.connect_pin(port.inner_pins[0])

            for y in range(len(definition.library.definitions)):
                if definition == definition.library.definitions[y]:
                    break
            definition.library.add_definition(definition_copy, y)
            definition_copys.append(definition_copy)
        return definition_copys


from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif
if __name__ == '__main__':
    parser = EdifParser.from_filename("TMR_hierarchy.edf")
    parser.parse()
    ir = parser.netlist
    work = Uniquifier()
    # test = util.get_leaf_cells(ir)
    test = work.run(ir)
    composer = ComposeEdif()
    composer.run(ir, "TMR_hierarchy_out.edf")
    print()