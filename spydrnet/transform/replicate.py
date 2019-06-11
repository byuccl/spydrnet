from spydrnet.composers.edif.composer import ComposeEdif
from spydrnet.ir import *
from spydrnet.parsers.edif.parser import EdifParser


# TODO rename file and class
class Replicator:

    # num_of_replications: The number of replications desired
    # ex. 2 will end with 3 instnaces of cells, 1 original and 2 replications
    def __init__(self, num_of_replications=None):
        self.cells = dict()
        self.unconnectedPins = dict()
        self.ir = None
        self.ports = None
        if num_of_replications is None:
            self.num_of_replications = 2
        else:
            self.num_of_replications = num_of_replications - 1

    # target: a list of cells  to replicate
    # ir: intermediate representation
    def run(self, target, ir=None):
        if target is None:
            return ir
        self.ir = ir
        self._process_ir_(ir)
        self.replicate_ports(target)
        added_cells = self._replicate_cells_(target)
        self._connect_nets_(target, added_cells)
        return ir

    # Replicate every cell found in cell
    # Return a list containing all the added cells
    def _replicate_cells_(self, target):
        added_cells = list()
        for loop in range(self.num_of_replications):
            foo = dict()
            for cell in target:
                instance = self._copy_instance_(self.cells[cell])
                self._add_suffix(instance, "_TMR_" + str(loop + 1))
                self.cells[cell].parent_definition.add_instance(instance)
                foo[self.cells[cell]] = instance
            added_cells.append(foo)
        return added_cells

    # Adds a suffix to a given object identifiers
    def _add_suffix(self, obj, suffix):
        metadata = obj._metadata
        if "EDIF.identifier" in metadata:
            obj.__setitem__("EDIF.identifier", obj.__getitem__("EDIF.identifier") + suffix)
        if "EDIF.original_identifier" in metadata:
            section = obj.__getitem__("EDIF.original_identifier").split('[', )
            obj.__setitem__("EDIF.original_identifier", section[0] + suffix + '[' + section[1])

    # Makes a copy of instance
    def _copy_instance_(self, instance):
        new_instance = Instance()
        metadata = instance._metadata
        if "EDIF.identifier" in metadata:
            new_instance.__setitem__("EDIF.identifier", metadata["EDIF.identifier"])
        if "EDIF.original_identifier" in metadata:
            new_instance.__setitem__("EDIF.original_identifier", metadata["EDIF.original_identifier"])
        self._copy_properties_(new_instance, instance)
        new_instance.definition = instance.definition
        self._create_outer_pin_(new_instance, instance)

        return new_instance

    # Add outer pins for new_instance using instance as template
    def _create_outer_pin_(self, new_instance, instance):
        pins = dict()
        for inner_pin, outer_pin in instance.outer_pins.items():
            pins[inner_pin] = OuterPin()
            pins[inner_pin].inner_pin = inner_pin
            pins[inner_pin].instance = new_instance
        new_instance.outer_pins = pins

    # Create a new cable with the same identifiers and add a suffix
    def create_cable(self, cable, num):
        metadata = cable._metadata
        new_cable = Cable()
        if "EDIF.identifier" in metadata:
            new_cable.__setitem__("EDIF.identifier", metadata["EDIF.identifier"])
        if "EDIF.original_identifier" in metadata:
            new_cable.__setitem__("EDIF.original_identifier", metadata["EDIF.original_identifier"])
        self._add_suffix(new_cable, "_TMR_" + str(num))
        return new_cable

    def connect_cable_to_cells(self, cable, group, new_wire):
        for pin in cable.wires[0].pins:
            if isinstance(pin, InnerPin):
                continue
            try:
                new_wire.connect_pin(group[pin.instance].outer_pins[pin.inner_pin])
            except KeyError:
                pass

    def is_connected_to_replicate_pin(self, cable):
        for pin in cable.wires[0].pins:
            if isinstance(pin, OuterPin):
                if pin.inner_pin.port in self.ports:
                    return True
            else:
                if pin.port in self.ports:
                    return True
        return False

    def connect_cable_to_port(self, cable, num, new_wire):
        num_ = num - 1
        for pin in cable.wires[0].pins:
            if isinstance(pin, OuterPin):
                if pin.inner_pin.port in self.ports:
                    test = self.ports[pin.inner_pin.port][num_]
                    position = self.port_position(pin.inner_pin, pin.inner_pin.port)
                    outer_pin = OuterPin()
                    outer_pin.inner_pin = test.inner_pins[position]
                    outer_pin.instance = pin.instance
                    new_wire.connect_pin(outer_pin)
            else:
                if pin.port in self.ports:
                    test = self.ports[pin.port][num_]
                    position = self.port_position(pin, pin.port)
                    new_wire.connect_pin(test.inner_pins[position])

    # Connect added cells together and make sure they have drivers
    def _connect_nets_(self, target, added_cells):
        cables = self._identify_cables_(target)
        replication = 1
        for group in added_cells:
            for cable in cables:
                # create new cable
                new_cable = self.create_cable(cable, replication)
                new_wire = new_cable.create_wire()
                # connect new cable to replicated cells
                self.connect_cable_to_cells(cable, group, new_wire)
                # if cable connected to replicated port
                if self.is_connected_to_replicate_pin(cable):
                    # connect to replicated port
                    self.connect_cable_to_port(cable, replication, new_wire)
                    # add new cable to IR
                    # cable.parent.add_cable(new_cable)
                # elif port is driver
                if self._check_for_driver(new_wire):
                    # change cable to connect to new cable pins
                    self._connect_to_original_wire(cable.wires[0], new_wire)
                # else
                else:
                    # add new cable to IR
                    cable.parent.add_cable(new_cable)
            replication += 1

    def connect_cable(self, wire):
        for pin in wire.pins:
            if isinstance(pin, InnerPin):
                continue
            if pin.inner_pin.port not in self.ports:
                continue
            port = pin.inner_pin.port
            x = self.port_position(pin.inner_pin, port)
            ports = self.ports[port]
            for port in ports:
                outer_pin = self.find_other_side(port.inner_pins[x])
                if outer_pin is None:
                    outer_pin = OuterPin()
                    outer_pin.inner_pin = port.inner_pins[x]
                    outer_pin.instance = pin.instance

                wire.connect_pin(outer_pin)

    def port_position(self, pin, port):
        for x in range(len(port.inner_pins)):
            if port.inner_pins[x] == pin:
                return x

    # Gets all the cables the the targeted cells are connected to
    def _identify_cables_(self, target):
        cables = set()
        for cell in target:
            instance = self.cells[cell]
            for inner_pin, outer_pin in instance.outer_pins.items():
                cable = self._get_cable_(outer_pin)
                cables = cables.union(self.trace_cable(cable))
                cables.add(cable)
        return list(cables)

    def trace_cable(self, cable):
        cables = set()
        stack = list()
        stack.append(cable)
        while len(stack) != 0:
            cable_ = stack.pop()
            for pin in cable_.wires[0].pins:
                if isinstance(pin, OuterPin):
                    pin_ = pin.inner_pin
                    if pin_.wire is None:
                        continue
                else:
                    pin_ = self.find_other_side(pin)
                    if pin_ is None:
                        continue
                if pin_.wire != cable_.wires[0]:
                    if pin_.wire.cable not in cables:
                        stack.append(pin_.wire.cable)
                    cables.add(cable_)

        return cables

    def _get_cable_(self, outer_pin):
        return outer_pin.wire.cable

    # Copy the properties from original_instance to instance
    def _copy_properties_(self, instance, original_instance):
        properties = list()
        if "EDIF.properties" not in original_instance._metadata:
            return
        for prop in original_instance._metadata["EDIF.properties"]:
            properties.append(prop.copy())
        instance.__setitem__("EDIF.properties", properties)

    # Process given ir creating a dictionary from name to the instance with the same name
    def _process_ir_(self, ir):
        for library in ir.libraries:
            for definition in library.definitions:
                for instance in definition.instances:
                    self.cells[instance._metadata["EDIF.identifier"]] = instance

    # Checks if given wire is driven
    # Returns true if the wire is not driven false otherwise
    def _check_for_driver(self, wire):
        for pin in wire.pins:
            if isinstance(pin, OuterPin):
                port = pin.inner_pin.port
                if port.direction == Port.Direction.OUT:
                    return False
            else:
                port = pin.port
                if port.direction == Port.Direction.IN:
                    return False
        return True

    def _connect_to_original_wire(self, original_wire, wire):
        for pin in wire.pins:
            original_wire.connect_pin(pin)
        while len(wire.pins) > 0:
            wire.pins.pop(0)

    def replicate_ports(self, target):
        in_port = set()
        out_port = set()
        ports = dict()
        for temp in target:
            cell = self.cells[temp]
            for blank, pin in cell.outer_pins.items():
                if pin.inner_pin.port.direction == Port.Direction.OUT:
                    out_port = out_port.union(self.trace_pin(pin))
                else:
                    in_port = in_port.union(self.trace_pin(pin))
        ports_to_replicate = in_port.intersection(out_port)
        for port in ports_to_replicate:
            ports[port] = list()
        for x in range(1, self.num_of_replications + 1):
            for port in ports_to_replicate:
                new_port = self.replicate_port(port, x)
                ports[port].append(new_port)
        self.ports = ports
        pass

    def replicate_port(self, port, x):
        definition = port.definition
        new_port = definition.create_port()
        new_port.__setitem__("metadata_prefix", ["EDIF"])
        new_port.__setitem__("EDIF.identifier", port._metadata["EDIF.identifier"] + "_TMR_" + str(x))
        new_port.initialize_pins(port.inner_pins.__len__())
        if hasattr(port, "is_array"):
            new_port.is_array = True
        new_port.direction = port.direction
        return new_port

    def trace_pin(self, pin):
        stack = list()
        port = set()
        trash = set()
        stack.append(pin)
        trash.add(pin)
        stack.pop()
        for pin_ in pin.wire.pins:
            if pin_ == pin:
                continue
            stack.append(pin_)
            trash.add(pin_)
        while len(stack) != 0:
            pin = stack.pop()
            for pin_ in pin.wire.pins:
                if pin_ not in trash:
                    stack.append(pin_)
                    trash.add(pin_)
            if isinstance(pin, OuterPin):
                if pin.inner_pin.wire is not None:
                    port.add(pin.inner_pin.port)
                    if pin.inner_pin not in trash:
                        stack.append(pin.inner_pin)
                        trash.add(pin.inner_pin)
            else:
                if pin.wire is not None:
                    port.add(pin.port)
                    test = self.find_other_side(pin)
                    stack.append(test)
        return port
        pass

    def find_other_side(self, pin):
        for library in self.ir.libraries:
            for definition in library.definitions:
                for cable in definition.cables:
                    for wire in cable.wires:
                        for pin_ in wire.pins:
                            if isinstance(pin_, InnerPin):
                                continue
                            if pin_.inner_pin == pin:
                                return pin_

            pass


if __name__ == "__main__":
    filename = "fourBitCounter.edf"
    parser = EdifParser.from_filename(filename)
    parser.parse()
    ir = parser.netlist

    triplicater = Replicator(2)
    # test = ["out_reg_0_", "out_reg_1_", "out_reg_2_", "out_reg_3_"]
    # test = ["out_0__i_1", "out_reg_0_", "out_1__i_1", "out_reg_1_",
    # "out_2__i_1", "out_reg_2_", "out_3__i_1", "out_reg_3_"]
    # test = ["out_0__i_1", "out_reg_3_"]
    # test = ["out_0__i_1", "out_reg_0_"]
    test = ["out_0__i_1", "out_reg_0_", "out_reg_1_"]
    # test = ["out_reg_0_"]
    triplicater.run(test, ir)
    # pr.print_stats(sort="tottime")
    compose = ComposeEdif()

    compose.run(ir, "test.edf")
