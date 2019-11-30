#%%
from src import ships
from src import defence
from src import facilities
from src import buildings

ship_properties = {
    'SmallCargo': {
        'Metal': 2000.0, 'Crystal': 2000.0, 'Deuterium': 0.0, 'StructuralIntegrity': 4000.0,
        'Armour': 400.0, 'ShieldPower': 10.0, 'WeaponPower': 5.0, 'CargoCapacity': 5000.0,
        'Speed': 5000.0, 'FuelCons.': 10.0
    },
    'LargeCargo': {
        'Metal': 6000.0, 'Crystal': 6000.0, 'Deuterium': 0.0, 'StructuralIntegrity': 12000.0,
        'Armour': 1200.0, 'ShieldPower': 25.0, 'WeaponPower': 5.0, 'CargoCapacity': 25000.0,
        'Speed': 7500.0, 'FuelCons.': 50.0
    },
    'LightFighter': {
        'Metal': 3000.0, 'Crystal': 1000.0, 'Deuterium': 0.0, 'StructuralIntegrity': 4000.0,
        'Armour': 400.0, 'ShieldPower': 10.0, 'WeaponPower': 50.0, 'CargoCapacity': 50.0,
        'Speed': 12500.0, 'FuelCons.': 20.0
    },
    'HeavyFighter': {
        'Metal': 6000.0, 'Crystal': 4000.0, 'Deuterium': 0.0, 'StructuralIntegrity': 10000.0,
        'Armour': 1000.0, 'ShieldPower': 25.0, 'WeaponPower': 150.0, 'CargoCapacity': 100.0,
        'Speed': 10000.0, 'FuelCons.': 75.0
    },
    'Cruiser': {
        'Metal': 20000.0, 'Crystal': 7000.0, 'Deuterium': 2000.0, 'StructuralIntegrity': 27000.0,
        'Armour': 2700.0, 'ShieldPower': 50.0, 'WeaponPower': 400.0, 'CargoCapacity': 800.0,
        'Speed': 15000.0, 'FuelCons.': 300.0
    },
    'Battleship': {
        'Metal': 45000.0, 'Crystal': 15000.0, 'Deuterium': 0.0, 'StructuralIntegrity': 60000.0,
        'Armour': 6000.0, 'ShieldPower': 200.0, 'WeaponPower': 1000.0, 'CargoCapacity': 1500.0,
        'Speed': 10000.0, 'FuelCons.': 500.0
    },
    'ColonyShip': {
        'Metal': 10000.0, 'Crystal': 20000.0, 'Deuterium': 10000.0, 'StructuralIntegrity': 30000.0,
        'Armour': 3000.0, 'ShieldPower': 100.0, 'WeaponPower': 50.0, 'CargoCapacity': 7500.0,
        'Speed': 2500.0, 'FuelCons.': 1000.0
    },
    'Recycler': {
        'Metal': 10000.0, 'Crystal': 6000.0, 'Deuterium': 2000.0, 'StructuralIntegrity': 16000.0,
        'Armour': 1600.0, 'ShieldPower': 10.0, 'WeaponPower': 1.0, 'CargoCapacity': 20000.0,
        'Speed': 2000.0, 'FuelCons.': 300.0
    },
    'EspionageProbe': {
        'Metal': 0.0, 'Crystal': 1000.0, 'Deuterium': 0.0, 'StructuralIntegrity': 1000.0,
        'Armour': 100.0, 'ShieldPower': 0.0, 'WeaponPower': 0.0, 'CargoCapacity': 5.0,
        'Speed': 100000000.0, 'FuelCons.': 1.0
    },
    'Bomber': {
        'Metal': 50000.0, 'Crystal': 25000.0, 'Deuterium': 15000.0, 'StructuralIntegrity': 75000.0,
        'Armour': 7500.0, 'ShieldPower': 500.0, 'WeaponPower': 1000.0, 'CargoCapacity': 500.0,
        'Speed': 4000.0, 'FuelCons.': 1000.0
    },
    'SolarSatellite': {
        'Metal': 0.0, 'Crystal': 2000.0, 'Deuterium': 500.0, 'StructuralIntegrity': 2000.0,
        'Armour': 200.0, 'ShieldPower': 1.0, 'WeaponPower': 1.0, 'CargoCapacity': float('nan'),
        'Speed': float('nan'), 'FuelCons.': float('nan')
    },
    'Destroyer': {
        'Metal': 60000.0, 'Crystal': 50000.0, 'Deuterium': 15000.0, 'StructuralIntegrity': 110000.0,
        'Armour': 11000.0, 'ShieldPower': 500.0, 'WeaponPower': 2000.0, 'CargoCapacity': 2000.0,
        'Speed': 5000.0, 'FuelCons.': 1000.0
    },
    'Deathstar': {
        'Metal': 5000000.0, 'Crystal': 4000000.0, 'Deuterium': 1000000.0,
        'StructuralIntegrity': 9000000.0, 'Armour': 900000.0, 'ShieldPower': 50000.0,
        'WeaponPower': 200000.0, 'CargoCapacity': 1000000.0, 'Speed': 100.0, 'FuelCons.': 1.0
    },
    'Battlecruiser': {
        'Metal': 30000.0, 'Crystal': 40000.0, 'Deuterium': 15000.0, 'StructuralIntegrity': 70000.0,
        'Armour': 7000.0, 'ShieldPower': 400.0, 'WeaponPower': 700.0, 'CargoCapacity': 750.0,
        'Speed': 10000.0, 'FuelCons.': 250.0
    }
}

