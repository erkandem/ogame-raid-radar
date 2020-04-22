from src import ships
from properties import ship_properties, ship_properties_mapping
from properties import defence_properties, defence_properties_mapping
from properties import facility_properties, facility_properties_mapping
from properties import building_properties, building_properties_mapping
from properties import moon_buildings_properties, moon_buildings_properties_mapping


def initializing_logic(props: dict, prop_to_obj_mapping: dict):
    """
    a tool to avoid hard coding object properties
    """
    init_objects = {}
    for obj_name, obj in prop_to_obj_mapping['objects'].items():
        for property_name, value in props[obj_name].items():
            attribute_name = prop_to_obj_mapping['attributes'][property_name]
            obj.__setattr__(attribute_name, value)
        init_objects[obj_name] = obj
    return init_objects


def ship_factory():
    return initializing_logic(ship_properties, ship_properties_mapping)


def defence_factory():
    return initializing_logic(defence_properties, defence_properties_mapping)


def facilities_factory():
    return initializing_logic(facility_properties, facility_properties_mapping)


def buildings_factory():
    return initializing_logic(building_properties, building_properties_mapping)


def moon_buildings_factory():
    return initializing_logic(moon_buildings_properties, moon_buildings_properties_mapping)


def universe_factory():
    return {
        'moon_buildings': moon_buildings_factory(),
        'facilities': facilities_factory(),
        'buildings': buildings_factory(),
        'ships': ship_factory(),
        'defences': defence_factory()
    }


if __name__ == '__main__':
    game = universe_factory()
