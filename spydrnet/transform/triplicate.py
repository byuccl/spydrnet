from spydrnet.ir import *
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif


#TODO rename file and class
class Triplicater:

    # num_of_replications: The number of replications desired
    # ex. 2 will end with 3 instnaces of cells, 1 original and 2 replications
    def __init__(self, num_of_replications=None):
        self.cells = dict()
        self.unconnectedPins = dict()
        if num_of_replications is None:
            self.num_of_replications = 2
        else:
            self.num_of_replications = num_of_replications - 1

    # target: a list of cells  to replicate
    # ir: intermediate representation
    def run(self, target, ir=None):
        if target is None:
            return ir
        self._process_ir_(ir)
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
                self._add_suffix(instance, "_TMR_" + str(loop))
                self.cells[cell].parent_definition.add_instance(instance)
                foo[self.cells[cell]] = instance
            added_cells.append(foo)
        return added_cells

    # Adds a suffix to a given object identifiers
    def _add_suffix(self, obj, suffix):
        metadata = obj._metadata
        if "EDIF.identifier" in metadata:
            obj.__setitem__("EDIF.identifier", metadata["EDIF.identifier"] + suffix)
        if "EDIF.original_identifier" in metadata:
            obj.__setitem__("EDIF.original_identifier", metadata["EDIF.original_identifier"] + suffix)

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
        self._copy_outer_pin_(new_instance, instance)

        return new_instance

    # Add outer pins for new_instance using instance as template
    def _copy_outer_pin_(self, new_instance, instance):
        pins = dict()
        for inner_pin, outer_pin in instance.outer_pins.items():
            pins[inner_pin] = OuterPin()
            pins[inner_pin].inner_pin = inner_pin
            pins[inner_pin].instance = new_instance
        new_instance.outer_pins = pins

    # Connect added cells together and make sure they have drivers
    def _connect_nets_(self, target, added_cells):
        cables = self._identify_cables_(target)
        replication = 0
        for group in added_cells:
            for cable in cables:
                metadata = cable._metadata
                new_cable = Cable()
                if "EDIF.identifier" in metadata:
                    new_cable.__setitem__("EDIF.identifier", metadata["EDIF.identifier"])
                if "EDIF.original_identifier" in metadata:
                    new_cable.__setitem__("EDIF.original_identifier", metadata["EDIF.original_identifier"])
                self._add_suffix(new_cable, "_TMR_" + str(replication))
                inner_pin = self.get_inner_pins(cable)
                wire = new_cable.create_wire()
                for instance, pin in inner_pin.items():
                    if instance in group:
                        wire.connect_pin(group[instance].outer_pins[pin])
                cable.parent.add_cable(new_cable)
                if self._check_for_driver(wire):
                    self._connect_to_original_wire(cable.wires[0], wire)
            replication += 1

    # Get the all the inner pins of a cable
    # Return dictionary with instance as key and inner pins and values
    def get_inner_pins(self, cable):
        pins = dict()
        for wire in cable.wires:
            for pin in wire.pins:
                if isinstance(pin, InnerPin):
                    pass
                else:
                    pins[pin.instance] = pin.inner_pin
        return pins

    # Gets all the cables the the targeted cells are connected to
    def _identify_cables_(self, target):
        cables = set()
        for cell in target:
            instance = self.cells[cell]
            for inner_pin, outer_pin in instance.outer_pins.items():
                cables.add(self._get_cable_(outer_pin))
        return list(cables)

    # Pulls all the ports the the cable is connected to
    def _identify_ports_(self, cable):
        ports = list()
        for wire in cable.wires:
            for pin in wire.pins:
                if isinstance(pin, InnerPin):
                    continue
                ports.append(pin.inner_pin.port.__getitem__("EDIF.identifier"))
        return ports

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
            port = pin.inner_pin.port
            if port.direction.name == "OUT":
                return False
        # print("ERROR:", wire.cable.__getitem__("EDIF.identifier"), "is not driven")
        return True

    def _connect_to_original_wire(self, original_wire, wire):
        pins_ = dict()
        for pin in wire.pins:
            # pins_[pin.instance] = pin.inner_pin.port.__getitem__("EDIF.identifier")
            pins_[pin.instance] = pin
        for instance, pin in pins_.items():
            # original_wire.connect_pin(instance.get_pin(pin))
            original_wire.connect_pin(pin)
        # disconnect pins
        while wire.pins.__len__() > 0:
            wire.pins.pop(0)
        # print()

if __name__ == "__main__":
    filename = "fourBitCounter.edf"
    parser = EdifParser.from_filename(filename)
    parser.parse()
    ir = parser.netlist

    triplicater = Triplicater(2)
    # test = ["out_reg_0_", "out_reg_1_", "out_reg_2_", "out_reg_3_"]
    # test = ["out_0__i_1", "out_reg_0_", "out_1__i_1", "out_reg_1_", "out_2__i_1", "out_reg_2_", "out_3__i_1", "out_reg_3_"]
    # test = ["out_0__i_1", "out_reg_3_"]
    test = ["out_0__i_1", "out_reg_0_"]
    test = ["out_0__i_1", "out_reg_0_", "out_reg_1_"]
    # test = ["out_reg_0_"]
    triplicater.run(test, ir)
    # pr.print_stats(sort="tottime")
    compose = ComposeEdif()

    compose.run(ir, "test.edf")
