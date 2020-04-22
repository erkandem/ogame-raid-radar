from src.utils import OrePrice
from typing import Union
from math import floor, ceil, exp


class Building:
    """Base class to derive specific buildings from."""
    level: Union[float, int]
    base_cost: OrePrice
    base_production: Union[float, int]
    consumption_factor: Union[float, int]
    production_factor: Union[float, int]
    universe_speed: Union[float, int]
    upgrade_cost_base: Union[float, int]

    def __init__(self, *, level=None, consumption_factor=None, production_factor=None):
        self.f_consumption = consumption_factor
        self.production_factor = production_factor
        self.level = level

    def get_production(self):
        return floor(self.production_factor * self.universe_speed * self.level * 1.1 ** self.level)

    def get_consumption(self):
        return ceil(self.consumption_factor * self.level * 1.1 ** self.level)

    def get_cost(self, **kwargs):
        if 'level' is kwargs:
            level = kwargs['level']
        else:
            level = self.level
        return self.base_cost * self.upgrade_cost_base ** (level- 1)

    def get_total_cost(self):
        level = int(self.level)
        total_cost = self.base_cost
        while level >= 0:
            total_cost += self.get_cost(level=level)
            level -= 1
        return total_cost


class MetalMine(Building):
    def __init__(self, level: int = None):
        super().__init__(production_factor=30, consumption_factor=10, level=level)
        self.base_production = 210


class CrystalMine(Building):
    def __init__(self, level: int = None):
        super().__init__(production_factor=20, consumption_factor=10, level=level)
        self.base_production = 110


class DeuteriumSynthesizer(Building):
    """creates deuterium"""
    def __init__(self, *, t_max_planet=None, level=None):
        super().__init__(production_factor=20, consumption_factor=10, level=level)
        self.base_cost = OrePrice(metal=225, crystal=75, deuterium=0)
        self.level = level
        self.t_max_planet = t_max_planet

    def get_production(self):
        f1 = self.production_factor * self.level * 1.1 ** self.level
        f2 = 1.36 - 0.004 * self.t_max_planet
        acceleration = 1
        production = f1 * f2 * acceleration
        return max(0, production)

    def get_efficiency(self):
        """ Deuterium / Energy """
        return self.get_production() / (1 * self.get_consumption())


class SolarPlant(Building):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FusionReactor(Building):
    """An energy producing building. Burns stored Deuterium"""
    def __init__(self, level=None, etech_level=None):
        super().__init__(production_factor=30, consumption_factor=10, level=level)
        self.level = level
        self.etech_level = etech_level
        self.base_cost = OrePrice(metal=900, crystal=360, deuterium=180)

    def get_production(self):
        return (self.production_factor * self.level
                * (1.05 + (0.01 * self.etech_level)) ** self.level)

    def get_consumption(self):
        acceleration = 1
        return (self.consumption_factor * self.level
                * 1.1 ** self.level
                * acceleration)

    def get_efficiency(self):
        """ Energy / Deuterium"""
        return self.get_production() / (self.get_consumption())


class Storage:
    """
    Base class to derive metal, crystal andd euterium storage
    objects from.
    """
    capacity: Union[float, int]
    level: int
    base_cost: OrePrice

    def get_capacity(self, **kwargs):
        if 'level' in kwargs:
            level = kwargs['level']
        else:
            level = self.level
        return 5000 * (2.5 * exp((20 / 33) * level))

    def get_cost(self, **kwargs):
        """The implementation depends on the actually stored resourcce"""
        pass

    def get_total_cost(self):
        level = int(self.level)
        total_cost = self.base_cost
        while level >= 0:
            total_cost += self.get_cost(level=level)
            level -= 1
        return total_cost


class MetalStorage(Storage):
    """
    Used to store metal. Production of new metal in the game
    is halted if the storage capacity is exhausted.
    """
    def get_cost(self, **kwargs):
        if 'level' in kwargs:
            level = kwargs['level']
        else:
            level = self.level
        m = 500 * 2 ** level
        return OrePrice(metal=m, crystal=0, deuterium=0)


class CrystalStorage(Storage):
    """
    Used to store crystal. Production of new deuterium in the game
    is halted if the storage capacity is exhausted.
    """
    def get_cost(self, **kwargs):
        if 'level' in kwargs:
            level = kwargs['level']
        else:
            level = self.level
        m = 500 * 2 ** level
        c = 250 * 2 ** level
        return OrePrice(metal=m, crystal=c, deuterium=0)


class DeuteriumTank(Storage):
    """
    Used to store deuterium. Production of new deuterium in the game
    is halted if the storage capacity is exhausted.
    """
    def get_cost(self, **kwargs):
        if 'level' in kwargs:
            level = kwargs['level']
        else:
            level = self.level
        m = 500 * 2 ** level
        c = 500 * 2 ** level
        return OrePrice(metal=m, crystal=c, deuterium=0)


class MoonBuildings(Building):
    pass


class LunarBase(MoonBuildings):
    pass


class SensorPhalanx(MoonBuildings):
    pass


class JumpGate(MoonBuildings):
    pass
