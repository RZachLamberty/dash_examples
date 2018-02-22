import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from app import app


all_options = {
    "america": ['new york city', 'san francisco', 'cincinnati'],
    'canada': ['montreal', 'toronto', 'ottawa']
}


layout = html.Div([
    html.H2("chained inputs"),
    dcc.RadioItems(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in all_options],
        value="america"
    ),
    html.Hr(),
    dcc.RadioItems(id='cities-dropdown'),
    html.Hr(),
    html.Div(id='display-selected-values'),
])


@app.callback(
    Output('cities-dropdown', 'options'),
    [Input('countries-dropdown', 'value')]
)
def set_cities_options(selected_country):
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@app.callback(
    Output('cities-dropdown', 'value'),
    [Input('cities-dropdown', 'options')]
)
def set_cities_value_default(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    [
        Input('countries-dropdown', 'value'),
        Input('cities-dropdown', 'value')
    ]
)
def set_display_children(selected_country, selected_city):
    return u'{} is a city in {}'.format(selected_city, selected_country)
