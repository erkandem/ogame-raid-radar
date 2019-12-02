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
        return df

    def get_default_layout(self):
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

    def get_universe_fig_data(self, df, final_query_str):
        """
            df:
            query_str:

        """
        data = []
        for planet_slot in self.planets_range:
            df_slice = df.query(final_query_str)
            data.append(
                go.Scattergl(
                    dict(
                        x=(df_slice['x'] * df_slice['r']),
                        y=(df_slice['y'] * df_slice['r']),
                        mode='markers',
                        marker=dict(
                            symbol='circle',
                            size=[6 for elm in range(len(df_slice))],
                            color=df_slice['taken'].apply(lambda x: '#66ff66' if x == 0 else '#ff6666'),
                 #           colorscale=[
                 #               [0, 'rgba(250, 250, 60, 0)'],
                 #               [1, 'rgba(204, 0, 0, 0.9)']
                 #           ]
                        ),
                        name=f'{planet_slot}. slot',
                        hoverinfo='text',
                        hovertext=df_slice['coords']
                    )
                )
            )
        return data

    def get_universe_fig_data2(self, df, query_str):
        """
            df:
            query_str:

        """
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
            }) for planet_slot in self.planets_range]
        return data

    def what_is_it_good_for(self):
        # %% append segmenting hint
        labels = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        values = [4500, 2500, 1053, 500]

        # %% Use `hole` to create a donut-like pie chart
        n_ = go.Pie(
            labels=labels,
            values=values,
            hole=self.minimum_distance
        )

    def _get_figure(self, df, final_query_str):
        data = self.get_universe_fig_data2(df, final_query_str)
        layout = self.get_default_layout()
        return go.Figure(
            data=data,
            layout=layout
        )

    def get_taken_planets_fig(self):
        final_query_str = ' '.join(['planet == @planet_slot', 'and', 'taken == 1'])
        return self._get_figure(self.df, final_query_str)

    def get_free_planets_fig(self):
        final_query_str = ' '.join(['planet == @planet_slot', 'and', 'taken == 0'])
        return self._get_figure(self.df, final_query_str)

    def get_dummy_planets_fig(self):
        final_query_str = ' '.join(['planet == @planet_slot'])
        return self._get_figure(self.df_dummy, final_query_str)


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
            id='universe-taken-or-free-toogle'
        ),
        dcc.Loading(
            html.Div(
                dcc.Graph(
                    figure=UNIVERSE_FIGURE.get_dummy_planets_fig(),
                    config={},
                    id='universe-graph'
                )
            )
        )], className='aptry'
    )


UNIVERSE_FIGURE = UniverseFigure()
server = flask.Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=CSS_LIST,
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
    [Input('universe-taken-or-free-toogle', 'value')],
)
def show_taken_or_free(value):
    if value == 'taken':
        return UNIVERSE_FIGURE.get_taken_planets_fig()
    if value == 'free':
        return UNIVERSE_FIGURE.get_free_planets_fig()


if __name__ == '__main__':
    app.run_server()
