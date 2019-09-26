import json
import requests


class Universes:
    def get_universes_url(self):
        return 'https://lobby.ogame.gameforge.com/api/servers'

    def load_data(self):
        response = requests.get(self.get_universes_url())
        json_str = response.content.decode('utf-8')
        return json.loads(json_str)
