"""
todo:
 - fix overflow from one 9:499:15 to 1:1:1
 - automate rendering after coordinates and range is entered by user
 - system specific range units (currently planets)
   - 1 galaxy
   - within 50 solar systems
   - within the next 60 planets

"""
from datetime import datetime as dt
import json
import math
from typing import Union
import re

import dash
from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dse
import flask
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from src.api.universe_api import get_janice_universe
from src.api.universe_api import UniverseData
from src.api.scores_api import get_janice_highscore
from src.api.scores_api import HighScoresData
from src.utils import calc_distance
from src.utils import calc_flight_time
from src.planet import Location
from src.planet import Coords


app_tag = 'ONSA - Defending Our Empire. Securing the Future'
CSS_LIST = ['/static/sakura-earthly.css']


def nowstr():
    return dt.now().strftime('%Y%m%d %H:%M:%S.%f')


def search_area_donut(lower_phi=None, upper_phi=None, shift_to_yaxis=None) -> [go.Pie]:
    if not lower_phi:
        lower_phi = math.pi / 4
    if not upper_phi:
        upper_phi = math.pi / 4 + math.pi / 4
    if not shift_to_yaxis:
        shift_to_yaxis = math.pi / 2
    search_area = upper_phi - lower_phi
    rad = 360 / (2 * math.pi)
    remainder = 2 * math.pi - search_area
    donut = go.Pie({
        'rotation': rad * (search_area + lower_phi - shift_to_yaxis),
        'values': [search_area, remainder],
        'textinfo': 'none',
        'hole': .9,
        'marker': {
            'colors': ['rgba(173,255,47,.3)', 'rgba(0,0,0,0.1)']
        },
        'showlegend': False,
        'name': 'search_area_donut',
        'hoverinfo': 'none',

    })
    return donut


def validate_coords(coords):
    """
    validate each part of the user defined coordinate.
    assumes a universe with
     - 9 galaxies, with
     - 499 solar systems, with
     - 15 planets
    """
    if 1 < coords['galaxy'] > 9:
        return {}
    if 1 < coords['system'] > 499:
        return {}
    if 1 < coords['planet'] > 15:
        return {}
    return coords


def validate_user_coords(coords: str):
    """a regex utility to validate user input to sth numerical"""
    result = re.findall(
        r'^([1-9]{1})'  # galaxy
        r':([1-9]{1,3})'  # system
        r':([1-9]{1,2})$',  # planet
        coords
    )
    if len(result) != 1:
        return {}
    coords = {'galaxy': int(result[0][0]),  'system': int(result[0][1]), 'planet': int(result[0][2])}
    coords = validate_coords(coords)
    return coords


def _get_ogame_coordinate(lin_coord: int):
    coords = COORDINATES_DF.query('n == @lin_coord')
    coords = coords.to_dict(orient='records')
    coords = coords[0]
    return coords


def calculate_limits_linear(user_coords: {}, user_range: int) -> {}:
    if 1 < user_range > 15*499:
        raise NotImplementedError
    coords_linear = calculate_linear_coordinate(user_coords)
    return {
        'lower': coords_linear - user_range,
        'upper': coords_linear + user_range
    }


def calculate_limits_coord(user_coords: {}, user_range: int) -> {}:
    if 1 < user_range > 15*499:
        raise NotImplementedError
    coords_linear = calculate_linear_coordinate(user_coords)
    return {
        'lower':  _get_ogame_coordinate(coords_linear - user_range),
        'upper':  _get_ogame_coordinate(coords_linear + user_range)
    }


def validate_user_range(user_range):
    if 1 < user_range > 15*499:
        return None
    return user_range


def calculate_linear_coordinate(coords: {}) -> int:
    """todo find out what it does"""
    value = (
        (coords['galaxy'] - 1) * 499 * 15
        + (coords['system'] - 1) * 15
        + coords['planet']
    )
    return int(value)


