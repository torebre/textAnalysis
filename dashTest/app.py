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
import textAnalysis.utilities as util
import html2markdown

DATE_FORMAT = '%m%d%y'

env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])
# env.attachCurrentThread()

paths_dict = util.getPaths()
textSearcher = TextSearcher(paths_dict['fs_directory'])
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
    html.Div(id="output_fragments"),

    dcc.Graph(
        id='occurrence-scatterplot'
    )
])


@app.callback(
    [Output(component_id="occurrence-scatterplot", component_property="figure"),
     Output(component_id="output_fragments", component_property="children")],
    [Input(component_id="search", component_property='n_clicks')],
    [State(component_id='search_text', component_property='value')]
)
def do_search(n_clicks, search_text):
    fragment_list = []

    if search_text is None:
        data_frame = pd.DataFrame([])
        data_frame['Date'] = []
        data_frame['Marker'] = []
    else:
        # TODO Where is the best place to call this?
        env.attachCurrentThread()

        hits = textSearcher.find_documents(search_text)
        date_list = []

        for hit in hits.scoreDocs:
            document_number = hit.doc
            document = textSearcher.get_document(document_number)
            doc_name = document.getField("doc_name")
            date = datetime.datetime.strptime(doc_name.stringValue(), '%m%d%y')
            date_list.append(date)

        data_frame = pd.DataFrame(date_list)
        data_frame['Marker'] = ['1'] * len(date_list)

        highlighted_hits = textSearcher.get_highlighted_hits()

        for highlighted_hit in highlighted_hits:
            for hit in highlighted_hit[1]:
                fragment_list.append(html.Li(dcc.Markdown(html2markdown.convert(hit))))

    data_frame.columns = ['Date', 'Marker']
    scatterplot = px.scatter(data_frame, x="Date", y="Marker", range_x=['2015-01-01', '2017-12-31'])

    print(fragment_list)

    return scatterplot, html.Ul(fragment_list)


if __name__ == '__main__':
    app.run_server(debug=True)
