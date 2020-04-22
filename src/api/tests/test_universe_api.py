from ogame_stats.highscores_api import HighScoreUrls
from .testing_utils import TestingFiles as tf


class TestHighScoresUrls:
    """
    talking about the low hanging fruits
    """
    universe_id = 999
    community = 'en'

    def test__get_base_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = f"https://s{self.universe_id}-{self.community}.ogame.gameforge.com/api/highscore.xml"
        assert hs._get_base_url() == expected

    def test__get_scores_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?somethig=special'
        result = hs._get_scores_url({'somethig': 'special'})
        assert result == expected

    def test__get_total_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?category=1&type=0'
        result = hs._get_total_url()
        assert result == expected

    def test__get_economy_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?category=1&type=1'
        result = hs._get_economy_url()
        assert result == expected

    def test__get_research_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?category=1&type=2'
        result = hs._get_research_url()
        assert result == expected

    def test__get_military_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?category=1&type=3'
        result = hs._get_military_url()
        assert result == expected

    def test__get_military_built_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?category=1&type=4'
        result = hs._get_military_built_url()
        assert result == expected

    def test__get_military_destroyed_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?category=1&type=5'
        result = hs._get_military_destroyed_url()
        assert result == expected

    def test__get_military_lost_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?category=1&type=6'
        result = hs._get_military_lost_url()
        assert result == expected

    def test__get_honor_url(self):
        hs = HighScoreUrls(self.universe_id, self.community)
        expected = hs._get_base_url() + '?category=1&type=7'
        result = hs._get_honor_url()
        assert result == expected