def calculate_radius(
        planet_slot: Union[int, float],
        *,
        minimum_distance: Union[int, float] = None,
        planet_increment: Union[int, float] = None
):
    """
    Plotting utility. Returns the the `radius` representing the distance
    of the planet form the center of the universe.
    All planets with the same slot in each solar system are modelled to
    have the same `radius`

    The values `minimum_distance` and `planet_increment` are empirical.

    Args:
        planet_slot (int, float):
        minimum_distance (int, float): the minimum distance every planet should have from the center of the universe
        planet_increment (int, float): distance between each planet slot
    """
    if minimum_distance is None:
        minimum_distance = 1.0
    if planet_increment is None:
        planet_increment = 1 / (15 * 2)
    return minimum_distance + planet_increment * planet_slot


def calculate_system_degree(
        coords: {},
        *,
        galaxy_increment: float = None,
        system_increment: float = None,
        shift_to_yaxis: float = None
) -> Union[float, pd.DataFrame]:
    """
    assumes the universe is modelled clock like in a circle where each
    system corresponds to the minutes/seconds/hours expressed in a degree
    between 0 and 2 * pi.

    Args:
        coords (dict, df): dict like with keys `galaxy` (int, float) and `system` (int, float)
        galaxy_increment (float):
        system_increment (float):
        shift_to_yaxis (float):

    """
    if galaxy_increment is None:
        galaxy_increment = (2 * math.pi) / 9
    if system_increment is None:
        system_increment = galaxy_increment / 499
    if shift_to_yaxis is None:
        shift_to_yaxis = math.pi / 2
    system_degree = (
            (coords['galaxy'] - 1) * galaxy_increment
            + (coords['system'] - 1) * system_increment
            + shift_to_yaxis
    )
    return system_degree