#%%

ship_properties_mapping = {
    'objects': {
        'Battleship': ships.BattleShip(),
        'ColonyShip': ships.ColonyShip(),
        'Deathstar': ships.DeathStar(),
        'SmallCargo': ships.SmallCargo(),
        'Bomber': ships.Bomber(),
        'Cruiser': ships.Cruiser(),
        'Battlecruiser': ships.Battlecruiser(),
        'SolarSatellite': ships.SolarSatellite(),
        'LargeCargo': ships.LargeCargo(),
        'LightFighter': ships.LightFighter(),
        'Recycler': ships.Recycler(),
        'HeavyFighter': ships.HeavyFighter(),
        'EspionageProbe': ships.EspionageProbe(),
        'Destroyer': ships.Destroyer()
    },
    'attributes': {
        'Metal': 'cost_metal',
        'Crystal': 'cost_crystal',
        'Deuterium': 'cost_deuterium',
        'Armour': 'base_armour',
        'Speed': 'base_speed',
        'FuelCons.': 'base_fuelconsumption',
        'StructuralIntegrity': 'structural_integrity',
        'CargoCapacity': 'base_cargo',
        'WeaponPower': 'base_weapon',
        'ShieldPower': 'base_shield'
    }
}

# %%
defence_properties = {
    'RocketLauncher': {
        'Metal': 2000.0, 'Crystal': 0.0, 'Deuterium': 0.0, 'StructuralIntegrity': 2000.0,
        'Armour': 200.0, 'ShieldPower': 20.0, 'WeaponPower': 80.0
    },
    'LightLaser': {
        'Metal': 1500.0, 'Crystal': 500.0, 'Deuterium': 0.0, 'StructuralIntegrity': 2000.0,
        'Armour': 200.0, 'ShieldPower': 25.0, 'WeaponPower': 100.0
    },
    'HeavyLaser': {
        'Metal': 6000.0, 'Crystal': 2000.0, 'Deuterium': 0.0,
        'StructuralIntegrity': 8000.0, 'Armour': 800.0, 'ShieldPower': 100.0,
        'WeaponPower': 250.0
    },
    'GaussCannon': {
        'Metal': 20000.0, 'Crystal': 15000.0, 'Deuterium': 2000.0,
        'StructuralIntegrity': 35000.0, 'Armour': 3500.0, 'ShieldPower': 200.0,
        'WeaponPower': 1100.0
    },
    'IonCannon': {
        'Metal': 2000.0, 'Crystal': 6000.0, 'Deuterium': 0.0, 'StructuralIntegrity': 8000.0,
        'Armour': 800.0, 'ShieldPower': 500.0, 'WeaponPower': 150.0
    },
    'PlasmaTurret': {
        'Metal': 50000.0, 'Crystal': 50000.0, 'Deuterium': 30000.0,
        'StructuralIntegrity': 100000.0, 'Armour': 10000.0, 'ShieldPower': 300.0,
        'WeaponPower': 3000.0
    },
    'SmallShieldDome': {
        'Metal': 10000.0, 'Crystal': 10000.0, 'Deuterium': 0.0,
        'StructuralIntegrity': 20000.0, 'Armour': 2000.0, 'ShieldPower': 2000.0,
        'WeaponPower': 1.0
    },
    'LargeShieldDome': {
        'Metal': 50000.0, 'Crystal': 50000.0, 'Deuterium': 0.0,
        'StructuralIntegrity': 100000.0, 'Armour': 10000.0, 'ShieldPower': 10000.0,
        'WeaponPower': 1.0
    },
    'Anti-BallisticMissiles': {
        'Metal': 8000.0, 'Crystal': 0.0, 'Deuterium': 2000.0,
        'StructuralIntegrity': 8000.0, 'Armour': 800.0, 'ShieldPower': 1.0,
        'WeaponPower': 1.0
    },
    'InterplanetaryMissiles': {
        'Metal': 12500.0, 'Crystal': 2500.0, 'Deuterium': 10000.0,
        'StructuralIntegrity': 15000.0, 'Armour': 1500.0, 'ShieldPower': 1.0,
        'WeaponPower': 12000.0
    }
}

