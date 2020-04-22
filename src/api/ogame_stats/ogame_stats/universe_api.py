#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 15 18:16:05 2019
@author: kan

Update frequencies:

    players.xml -> daily
    universe.xml -> weekly
    highscore.xml -> hourly
    alliances.xml -> daily
    serverData.xml -> daily
    playerData.xml -> weekly
    localization.xml -> static
    universes.xml -> static

"""
import json
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import xmltodict
from urllib.parse import urlencode
from .utils import ApiBaseClass


class UniverseDataUrls(ApiBaseClass):
    def __init__(self, universe: int, community: str):
        self.universe = universe
        self.community = community

    def _get_base_url(self):
        return f"https://s{self.universe}-{self.community}.ogame.gameforge.com/api"

    def _get_serverdata_url(self):
        return f"{self._get_base_url()}/serverData.xml"

    def _get_universe_url(self):
        return f"{self._get_base_url()}/universe.xml"

    def _get_players_url(self):
        return f"{self._get_base_url()}/players.xml"

    def _get_alliences_url(self):
        return f"{self._get_base_url()}/alliances.xml"

    def _get_localization_url(self):
        return f"{self._get_base_url()}/localization.xml"

    def _get_playerdata_url(self, player_id: int):
        query = {'id': player_id}
        return f'{self._get_base_url()}/playerData.xml?{urlencode(query)}'

    def load_server_data(self):
        url = self._get_serverdata_url()
        response = requests.get(url)
        xml_string = response.content.decode('utf-8')
        root = ET.fromstring(xml_string)
        return {elm.tag: elm.text for elm in root.getchildren()}

    def load_players_data(self):
        """['id', 'name', 'status', 'alliance']"""
        url = self._get_players_url()
        return self._load_data_as_df(url)

    def load_universe_data(self):
        """['id', 'player', 'name', 'coords']"""
        url = self._get_universe_url()
        return self._load_data_as_df(url)

    def load_alliances_data(self):
        """['foundDate', 'founder', 'homepage', 'id', 'logo', 'name', 'open', 'tag']"""
        url = self._get_alliences_url()
        return self._load_data_as_df(url)

    def load_game_schema(self):
        """{'techs': {'1': 'Metal Mine'}, 'missions': {'1': 'Attack'}"""
        url = self._get_localization_url()
        response = requests.get(url)
        xml_string = response.content.decode('utf-8')
        root = ET.fromstring(xml_string)
        return {
            elm.tag: {
                child.attrib['id']: child.text
                for child in list(elm)
            } for elm in root.getchildren()
        }


class UniverseData:
    players: pd.DataFrame = None
    universe: pd.DataFrame = None
    alliences: pd.DataFrame = None
    serverdata: dict = None
    techs: dict = None
    missions: dict = None
    universe_id: int = None
    community: str = None
    urls: UniverseDataUrls = None

    def __init__(self, universe_id: int, community: str):
        """
        Args:
            universe_id (int): an integer identifying the universe (e.g. 162 - Janice)
            community (str):  an string indicating (language) community='en'
        """
        self.universe_id = universe_id
        self.community = community
        self.urls = UniverseDataUrls(universe_id, community)
        self.players = self.urls.load_players_data()
        self.universe = self.urls.load_universe_data()
        self.universe_coords_list = self.universe['coords'].to_list()
        self.alliences = self.urls.load_alliances_data()
        self.serverdata = self.urls.load_server_data()
        game_schema = self.urls.load_game_schema()
        self.techs = game_schema['techs']
        self.missions = game_schema['missions']

    def get_planets_of_player(self, player_name: str) -> dict:
        player_id_str = self.get_player_id(player_name)
        results = self.universe.query('player == @player_id_str')
        results = results.reset_index(drop=True)
        return results[['coords', 'name']].to_dict(orient='records')

    def get_planets_of_player_by_id(self, player_id_str: str) -> dict:
        results = self.universe.query('player == @player_id_str')
        results = results.reset_index(drop=True)
        return results[['coords', 'name']].to_dict(orient='records')

    def get_planets_of_player_as_json(self, player_name: str):
        results = self.get_planets_of_player(player_name)
        return json.dumps(results, indent=2)

    def get_player_id(self, player_name: str) -> str:
        try:
            return str(self.players.query('name == @player_name').iloc[0]['id'])
        except IndexError:
            print(f"`{player_name}` not found. look at `players['name']` for valid player names")

    def get_player_status(self, player_name: str) -> str:
        """['a', nan, 'vi', 'v', 'I', 'vIb', 'vb', 'vI', 'i', 'o', 'vib', 'vo']"""
        return str(self.players.query("name == @player_name").iloc[0]['status'])

    def get_player_alliance(self, player_name: str) -> str:
        """integer as str"""
        return str(self.players.query("name == @player_name").iloc[0]['alliance'])

    def get_player_data(self, player_name: str) -> dict:
        player_id_str = self.get_player_id(player_name)
        url = self.urls._get_playerdata_url(int(player_id_str))
        response = requests.get(url)
        xml_string = response.content.decode('utf-8')
        return dict(xmltodict.parse(xml_string))

    def get_player_data_as_json(self, player_name: str) -> str:
        return json.dumps(self.get_player_data(player_name), indent=2)

    def get_alliance_id_by_tag(self, tag: str) -> str:
        return self.alliences.query('tag == @tag').iloc[0]['id']

    def get_alliance_id_by_name(self, name: str) -> str:
        return self.alliences.query('name == @name').iloc[0]['id']

    def get_players_of_allience(self, tag: str) -> pd.DataFrame:
        allience_id = self.get_alliance_id_by_tag(tag)
        members = self.players.query('alliance == @allience_id')
        return members

    def get_players_of_allience_by_name(self, name: str) -> pd.DataFrame:
        allience_id = self.get_alliance_id_by_name(name)
        members = self.players.query('alliance == @allience_id')
        return members

    def get_planets_of_alliance(self, tag: str) -> [str]:
        members = self.get_players_of_allience(tag)
        member_ids = members['id'].to_list()
        data = [self.get_planets_of_player_by_id(player_id) for player_id in member_ids]
        coords = [planet['coords'] for player in data for planet in player]
        coords.sort()
        return coords

    def get_planets_distribution_by_galaxy(self, allience_tag: str) -> dict:
        galaxy_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        coords = self.get_planets_of_alliance(allience_tag)
        return {galaxy: sum([elm[0] == galaxy for elm in coords]) for galaxy in galaxy_list}

    def is_planet_taken(self, coords_str: str) -> bool:
        if coords_str in self.universe_coords_list:
            result = True
        else:
            result = False
        return result
