import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State

from app import app


layout = html.Div([
    html.H2("callbacks with state"),
    html.Div([
        dcc.Input(id='input-1-state', type='text', value='Montreal'),
        dcc.Input(id='input-2-state', type='text', value='Canada'),
        html.Button(id='submit-button', n_clicks=0, children="Submit"),
        html.Div(id='output-state'),
    ]),
])


# callbacks with state
@app.callback(
    Output('output-state', 'children'),
    [Input('submit-button', 'n_clicks')],
    [
        State('input-1-state', 'value'),
        State('input-2-state', 'value')
    ]
)
def update_output(n_clicks, input1, input2):
    s = 'button has been pressed {} times, input 1 is "{}", input 2 is "{}"'
    return s.format(n_clicks, input1, input2)
