import os

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output

from app import app


dfgap = pd.read_csv(os.path.join('data', 'gapminderDataFiveYear.csv'))


layout = html.Div([
    html.H2("graph with slider"),
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='year-slider',
        min=dfgap['year'].min(),
        max=dfgap['year'].max(),
        value=dfgap['year'].min(),
        step=None,
        marks={str(year): str(year) for year in dfgap['year'].unique()}
    ),
])


@app.callback(
    Output('graph-with-slider', 'figure'), [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    filtered_df = dfgap[dfgap.year == selected_year]
    traces = [
        go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}

            },
            name=continent
        )
        for (continent, df_by_continent) in filtered_df.groupby('continent')
    ]

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )

    }
