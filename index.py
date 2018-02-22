# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

# load the app itself
from app import app

# load the individual app sub-pages
from apps import (
    barchartexample, callbackwcaching, callbackwdistagg, callbackwhiddendiv,
    callbackwstate, chainedinputs, crossfilter, graphproperties, graphslider,
    hoverupdate, interactivewidget, liveupdate, markdown, multiinput,
    plotexample, tableexample, widgets
)


server = app.server

# boooooootleg route table
ROUTES = {
    '/': html.H2("hello, world"),
    '/barchart_example': barchartexample.layout,
    '/callback_w_caching': callbackwcaching.layout,
    '/callback_w_dist_agg': callbackwdistagg.layout,
    '/callback_w_hidden_div': callbackwhiddendiv.layout,
    '/callback_w_state': callbackwstate.layout,
    '/chained_inputs': chainedinputs.layout,
    '/crossfilter': crossfilter.layout,
    '/graph_properties': graphproperties.layout,
    '/graph_with_slider': graphslider.layout,
    '/hover_update': hoverupdate.layout,
    '/interactive_widget': interactivewidget.layout,
    '/live_updates': liveupdate.layout,
    '/markdown': markdown.layout,
    '/multiple_inputs': multiinput.layout,
    '/plot_example': plotexample.layout,
    '/table_example': tableexample.layout,
    '/widgets': widgets.layout,
}

# build the frame in which we will render the different apps based on url. leave
# the list of other padges at the top like a very shitty toc
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(className="row", children=[
        html.Div(className="three columns", children=[
            html.H2('app list'),
            html.Ul([
                html.Li([html.A(children=href, href=href)])
                for href in ROUTES.keys()
            ]),
        ]),
        html.Div(className="nine columns", id='page-content'),
    ]),
], className="container")


# this callback will replace the page-content div with whatever the url dictates
# (think of this as a bad routing table)
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    return ROUTES.get(pathname, '404')


if __name__ == "__main__":
    app.run_server(debug=True)
