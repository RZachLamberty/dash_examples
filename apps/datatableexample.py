import os

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from app import app

dfagg = pd.read_csv(
    os.path.join('data', 'usa-agricultural-exports-2011.csv'),
    index_col=0
)

# dash script elements don't get loaded with the page -- they get added
# post-facto by react. in order to have an "on document ready" trigger, you
# *have* to serve it externally. SHITTY.
DATATABLE_GIST_URL = (
    "https://cdn.rawgit.com/RZachLamberty/4945b4ac3fb335064cf2d66c5231acd6/raw/"
    "3ef2ef45b6349fb6f692025b6433ee52d5034a1f/dashapp.datatableexample.js"
)
DATATABLE_ID = "datatable_table"


def generate_table(dataframe, tableid='mytable'):
    return html.Table(
        # Header
        [
            html.Thead(
                [html.Tr([html.Th(col) for col in dataframe.columns])]
            )
        ] +
        # Body
        [
            html.Tr(
                [
                    html.Td(row[col]) for col in dataframe.columns
                ]
            )
            for (ind, row) in dataframe.iterrows()
        ],
        id=tableid,
        className="display",
        style={'width': '100%'},
    )

layout = html.Div([
    html.H2("US Agriculture Exports (2011), DataTable Implementation"),
    html.Div(
        generate_table(dfagg, tableid=DATATABLE_ID)
    ),
])

# add external datatables files (css and js)
CSS_URLS = ['https://cdn.datatables.net/1.10.16/css/jquery.dataTables.min.css']
for cssurl in CSS_URLS:
    app.css.append_css({'external_url': cssurl})

JS_URLS = [
    'https://code.jquery.com/jquery-1.12.4.js',
    'https://cdn.datatables.net/1.10.16/js/jquery.dataTables.min.js',
    DATATABLE_GIST_URL,
]
for jsurl in JS_URLS:
    app.scripts.append_script({'external_url': jsurl})
