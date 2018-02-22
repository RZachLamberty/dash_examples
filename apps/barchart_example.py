import os

import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    html.H2("US Agriculture Exports (2011)"),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'TOR'},
            ],
            'layout': {'title': 'Dash Data Visualization',}
        }
    ),
])
