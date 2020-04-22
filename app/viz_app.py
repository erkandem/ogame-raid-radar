from src import HighScoresData
from src import UniverseData


def get_janice_highscore():
    return HighScoresData(universe_id=162, community='en', do_init=True)

def get_janice_universe():
    return UniverseData(universe_id=162, community='en')


def sth_completly_different():
    """ found undocumented. keep until next review Nov2019"""

    janice = get_janice_universe()
    janice_scores = HighScoresData(162, 'en', do_init=True)
    inactive = janice.players.query("status == 'i' ")
    planet_of_inactivate = janice.universe.join(inactive, )
