from spydrnet.ir import *
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif


class TMRInserter:
    def __init__(self):
        self.net = dict()
        self.voter_number = 0
        self.lut3 = None

    def run(self, target, ir=None):
        if ir is None or target is None:
            return
        self._preprocess(ir)
        for net in target:
            if self._determine_voter_type(self.net[net]) == 1:
                self._insert_reduction(net)
            else:
                self._insert_triplicate(net)

    def define_lut3(self, ir):
        my_lut_3 = Definition()
        my_lut_3['EDIF.identifier'] = 'LUT3'
        my_lut_3['EDIF.cellType'] = 'celltype'
        my_lut_3['EDIF.view.identifier'] = 'netlist'
        my_lut_3['EDIF.view.viewType'] = 'viewtype'
        my_port = my_lut_3.create_port()
        my_port.direction = Port.Direction.OUT
        my_port['metadata_prefix'] = ['EDIF']
        my_port['EDIF.identifier'] = 'O'
        my_port = my_lut_3.create_port()
        my_port.direction = Port.Direction.IN
        my_port['metadata_prefix'] = ['EDIF']
        my_port['EDIF.identifier'] = 'I0'
        my_port = my_lut_3.create_port()
        my_port.direction = Port.Direction.IN
        my_port['metadata_prefix'] = ['EDIF']
        my_port['EDIF.identifier'] = 'I1'
        my_port = my_lut_3.create_port()
        my_port.direction = Port.Direction.IN
        my_port['metadata_prefix'] = ['EDIF']
        my_port['EDIF.identifier'] = 'I2'
        ir.libraries[0].add_definition(my_lut_3)
        return my_lut_3

    # Process ir extracting identifier and map it to the cable
    def _preprocess(self, ir):
        has_lut3 = False
        for library in ir.libraries:
            for definition in library.definitions:
                if definition.__getitem__("EDIF.identifier") == "LUT3":
                    self.lut3 = definition
                    has_lut3 = True
                for cable in definition.cables:
                    self.net[cable.__getitem__("EDIF.identifier")] = cable
        if not has_lut3:
            self.lut3 = self.define_lut3(ir)

    # Insert three voter
    def _insert_triplicate(self, net):
        cables = self._generate_input(self.net[net], net)
        new_cable = list()
        for cable in cables:
            pin = self._get_net_driver(cable)
            new_cable.append(self.disconnect_pin(pin))
        definition = self.net[net].definition
        for cable in cables:
            voter = self.create_voter()
            definition.add_instance(voter)
            self.connect_voter(new_cable, cable, voter)

    # Insert a reduction voter
    def _insert_reduction(self, net):
        pin = self._get_net_driver(self.net[net])
        cable = self.disconnect_pin(pin)
        input = self._generate_input(cable, net)
        definition = self.net[net].definition
        voter = self.create_voter()
        definition.add_instance(voter)
        self.connect_voter(input, self.net[net], voter)

    # Returns a list of the original cable and the replicated cables
    def _generate_input(self, cable, net):
        tmr0_cable = cable.parent.lookup_element(Cable, "EDIF.identifier", net + "_TMR_1")
        tmr1_cable = cable.parent.lookup_element(Cable, "EDIF.identifier", net + "_TMR_2")
        return [cable, tmr0_cable, tmr1_cable]

    # Determine what can of voter needs to be inserted
    # Returns 0 if the replicate had driver
    # Returns 1 if the replicate does not have a driver
    def _determine_voter_type(self, net):
        tmr_0_cable = net.parent.lookup_element(Cable, "EDIF.identifier", net.__getitem__("EDIF.identifier") + "_TMR_1")
        wire = tmr_0_cable.wires[0]
        for pin in wire.pins:
            if pin.inner_pin.port.direction.name == "IN":
                return 0
        return 1

    # Disconnect the pin from it connected cable
    # pin: Outer_Pin
    # Return a cable connected to the disconnected pin
    def disconnect_pin(self, pin):
        wire = pin.wire
        wire.pins.remove(pin)
        temp = wire.cable.__getitem__("EDIF.identifier")
        pin.wire = None
        cable = Cable()
        new_wire = cable.create_wire()
        new_wire.connect_pin(pin)
        cable.__setitem__("EDIF.identifier", temp + "_voter")
        pin.instance.parent_definition.add_cable(cable)
        return cable

    # Creates a voter instance
    # Returns the voter
    def create_voter(self):
        voter = Instance()
        voter.__setitem__("EDIF.identifier", "voter_" + str(self._get_voter_number()))
        properties = list()
        property = dict()
        property["identifier"] = "INIT"
        property["value"] = "8'he8"
        properties.append(property)
        voter.__setitem__("EDIF.properties", properties)
        voter.definition = self.lut3
        outer_pins = dict()
        for port in self.lut3.ports:
            pin = OuterPin()
            pin.inner_pin = port.inner_pins[0]
            pin.instance = voter
            outer_pins[port.inner_pins[0]] = pin
        voter.outer_pins = outer_pins
        return voter

    # Return the number associated with the number
    def _get_voter_number(self):
        voter_number = self.voter_number
        self.voter_number += 1
        return str(voter_number)

    # input(list) what to connect to voter inputs
    # output(Wire) what to connect to voter output
    # voter voter to connect
    def connect_voter(self, inputs, output, voter):
        output_wire = output.wires[0]
        output_wire.connect_pin(voter.get_pin("O"))
        x = 0
        for input in inputs:
            wire = input.wires[0]
            wire.connect_pin(voter.get_pin("I" + str(x)))
            x += 1
        pass

    # Get the driver pin for a cable
    # Returns the pin
    def _get_net_driver(self, cable):
        _ = cable.wires[0]
        for pin in cable.wires[0].pins:
            if pin.inner_pin.port.direction.name == "OUT":
                return pin
        pass


if __name__ == "__main__":
    filename = "fourBitCounter.edf"
    out_filename = "fourBitCounter_insert.edf"
    parser = EdifParser.from_filename(filename)
    parser.parse()
    ir = parser.netlist

    inserter = TMRInserter()
    voter_locations = ["out_OBUF_0_", "out_OBUF_1_"]
    inserter.run(voter_locations, ir)
    compose = ComposeEdif()

    compose.run(ir, out_filename)
