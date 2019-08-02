from spydrnet.ir import *
import spydrnet.utility.utility as util
from spydrnet.utility.HierarchicalLookup import HierarchicalLookup
from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.composers.edif.composer import ComposeEdif

class DWCInserter:

    def __init__(self):
        self.net = dict()
        self.comparator_number = 0
        self.lookup = None

    def run(self, target, ir):
        self._preprocess(ir)
        test = list()
        for net in target:
            self._place_comparator(net)
            if self.net[net].definition is ir.top_instance.definition:
                test.append(self.net[net])
        self._place_black_box(ir)

    def _place_black_box(self, ir):
        black_box = Definition()
        black_box['EDIF.identifier'] = ' dwc_jtag_interface'
        black_box['EDIF.cellType'] = 'celltype'
        black_box['EDIF.view.identifier'] = 'netlist'
        black_box['EDIF.view.viewType'] = 'viewtype'
        I0 = black_box.create_port()
        I0.direction = Port.Direction.IN
        I0['metadata_prefix'] = ['EDIF']
        I0['EDIF.identifier'] = 'I0'
        I1 = black_box.create_port()
        I1.direction = Port.Direction.IN
        I1['metadata_prefix'] = ['EDIF']
        I1['EDIF.identifier'] = 'I1'
        ir.top_instance.definition.library.add_definition(black_box, 0)
        black_box_instance = Instance()
        black_box_instance.definition = black_box
        black_box_instance['EDIF.identifier'] = 'dwc_jtag_interface'
        ir.top_instance.definition.add_instance(black_box_instance)
        dwc_pair = self._get_dwc_object(ir)
        for x in range(len(dwc_pair[0][0])):
            self._connect_black_box('DWC_0', I0, dwc_pair[0][0][x], x, black_box_instance, ir)
            self._connect_black_box('DWC_1', I1, dwc_pair[0][1][x], x, black_box_instance, ir)

        wire_pair = self._get_top_dwc_cable(ir)
        for pair in wire_pair:
            temp = list(pair)
            temp[0].connect_pin(self._create_outer_pin(I0.create_pin(), black_box_instance))
            temp[1].connect_pin(self._create_outer_pin(I1.create_pin(), black_box_instance))

        if len(I0.inner_pins) > 1:
            I0.is_array = True
            I1.is_array = True

    def _connect_black_box(self, dwc, port, pin, num, black_box, ir):
        dwc_cable = Cable()
        dwc_wire = dwc_cable.create_wire()
        dwc_cable['EDIF.identifier'] = dwc + '_' + str(num) + '_'
        dwc_cable['EDIF.origiinal_identifier'] = dwc + '[' + str(num) + ']'
        dwc_wire.connect_pin(pin)
        black_box_pin = port.create_pin()
        dwc_wire.connect_pin(self._create_outer_pin(black_box_pin, black_box))
        dwc_cable.comparator = pin.inner_pin.wire.cable.comparator
        ir.top_instance.definition.add_cable(dwc_cable)

    def _get_top_dwc_cable(self, ir):
        cable_pair = list()
        temp = list()
        for instance in ir.top_instance.definition.instances:
            if instance['EDIF.identifier'][0:10] == 'comparator':
                if {instance, instance.partner_comparator} not in temp:
                    temp.append({instance, instance.partner_comparator})
        for pair in temp:
            for instance in pair:
                port1 = instance.definition.lookup_element(Port, 'EDIF.identifier', 'O')
                port2 = instance.partner_comparator.definition.lookup_element(Port, 'EDIF.identifier', 'O')
                cable_pair.append([instance.outer_pins[port1.inner_pins[0]].wire, instance.partner_comparator.outer_pins[port2.inner_pins[0]].wire])
                break
        return cable_pair

    def _create_outer_pin(self, pin, instance):
        new_pin = OuterPin()
        new_pin.inner_pin = pin
        new_pin.instance = instance
        instance.outer_pins[pin] = new_pin
        return new_pin

    def _define_lut2(self, ir):
        my_lut_2 = Definition()
        my_lut_2['EDIF.identifier'] = 'LUT3'
        my_lut_2['EDIF.cellType'] = 'celltype'
        my_lut_2['EDIF.view.identifier'] = 'netlist'
        my_lut_2['EDIF.view.viewType'] = 'viewtype'
        my_port = my_lut_2.create_port()
        my_port.direction = Port.Direction.OUT
        my_port['metadata_prefix'] = ['EDIF']
        my_port['EDIF.identifier'] = 'O'
        my_port = my_lut_2.create_port()
        my_port.direction = Port.Direction.IN
        my_port['metadata_prefix'] = ['EDIF']
        my_port['EDIF.identifier'] = 'I0'
        my_port = my_lut_2.create_port()
        my_port.direction = Port.Direction.IN
        my_port['metadata_prefix'] = ['EDIF']
        my_port['EDIF.identifier'] = 'I1'
        ir.libraries[0].add_definition(my_lut_2)
        return my_lut_2
    pass

    # Process ir extracting identifier and map it to the cable
    def _preprocess(self, ir):
        has_lut2 = False
        for library in ir.libraries:
            for definition in library.definitions:
                if definition.__getitem__("EDIF.identifier") == "LUT2":
                    self.lut2 = definition
                    has_lut2 = True
                for cable in definition.cables:
                    self.net[cable.__getitem__("EDIF.identifier")] = cable
        if not has_lut2:
            self.lut2 = self.define_lut2(ir)
        self.lookup = HierarchicalLookup(ir)

    def _place_comparator(self, net):
        comparator_1 = self._create_comparator()
        out_cable_1 = self._connect_comparator(net, comparator_1)
        comparator_2 = self._create_comparator()
        out_cable_2 = self._connect_comparator(net, comparator_2)
        definition = self.net[net].definition
        definition.add_instance(comparator_1)
        definition.add_instance(comparator_2)
        comparator_1.partner_comparator = comparator_2
        comparator_2.partner_comparator = comparator_1
        self._rout_to_top_instance(out_cable_1, out_cable_2)

    def _create_comparator(self):
        comparator = Instance()
        comparator['EDIF.identifier'] = "comparator" + str(self.comparator_number)
        self.comparator_number += 1
        properties = list()
        property = dict()
        property['identifier'] = "INIT"
        property['value'] = "8'h6"
        properties.append(property)
        comparator['EDIF.properties'] = properties
        comparator.definition = self.lut2
        outer_pins = dict()
        for port in self.lut2.ports:
            pin = OuterPin()
            pin.inner_pin = port.inner_pins[0]
            pin.instance = comparator
            outer_pins[port.inner_pins[0]] = pin
        comparator.outer_pins = outer_pins
        return comparator

    def _connect_comparator(self, net, comparator):
        cable = self.net[net]
        dwc_cable = cable.parent.lookup_element(Cable, "EDIF.identifier", net + "_TMR_1")
        cable.wires[0].connect_pin(comparator.get_pin("I0"))
        dwc_cable.wires[0].connect_pin(comparator.get_pin("I1"))
        out_cable = cable.parent.create_cable()
        out_wire = out_cable.create_wire()
        out_cable['EDIF.identifier'] = comparator['EDIF.identifier'] + "_DWC_OUT"
        out_wire.connect_pin(comparator.get_pin("O"))
        out_cable.comparator = comparator
        return out_cable

    def _rout_to_top_instance(self, cable_1, cable_2):
        comparator_1 = cable_1.comparator
        comparator_2 = cable_2.comparator
        name = util.get_hierarchical_name(cable_1)
        self.lookup.rebuild()
        trace = self.lookup.get_cable_from_name(name)
        trace.pop()
        if len(trace) == 0:
            return
        instance = trace.pop()
        try:
            dwc_0_port = instance.definition.lookup_element(Port, "EDIF.identifier", "DWC_0")
            dwc_0_port.is_array = True
        except:
            dwc_0_port = instance.definition.create_port()
            dwc_0_port.direction = Port.Direction.OUT
            dwc_0_port["EDIF.identifier"] = "DWC_0"
        try:
            dwc_1_port = instance.definition.lookup_element(Port, "EDIF.identifier", "DWC_1")
            dwc_1_port.is_array = True
        except:
            dwc_1_port = instance.definition.create_port()
            dwc_1_port.direction = Port.Direction.OUT
            dwc_1_port["EDIF.identifier"] = "DWC_1"
        dwc_0_pin = dwc_0_port.create_pin()
        dwc_1_pin = dwc_1_port.create_pin()
        cable_1.wires[0].connect_pin(dwc_0_pin)
        cable_2.wires[0].connect_pin(dwc_1_pin)
        dwc_0_out_pin = OuterPin()
        dwc_0_out_pin.inner_pin = dwc_0_pin
        dwc_0_out_pin.instance = instance

        dwc_1_out_pin = OuterPin()
        dwc_1_out_pin.inner_pin = dwc_1_pin
        dwc_1_out_pin.instance = instance

        while len(trace) > 0:
            instance = trace.pop()
            dwc_0_cable = Cable()
            dwc_0_cable['EDIF.identifier'] = instance['EDIF.identifier'] + "_DWC_0_" + str(len(dwc_0_port.inner_pins) - 1) + "_"
            temp = instance['EDIF.identifier'] + "_DWC_0[" + str(len(dwc_0_port.inner_pins) - 1) + "]"
            dwc_0_cable['EDIF.original_identifier'] = temp
            dwc_0_cable.comparator = comparator_1
            instance.definition.add_cable(dwc_0_cable)
            dwc_0_cable.create_wire().connect_pin(dwc_0_out_pin)
            dwc_1_cable = Cable()
            dwc_1_cable['EDIF.identifier'] = instance['EDIF.identifier'] + "_DWC_1_" + str(len(dwc_1_port.inner_pins) - 1) + "_"
            temp = instance['EDIF.identifier'] + "_DWC_1[" + str(len(dwc_1_port.inner_pins) - 1) + "]"
            dwc_1_cable['EDIF.original_identifier'] = temp
            dwc_1_cable.create_wire().connect_pin(dwc_1_out_pin)
            dwc_1_cable.comparator = comparator_2
            instance.definition.add_cable(dwc_1_cable)

            try:
                dwc_0_port = instance.definition.lookup_element(Port, "EDIF.identifier", "DWC_0")
            except:
                dwc_0_port = instance.definition.create_port()
                dwc_0_port.direction = Port.Direction.OUT
                dwc_0_port["EDIF.identifier"] = "DWC_0"
            try:
                dwc_1_port = instance.definition.lookup_element(Port, "EDIF.identifier", "DWC_1")
            except:
                dwc_1_port = instance.definition.create_port()
                dwc_1_port.direction = Port.Direction.OUT
                dwc_1_port["EDIF.identifier"] = "DWC_1"
            dwc_0_pin = dwc_0_port.create_pin()
            dwc_1_pin = dwc_1_port.create_pin()
            dwc_0_cable.wires[0].connect_pin(dwc_0_pin)
            dwc_1_cable.wires[0].connect_pin(dwc_1_pin)
            dwc_0_out_pin = OuterPin()
            dwc_0_out_pin.inner_pin = dwc_0_pin
            dwc_0_out_pin.instance = instance

            dwc_1_out_pin = OuterPin()
            dwc_1_out_pin.inner_pin = dwc_1_pin
            dwc_1_out_pin.instance = instance

        pass

    def _get_dwc_object(self, ir):
        top_instance = ir.top_instance
        dwc_pairs = list()
        for instance in top_instance.definition.instances:
            try:
                dwc_0_port = instance.definition.lookup_element(Port, "EDIF.identifier", "DWC_0")
                dwc_0_pins = list()
                dwc_1_port = instance.definition.lookup_element(Port, "EDIF.identifier", "DWC_1")
                dwc_1_pins = list()
                for pin in dwc_0_port.inner_pins:
                    if pin not in instance.outer_pins.keys():
                        new_pin = OuterPin()
                        new_pin.inner_pin = pin
                        new_pin.instance = instance
                        dwc_0_pins.append(new_pin)
                    else:
                        dwc_0_pins.append(instance.outer_pins[pin])
                for pin in dwc_1_port.inner_pins:
                    if pin not in instance.outer_pins.keys():
                        new_pin = OuterPin()
                        new_pin.inner_pin = pin
                        new_pin.instance = instance
                        dwc_1_pins.append(new_pin)
                    else:
                        dwc_1_pins.append(instance.outer_pins[pin])
                dwc_pairs.append([dwc_0_pins, dwc_1_pins])
            except:
                pass
        return dwc_pairs
