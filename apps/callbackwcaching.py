import copy
import os
import time

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd

from dash.dependencies import Input, Output
from flask_caching import Cache

from app import app


dfind = pd.read_csv(os.path.join('data', 'indicators.csv'))
available_indicators = dfind['Indicator Name'].unique()

N = 100
dffruit = pd.DataFrame({
    'category': (
        (['apples'] * 5 * N) +
        (['oranges'] * 10 * N) +
        (['figs'] * 20 * N) +
        (['pineapples'] * 15 * N)
    )
})
dffruit['x'] = np.random.randn(len(dffruit['category']))
dffruit['y'] = np.random.randn(len(dffruit['category']))


cache = Cache()

CACHE_DIR = os.path.join(os.sep, 'tmp', 'dash_cache')
if not os.path.isdir(CACHE_DIR):
    os.makedirs(CACHE_DIR)

CACHE_CONFIG = {
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': CACHE_DIR,
}
cache.init_app(app.server, config=CACHE_CONFIG)


layout = html.Div([
    html.H2("data sharing between callbacks: caching"),
    html.Div([
        dcc.Dropdown(
            id='cache-dropdown',
            options=[
                {'label': i, 'value': i}
                    for i in dffruit['category'].unique()
            ],
            value='apples'
        ),
        html.Div([
            html.Div(dcc.Graph(id='cache-g-1'), className="six columns"),
            html.Div(dcc.Graph(id='cache-g-2'), className="six columns"),
        ], className="row"),
        html.Div([
            html.Div(dcc.Graph(id='cache-g-3'), className="six columns"),
            html.Div(dcc.Graph(id='cache-g-4'), className="six columns"),
        ], className="row"),
        html.Div(id='cache-signal', style={'display': 'none'})
    ]),
])

# data sharing between callbacks: caching
#  we start by performing a costly calc in the app's scope (global)
@cache.memoize()
def global_store(value):
    print('computing value with {}'.format(value))
    time.sleep(5)
    return dffruit[dffruit['category'] == value]


def generate_figure(value, figure):
    fig = copy.deepcopy(figure)
    filtered_dataframe = global_store(value)
    fig['data'][0]['x'] = filtered_dataframe['x']
    fig['data'][0]['y'] = filtered_dataframe['y']
    fig['layout'] = {'margin': {'l': 20, 'r': 10, 'b': 20, 't': 10}}
    return fig

@app.callback(
    Output('cache-signal', 'children'), [Input('cache-dropdown', 'value')]
)
def compute_value(value):
    global_store(value)
    return value


@app.callback(
    Output('cache-g-1', 'figure'), [Input('cache-signal', 'children')]
)
def update_graph_1(value):
    return generate_figure(value, {
        'data': [{
            'type': 'scatter',
            'mode': 'markers',
            'marker': {
                'opacity': 0.5,
                'size': 14,
                'line': {'border': 'thin darkgrey solid'}
            }
        }]
    })


@app.callback(
    Output('cache-g-2', 'figure'), [Input('cache-signal', 'children')]
)
def update_graph_2(value):
    return generate_figure(value, {
        'data': [{
            'type': 'scatter',
            'mode': 'lines',
            'line': {'shape': 'spline', 'width': 0.5},
        }]
    })


@app.callback(
    Output('cache-g-3', 'figure'), [Input('cache-signal', 'children')]
)
def update_graph_3(value):
    return generate_figure(value, {'data': [{'type': 'histogram2d',}]})


@app.callback(
    Output('cache-g-4', 'figure'), [Input('cache-signal', 'children')]
)
def update_graph_4(value):
    return generate_figure(value, {'data': [{'type': 'histogram2dcontour',}]})
