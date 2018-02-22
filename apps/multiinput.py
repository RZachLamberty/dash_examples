import os

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output

from app import app


dfind = pd.read_csv(os.path.join('data', 'indicators.csv'))
available_indicators = dfind['Indicator Name'].unique()


layout = html.Div([
    html.H2("multiple inputs"),
    html.Div([
        html.Div(
            [
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[
                        {'label': i, 'value': i}
                            for i in available_indicators
                    ],
                    value='Fertility rate, total (births per woman)'
                ),
                dcc.RadioItems(
                    id='xaxis-type',
                    options=[
                        {'label': i, 'value': i} for i in ['Linear', 'Log']
                    ],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={'width': '48%', 'display': 'inline-block'}
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[
                        {'label': i, 'value': i}
                            for i in available_indicators
                    ],
                    value='Life expectancy at birth, total (years)'
                ),
                dcc.RadioItems(
                    id='yaxis-type',
                    options=[
                        {'label': i, 'value': i} for i in ['Linear', 'Log']
                    ],
                    value='Linear',
                    labelStyle={'display': 'inline-block'}
                )
            ],
            style={
                'width': '48%', 'float': 'right', 'display': 'inline-block'
            }
        )
    ]),
    dcc.Graph(id='indicator-graphic'),
    dcc.Slider(
        id='year--slider',
        min=dfind['Year'].min(),
        max=dfind['Year'].max(),
        value=dfind['Year'].max(),
        step=None,
        marks={str(year): str(year) for year in dfind['Year'].unique()}
    ),
])



@app.callback(
    Output('indicator-graphic', 'figure'),
    [
        Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value'),
        Input('xaxis-type', 'value'),
        Input('yaxis-type', 'value'),
        Input('year--slider', 'value'),
    ]
)
def update_graph(xaxis_column_name, yaxis_column_name, xaxis_type, yaxis_type,
                 year_value):
    dff = dfind[dfind['Year'] == year_value]

    return {
        'data': [go.Scatter(
            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}

            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'

            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'

            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )

    }
