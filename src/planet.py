from typing import Union
from collections import namedtuple


Coords = namedtuple(
    'Coords',
    ['galaxy', 'system', 'planet']
)


class StellarObject:
    pass

class Location:
    coords: Coords
    object: StellarObject

class Universe:
    galaxies: {}


class Galaxy:
    systems: {}


class System:
    planets: {}


class DebrisField(StellarObject):
    resources: {}


class Moon(StellarObject):
    coods: Coords
    fields: Union[float, int]
    resources: {}
    buildings: {}
    facilities: {}

    def __init__(self, *args, **kwargs):
        self.__dict__.update(kwargs)


class Planet(StellarObject):
    coords: Coords
    fields: Union[float, int]
    resources: {}
    buildings: {}
    facilities: {}
    defence: {}
    moon: Moon

    def __init__(self, galaxy: int, system: int, planet: int, *args, **kwargs):
        self.coords = Coords(galaxy, system, planet)
        self.__dict__.update(kwargs)

    def get_coords_str(self):
        return f'{self.coords.galaxy}:{self.coords.system}:{self.coords.planet}'
