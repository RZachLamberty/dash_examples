import dash_core_components as dcc
import dash_html_components as html

with open('demo.md', 'r') as f:
    markdown_text = f.read()


layout = html.Div([
    html.H2("markdown example"),
    dcc.Markdown(children=markdown_text),
])
