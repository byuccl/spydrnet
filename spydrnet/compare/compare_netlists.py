from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.ir import OuterPin
import sys
import logging
import time

# filename_orig = r"seven_segment_decoder.edf"
# filename_composer = r"fourBitCounter_inverted.edf"
# filename_composer = r"seven_segment_decoder_composed.edf"


# filename_composer = r"fourBitCounter_composed.edf"

class Comparer:

    def __init__(self, filename_orig, filename_composer):
        if filename_orig is None:
            raise Exception('filename cannot be None')
        elif filename_composer is None:
            raise Exception('outfileName cannot be none')
        self.filename_orig = filename_orig
        self.filename_composer = filename_composer


    def run(self):
        # logging.basicConfig(level=# logging.INFO, format="%(levelname)s - %(message)s")

        # parse original
        print("Reading original EDIF")
        parser_orig = EdifParser.from_filename(self.filename_orig)
        parser_orig.parse()
        ir_orig = parser_orig.netlist

        # parse composed
        print("Reading composed EDIF")
        parser_composer = EdifParser.from_filename(self.filename_composer)
        parser_composer.parse()
        ir_composer = parser_composer.netlist

        # compare netlists
        time.sleep(0.01)
        print("Comparing read EDIFs")
        self.compare(ir_orig, ir_composer)
        time.sleep(0.01)
        print("The edf files contain the same circuit")


    def compare(self, ir_orig, ir_composer):
        if self.get_identifier(ir_orig) != self.get_identifier(ir_composer):
            # logging.error("Environments do not have the same identifier")
            raise Exception("Environments do not have the same identifier")

        if ir_orig.top_instance is None:
            # logging.warning("Parser gave NoneType for top_instance")
            pass
        self.compare_instances(ir_orig.top_instance, ir_composer.top_instance)
        # elif ir_orig.top_instance != ir_composer.top_instance:
        #     # logging.error("Top instance is not the same")
        #     raise Exception("Top instance is not the same")
        print()
        if ir_orig.libraries.__len__() != ir_composer.libraries.__len__():
            # logging.error("Environments do not have the same number of libraries")
            raise Exception("Environments do not have the same number of libraries")
        for x in range(ir_orig.libraries.__len__()):
            # logging.info("Checking %d out of %d libraries", x + 1, ir_orig.libraries.__len__())
            self.compare_libraries(ir_orig.libraries[x], ir_composer.libraries[x])


    def compare_libraries(self, library_orig, library_composer):
        if self.get_identifier(library_orig) != self.get_identifier(library_composer):
            # logging.error("Libraries do not have the same identifier")
            raise Exception("Libraries do not have the same identifier")
        if library_orig.definitions.__len__() != library_composer.definitions.__len__():
            # logging.error("Libraries do not have the same amount of definitions")
            raise Exception("Libraries do not have the same amount of definitions")
        for definition in range(library_orig.definitions.__len__()):
            # logging.info("Checking %d out of %d definition in %s", definition + 1, library_orig.definitions.__len__(),
            #             self.get_identifier(library_orig))
            x = self.search_list(library_composer.definitions, library_orig.definitions[definition])
            self.compare_definition(library_orig.definitions[definition], library_composer.definitions[x])


    def compare_definition(self, definition_orig, definition_composer, check_identifier=True):
        if check_identifier:
            if self.get_identifier(definition_orig) != self.get_identifier(definition_composer):
                # logging.error("Definitions do not have the same identifier")
                # logging.error("%s compared to %s", self.get_identifier(definition_orig),
                #              self.get_identifier(definition_composer))
                raise Exception("Definitions do not have the same identifier")

        # Checking the cables
        if definition_orig.cables.__len__() != definition_composer.cables.__len__():
            # logging.error("Definitions do not have the same number of cables")
            raise Exception("Definitions do not have the same number of cables")
        for cable in range(definition_orig.cables.__len__()):
            # logging.info("Checking %d out of %d cables in %s", cable + 1, definition_orig.cables.__len__(),
            #             self.get_identifier(definition_orig))
            x = self.search_list(definition_composer.cables, definition_orig.cables[cable])
            if x == -1:
                # logging.error("Cables do not have the same identifier")
                raise Exception("Cables do not have the same identifier")
            self.compare_cables(definition_orig.cables[cable], definition_composer.cables[x])

        # Checking the instances
        if definition_orig.instances.__len__() != definition_composer.instances.__len__():
            # logging.error("Definitions do not have the same number of instances")
            raise Exception("Definitions do not have the same number of instances")
        for instance in range(definition_orig.instances.__len__()):
            # logging.info("Checking %d out of %d instances in %s", instance + 1, definition_orig.instances.__len__(),
            #             self.get_identifier(definition_orig))
            x = self.search_list(definition_composer.instances, definition_orig.instances[instance])
            if x == -1:
                # logging.error("Instances do not have the same identifier")
                raise Exception("Instances do not have the same identifier")
            self.compare_instances(definition_orig.instances[instance], definition_composer.instances[x])

        # Checking the ports
        if definition_orig.ports.__len__() != definition_composer.ports.__len__():
            # logging.error("Definitions do not have the same number of ports")
            raise Exception("Definitions do not have the same number of ports")
        for port in range(definition_orig.ports.__len__()):
            # logging.info("Checking %d out of %d ports in %s", port + 1, definition_orig.ports.__len__(),
            #             self.get_identifier(definition_orig))
            x = self.search_list(definition_composer.ports, definition_orig.ports[port])
            if x == -1:
                # logging.error("Ports do not have the same identifier")
                raise Exception("Ports do not have the same identifier")
            self.compare_ports(definition_orig.ports[port], definition_composer.ports[x])


    def compare_cables(self, cables_orig, cables_composer):
        if self.get_identifier(cables_orig) != self.get_identifier(cables_composer):
            # logging.error("Cables do not have the same identifier")
            raise Exception("Cables do not have the same identifier")
        if self.get_original_identifier(cables_orig) != self.get_original_identifier(cables_composer):
            # logging.error("Cables do not have the same original identifier")
            raise Exception("Cables do not have the same original identifier")
        if cables_orig.wires.__len__() != cables_composer.wires.__len__():
            # logging.error("Cables do not have the same number of wires")
            raise Exception("Cables do not have the same number of wires")
        # logging.info("Checking pins connected to %s", self.get_identifier(cables_orig))
        for x in range(cables_orig.wires.__len__()):
            for y in range(cables_orig.wires[x].pins.__len__()):
                pin_orig = cables_orig.wires[x].pins[y]
                pin_composer = cables_composer.wires[x].pins[y]
                if type(pin_orig) != type(pin_composer):
                    # logging.error("Pins are not of the same type")
                    raise Exception("Environments do not have the same number of libraries")
                if isinstance(pin_orig, OuterPin):
                    self.compare_outer_pins(pin_orig, pin_composer)
                else:
                    self.compare_inner_pins(pin_orig, pin_composer)


    def compare_outer_pins(self, pin_orig, pin_composer):
        if self.get_identifier(pin_orig.instance) != self.get_identifier(pin_composer.instance):
            # logging.error("Net does not connect the same ports")
            raise Exception("Net does not connect the same ports")
        if self.get_identifier(pin_orig.inner_pin.port) != self.get_identifier(pin_composer.inner_pin.port):
            # logging.error("Net does not connect the same ports")
            raise Exception("Net does not connect the same ports")
        for orig in range(pin_orig.inner_pin.port.inner_pins.__len__()):
            if pin_orig.inner_pin.port.inner_pins[orig] == pin_orig.inner_pin:
                break
        for compose in range(pin_composer.inner_pin.port.inner_pins.__len__()):
            if pin_composer.inner_pin.port.inner_pins[compose] == pin_composer.inner_pin:
                break
        if compose != orig:
            # logging.error("Net does not connect to the correct port")
            raise Exception("Net does not connect to the correct port")


    def compare_inner_pins(self, pin_orig, pin_composer):
        if self.get_identifier(pin_orig.port) != self.get_identifier(pin_composer.port):
            # logging.error("Net does not connect the same ports")
            raise Exception("Net does not connect the same ports")
        for orig in range(pin_orig.port.inner_pins.__len__()):
            if pin_orig == pin_orig.port.inner_pins[orig]:
                break
        for composer in range(pin_composer.port.inner_pins.__len__()):
            if pin_composer == pin_composer.port.inner_pins[composer]:
                break
        if orig != composer:
            # logging.error("Net does not connect to the correct port")
            raise Exception("Net does not connect to the correct port")


    def compare_ports(self, port_orig, port_composer):
        if self.get_identifier(port_orig) != self.get_identifier(port_composer):
            # logging.error("Ports do not have the same identifier")
            raise Exception("Ports do not have the same identifier")

        if port_orig.direction != port_composer.direction:
            # logging.error("Ports are not facing the same direction")
            raise Exception("Ports are not facing the same direction")

        if hasattr(port_orig, "is_array"):
            if not hasattr(port_orig, "is_array"):
                # logging.error("Ports Array mismatch")
                raise Exception("Ports Array mismatch")
            if port_orig.inner_pins.__len__() != port_composer.inner_pins.__len__():
                # logging.error("Ports do not have the same number of pins")
                raise Exception("Ports do not have the same number of pins")

    def compare_instances(self, instances_orig, instances_composer):
        instances_orig_identifier = self.get_identifier(instances_orig)
        instances_composer_identifier = self.get_identifier(instances_composer)
        if instances_orig_identifier != instances_composer_identifier:
            # logging.error("Instances do not have the same identifier")
            raise Exception(f"Instances do not have the same identifier, orig \"{instances_orig_identifier}\" "
                            f"composer \"{instances_composer_identifier}\"")

        instances_orig_original_identifier = self.get_original_identifier(instances_orig)
        instances_composer_original_identifier = self.get_original_identifier(instances_composer)
        if instances_orig_original_identifier != instances_composer_original_identifier:
            # logging.error("Instances do not have the same original identifier")
            raise Exception(f"Instances do not have the same original identifier, orig "
                            f"\"{instances_orig_original_identifier}\" composer "
                            f"\"{instances_composer_original_identifier}\"")
        # logging.info("Checking properties of %s", self.get_identifier(instances_orig))
        if "EDIF.properties" in instances_orig._metadata:
            if "EDIF.properties" not in instances_composer._metadata:
                # logging.error("Composer is missing properties")
                raise Exception("Composer is missing properties")
            properties_orig = instances_orig._metadata["EDIF.properties"]
            properties_composer = instances_composer._metadata["EDIF.properties"]
            for x in range(properties_orig.__len__()):
                for key, value in properties_orig[x].items():
                    if value is None:
                        # logging.warning("Parser gave NoneType for %s property in %s", properties_orig[x]["identifier"],
                        #                self.get_identifier(instances_orig))
                        continue
                    else:
                        if properties_orig[x][key] != properties_composer[x][key]:
                            # logging.error("Instances do not have the same properties")
                            raise Exception("Instances do not have the same properties")


    def search_list(self, lst, target):
        for x in range(lst.__len__()):
            if self.get_identifier(lst[x]) == self.get_identifier(target):
                return x
        return -1


    def get_identifier(self, obj):
        if "EDIF.identifier" in obj._metadata:
            return obj._metadata["EDIF.identifier"]


    def get_original_identifier(self, obj):
        if "EDIF.original_identifier" in obj._metadata:
            return obj._metadata["EDIF.original_identifier"]


if __name__ == "__main__":
    compare = Comparer("unique_challenge.edf", "unique_challenge_composed.edf")
    compare.run()