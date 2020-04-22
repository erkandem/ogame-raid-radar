import json
import requests


class UniversesData:

    def __init__(self):
        self.data = self.load_data()

    def _get_universes_url(self) -> str:
        return 'https://lobby.ogame.gameforge.com/api/servers'

    def load_data(self):
        response = requests.get(self._get_universes_url())
        json_str = response.content.decode('utf-8')
        return json.loads(json_str)

