import os

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

dfgdp = pd.read_csv(os.path.join('data', 'gdp-life-exp-2007.csv'))


layout = html.Div([
    html.H2("life expectancy vs gdp"),
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure={
            'data': [
                go.Scatter(
                    x=dfgdp[dfgdp['continent'] == i]['gdp per capita'],
                    y=dfgdp[dfgdp['continent'] == i]['life expectancy'],
                    text=dfgdp[dfgdp['continent'] == i]['country'],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15, 'line': {'width': 0.5, 'color': 'white'}
                    },
                    name=i
                )
                    for i in dfgdp.continent.unique()
            ],
            'layout': go.Layout(
                xaxis={'type': 'log', 'title': 'gdp per capita'},
                yaxis={'title': 'life expectancy'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
            )
        }
    ),
])
