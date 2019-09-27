from src.utils import OrePrice
from typing import  Union
from math import floor, ceil


class Building:
    level: Union[float, int]
    base_cost: OrePrice
    base_production: Union[float, int]
    consumption_factor: Union[float, int]
    production_factor: Union[float, int]
    universe_speed: Union[float, int]
    cost_factor: Union[float, int]

    def __init__(self, *, level=None, consumption_factor=None, production_factor=None):
        self.f_consumption = consumption_factor
        self.production_factor = production_factor
        self.level = level

    def get_production(self):
        return floor(self.production_factor * self.universe_speed * self.level * 1.1 ** self.level)

    def get_consumption(self):
        return ceil(self.consumption_factor * self.level * 1.1 ** self.level)

    def get_cost(self):
        return self.base_cost * self.cost_factor ** (self.level - 1)


class MetalMine(Building):
    def __init__(self, level: int = None):
        super().__init__(production_factor=30, consumption_factor=10, level=level)
        self.base_production = 210


class CrystalMine(Building):
    def __init__(self, level: int=None):
        super().__init__(production_factor=20, consumption_factor=10, level=level)
        self.base_production = 110


class DeuteriumSynthesizer(Building):
    def __init__(self, *, t_max_planet=None, level=None, acceleration: int = 1):
        super().__init__(production_factor=20, consumption_factor=10, level=level)
        self.acceleration = acceleration
        self.base_cost = OrePrice(metal=225, crystal=75, deuterium=0)
        self.level = level
        self.t_max_planet = t_max_planet

    def get_cost(self) -> OrePrice:
        return self.base_cost * 1.5 ** (self.level - 1)

    def get_production(self):
        f1 = 10 * self.level * 1.1 ** self.level
        f2 = 1.36 - 0.004 * self.t_max_planet
        production = f1 * f2 * self.acceleration
        return max(0, production)

    def get_consumption(self):
        return -20 * self.level * 1.1 ** self.level

    def get_efficiency(self):
        """ Deuterium / Energy """
        return self.get_production() / (1 * self.get_consumption())


class SolarPlant(Building):
    def __init__(self, level=None, etech_level=None, acceleration=1):
        super().__init__(production_factor=20, consumption_factor=0, level=level)

    def get_consumption(self):
        return 0


class FusionReactor(Building):
    def __init__(self, level=None, etech_level=None, acceleration=1):
        super().__init__(production_factor=30, consumption_factor=10, level=level)
        self.level = level
        self.etech_level = etech_level
        self.acceleration = acceleration
        self.base_cost = OrePrice(metal=900, crystal=360, deuterium=180)

    def get_cost(self) -> OrePrice:
        return self.base_cost * (1.8 ** (self.level - 1))

    def get_production(self):
        f1 = self.production_factor * self.level
        f2 = (1.05 + (0.01 * self.etech_level)) ** self.level
        return f1 * f2

    def get_consumption(self):
        f1 = self.consumption_factor * self.level
        f2 = 1.1 ** self.level
        return f1 * f2 * self.acceleration

    def get_efficiency(self):
        """ Energy / Deuterium"""
        return self.get_production() / (self.get_consumption())


class Storage(Building):
    capacity: Union[float, int]
    pass


class MetalStorage(Storage):
    pass


class CrystalStorage(Storage):
    pass


class DeuteriumTank(Storage):
    pass


class ShieldedMetalDen(Storage):
    pass


class UndergroundCrystalDen(Storage):
    pass


class SeabedDeuteriumDen(Storage):
    pass


class MoonBuildings(Building):
    pass


class LunarBase(MoonBuildings):
    pass


class SensorPhalanx(MoonBuildings):
    pass


class JumpGate(MoonBuildings):
    pass
