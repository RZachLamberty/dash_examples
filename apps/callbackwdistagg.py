import json
import os

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from dash.dependencies import Input, Output

from app import app


dfind = pd.read_csv(os.path.join('data', 'indicators.csv'))
available_indicators = dfind['Indicator Name'].unique()


layout = html.Div([
    html.H2("data sharing between callbacks: distributing aggregations"),
    dcc.Dropdown(
        id='dropdown-for-agg-div',
        options=[
            {'label': 'head', 'value': 'head'},
            {'label': 'tail', 'value': 'tail'},
        ],
        value='head'
    ),
    html.P(
        "this is really just an ammendment to the hidden div approach "
        "(below) in which we pre-calculate several items and store them as "
        "a unit within a hidden div, and then use the update of that "
        "hidden div element to trigger some smaller updates. imagine we "
        "had a scenario where we wanted to filter down a *huge* dataset, "
        "or do a large query, and the results as a dataset were small and "
        "re-used by several widgets (a graph, a table, etc). we could "
        "store the jsonified version of the intermediate result and, on "
        "storage, update all dependent widgets"
    ),
    html.Ul([
        html.Li(id='agg-list-elem-1'),
        html.Li(id='agg-list-elem-2'),
        html.Li(id='agg-list-elem-3'),
    ]),
    html.Div(id='intermediate-agg-value', style={'display': 'none'}),
])


# data sharing between callbacks: distributing aggregations
@app.callback(
    Output('intermediate-agg-value', 'children'),
    [Input('dropdown-for-agg-div', 'value')]
)
def clean_data_hidden(value):
    if value == 'head':
        x = dfind.dropna().head()
    elif value == 'tail':
        x = dfind.dropna().tail()
    else:
        raise ValueError('value must be head or tail')

    toshare = {
        'agg_1': int(x.Year.max()),
        'agg_2': int(x.Value.max()),
        'agg_3': x['Country Name'].max()
    }
    return json.dumps(toshare)


@app.callback(
    Output('agg-list-elem-1', 'children'),
    [Input('intermediate-agg-value', 'children')]
)
def update_li_1(shared_json):
    return json.loads(shared_json).get('agg_1', 'not found')


@app.callback(
    Output('agg-list-elem-2', 'children'),
    [Input('intermediate-agg-value', 'children')]
)
def update_li_2(shared_json):
    return json.loads(shared_json).get('agg_2', 'not found')


@app.callback(
    Output('agg-list-elem-3', 'children'),
    [Input('intermediate-agg-value', 'children')]
)
def update_li_3(shared_json):
    return json.loads(shared_json).get('agg_3', 'not found')
