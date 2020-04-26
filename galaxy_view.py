"""
todo:
 - fix overflow from one 9:499:15 to 1:1:1
 - automate rendering after coordinates and range is entered by user
 - system specific range units (currently planets)
   - 1 galaxy
   - within 50 solar systems
   - within the next 60 planets

"""
import copy
from datetime import datetime as dt
import json
import math
from typing import Union, Dict, List
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
from ogame_stats import UniverseData, UniverseQuestions
from ogame_stats import HighScoreData
import requests_cache
requests_cache.install_cache('demo_cache')


app_tag = 'ONSA - Defending Our Empire. Securing the Future'
CSS_LIST = ['/static/sakura-solarized-dark.css']


def nowstr():
    return dt.now().strftime('%Y%m%d %H:%M:%S.%f')


def search_area_donut(
        lower_phi=None,
        upper_phi=None,
        shift_to_yaxis=None
) -> [go.Pie]:
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


def parse_user_coords(coords: str):
    """a regex utility to validate user input to sth numerical"""
    result = re.findall(
        r'^([1-9])'  # galaxy
        r':([1-9]{1,3})'  # system
        r':([1-9]{1,2})$',  # planet
        coords
    )
    if len(result) != 1:
        return {}
    coords = {
        'galaxy': int(result[0][0]),
        'system': int(result[0][1]),
        'planet': int(result[0][2])
    }
    coords = validate_coords(coords)
    return coords


def calculate_limits_coord(user_coords: {}, user_range: int) -> {}:
    if user_range < 1:
        raise NotImplementedError('range must be positive non zero')
    if user_range > (max(UNIVERSE_FIGURE.systems_range)):
        raise NotImplementedError(
            'Overflow not implemented (move from end of universe to beginning)'
        )

    # translate user_range to systems
    user_range = user_range * max(UNIVERSE_FIGURE.planets_range)

    # adjust the planet of the user to the last planet in the system
    user_coords_copy = copy.deepcopy(user_coords)
    user_coords_copy['planet'] = max(UNIVERSE_FIGURE.planets_range)
    coords_linear = UNIVERSE_FIGURE.calculate_linear_coordinate(user_coords_copy)
    return {
        'lower': UNIVERSE_FIGURE._get_ogame_coordinate_from_linear(coords_linear - user_range),
        'upper': UNIVERSE_FIGURE._get_ogame_coordinate_from_linear(coords_linear + user_range)
    }


def validate_user_range(user_range):
    if 1 < user_range > 15*499:
        return None
    return user_range


