"""
taken from work done by [alaingilbert](https://github.com/alaingilbert/pyogame)
low level dictionary object to capture state

"""

config = {
    'Player': {
        'Planets': [{
            'Planet': {  # replace by (unique) address
                'Resources': {
                    'Metal': 0,
                    'Crystal': 0,
                    'Deuterium': 0,
                },
                'Buildings': {
                    'MetalMine': 0,
                    'CrystalMine': 0,
                    'DeuteriumSynthesizer': 0,
                    'SolarPlant': 0,
                    'FusionReactor': 0,
                    'MetalStorage': 0,
                    'CrystalStorage': 0,
                    'DeuteriumTank': 0,
                    'ShieldedMetalDen': 0,
                    'UndergroundCrystalDen': 0,
                    'SeabedDeuteriumDen': 0
                },
                'Facilities': {
                    'AllianceDepot': 0,
                    'RoboticsFactory': 0,
                    'Shipyard': 0,
                    'ResearchLab': 0,
                    'MissileSilo': 0,
                    'NaniteFactory': 0,
                    'Terraformer': 0,
                    'SpaceDock': 0
                },
                'Defence': {
                    'RocketLauncher': 0,
                    'LightLaser': 0,
                    'HeavyLaser': 0,
                    'GaussCannon': 0,
                    'IonCannon': 0,
                    'PlasmaTurret': 0,
                    'SmallShieldDome': 0,
                    'LargeShieldDome': 0,
                    'AntiBallisticMissiles': 0,
                    'InterplanetaryMissiles': 0
                },
                'Ships': {
                    'SmallCargo': 0,
                    'LargeCargo': 0,
                    'LightFighter': 0,
                    'HeavyFighter': 0,
                    'Cruiser': 0,
                    'Battleship': 0,
                    'ColonyShip': 0,
                    'Recycler': 0,
                    'EspionageProbe': 0,
                    'Bomber': 0,
                    'SolarSatellite': 0,
                    'Destroyer': 0,
                    'Deathstar': 0,
                    'Battlecruiser': 0
                }
            }
        }],
        'Research': {
            'EspionageTechnology': 0,
            'ComputerTechnology': 0,
            'WeaponsTechnology': 0,
            'ShieldingTechnology': 0,
            'ArmourTechnology': 0,
            'EnergyTechnology': 0,
            'HyperspaceTechnology': 0,
            'CombustionDrive': 0,
            'ImpulseDrive': 0,
            'HyperspaceDrive': 0,
            'LaserTechnology': 0,
            'IonTechnology': 0,
            'PlasmaTechnology': 0,
            'IntergalacticResearchNetwork': 0,
            'Astrophysics': 0,
            'GravitonTechnology': 0,
        }
    }
}

if __name__ == '__main__':
    print('ready')
