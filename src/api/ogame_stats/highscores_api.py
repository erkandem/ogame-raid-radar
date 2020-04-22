from urllib.parse import urlencode
import pandas as pd
from .utils import ApiBaseClass


class HighScoreUrls(ApiBaseClass):
    universe_id: int
    community: str
    hs_categories = {
        'player': 1,
        'alliance': 2
    }
    hs_types = {
        'total': 0,
        'economy': 1,
        'research': 2,
        'military': 3,
        'mil_built': 4,
        'mil_destroyed': 5,
        'mil_lost': 6,
        'honor': 7
    }

    def __init__(self, universe_id: int, community: str):
        self.universe_id = universe_id
        self.community = community

    def _get_base_url(self):
        return f"https://s{self.universe_id}-{self.community}.ogame.gameforge.com/api/highscore.xml"

    def _get_scores_url(self, query: dict):
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_total_url(self):
        """ position: str, id: str, score: str"""
        query = {'category': 1, 'type': 0}
        return self._get_scores_url(query)

    def _get_economy_url(self):
        query = {'category': 1, 'type': 1}
        return self._get_scores_url(query)

    def _get_research_url(self):
        query = {'category': 1, 'type': 2}
        return self._get_scores_url(query)

    def _get_military_url(self):
        query = {'category': 1, 'type': 3}
        return self._get_scores_url(query)

    def _get_military_built_url(self):
        query = {'category': 1, 'type': 4}
        return self._get_scores_url(query)

    def _get_military_destroyed_url(self):
        query = {'category': 1, 'type': 5}
        return self._get_scores_url(query)

    def _get_military_lost_url(self):
        query = {'category': 1, 'type': 6}
        return self._get_scores_url(query)

    def _get_honor_url(self):
        query = {'category': 1, 'type': 7}
        return self._get_scores_url(query)

    def get_total_data(self):
        url = self._get_total_url()
        df = self._load_data_as_df(url)
        df['score'] = df['score'].astype(float)
        return df

    def get_economy_data(self):
        url = self._get_economy_url()
        df = self._load_data_as_df(url)
        df['score'] = df['score'].astype(float)
        return df

    def get_research_data(self):
        url = self._get_research_url()
        df = self._load_data_as_df(url)
        df['score'] = df['score'].astype(float)
        return df

    def get_military_data(self):
        url = self._get_military_url()
        df = self._load_data_as_df(url)
        df['score'] = df['score'].astype(float)
        return df

    def get_military_built_data(self):
        url = self._get_military_built_url()
        df = self._load_data_as_df(url)
        df['score'] = df['score'].astype(float)
        return df

    def get_military_destroyed_data(self):
        url = self._get_military_destroyed_url()
        df = self._load_data_as_df(url)
        df['score'] = df['score'].astype(float)
        return df

    def get_military_lost_data(self):
        url = self._get_military_lost_url()
        df = self._load_data_as_df(url)
        df['score'] = df['score'].astype(float)
        return df

    def get_honor_data(self):
        url = self._get_honor_url()
        df = self._load_data_as_df(url)
        df['score'] = df['score'].astype(float)
        return df


class HighScoresData:
    universe_id: int
    community: str
    total: pd.DataFrame
    economy: pd.DataFrame
    research: pd.DataFrame
    military: pd.DataFrame
    mil_built: pd.DataFrame
    mil_destroyed: pd.DataFrame
    mil_lost: pd.DataFrame
    honor: pd.DataFrame
    urls: HighScoreUrls

    def __init__(self, universe_id: int, community: str, do_init: bool = False):
        self.universe_id = universe_id
        self.community = community
        self.urls = HighScoreUrls(universe_id, community)
        self.total = self.urls.get_total_data()
        self.economy = self.urls.get_economy_data()
        self.research = self.urls.get_research_data()
        self.military = self.urls.get_military_data()
        self.military_built = self.urls.get_military_built_data()
        self.military_destroyed = self.urls.get_military_destroyed_data()
        self.military_lost = self.urls.get_military_lost_data()
        self.honor = self.urls.get_honor_data()