#%%

defence_properties_mapping = {
    'objects': {
        'RocketLauncher': defence.RocketLauncher(),
        'LightLaser': defence.LightLaser(),
        'HeavyLaser': defence.HeavyLaser(),
        'GaussCannon': defence.GaussCannon(),
        'IonCannon': defence.IonCannon(),
        'PlasmaTurret': defence.PlasmaTurret(),
        'SmallShieldDome': defence.SmallShieldDome(),
        'LargeShieldDome': defence.LargeShieldDome(),
        'Anti-BallisticMissiles': defence.AntiBallisticMissiles(),
        'InterplanetaryMissiles': defence.InterplanetaryMissiles()
    },
    'attributes': {
        'Metal': 'cost_metal',
        'Crystal': 'cost_crystal',
        'Deuterium': 'cost_deuterium',
        'Armour': 'base_armour',
        'StructuralIntegrity': 'structural_integrity',
        'WeaponPower': 'base_weapon',
        'ShieldPower': 'base_shield'
    }
}

# %%

rapidfire_from_ship_to_ships = {
    'SmallCargo': {
        'LargeCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0, 'Cruiser': 0.0,
        'Battleship': 0.0,
        'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0,
        'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'LargeCargo': {
        'SmallCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0, 'Cruiser': 0.0,
        'Battleship': 0.0,
        'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0,
        'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'LightFighter': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'HeavyFighter': 0.0, 'Cruiser': 0.0,
        'Battleship': 0.0,
        'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0,
        'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'HeavyFighter': {
        'SmallCargo': 3.0, 'LargeCargo': 0.0, 'LightFighter': 0.0, 'Cruiser': 0.0,
        'Battleship': 0.0,
        'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0,
        'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'Cruiser': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'LightFighter': 6.0, 'HeavyFighter': 0.0,
        'Battleship': 0.0, 'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0, 'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'Battleship': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0,
        'Cruiser': 0.0,
        'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0,
        'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'ColonyShip': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0,
        'Cruiser': 0.0,
        'Battleship': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0,
        'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'Recycler': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0,
        'Cruiser': 0.0,
        'Battleship': 0.0, 'ColonyShip': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0, 'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'EspionageProbe': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0,
        'Cruiser': 0.0,
        'Battleship': 0.0, 'ColonyShip': 0.0, 'Recycler': 0.0, 'Bomber': 0.0, 'SolarSatellite': 0.0,
        'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'Bomber': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0,
        'Cruiser': 0.0,
        'Battleship': 0.0, 'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0,
        'SolarSatellite': 5.0, 'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'SolarSatellite': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0,
        'Cruiser': 0.0,
        'Battleship': 0.0, 'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 0.0, 'Bomber': 0.0,
        'Destroyer': 0.0, 'Deathstar': 0.0, 'Battlecruiser': 0.0
    },
    'Destroyer': {
        'SmallCargo': 0.0, 'LargeCargo': 0.0, 'LightFighter': 0.0, 'HeavyFighter': 0.0,
        'Cruiser': 0.0,
        'Battleship': 0.0, 'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0, 'Deathstar': 0.0, 'Battlecruiser': 2.0
    },
    'Deathstar': {
        'SmallCargo': 250.0, 'LargeCargo': 250.0, 'LightFighter': 200.0, 'HeavyFighter': 100.0,
        'Cruiser': 33.0, 'Battleship': 30.0, 'ColonyShip': 250.0, 'Recycler': 250.0,
        'EspionageProbe': 1250.0, 'Bomber': 25.0, 'SolarSatellite': 1250.0, 'Destroyer': 5.0,
        'Battlecruiser': 15.0
    },
    'Battlecruiser': {
        'SmallCargo': 3.0, 'LargeCargo': 3.0, 'LightFighter': 0.0, 'HeavyFighter': 4.0,
        'Cruiser': 4.0,
        'Battleship': 7.0, 'ColonyShip': 0.0, 'Recycler': 0.0, 'EspionageProbe': 5.0, 'Bomber': 0.0,
        'SolarSatellite': 5.0, 'Destroyer': 0.0, 'Deathstar': 0.0
    }
}

