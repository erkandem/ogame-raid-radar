import math
from src.research import Drive
from src.utils import OrePrice
from typing import Union


class Ship:
    cost_metal: Union[float, int]
    cost_crystal: Union[float, int]
    cost_deuterium: Union[float, int]
    cost: OrePrice
    base_speed: Union[float, int]
    base_cargo: Union[float, int]
    base_attack: Union[float, int]
    base_shield: Union[float, int]
    base_armor: Union[float, int]
    base_fuelconsumption: Union[float, int]
    drive: Drive
    cargo_multiplier: Union[float, int]
    hst_level:  Union[float, int]
    attack_multiplier: Union[float, int]
    attack_level: Union[float, int]
    shield_multiplier: Union[float, int]
    shield_level: Union[float, int]
    armor_multiplier: Union[float, int]
    armor_level: Union[float, int]
    structural_integrity: Union[float, int]

    def get_speed(self, drive_multiplier=None, drive_level=None):
        if drive_level and drive_multiplier:
            gross_factor = (1 + drive_multiplier * drive_level)
        else:
            gross_factor = (1 + self.drive.drive_multiplier * self.drive.drive_level)
        return self.base_speed * gross_factor

    def get_cargo(self, multiplier=None, hst_level=None):
        if multiplier and hst_level:
            gross_factor = (1 + multiplier * hst_level)
        else:
            gross_factor = (1 + self.cargo_multiplier * self.hst_level)
        return self.base_cargo * gross_factor

    def get_attack(self, multiplier=None, attack_level=None):
        if multiplier and attack_level:
            gross_factor = (1 + multiplier * attack_level)
        else:
            gross_factor = (1 + self.attack_multiplier * self.attack_level)
        return self.base_attack * gross_factor

    def get_shield(self, multiplier=None, shield_level=None):
        if multiplier and shield_level:
            gross_factor = (1 + multiplier * shield_level)
        else:
            gross_factor = (1 + self.shield_multiplier * self.shield_level)
        return self.base_shield * gross_factor

    def get_armour(self, multiplier=None, armor_level=None):
        if multiplier and armor_level:
            gross_factor = (1 + multiplier * armor_level)
        else:
            gross_factor = (1 + self.armor_multiplier * self.armor_level)
        return self.base_shield * gross_factor


class EspionageProbe(Ship):
    """ "Espionage Probe", 100000000, "Combustion Drive" """
    pass


class Cruiser(Ship):
    """ "Cruiser", 15000, "Impulse Drive" """
    pass


class LightFighter(Ship):
    """ "Light Fighter", 12500, "Combustion Drive" """
    pass


class HeavyFighter(Ship):
    """ "Heavy Fighter", 10000, "Impulse Drive" """
    pass


class BattleShip(Ship):
    """ "Battle Ship", 10000,"Hyperspace Drive" """
    pass


class SmallCargo(Ship):
    """
    "Small Cargo", 5000, "Combustion Drive"
    "Small Cargo*", 10000, "Impulse Drive Level 5"
    """
    pass


class LargeCargo(Ship):
    """ "Large Cargo", 7500, "Combustion Drive" """
    pass


class DeathStar(Ship):
    """ "Death Star", 100, "Hyperspace Drive" """
    pass


class Recycler(Ship):
    """
    "Recycler", 2000, "Combustion Drive"
    "Recycler***", 4000, "Impulse Drive Level 17"
    "Recycler****", 6000, "Hyperspace Drive Level 15"
    """
    pass


class Bomber(Ship):
    """
    "Bomber", 4000, "Impulse Drive"
    "Bomber**", 5000, "Hyperspace Drive Level 8"
    """
    pass


class Destroyer(Ship):
    """ "Destroyer", 5000, "Hyperspace Drive" """
    pass


class Battlecruiser(Ship):
    """ "Battlecruiser", 10000, "Hyperspace Drive" """
    pass


class SolarSatellite(Ship):
    """ "Solar Satellite", 0, "None" """
    pass


class ColonyShip(Ship):
    """ "Colony Ship", 2500, "Impulse Drive" """
    pass
