from src.utils import OrePrice


class ResearchField:
    base_cost: OrePrice
    level: int
    ogame_api_code: int
    official_name: str
    requirements: {}

    def get_cost(self):
        cost_multiplier = self.get_cost_multiplier()
        return self.base_cost * cost_multiplier

    def calculate_research_time(self, research_Lab_level):
        universe_speed = 7
        cost = self.get_cost()
        gross_factor = (1 + research_Lab_level)
        research_time = (cost.m + cost.c) / (universe_speed * 1000 * gross_factor)
        return research_time

    def get_cost_multiplier(self):
        if self.__str__() == 'Astrophysics':
            cost_factor = 1.75
        elif self.__str__() == 'GravitonTechnology':
            cost_factor = 3
        else:
            cost_factor = 2
        return cost_factor


class EspionageTechnology(ResearchField):
    pass


class ComputerTechnology(ResearchField):
    pass


class WeaponsTechnology(ResearchField):
    pass


class ShieldingTechnology(ResearchField):
    pass


class ArmourTechnology(ResearchField):
    pass


class EnergyTechnology(ResearchField):
    pass


class HyperspaceTechnology(ResearchField):
    pass


class LaserTechnology(ResearchField):
    pass


class IonTechnology(ResearchField):
    pass


class PlasmaTechnology(ResearchField):
    pass


class GravitonTechnology(ResearchField):
    pass


class IntergalacticResearchNetwork(ResearchField):
    pass


class Astrophysics(ResearchField):
    pass


class Drive(ResearchField):
    def __init__(self, drive_level, drive_multiplier):
        self.drive_level = drive_level
        self.drive_multiplier = drive_multiplier


class CombustionDrive(Drive):
    def __init__(self, *args):
        super().__init__(*args)
    pass


class ImpulseDrive(Drive):
    def __init__(self, *args):
        super().__init__(*args)
    pass


class HyperspaceDrive(Drive):
    def __init__(self, *args):
        super().__init__(*args)
    pass

from math import  floor, ceil


class PlasmasTechAdjustment:

    def __init__(self, level: int = 0):
        self.level = level

    def _get_metal_factor(self):
        return 1 + self.level * 0.01

    def _get_crystal_factor(self):
        return 1 + self.level * 0.0066

    def _get_deuterium_factor(self):
        return 1 + self.level * 0.0033

    def _get_metal_production(self, metal):
        return floor(self._get_metal_factor() * metal)

    def _get_crystal_production(self, crystal):
        return floor(self._get_crystal_factor() * crystal)

    def _get_deuterium_production(self, deuterium):
        return floor(self._get_deuterium_factor() * deuterium)