# %%

rapidfire_from_ships_to_defence = {
    'Cruiser': {
        'RocketLauncher': 10.0, 'LightLaser': 0.0, 'HeavyLaser': 0.0, 'GaussCannon': 0.0,
        'IonCannon': 0.0, 'PlasmaTurret': 0.0, 'SmallShieldDome': 0.0, 'LargeShieldDome': 0.0
    },
    'Bomber': {
        'RocketLauncher': 20.0, 'LightLaser': 20.0, 'HeavyLaser': 10.0, 'GaussCannon': 0.0,
        'IonCannon': 10.0, 'PlasmaTurret': 0.0, 'SmallShieldDome': 0.0, 'LargeShieldDome': 0.0
    },
    'Destroyer': {
        'RocketLauncher': 0.0, 'LightLaser': 10.0, 'HeavyLaser': 0.0, 'GaussCannon': 0.0,
        'IonCannon': 0.0, 'PlasmaTurret': 0.0, 'SmallShieldDome': 0.0, 'LargeShieldDome': 0.0
    },
    'Deathstar': {
        'RocketLauncher': 200.0, 'LightLaser': 200.0, 'HeavyLaser': 100.0, 'GaussCannon': 50.0,
        'IonCannon': 100.0, 'PlasmaTurret': 0.0, 'SmallShieldDome': 0.0, 'LargeShieldDome': 0.0
    }
}
# %%

