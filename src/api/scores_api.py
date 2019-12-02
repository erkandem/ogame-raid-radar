from urllib.parse import urlencode
import requests
import xml.etree.ElementTree as ET
import pandas as pd


class HighScoreUrls:
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

    def __init__ (self, universe_id: int, community: str):
        self.universe_id = universe_id
        self.community = community
        return

    def _get_base_url(self):
        return f"https://s{self.universe_id}-{self.community}.ogame.gameforge.com/api/highscore.xml"

    def __get_scores_url(self, query: dict):
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_total_url(self):
        query = {'category': 1, 'type': 0}
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_economy_url(self):
        query = {'category': 1, 'type': 1}
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_research_url(self):
        query = {'category': 1, 'type': 2}
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_military_url(self):
        query = {'category': 1, 'type': 3}
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_military_built_url(self):
        query = {'category': 1, 'type': 4}
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_military_destroyed_url(self):
        query = {'category': 1, 'type': 5}
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_military_lost_url(self):
        query = {'category': 1, 'type': 6}
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _get_honor_url(self):
        query = {'category': 1, 'type': 7}
        return f'{self._get_base_url()}?{urlencode(query)}'

    def _load_data(self, url):
        """['id', 'name', 'status', 'alliance']"""
        response = requests.get(url)
        xml_string = response.content.decode('utf-8')
        root = ET.fromstring(xml_string)
        return [elm.attrib for elm in root]

    def _load_data_as_df(self, url):
        data = self._load_data(url)
        return pd.DataFrame(data)

    def get_total_data(self):
        url = self._get_total_url()
        return self._load_data_as_df(url)

    def get_economy_data(self):
        url = self._get_economy_url()
        return self._load_data_as_df(url)

    def get_research_data(self):
        url = self._get_research_url()
        return self._load_data_as_df(url)

    def get_military_data(self):
        url = self._get_military_url()
        return self._load_data_as_df(url)

    def get_military_built_data(self):
        url = self._get_military_built_url()
        return self._load_data_as_df(url)

    def get_military_destroyed_data(self):
        url = self._get_military_destroyed_url()
        return self._load_data_as_df(url)

    def get_military_lost_data(self):
        url = self._get_military_lost_url()
        return self._load_data_as_df(url)

    def get_honor_data(self):
        url = self._get_honor_url()
        return self._load_data_as_df(url)


class HighScoresDataApi:
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
        return


def get_janice_highscore():
    return HighScoresDataApi(universe_id=162, community='en', do_init=True)
