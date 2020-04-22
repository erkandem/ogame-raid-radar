from collections import namedtuple
import math
from typing import Union

from src.planet import Location

ExchangeRate = namedtuple(
    'ExchangeRate',
    ['metal', 'crystal', 'deuterium']
)


def calc_distance(
        p1: Location,
        p2: Location
) -> float:
    """

    Args:
        p1 (Location): planet 1 of interest
        p2 (Location): planet 1 of interest

    """
    if p1.coords.galaxy != p1.coords.galaxy:
        distance = 20000 * math.fabs(p2.coords.galaxy - p1.coords.planet)
    else:
        if p1.coords.system != p2.coords.system:
            distance = 2700 + 95 * math.fabs(p2.coords.system - p1.coords.system)
        else:
            if p1.coords.planet != p2.coords.planet:
                distance = 1000 + 5 * math.fabs(p2.coords.planet - p1.coords.planet)
            else:
                raise ValueError
    return distance


def calc_flight_time(
        p1: Location,
        p2: Location
) -> float:
    """
    find out how much time it will take to get from `p1` to `p2`

    Args:
        p1 (Location): departure
        p2 (Location): destination
    """
    speed_factor = 1.0  # element  [0, 1]
    minimum_speed = 100
    universe_fleet_speed = 7
    distance = calc_distance(p1, p2)
    duration = 10 + 3500 / speed_factor + math.sqrt(10 * distance / minimum_speed)
    duration = duration / universe_fleet_speed
    return duration


class OrePrice:
    """
    represents cost and or price

    TODO: consider implement energy, too.
          some research construction needs one off energy
    """
    metal: Union[float, int] = None
    crystal: Union[float, int] = None
    deuterium: Union[float, int] = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        return f'M:{self.metal:.0f} C:{self.crystal:.0f} D:{self.deuterium:.0f}'

    def __repr__(self):
        return f'M:{self.metal:.1E} C:{self.crystal:.1E} D:{self.deuterium:.1E}'

    def __eq__(self, other):
        return all([
            self.metal == other.metal,
            self.crystal == other.crystal,
            self.deuterium == other.deuterium
        ])

    def __and__(self, other):
        return OrePrice(
            metal=self.metal + other.metal,
            crystal=self.crystal + other.crystal,
            deuterium=self.deuterium + other.deuterium
        )

    def __add__(self, other):
        return OrePrice(
            metal=self.metal + other.metal,
            crystal=self.crystal + other.crystal,
            deuterium=self.deuterium + other.deuterium
        )

    def __sub__(self, other):
        return OrePrice(
            metal=self.metal - other.metal,
            crystal=self.crystal - other.crystal,
            deuterium=self.deuterium - other.deuterium
        )

    def __mul__(self, factor):
        return OrePrice(
            metal=self.metal * factor,
            crystal=self.crystal * factor,
            deuterium=self.deuterium * factor
        )

    def __pow__(self, factor):
        return OrePrice(
            metal=self.metal ** factor,
            crystal=self.crystal ** factor,
            deuterium=self.deuterium ** factor
        )

    def to_dict(self):
        return {
            'metal': self.metal,
            'crystal': self.crystal,
            'deuterium': self.deuterium
        }

    def get_meu(self, rate: ExchangeRate = None):
        raise NotImplementedError()
        if rate is None:
            rate = ExchangeRate(metal=3, crystal=2, deuterium=1)
        base = rate.metal + rate.crystal + rate.deuterium
        meu = (
                  (1 / rate.metal) * self.metal
                + (1 / rate.crystal) * self.crystal
                + (1 / rate.deuterium) * self.deuterium
        )
        return meu