research_parameters = {
    'EspionageTechnology': {
        'Metal': 200.0, 'Crystal': 1000.0, 'Deuterium': 200.0, 'Energy': 0.0
    },
    'ComputerTechnology': {
        'Metal': 0.0, 'Crystal': 400.0, 'Deuterium': 600.0, 'Energy': 0.0
    },
    'WeaponsTechnology': {
        'Metal': 800.0, 'Crystal': 200.0, 'Deuterium': 0.0, 'Energy': 0.0
    },
    'ShieldingTechnology': {
        'Metal': 200.0, 'Crystal': 600.0, 'Deuterium': 0.0, 'Energy': 0.0
    },
    'ArmourTechnology': {
        'Metal': 1000.0, 'Crystal': 0.0, 'Deuterium': 0.0, 'Energy': 0.0
    },
    'EnergyTechnology': {
        'Metal': 0.0, 'Crystal': 800.0, 'Deuterium': 400.0, 'Energy': 0.0
    },
    'HyperspaceTechnology': {
        'Metal': 0.0, 'Crystal': 4000.0, 'Deuterium': 2000.0, 'Energy': 0.0
    },
    'CombustionDrive': {
        'Metal': 400.0, 'Crystal': 0.0, 'Deuterium': 600.0, 'Energy': 0.0
    },
    'ImpulseDrive': {
        'Metal': 2000.0, 'Crystal': 4000.0, 'Deuterium': 600.0, 'Energy': 0.0
    },
    'HyperspaceDrive': {
        'Metal': 10000.0, 'Crystal': 20000.0, 'Deuterium': 6000.0, 'Energy': 0.0
    },
    'LaserTechnology': {
        'Metal': 200.0, 'Crystal': 100.0, 'Deuterium': 0.0, 'Energy': 0.0
    },
    'IonTechnology': {
        'Metal': 1000.0, 'Crystal': 300.0, 'Deuterium': 100.0, 'Energy': 0.0
    },
    'PlasmaTechnology': {
        'Metal': 2000.0, 'Crystal': 4000.0, 'Deuterium': 1000.0, 'Energy': 0.0
    },
    'IntergalacticResearchNetwork': {
        'Metal': 240000.0, 'Crystal': 400000.0, 'Deuterium': 160000.0, 'Energy': 0.0
    },
    'ExpeditionTechnology': {
        'Metal': 4000.0, 'Crystal': 8000.0, 'Deuterium': 4000.0, 'Energy': 0.0
    },
    'Astrophysics': {
        'Metal': 4000.0, 'Crystal': 8000.0, 'Deuterium': 4000.0, 'Energy': 0.0
    },
    'GravitonTechnology': {
        'Metal': 0.0, 'Crystal': 0.0, 'Deuterium': 0.0, 'Energy': 300000.0
    }
}
# %%

building_properties = {
    'MetalMine': {
        'Metal': 60, 'Crystal': 15, 'Deuterium': 0.0, 'Energy': 0.0,
        'UpgradeCostBase': 1.5, 'ProductionBase': 1.1,
        'ProductionFactor': 30, 'ConsumptionFactor': 10
    },
    'CrystalMine': {
        'Metal': 48.0, 'Crystal': 24.0, 'Deuterium': 0.0, 'Energy': 0.0,
        'UpgradeCostBase': 1.6, 'ProductionBase': 1.1,
        'ProductionFactor': 20, 'ConsumptionFactor': 10
    },
    'DeuteriumSynthesizer': {
        'Metal': 225.0, 'Crystal': 75.0, 'Deuterium': 0.0, 'Energy': 0.0,
        'UpgradeCostBase': 1.5, 'ProductionBase': 1.1,
        'ProductionFactor': 1, 'ConsumptionFactor': 20
    },
    'SolarPlant': {
        'Metal': 75.0, 'Crystal': 30.0, 'Deuterium': 0.0, 'Energy': 0.0,
        'UpgradeCostBase': 1.5, 'ProductionBase': 1.1,
        'ProductionFactor': 20, 'ConsumptionFactor': 0
    },
    'FusionReactor': {
        'Metal': 900.0, 'Crystal': 360.0, 'Deuterium': 180.0, 'Energy': 0.0,
        'UpgradeCostBase': 1.8, 'ProductionBase': 1,
        'ProductionFactor': 30, 'ConsumptionFactor': 10
    },
    'MetalStorage': {
        'Metal': 1000.0, 'Crystal': 0.0, 'Deuterium': 0.0, 'Energy': 0.0
    },
    'CrystalStorage': {
        'Metal': 1000.0, 'Crystal': 500.0, 'Deuterium': 0.0, 'Energy': 0.0
    },
    'DeuteriumTank': {
        'Metal': 1000.0, 'Crystal': 1000.0, 'Deuterium': 0.0, 'Energy': 0.0
    }
}

