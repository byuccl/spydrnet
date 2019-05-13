from spydrnet.parsers.edif.parser import EdifParser
from spydrnet.ir import OuterPin
import sys
import logging
import time

filename_orig = r"fourBitCounter.edf"
# filename_composer = r"fourBitCounter_inverted.edf"
filename_composer = r"fourBitCounter.edf"


# filename_composer = r"fourBitCounter_composed.edf"

counter = 0


def run():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

    # parse original
    parser_orig = EdifParser.from_filename(filename_orig)
    parser_orig.parse()
    ir_orig = parser_orig.netlist

    # parse composed
    parser_composer = EdifParser.from_filename(filename_composer)
    parser_composer.parse()
    ir_composer = parser_composer.netlist

    # compare netlists
    time.sleep(0.01)
    compare(ir_orig, ir_composer)
    time.sleep(0.01)
    print("The edf files contain the same circuit")


def compare(ir_orig, ir_composer):
    if get_identifier(ir_orig) != get_identifier(ir_composer):
        logging.error("Environments do not have the same identifier")
        sys.exit()

    if ir_orig.top_instance is None:
        logging.warning("Parser gave NoneType for top_instance")
    elif ir_orig.top_instance != ir_composer.top_instance:
        logging.error("Top instance is not the same")
        sys.exit()

    if ir_orig.libraries.__len__() != ir_composer.libraries.__len__():
        logging.error("Environments do not have the same number of libraries")
    for x in range(ir_orig.libraries.__len__()):
        logging.info("Checking %d out of %d libraries", x + 1, ir_orig.libraries.__len__())
        compare_libraries(ir_orig.libraries[x], ir_composer.libraries[x])


def compare_libraries(library_orig, library_composer):
    if get_identifier(library_orig) != get_identifier(library_composer):
        logging.error("Libraries do not have the same identifier")
        sys.exit()
    if library_orig.definitions.__len__() != library_composer.definitions.__len__():
        logging.error("Libraries do not have the same amount of definitions")
    for definition in range(library_orig.definitions.__len__()):
        logging.info("Checking %d out of %d definition in %s", definition + 1, library_orig.definitions.__len__(),
                     get_identifier(library_orig))
        x = search_list(library_composer.definitions, library_orig.definitions[definition])
        compare_definition(library_orig.definitions[definition], library_composer.definitions[x])


def compare_definition(definition_orig, definition_composer):
    if get_identifier(definition_orig) != get_identifier(definition_composer):
        logging.error("Definitions do not have the same identifier")
        logging.error("%s compared to %s", get_identifier(definition_orig), get_identifier(definition_composer))
        sys.exit()

    # Checking the cables
    if definition_orig.cables.__len__() != definition_composer.cables.__len__():
        logging.error("Definitions do not have the same number of cables")
        sys.exit()
    for cable in range(definition_orig.cables.__len__()):
        logging.info("Checking %d out of %d cables in %s", cable + 1, definition_orig.cables.__len__(),
                     get_identifier(definition_orig))
        x = search_list(definition_composer.cables, definition_orig.cables[cable])
        if x == -1:
            logging.error("Cables do not have the same identifier")
            sys.exit()
        compare_cables(definition_orig.cables[cable], definition_composer.cables[x])

    # Checking the instances
    if definition_orig.instances.__len__() != definition_composer.instances.__len__():
        logging.error("Definitions do not have the same number of instances")
        sys.exit()
    for instance in range(definition_orig.instances.__len__()):
        logging.info("Checking %d out of %d instances in %s", instance + 1, definition_orig.instances.__len__(),
                     get_identifier(definition_orig))
        x = search_list(definition_composer.instances, definition_orig.instances[instance])
        if x == -1:
            logging.error("Instances do not have the same identifier")
            sys.exit()
        compare_instances(definition_orig.instances[instance], definition_composer.instances[x])

    # Checking the ports
    if definition_orig.ports.__len__() != definition_composer.ports.__len__():
        logging.error("Definitions do not have the same number of ports")
        sys.exit()
    for port in range(definition_orig.ports.__len__()):
        logging.info("Checking %d out of %d ports in %s", port + 1, definition_orig.ports.__len__(),
                     get_identifier(definition_orig))
        x = search_list(definition_composer.ports, definition_orig.ports[port])
        if x == -1:
            logging.error("Ports do not have the same identifier")
            sys.exit()
        compare_ports(definition_orig.ports[port], definition_composer.ports[x])


