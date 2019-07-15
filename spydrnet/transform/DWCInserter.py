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
        for net in target:
            self._place_comparator(net)

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
            # dwc_0_cable = instance.definition.create_cable()
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