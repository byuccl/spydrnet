"""
From the specification for version 1.0:

Creation API calls:
create_design 
create_cell
create_port
create_cable
create_library
create_property

These calls are collected/imported/defined here
"""
from spydrnet.ir import *
from spydrnet.data_manager import DataManager

environment_manager = DataManager.from_element_type_and_metadata_key(Environment, 'EDIF.identifier')

def create_design():
    environment = Environment()
    environment.add_data_manager(
        DataManager.from_element_type_and_metadata_key(
            Library, 'EDIF.identifier'
            )
        )
    return environment

def create_instance(definition):
    instance = Instance()
    instance['metadata_prefix'] = list()
    instance.definition = definition
    return instance

def create_definition():
    definition = Definition()
    definition.add_data_manager(
        DataManager.from_element_type_and_metadata_key(
            Port, 'EDIF.identifier'
            )
        )
    definition.add_data_manager(
        DataManager.from_element_type_and_metadata_key(
            Cable, 'EDIF.identifier'
            )
        )
    definition.add_data_manager(
        DataManager.from_element_type_and_metadata_key(
            Instance, 'EDIF.identifier'
            )
        )
    return definition

def create_port():
    return Port()

def create_cable():
    return Cable()

def create_library():
    library = Library()
    library.add_data_manager(
        DataManager.from_element_type_and_metadata_key(
            Definition, 'EDIF.identifier'
            )
        )
    return library

def create_property(identifier, original_identifier, value):
    prop = dict()
    prop['identifier'] = identifier
    prop['original identifier'] = original_identifier
    prop['value'] = value
    return prop
