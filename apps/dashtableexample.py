import os

import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd

from app import app

dfagg = pd.read_csv(
    os.path.join('data', 'usa-agricultural-exports-2011.csv'),
    index_col=0
)


def generate_table(dataframe, tableid):
    return dt.DataTable(
        rows=dataframe.to_dict('records'),
        columns=dataframe.columns,
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[],
        id=tableid,
    )

layout = html.Div([
    html.H2("US Agriculture Exports (2011), DataTable Implementation"),
    html.Div(
        generate_table(dfagg, tableid="datatable_table")
    ),
])