class UniverseFigure:
    galaxies_range = list(range(1, 10))
    systems_range = list(range(1, 500))
    planets_range = list(range(1, 16))
    planet_increment = 1 / (15 * 2)
    galaxy_increment = (2 * math.pi) / 9
    system_increment = galaxy_increment / 499
    minimum_distance = 1
    shift_to_yaxis = math.pi / 2
    universe_data: UniverseData
    highscore_data: HighScoresData
    figure: go.Figure
    df_dummy: pd.DataFrame
    df: pd.DataFrame
    coordinates_df: pd.DataFrame

    def __init__(self):
        self.highscore_data = get_janice_highscore()
        self.universe_data = get_janice_universe()
        self.df_dummy = self.get_dummy_universe_df()
        self.df = self.get_dummy_universe_df()
        self.df = self.insert_universe_data(self.df)
        self.coordinates_df = self.generate_coordinates_df()

    def get_dummy_universe_df(self):
        universe = [{
            'galaxy': galaxy,
            'system': system,
            'planet': planet,
            'taken': 0,
            'coords': f'{galaxy}:{system}:{planet}',
            'x': 0.0,
            'y': 0.0,
            'r': 0.0,
            'system_degree': 0.0
        }
            for galaxy in self.galaxies_range
            for system in self.systems_range
            for planet in self.planets_range
        ]
        df = pd.DataFrame(universe)
        return df

    @staticmethod
    def generate_coordinates_df():
        all_coordinates = [{
            'galaxy': galaxy,
            'system': system,
            'planet': planet,
            'coords': f'{galaxy}:{system}:{planet}',
        }
            for galaxy in UniverseFigure.galaxies_range
            for system in UniverseFigure.systems_range
            for planet in UniverseFigure.planets_range
        ]
        df = pd.DataFrame(all_coordinates)
        df = UniverseFigure.calculate_linear_coordinate_df(df)
        return df

    def calculate_radius(self, x):
        return self.minimum_distance + self.planet_increment * x

    def get_ogame_coordinate(self, lin_coord: int):
        coords = self.coordinates_df.query('n = @lin_coord').to_dict()
        return coords

    @staticmethod
    def calculate_linear_coordinate_df(df):
        df['n'] = (
                (df['galaxy'] - 1) * max(UniverseFigure.systems_range) * max(UniverseFigure.planets_range)
                + (df['system'] - 1) * max(UniverseFigure.planets_range)
                + df['planet']
        )
        return df

    def calculate_system_degree_df(self, df):
        df['system_degree'] = (
                (df['galaxy'] - 1) * self.galaxy_increment
                + (df['system'] - 1) * self.system_increment
                + self.shift_to_yaxis
        )
        return df

    def insert_universe_data(self, df):
        df['taken'] = df['coords'].apply(lambda x: int(self.universe_data.is_planet_taken(x)))
        df = self.calculate_system_degree_df(df)
        df['x'] = df['system_degree'].apply(lambda x: math.cos(x))
        df['y'] = df['system_degree'].apply(lambda x: math.sin(x))
        df['r'] = df['planet'].apply(lambda x: self.calculate_radius(x))
        df = self.calculate_linear_coordinate_df(df)
        return df

    def _get_default_layout(self):
        return go.Layout({
            'autosize': False,
            'width': 700,
            'height': 600,
            'plot_bgcolor': '#f9f9f9',
            'paper_bgcolor': '#f9f9f9',
            'margin': {'l': 20, 'b': 20, 't': 20, 'r': 20},
            'xaxis': {
                'range': [1.75, -1.75],
                'showgrid': False,
                'tickmode': 'auto',
                'nticks': 0,
                'showticklabels': False
            },
            'yaxis': {
                'range': [-1.75, 1.75],
                'showgrid': False,
                'tickmode': 'auto',
                'nticks': 0,
                'showticklabels': False,
                'scaleanchor': 'x',
                'scaleratio': 1
            }
        })

    def _get_figure_data(self, df):
        """
            query_str:
        """
        query_str = 'planet == @planet_slot'
        data = [
                go.Scattergl({
                        'x': (df.query(query_str)['x'] * df.query(query_str)['r']),
                        'y': (df.query(query_str)['y'] * df.query(query_str)['r']),
                        'mode': 'markers',
                        'marker': {
                            'symbol': 'circle',
                            'size': [6 for elm in range(len(df.query(query_str)))],
                            'color': df.query(query_str)['taken'].apply(lambda x: '#66ff66' if x == 0 else '#ff6666'),
                        },
                        'name': f'{planet_slot}. slot',
                        'hoverinfo': 'text',
                        'hovertext': df.query(query_str)['coords']
            }) for planet_slot in self.planets_range
        ]
        return data

    def what_is_it_good_for(self):
        #%% append segmenting hint
        labels = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        values = [4500, 2500, 1053, 500]

        #%% Use `hole` to create a donut-like pie chart
        n_ = go.Pie(
            labels=labels,
            values=values,
            hole=self.minimum_distance
        )

    def _get_figure(self, df):
        data = self._get_figure_data(df)
        layout = self._get_default_layout()
        return go.Figure(
            data=data,
            layout=layout
        )

    def get_dummy_planets_data(self):
        return self.df_dummy

    def get_taken_planets_data(self):
        query_str = 'taken == 1'
        return self.df.query(query_str)

    def get_free_planets_data(self):
        query_str = 'taken == 0'
        return self.df.query(query_str)

    def get_universe_with_player_deteils(self, df_raw):
        df_player_name = UNIVERSE_FIGURE.universe_data.players.loc[:, ['id', 'name', 'status', 'alliance']]
        df_player_name.set_index('alliance', inplace=True)
        df_player_name.rename(index=str, columns={'id': 'player_id','name': 'player_name'}, inplace=True)

        allience_names = UNIVERSE_FIGURE.universe_data.alliences.loc[:, ['id', 'name']]
        allience_names.set_index('id', inplace=True)
        allience_names.rename(index=str, columns={'name': 'allience_name'}, inplace=True)

        df_player = df_player_name.join(allience_names)
        df_player.set_index('player_id', inplace=True, drop=True)

        df_eco_score = UNIVERSE_FIGURE.highscore_data.economy.loc[:, ['id', 'score']]
        df_eco_score.rename(index=str, columns={'id': 'player_id', 'score': 'eco_score'}, inplace=True)
        df_eco_score.set_index('player_id', inplace=True)
        df_player_with_score = df_player.join(df_eco_score)

        df_detailed = df_raw.set_index('player').join(df_player_with_score)

        df_viz = UNIVERSE_FIGURE.df.loc[:, ['coords', 'x', 'y', 'r', 'n', 'taken', 'planet', 'galaxy', 'system']]
        df_viz.set_index('coords', inplace=True)
        df = df_detailed.set_index('coords').join(df_viz)
        df.reset_index(inplace=True)
        df['n2'] = df['n']  # introduce possible second filter rule
        df = df[['n', 'n2', 'x', 'y', 'r', 'galaxy', 'system', 'planet', 'taken', 'coords', 'planet_name', 'player_name', 'status', 'allience_name', 'eco_score']]
        return df

    def get_dummy_planets_fig(self):
        df = self.get_dummy_planets_data()
        return self._get_figure(df)

    def get_taken_planets_fig(self):
        df = self.get_taken_planets_data()
        return self._get_figure(df)

    def get_free_planets_fig(self):
        df = self.get_free_planets_data()
        return self._get_figure(df)

    def get_taken_inactive_planets_fig(self):
        df = self.get_taken_inactive_planets_data()
        return self._get_figure(df)

    def get_taken_active_planets_fig(self):
        df = self.get_taken_active_planets_data()
        return self._get_figure(df)

    def _get_active_players(self):
        return self.universe_data.players.query("status != 'i' ")['id'].tolist()

    def _get_inactive_players(self):
        return self.universe_data.players.query("status == 'i' ")['id'].tolist()

    def get_taken_inactive_planets_data(self):
        inactive = self._get_inactive_players()
        query_str = 'player == @inactive'
        coords = self.universe_data.universe.query(query_str)['coords'].to_list()
        return self.df.query('taken == 1 and coords in @coords')

    def get_taken_active_planets_data(self):
        active = self._get_active_players()
        query_str = 'player == @active'
        coords = self.universe_data.universe.query(query_str)['coords'].to_list()
        return self.df.query('taken == 1 and coords in @coords')


