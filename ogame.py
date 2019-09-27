from src import ships
from properties import ship_properties_mapping, ship_properties
from properties import defence_properties_mapping, defence_properties
from properties import defence_properties_mapping, defence_properties


def universe_factory():
    pass


def ship_factory():
    initialized_ships = []
    for ship_name, ship_obj in ship_properties_mapping['objects'].items():
        for property_name, value in ship_properties[ship_name].items():
            attribute_name = ship_properties_mapping['attributes'][property_name]
            ship_obj.__setattr__(attribute_name, value)
        initialized_ships.append(ship_obj)
    return initialized_ships


def defence_factory():
    initialized_defence = []
    for ship_name, defence_obj in defence_properties_mapping['objects'].items():
        for property_name, value in defence_properties[ship_name].items():
            attribute_name = defence_properties_mapping['attributes'][property_name]
            defence_obj.__setattr__(attribute_name, value)
        initialized_defence.append(defence_obj)
    return initialized_defence


def facilities_factory():
    pass


def buildings_factory():
    pass