building_properties_mapping = {
    'objects': {
        'MetalMine': buildings.MetalMine(),
        'CrystalMine': buildings.CrystalMine(),
        'DeuteriumSynthesizer': buildings.DeuteriumSynthesizer(),
        'SolarPlant': buildings.SolarPlant(),
        'FusionReactor': buildings.FusionReactor(),
        'MetalStorage': buildings.MetalStorage(),
        'CrystalStorage': buildings.CrystalStorage(),
        'DeuteriumTank': buildings.DeuteriumTank()
    },
    'attributes': {
        'Metal': 'cost_metal',
        'Crystal': 'cost_crystal',
        'Deuterium': 'cost_deuterium',
        'Energy': 'cost_energy',
        'UpgradeCostBase': 'upgrade_cost_factor',
        'ConsumptionFactor': 'consumption_factor',
        'ProductionFactor': 'production_factor',
        'ProductionBase': 'production_base'
    }
}

# %%

moon_buildings_properties = {
    'LunarBase': {
        'Metal': 20000.0, 'Crystal': 40000.0, 'Deuterium': 20000.0, 'Energy': 0.0
    },
    'SensorPhalanx': {
        'Metal': 20000.0, 'Crystal': 40000.0, 'Deuterium': 20000.0, 'Energy': 0.0
    },
    'JumpGate': {
        'Metal': 2000000.0, 'Crystal': 4000000.0, 'Deuterium': 2000000.0, 'Energy': 0.0
    }
}
moon_buildings_properties_mapping = {
    'objects': {
        'LunarBase': buildings.LunarBase(),
        'SensorPhalanx': buildings.SensorPhalanx(),
        'JumpGate': buildings.JumpGate()
    },
    'attributes': {
        'Metal': 'cost_metal',
        'Crystal': 'cost_crystal',
        'Deuterium': 'cost_deuterium',
        'Energy': 'cost_energy'
    }
}

# %%

facility_properties_mapping = {
    'objects': {
        'RoboticsFactory': facilities.RoboticsFactory(),
        'Shipyard': facilities.Shipyard(),
        'ResearchLab': facilities.ResearchLab(),
        'AllianceDepot': facilities.AllianceDepot(),
        'MissileSilo': facilities.MissileSilo(),
        'NaniteFactory': facilities.NaniteFactory(),
        'Terraformer': facilities.Terraformer()
    },
    'attributes': {
        'Metal': 'cost_metal',
        'Crystal': 'cost_crystal',
        'Deuterium': 'cost_deuterium',
        'Energy': 'cost_energy'
    }
}

facility_properties = {
    'RoboticsFactory': {
        'Metal': 400.0, 'Crystal': 120.0, 'Deuterium': 200.0, 'Energy': 0.0
    },
    'Shipyard': {
        'Metal': 400.0, 'Crystal': 200.0, 'Deuterium': 100.0, 'Energy': 0.0
    },
    'ResearchLab': {
        'Metal': 200.0, 'Crystal': 400.0, 'Deuterium': 200.0, 'Energy': 0.0
    },
    'Terraformer': {
        'Metal': 0.0, 'Crystal': 50000.0, 'Deuterium': 100000.0, 'Energy': 1000.0
    },
    'AllianceDepot': {
        'Metal': 20000.0, 'Crystal': 40000.0, 'Deuterium': 0.0, 'Energy': 0.0
    },
    'MissileSilo': {
        'Metal': 20000.0, 'Crystal': 20000.0, 'Deuterium': 1000.0, 'Energy': 0.0
    },
    'NaniteFactory': {
        'Metal': 1000000.0, 'Crystal': 500000.0, 'Deuterium': 100000.0, 'Energy': 0.0
    }
}