def get_inactive_player():
    inactive = UNIVERSE_FIGURE._get_inactive_players()
    query_str = 'player == @inactive'
    df_raw = UNIVERSE_FIGURE.universe_data.universe.query(query_str)
    df_raw.rename(index=str, columns={'name': 'planet_name'}, inplace=True)
    df = UNIVERSE_FIGURE.get_universe_with_player_deteils(df_raw)
    return df


def get_active_player():
    active = UNIVERSE_FIGURE._get_inactive_players()
    query_str = 'player == @active'
    df_raw = UNIVERSE_FIGURE.universe_data.universe.query(query_str)
    df_raw.rename(index=str, columns={'name': 'planet_name'}, inplace=True)
    df = UNIVERSE_FIGURE.get_universe_with_player_deteils(df_raw)
    return df


def cast_to_dash_table(df):
    return dse.DataTable(**{
        'id': 'universe-data-table',
        'columns': [{'name': col, 'id': col} for col in df.columns],
        'data': df.to_dict('records'),
        'id': 'universe-data-table',
        'filter_action': 'native',
        'sort_action': 'native',
        'export_format': 'csv',
        'export_headers': 'display',
        'style_cell': {
            'minWidth': '40px',
            'maxWidth': '100px',
            'textOverflow': 'clip',
            'overflow': 'hidden',
        }
    })


