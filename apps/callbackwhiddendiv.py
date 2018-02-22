import os

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from dash.dependencies import Input, Output

from app import app


dfind = pd.read_csv(os.path.join('data', 'indicators.csv'))
available_indicators = dfind['Indicator Name'].unique()


layout = html.Div([
    html.H2("data sharing between callbacks: storing data in hidden divs"),
    dcc.Dropdown(
        id='dropdown-for-hidden-div',
        options=[
            {'label': 'head', 'value': 'head'},
            {'label': 'tail', 'value': 'tail'},
        ],
        value='head'
    ),
    html.Div("look at src code for a div immediately following this one"),
    html.Div(id='intermediate-value', style={'display': 'none'}),
])


# data sharing between callbacks: storing data in hidden divs
@app.callback(
    Output('intermediate-value', 'children'),
    [Input('dropdown-for-hidden-div', 'value')]
)
def clean_data_hidden(value):
    if value == 'head':
        x = dfind.head()
    elif value == 'tail':
        x = dfind.tail()
    else:
        raise ValueError('value must be head or tail')
    return x.to_json(date_format='iso', orient='split')
