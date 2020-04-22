import json
import requests
from .utils import ApiBaseClass, nowstr


class UniversesData(ApiBaseClass):

    def __init__(self):
        self.data = self.load_universes()

    def _get_universes_url(self) -> str:
        return 'https://lobby.ogame.gameforge.com/api/servers'

    def _load_data(self, url):
        """overwrites parents because we receive json instead of xml"""
        response = requests.get(self._get_universes_url())
        json_str = response.content.decode('utf-8')
        return json.loads(json_str)

    def load_universes(self):
        url = self._get_universes_url()
        self._load_data_as_df(url)
