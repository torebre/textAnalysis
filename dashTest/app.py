# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import lucene
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from textAnalysis.TextSearcher import TextSearcher
import datetime

DATE_FORMAT = '%m%d%y'

env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
# env.attachCurrentThread()

textSearcher = TextSearcher()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Input(id="search_text", placeholder="Enter text",
                 style={"width": "100%"}),

    html.Button('Search', id='search', n_clicks=0),

    html.Div(id="test_output"),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

@app.callback(
    Output(component_id="test_output", component_property="children"),
    [Input(component_id="search", component_property='n_clicks')],
    [State(component_id='search_text', component_property='value')]
)
def do_search(n_clicks, search_text):
    # TODO Where is the best place to call this?
    env.attachCurrentThread()

    hits = textSearcher.find_documents(search_text)

    for hit in hits.scoreDocs:
        document_number = hit.doc
        document = textSearcher.get_document(document_number)
        doc_name = document.getField("doc_name")

        date = datetime.datetime.strptime(doc_name.stringValue(), DATE_FORMAT)
        print("Date: %s" % date)

        for field in document.getFields():
            print("Field: %s. Value: %s" % (field.name(), field.stringValue()))
    return textSearcher.search(search_text)


if __name__ == '__main__':
    app.run_server(debug=True)