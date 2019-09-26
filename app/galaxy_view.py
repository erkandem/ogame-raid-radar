#%%
import math
from src.backbone_app import get_janice
import pandas as pd
import plotly.graph_objects as go

#%%
galaxies_range = [elm for elm in range(1, 10)]
systems_range = [elm for elm in range(1, 500)]
planets_range = [elm for elm in range(1, 16)]
planet_distance = 1 / (15 * 2)
galaxy_increment = (2 * math.pi) / 9
system_increment = galaxy_increment / 499
minimum_distance = 1

#%%
janice = get_janice()

#%%
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
    for galaxy in galaxies_range
    for system in systems_range
    for planet in planets_range
]

#%%
df = pd.DataFrame(universe)

#%%
shift_to_yaxis = math.pi / 2
df['taken'] = df['coords'].apply(lambda x: int(janice.is_planet_taken(x)))
df['system_degree'] = (
        (df['galaxy'] - 1) * galaxy_increment
        + (df['system'] - 1) * system_increment
        + shift_to_yaxis
)

df['x'] = df['system_degree'].apply(lambda x: math.cos(x))
df['y'] = df['system_degree'].apply(lambda x: math.sin(x))
df['r'] = minimum_distance + planet_distance * df['planet']

#%%
data = []
for planet_slot in planets_range:
    slice = df.query('planet == @planet_slot')
    data.append(
        go.Scattergl(
            dict(
                x=(slice['x'] * slice['r']).tolist(),
                y=(slice['y'] * slice['r']).tolist(),
                mode='markers',
                marker=dict(
                    size=[5 for elm in range(len(slice))],
                    color=slice['taken'].tolist(),
                    colorscale=[[0, 'rgba(250, 250, 60, 0.001)'], [1, 'rgb(204, 0, 0, 1)']]
                ),
                name=f'{planet_slot}. slot',
                hovertext=slice['coords']
            )
        )
    )

#%% append segmenting hint
labels = ['One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
values = [4500, 2500, 1053, 500]

# Use `hole` to create a donut-like pie chart
n_ = go.Pie(
    labels=labels,
    values=values,
    hole=minimum_distance
)

#%%
fig = go.Figure(data=data)
fig.show()

#%%
from src.scores_api import HighScoresApi
from src.backbone_app import get_janice

janice = get_janice()
janice_scores = HighScoresApi(162, 'en', do_init=True)
inactive = janice.players.query("status == 'i' ")
# planet_of_inactivate = janice.universe.join(inactive, )
