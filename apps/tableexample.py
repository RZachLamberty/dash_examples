import os

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

dfagg = pd.read_csv(os.path.join('data', 'usa-agricultural-exports-2011.csv'))


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


layout = html.Div([
    html.H2("US Agriculture Exports (2011)"),
    generate_table(dfagg),
])
