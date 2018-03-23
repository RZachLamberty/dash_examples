# -*- coding: utf-8 -*-
import re

import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt

from dash.dependencies import Input, Output

# load the app itself
from app import app

# load the individual app sub-pages
from apps import (
    barchartexample, callbackwcaching, callbackwdistagg, callbackwhiddendiv,
    callbackwstate, chainedinputs, crossfilter, graphproperties, graphslider,
    hoverupdate, interactivewidget, liveupdate, markdown, multiinput,
    plotexample, tableexample, widgets,
    datatableexample, dashtableexample,
)


server = app.server

# boooooootleg route table
TABS = {
    'hello, world': html.H2("hello, world"),
    'barchart example': barchartexample.layout,
    'callback w caching': callbackwcaching.layout,
    'callback w dist agg': callbackwdistagg.layout,
    'callback w hidden div': callbackwhiddendiv.layout,
    'callback w state': callbackwstate.layout,
    'chained inputs': chainedinputs.layout,
    'crossfilter': crossfilter.layout,
    'graph properties': graphproperties.layout,
    'graph with slider': graphslider.layout,
    'hover update': hoverupdate.layout,
    'interactive widget': interactivewidget.layout,
    'live updates': liveupdate.layout,
    'markdown': markdown.layout,
    'multiple inputs': multiinput.layout,
    'plot example': plotexample.layout,
    'table example': tableexample.layout,
    'widgets': widgets.layout,
    'datatable example': datatableexample.layout,
    'dash table example': dashtableexample.layout,
}
TAB_URLS = {
    '/{}'.format(re.sub('\s+', '_', re.sub('[^\s\w]+', '', tabname))): tabname
    for tabname in TABS
}
# add one landing tab, hard-coded
TAB_URLS['/'] = 'hello, world'

# build the frame in which we will render the different apps based on url. leave
# the list of other padges at the top like a very shitty toc
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.H1("tabs are fab"),
        html.Div(
            className="row",
            children=[
                html.Div(
                    id='tab-list',
                    children=dcc.Tabs(
                        tabs=[{'label': k, 'value': k} for k in TABS],
                        value=3,
                        id='tabs',
                        vertical=True,
                        style={
                            'height': '100vh',
                            'borderRight': 'thin lightgrey solid',
                            'textAlign': 'left',
                        }
                    ),
                    style={'width': '20%', 'float': 'left'},
                ),
                html.Div(id="tab-spacer", style={'width': '3%'}),
                html.Div(
                    id='tab-output',
                    style={'width': '77%', 'float': 'right'},
                ),
            ]
        ),
        # wowwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww
        #https://community.plot.ly/t/unable-to-load-table-on-multipage-dash/6347
        html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    ],
    className="container",
    style={'max-width': '80%'}
)


# for each tab, just replace the content with the sub-app layout element
@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_tab(tabval):
    return TABS.get(tabval, '404')


@app.callback(Output('tabs', 'value'), [Input('url', 'pathname')])
def update_tab_from_url(urlpathname):
    # remove punctuation and replace all whitespaces with underscores
    return TAB_URLS.get(urlpathname)


if __name__ == "__main__":
    app.run_server(debug=True)
