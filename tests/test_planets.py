import pytest
from src import planet


class TestStellarObject:
    pass


class TestLocation:
    pass


class TestUniverse:
    pass


class TestGalaxy:
    pass


class TestDebrisField:
    pass


class TestMoon:
    pass


class TestPlanet:

    def test_get_coords(self):
        p = planet.Planet(
            galaxy=1,
            system=1,
            planet=1
        )
        assert p.get_coords_str() == '1:1:1'