def get_initial_app_layout():
    return html.Div([
        html.Button(
            children='Re Render',
            type='submit',
            id='universe-graph-render-button'
        ),
        dcc.RadioItems(
            options=[
                {'label': 'free', 'value': 'free'},
                {'label': 'taken', 'value': 'taken'}
            ],
            value='taken',
            id='universe-taken-free-toggle'
        ),
        dcc.RadioItems(
            options=[
                {'label': 'active', 'value': 'active'},
                {'label': 'inactive', 'value': 'inactive'}
            ],
            value='active',
            id='universe-active-inactive-toggle'
        ),
        html.Div([
            dcc.Loading(
                dcc.Graph(
                        figure=UNIVERSE_FIGURE.get_dummy_planets_fig(),
                        config={},
                        id='universe-graph'
                    )
                ),
            dcc.Loading(
                html.Div([
                    dse.DataTable()
                ], id='universe-data-table-wrapper')
            )
        ])
    ], className='aptry')


dbug = '''
UNIVERSE_FIGURE = UniverseFigure()
import pickle
with open('cache.pickle', 'wb') as file:
     pickle.dump(UNIVERSE_FIGURE, file)'''
import pickle
with open('cache.pickle', 'rb') as file_2:
    UNIVERSE_FIGURE = pickle.load(file_2)


server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True
)

app.layout = get_initial_app_layout()


cb = '''
@app.callback(
    Output('universe-graph', 'figure'),
    [Input('universe-graph-render-button', 'n_clicks')]
)
def rerender_figure(n_clicks):
    return get_universe_fig()
'''


@app.callback(
    Output('universe-graph', 'figure'),
    [Input('universe-active-inactive-toggle', 'value'),
     Input('universe-taken-free-toggle', 'value')],
    [State('universe-graph', 'figure')]
)
def show_taken_or_free(activeOrInactive, takenOrFree, figure):
    if activeOrInactive == 'active' and takenOrFree == 'taken':
        return UNIVERSE_FIGURE.get_taken_active_planets_fig()
    if activeOrInactive == 'inactive' and takenOrFree == 'taken':
        return UNIVERSE_FIGURE.get_taken_inactive_planets_fig()
    if activeOrInactive == 'active' and takenOrFree == 'free':
        return UNIVERSE_FIGURE.get_free_planets_fig()
    if activeOrInactive == 'inactive' and takenOrFree == 'free':
        return figure


@app.callback(
    Output('universe-data-table-wrapper', 'children'),
    [Input('universe-active-inactive-toggle', 'value'),
     Input('universe-taken-free-toggle', 'value')],
    [State('universe-data-table-wrapper', 'children')]
)
def render_data_table(activeOrInactive, takenOrFree, child):
    if activeOrInactive == 'active' and takenOrFree == 'taken':
        active = UNIVERSE_FIGURE._get_active_players()
        query_str = 'player == @active'
        df_raw = UNIVERSE_FIGURE.universe_data.universe.query(query_str)
        df_raw.rename(index=str, columns={'name': 'planet_name'}, inplace=True)
        df = UNIVERSE_FIGURE.get_universe_with_player_deteils(df_raw)
        return html.Div(cast_to_dash_table(df))
    if activeOrInactive == 'inactive' and takenOrFree == 'taken':
        inactive = UNIVERSE_FIGURE._get_inactive_players()
        query_str = 'player == @inactive'
        df_raw = UNIVERSE_FIGURE.universe_data.universe.query(query_str)
        df_raw.rename(index=str, columns={'name': 'planet_name'}, inplace=True)
        df = UNIVERSE_FIGURE.get_universe_with_player_deteils(df_raw)
        return html.Div(cast_to_dash_table(df))
    if activeOrInactive == 'active' and takenOrFree == 'free':
        df = UNIVERSE_FIGURE.get_free_planets_data()
        return html.Div(cast_to_dash_table(df))
    if activeOrInactive == 'inactive' and takenOrFree == 'free':
        df = UNIVERSE_FIGURE.get_free_planets_data()
        return html.Div(cast_to_dash_table(df))


if __name__ == '__main__':
    app.run_server()