class UniverseFigure:

    def __init__(self):
        """
        TODO: remove hardcoding of universe to plot, and galaxies per universe and so on
              these values depend on the specific universe
        """
        self.galaxies_range = list(range(1, 10))
        self.systems_range = list(range(1, 500))
        self.planets_range = list(range(1, 16))
        self.planet_increment = 1 / (max(self.planets_range) * 2)
        self.galaxy_increment = (2 * math.pi) / max(self.galaxies_range)
        self.system_increment = self.galaxy_increment / max(self.systems_range)
        self.minimum_distance = 1
        self.shift_to_yaxis = math.pi / 2
        self.highscore_data = HighScoreData(universe_id=162, community='en')
        self.universe_data = UniverseQuestions(universe_id=162, community='en')
        self.df_dummy = self.get_dummy_universe_df()
        self.df = self.get_dummy_universe_df()
        self.df = self.insert_universe_data(self.df)

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
        df['n'] = self.calculate_linear_coordinate(df)
        return df

    def calculate_radius(
            self,
            planet_slot: Union[int, float],
            *,
            minimum_distance: Union[int, float] = None,
            planet_increment: Union[int, float] = None
    ) -> float:
        """
        Plotting utility. Returns the the `radius` representing the distance
        of the planet form the center of the universe.
        All planets with the same slot in each solar system are modelled to
        have the same `radius`

        The values `minimum_distance` and `planet_increment` are empirical.

        Args:
            planet_slot (int, float):
            minimum_distance (int, float): the minimum distance every planet should
                                           have from the center of the universe
            planet_increment (int, float): distance between each planet slot

        Return:
            (float)
        """
        if minimum_distance is None:
            minimum_distance = self.minimum_distance
        if planet_increment is None:
            planet_increment = self.planet_increment

        return minimum_distance + planet_increment * planet_slot

    def _get_ogame_coordinate_from_linear(
            self,
            lin_coord: int
    ) -> {str: int}:
        """
        Inverse operation of `calculate_linear_coordinate`

        Args:
            lin_coord(int):

        Returns:
            (dict) with `galaxy`, `system` and `planet` keys, with integer values
        """
        coords = self.df_dummy.query('n == @lin_coord')
        coords = coords.to_dict(orient='records')
        coords = coords[0]
        return coords

    def calculate_linear_coordinate(
            self,
            df:
            Union[pd.DataFrame, Dict]
    ) -> Union[pd.Series, int]:
        """
        calculates a unique planet ID (integer) based on the universe configuration.
        
        Inverse of `_get_ogame_coordinate_from_linear`
        
        Args:
            df (pd.DataFrame): contains at least `galaxy`, `system` `planet`.
        """

        value = (
                (df['galaxy'] - 1) * max(self.systems_range) * max(self.planets_range)
                + (df['system'] - 1) * max(self.planets_range)
                + df['planet']
        )
        return value

    def calculate_system_degree(
            self,
            df: Union[pd.DataFrame, Dict],
            *,
            galaxy_increment: float = None,
            system_increment: float = None,
            shift_to_yaxis: float = None
    ) -> Union[pd.Series, float]:
        """
        assumes the universe is modelled clock like in a circle where each
        system corresponds to the minutes/seconds/hours expressed in a degree
        between 0 and 2 * pi.

        will prefer user supplied values in `kwargs` or look them up in the instance

        Args:
            df (pd.DataFrame, dict): dict like with keys `galaxy` (int, float) and `system` (int, float)
            galaxy_increment (float):
            system_increment (float):
            shift_to_yaxis (float):

        Returns:
            (pd.Series, float): depending on the input

        """
        if not galaxy_increment:
            galaxy_increment = self.galaxy_increment
        if not system_increment:
            system_increment = self.system_increment
        if not shift_to_yaxis:
            shift_to_yaxis = self.shift_to_yaxis
        system_degree = (
                (df['galaxy'] - 1) * galaxy_increment
                + (df['system'] - 1) * system_increment
                + shift_to_yaxis
        )
        return system_degree

    def insert_universe_data(self, df):
        df['taken'] = df['coords'].apply(lambda x: int(self.universe_data.is_planet_taken(x)))
        df['system_degree'] = self.calculate_system_degree(df)
        df['x'] = df['system_degree'].apply(lambda x: math.cos(x))
        df['y'] = df['system_degree'].apply(lambda x: math.sin(x))
        df['r'] = df['planet'].apply(lambda x: self.calculate_radius(x))
        return df

    def _get_default_layout(self):
        return go.Layout({
            'title': {
                'text': 'inactive players in your area',
                'font': {
                    'family': 'serif',
                    'size': 18,
                    'color': '#00DA00'
                },
                'x': 0.025,
                'y': 0.975,
            'yanchor': 'top',
            'xanchor': 'left',
            },
            'autosize': False,
            'width': 650,
            'height': 500,
            'plot_bgcolor': '#005A6F',
            'paper_bgcolor': '#005A6F',
            'margin': {'l': 20, 'b': 20, 't': 20, 'r': 20},
            'xaxis': {
                'range': [1.55, -1.55],
                'zeroline': False,
                'showgrid': False,
                'tickmode': 'auto',
                'nticks': 0,
                'showticklabels': False
            },
            'yaxis': {
                'range': [-1.55, 1.55],
                'zeroline': False,
                'showgrid': False,
                'tickmode': 'auto',
                'nticks': 0,
                'showticklabels': False,
                'scaleanchor': 'x',
                'scaleratio': 1
            }
        })

    def _get_figure_data(self, df: pd.DataFrame) -> List[go.Scattergl]:
        """
        casts data within a pandas object into a list of dash object.
        iterate over each all planet slots available for that universe
        and create a scatter char with for each slot (same slot -> same radius).

        TODO change color intensity with eco score of each planet to represent juiciness
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
                        'hovertext': df.query(query_str)['coords'],
                        'showlegend': False,
            }) for planet_slot in self.planets_range
        ]
        return data

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

    def get_universe_with_player_details(self, df_raw):
        df_player_name = UNIVERSE_FIGURE.universe_data.players.loc[:, ['id', 'name', 'status', 'alliance']]
        df_player_name.set_index('alliance', inplace=True)
        df_player_name.rename(index=str, columns={'id': 'player_id','name': 'player_name'}, inplace=True)

        alliance_names = UNIVERSE_FIGURE.universe_data.alliances.loc[:, ['id', 'name']]
        alliance_names.set_index('id', inplace=True)
        alliance_names.rename(index=str, columns={'name': 'alliance_name'}, inplace=True)

        df_player = df_player_name.join(alliance_names)
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
        df = df[['n', 'n2', 'x', 'y', 'r', 'galaxy', 'system', 'planet', 'taken', 'coords', 'planet_name', 'player_name', 'status', 'alliance_name', 'eco_score']]
        return df

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

    def get_inactive_players(self):
        inactive = self._get_inactive_players()
        query_str = 'player == @inactive'
        df_raw = self.universe_data.universe.query(query_str)
        df_raw.rename(index=str, columns={'name': 'planet_name'}, inplace=True)
        df = self.get_universe_with_player_details(df_raw)
        return df

    def get_active_players(self):
        active = self._get_inactive_players()
        query_str = 'player == @active'
        df_raw = self.universe_data.universe.query(query_str)
        df_raw.rename(index=str, columns={'name': 'planet_name'}, inplace=True)
        df = self.get_universe_with_player_details(df_raw)
        return df


def cast_to_dash_table(df: pd.DataFrame, columns: List = None) -> dse.DataTable:
    """
    casts the data of an pandas object into
    dash DataTable object

    Args:
        df (pd.DataFrame):
    """
    if not columns:
        columns = df.columns
    return dse.DataTable(**{
        'id': 'universe-data-table',
        'columns': [{'name': col, 'id': col} for col in columns],
        'data': df.to_dict('records'),
        'filter_action': 'native',
        'sort_action': 'native',
        'export_format': 'csv',
        'export_headers': 'display',
        'row_selectable': 'multi',
        'row_deletable': True,
        'selected_columns': [],
        'selected_rows': [],
        'page_current': 0,
        'page_size': 10,
        'style_cell': {
            'minWidth': '40px',
            'maxWidth': '100px',
            'textOverflow': 'clip',
            'overflow': 'hidden',
        }
    })


def get_initial_app_layout():
    return html.Div([
        html.Div([
            html.H3('Raid Radar'),
            html.Div(
                'The plot below will visualize the planets in the area of your planet'
                ' form which your starting to collect the resources of inactive users'
            ),
            html.Br(),
            html.Div([
                html.Div([
                    html.Label('acceptable travel range in systems (e.g. 1-499)'),
                    dcc.Input(
                        type='number',
                        value=50,
                        id='universe-range-query-range'
                    ),
                ]),
                html.Div([
                    html.Label('departure planet (e.g. 2:222:2)'),
                    dcc.Input(
                        placeholder='Your planet (e.g. 2:222:2)',
                        type='text',
                        value='2:222:2',
                        id='universe-range-query-start-coords'
                    ),
                ]),
                html.Div(
                    '[{}]',
                    id='universe-range-query-intermediate-data',
                    style={'display': 'none'}),
            ], id='universe-range-query-container'
            ),
            html.Br(),
            dcc.Graph(
                    figure=UNIVERSE_FIGURE.get_taken_inactive_planets_fig(),
                    config={},
                    id='universe-graph'
                ),
            html.Br(),
            dcc.Loading(
                html.Div([
                    html.Div(
                        cast_to_dash_table(
                            UNIVERSE_FIGURE.get_inactive_players(),
                            columns=['coords','galaxy', 'system', 'planet', 'taken', 'planet_name', 'player_name', 'status', 'alliance_name', 'eco_score']
                        )
                    )
                ], id='universe-data-table-wrapper')
            ),
            html.Div(id='universe-data-interactivity-container')
        ])
    ], className='raid-radar-app')


UNIVERSE_FIGURE = UniverseFigure()
server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    external_stylesheets=CSS_LIST
)

app.layout = get_initial_app_layout()


@app.callback(
    Output('universe-data-interactivity-container', 'children'),
    [Input('universe-data-table', 'derived_virtual_data'),
     Input('universe-data-table', 'derived_virtual_selected_rows')],
    [State('universe-active-inactive-toggle', 'value'),
     State('universe-taken-free-toggle', 'value'),
     State('universe-data-interactivity-container', 'children')]
)
def update_graphs(
        rows,
        derived_virtual_selected_rows,
        activeOrInactive,
        takenOrFree,
        container_child
):
    """
    Update graphs according to data in the dashTable

        rows: rows of  data to plot
        derived_virtual_selected_rows:
        activeOrInactive: value of player status selector
        takenOrFree: value of planet status selector
        container_child: dummy html container element used to start the app

    """
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    if not rows:
        return container_child
    if len(rows) == 0:
        return container_child
    dff = pd.DataFrame(rows)
    fig = UNIVERSE_FIGURE._get_figure(dff)
    return dcc.Graph(
        figure=fig,
        config={},
        id='universe-data-custom-graph'
    )


@app.callback(
    Output('universe-range-query-intermediate-data', 'children'),
    [Input('universe-range-query-start-coords', 'value'),
     Input('universe-range-query-range', 'value')]
)
def aggregate_data_processing(user_coords, user_range):
    """
    dangerous - using an invisible dict to store data in the clients browser
    """
    user_coords = parse_user_coords(user_coords)
    if len(list(user_coords)) == 0:
        return json.dumps([{'error_msg': 'invalid coordinates'}])
    user_range = validate_user_range(user_range)
    if user_range is None:
        return json.dumps([{'error_msg': 'invalid range'}])
    limits = calculate_limits_coord(user_coords, user_range)
    if len(list(limits)) == 0:
        return json.dumps([{'error_msg': 'server error'}])
    data = [{
        'plotable_limits': {
            'user': {
                'phi': UNIVERSE_FIGURE.calculate_system_degree(user_coords),
                'radius': UNIVERSE_FIGURE.calculate_radius(user_coords['planet'])
            },
            'lower': {
                'phi': UNIVERSE_FIGURE.calculate_system_degree(limits['lower']),
                'radius': UNIVERSE_FIGURE.calculate_radius(limits['lower']['planet'])},
            'upper': {
                'phi': UNIVERSE_FIGURE.calculate_system_degree(limits['upper']),
                'radius': UNIVERSE_FIGURE.calculate_radius(limits['upper']['planet'])
            },
        },
        'query_limits': {
            'lower': UNIVERSE_FIGURE.calculate_linear_coordinate(limits['lower']),
            'upper': UNIVERSE_FIGURE.calculate_linear_coordinate(limits['upper'])
        }
    }]
    return json.dumps(data)


@app.callback(
    Output('universe-graph', 'figure'),
    [Input('universe-range-query-intermediate-data', 'children')],
    [State('universe-graph', 'figure')]
)
def update_graph_1(jsonified_cleaned_data, figure):
    dataset = json.loads(jsonified_cleaned_data)[0]
    if 'plotable_limits' not in dataset:
        return figure
    dataset = dataset['plotable_limits']
    min_raidus = UNIVERSE_FIGURE.minimum_distance
    user = go.Scattergl({
            'x': [0, dataset['user']['radius'] * math.cos(dataset['user']['phi'])],
            'y': [0, dataset['user']['radius'] * math.sin(dataset['user']['phi'])],
            'mode': 'lines+markers',
            'marker': {'size': 4, 'color': '#000000'},
            'line': {'width': 1, 'color': '#000000'},
            'name': 'user_vector',
            'hoverinfo': 'none',
            'showlegend': False,
    })
    lower_limit = go.Scattergl({
            'x': [
                min_raidus * math.cos(dataset['lower']['phi']),
                dataset['lower']['radius'] * math.cos(dataset['lower']['phi']),
            ],
            'y': [
                min_raidus * math.sin(dataset['lower']['phi']),
                dataset['lower']['radius'] * math.sin(dataset['lower']['phi'])
            ],
            'mode': 'lines+markers',
            'marker': {'size': 4, 'color': '#00DA00'},
            'line': {'width': 1, 'color': '#00DA00'},
            'name': 'lower_limit',
            'hoverinfo': 'none',
            'showlegend': False,
    })
    upper_limit = go.Scattergl({
            'x': [
                min_raidus * math.cos(dataset['upper']['phi']),
                dataset['upper']['radius'] * math.cos(dataset['upper']['phi']),
            ],
            'y': [
                min_raidus * math.sin(dataset['upper']['phi']),
                dataset['upper']['radius'] * math.sin(dataset['upper']['phi'])
            ],
            'mode': 'lines+markers',
            'marker': {'size': 4, 'color': '#00DA00'},
            'line': {'width': 1, 'color': '#00DA00'},
            'name': 'upper_limit',
            'hoverinfo': 'none',
            'showlegend': False,
    })

    def replace_figure_data(figure, figure_name, go_object):
        for k, elm in enumerate(figure['data']):
            if 'name' in elm:
                if elm['name'] == figure_name:
                    figure['data'][k] = go_object
                    break
            if k + 1 == len(figure['data']):
                figure['data'] = [go_object] + figure['data']
        return figure

    figure = replace_figure_data(figure, 'user_vector', user)
    figure = replace_figure_data(figure, 'lower_limit', lower_limit)
    figure = replace_figure_data(figure, 'upper_limit', upper_limit)
    return figure


if __name__ == '__main__':
    app.run_server()