def compare_cables(cables_orig, cables_composer):
    if get_identifier(cables_orig) != get_identifier(cables_composer):
        logging.error("Cables do not have the same identifier")
        sys.exit()
    if get_original_identifier(cables_orig) != get_original_identifier(cables_composer):
        logging.error("Cables do not have the same original identifier")
        sys.exit()
    if cables_orig.wires.__len__() != cables_composer.wires.__len__():
        logging.error("Cables do not have the same number of wires")
        sys.exit()
    logging.info("Checking pins connected to %s", get_identifier(cables_orig))
    for x in range(cables_orig.wires.__len__()):
        for y in range(cables_orig.wires[x].pins.__len__()):
            pin_orig = cables_orig.wires[x].pins[y]
            pin_composer = cables_composer.wires[x].pins[y]
            if type(pin_orig) != type(pin_composer):
                logging.error("Pins are not of the same type")
            if isinstance(pin_orig, OuterPin):
                compare_outer_pins(pin_orig, pin_composer)
            else:
                compare_inner_pins(pin_orig, pin_composer)


def compare_outer_pins(pin_orig, pin_composer):
    if get_identifier(pin_orig.instance) != get_identifier(pin_composer.instance):
        logging.error("Net does not connect the same ports")
        sys.exit()
    if get_identifier(pin_orig.inner_pin.port) != get_identifier(pin_composer.inner_pin.port):
        logging.error("Net does not connect the same ports")
        sys.exit()


def compare_inner_pins(pin_orig, pin_composer):
    if get_identifier(pin_orig.port) != get_identifier(pin_composer.port):
        logging.error("Net does not connect the same ports")
        sys.exit()


def compare_ports(port_orig, port_composer):
    if get_identifier(port_orig) != get_identifier(port_composer):
        logging.error("Ports do not have the same identifier")
        sys.exit()

    if port_orig.direction != port_composer.direction:
        logging.error("Ports are not facing the same direction")

    if hasattr(port_orig, "is_array"):
        if not hasattr(port_orig, "is_array"):
            logging.error("Ports Array mismatch")
            sys.exit()
        if port_orig.inner_pins.__len__() != port_composer.inner_pins.__len__():
            logging.error("Ports do not have the same number of pins")
            sys.exit()


def compare_instances(instances_orig, instances_composer):
    if get_identifier(instances_orig) != get_identifier(instances_composer):
        logging.error("Instances do not have the same identifier")
        sys.exit()
    if get_original_identifier(instances_orig) != get_original_identifier(instances_composer):
        logging.error("Instances do not have the same original identifier")
        sys.exit()
    logging.info("Checking properties of %s", get_identifier(instances_orig))
    if "EDIF.properties" in instances_orig._metadata:
        if "EDIF.properties" not in instances_composer._metadata:
            logging.error("Composer is missing properties")
            sys.exit()
        properties_orig = instances_orig._metadata["EDIF.properties"]
        properties_composer = instances_composer._metadata["EDIF.properties"]
        for x in range(properties_orig.__len__()):
            for key, value in properties_orig[x].items():
                if value is None:
                    logging.warning("Parser gave NoneType for %s property in %s", properties_orig[x]["identifier"],
                                    get_identifier(instances_orig))
                    continue
                else:
                    if properties_orig[x][key] != properties_composer[x][key]:
                        logging.error("Instances do not have the same properties")
                        sys.exit()


def search_list(lst, target):
    for x in range(lst.__len__()):
        if get_identifier(lst[x]) == get_identifier(target):
            return x
    return -1


def get_identifier(obj):
    if "EDIF.identifier" in obj._metadata:
        return obj._metadata["EDIF.identifier"]


def get_original_identifier(obj):
    if "EDIF.original_identifier" in obj._metadata:
        return obj._metadata["EDIF.original_identifier"]


run()
