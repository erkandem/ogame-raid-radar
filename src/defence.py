"""

"""
from typing import Union
from src.utils import OrePrice


class Defence:
    cost_metal: Union[float, int]
    cost_crystal: Union[float, int]
    cost_deuterium: Union[float, int]
    base_armour: Union[float, int]
    base_weapon: Union[float, int]
    base_shield: Union[float, int]
    cost: OrePrice
    structural_integrity: Union[float, int]


class RocketLauncher(Defence):
    pass


class LightLaser(Defence):
    pass


class HeavyLaser(Defence):
    pass


class GaussCannon(Defence):
    pass


class IonCannon(Defence):
    pass


class PlasmaTurret(Defence):
    pass


class SmallShieldDome(Defence):
    pass


class LargeShieldDome(Defence):
    pass


class AntiBallisticMissiles(Defence):
    pass


class InterplanetaryMissiles(Defence):
    pass
