from src.api.scores_api import HighScoresApi
from src.api.universe_api import get_janice


def sth_completly_different():
    """ found undocumented. keep until next review Nov2019"""

    janice = get_janice()
    janice_scores = HighScoresApi(162, 'en', do_init=True)
    inactive = janice.players.query("status == 'i' ")
    # planet_of_inactivate = janice.universe.join(inactive, )
