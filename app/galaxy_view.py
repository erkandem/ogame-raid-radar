"""

Basic Data Table functionality works but
the data like x, y and r are irelevant

More useful would be actionable data like:
 - player name
 - ranking
 - planet name


from collections import namedtuple
Condition = namedtuple('Condition', ['column', 'operator', 'variable'])
ConditionGroup = namedtuple('ConditionGroup', ['c1', 'conj', 'c2'])
Query = [Condition]
Query2 = [ConditionGroup(c1=Condition, conj='and', c2=Condition)]

Query2[0].c1, Query2[0].c2
def render_condition(c: Condition):
    return f'{c[0]} {c[1]} {c[3]}'


def render_condition_group(cg: ConditionGroup):
    if type(cg.c1):

    return f'{render_condition(cg.c1)} {cg.conj} {render_condition(cg.c2)}'

c = Condition(column='planet', operator='==', variable='@planet_slot')
query = [c, 'conjunction' ]
render_query

"""
from datetime import datetime as dt
import math
import numpy as np
import dash
from dash.dependencies import Output, Input, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dse
import flask
import pandas as pd
import plotly.graph_objects as go

from src.api.universe_api import get_janice_universe, UniverseDataApi
from src.api.scores_api import get_janice_highscore, HighScoresDataApi


app_tag = 'ONSA - Defending Our Empire. Securing the Future'
CSS_LIST = ['/static/sakura-earthly.css']


def nowstr():
    return dt.now().strftime('%Y%m%d %H:%M:%S.%f')


#%%
class UniverseFigure:
    galaxies_range = list(range(1, 10))
    systems_range = list(range(1, 500))
    planets_range = list(range(1, 16))
    planet_distance = 1 / (15 * 2)
    galaxy_increment = (2 * math.pi) / 9
    system_increment = galaxy_increment / 499
    minimum_distance = 1
    universe_data: UniverseDataApi
    highscore_data: HighScoresDataApi
    figure: go.Figure
    df_dummy: pd.DataFrame
    df: pd.DataFrame

    def __init__(self):
        self.highscore_data = get_janice_highscore()
        self.universe_data = get_janice_universe()
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
        return df

    def insert_universe_data(self, df):
        shift_to_yaxis = math.pi / 2
        df['taken'] = df['coords'].apply(lambda x: int(self.universe_data.is_planet_taken(x)))
        df['system_degree'] = (
                (df['galaxy'] - 1) * self.galaxy_increment
                + (df['system'] - 1) * self.system_increment
                + shift_to_yaxis
        )
        df['x'] = df['system_degree'].apply(lambda x: math.cos(x))
        df['y'] = df['system_degree'].apply(lambda x: math.sin(x))
        df['r'] = df['planet'].apply(lambda x: self.minimum_distance + self.planet_distance * x)
        df['n'] = (
                (df['galaxy'] - 1) * max(self.systems_range) * max(self.planets_range)
                + (df['system'] - 1) * max(self.planets_range)
                + df['planet']
        )
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


def cast_to_dash_table(df):
    return dse.DataTable(**{
        'columns': [{"name": col, "id": col} for col in df.columns],
        'data': df.to_dict('records'),
        'id': 'universe-data-table',
        'filter_action': 'native',
        'sort_action': 'native'
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


# UNIVERSE_FIGURE = UniverseFigure()
import pickle
# with open('cache.pickle', 'wb') as file:
#     pickle.dump(UNIVERSE_FIGURE, file)
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

        df_player_name = UNIVERSE_FIGURE.universe_data.players.loc[:, ['id', 'name', 'status', 'alliance']]
        df_player_name.set_index('alliance', inplace=True)
        df_player_name.rename(index=str, columns={'id': 'player_id', 'name': 'player_name'}, inplace=True)

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

        df_viz = UNIVERSE_FIGURE.df.loc[:, ['coords', 'galaxy', 'system', 'planet']]
        df_viz = df_viz.loc[:, ['coords', 'n']]
        df_viz.set_index('coords', inplace=True)
        df = df_detailed.set_index('coords').join(df_viz)

        df.reset_index(inplace=True)
        df = df[['n', 'coords', 'planet_name', 'player_name', 'status', 'allience_name', 'eco_score']]
        return html.Div(cast_to_dash_table(df))
    if activeOrInactive == 'inactive' and takenOrFree == 'taken':
        inactive = UNIVERSE_FIGURE._get_inactive_players()
        query_str = 'player == @inactive'
        df_raw = UNIVERSE_FIGURE.universe_data.universe.query(query_str)
        df_raw.rename(index=str, columns={'name': 'planet_name'}, inplace=True)

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

        df_viz = UNIVERSE_FIGURE.df.loc[:, ['coords', 'galaxy', 'system', 'planet']]
        df_viz = df_viz.loc[:, ['coords', 'n']]
        df_viz.set_index('coords', inplace=True)
        df = df_detailed.set_index('coords').join(df_viz)

        df.reset_index(inplace=True)
        df = df[['n', 'coords', 'planet_name', 'player_name', 'status', 'allience_name', 'eco_score']]
        return html.Div(cast_to_dash_table(df))
    if activeOrInactive == 'active' and takenOrFree == 'free':
        df = UNIVERSE_FIGURE.get_free_planets_data()
        return html.Div(cast_to_dash_table(df))
    if activeOrInactive == 'inactive' and takenOrFree == 'free':
        df = UNIVERSE_FIGURE.get_free_planets_data()
        return html.Div(cast_to_dash_table(df))


if __name__ == '__main__':
    app.run_server()
