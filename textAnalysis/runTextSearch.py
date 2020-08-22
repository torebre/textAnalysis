import datetime

import lucene
import pandas as pd
import plotly.express as px

import textAnalysis.utilities as util
from textAnalysis.TextSearcher import TextSearcher

env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

paths_dict = util.getPaths()
textSearcher = TextSearcher(paths_dict['fs_directory'])

hits = textSearcher.find_documents("Test")

date_list = []

for hit in hits.scoreDocs:
    document_number = hit.doc
    document = textSearcher.get_document(document_number)
    doc_name = document.getField("doc_name")

    date = datetime.datetime.strptime(doc_name.stringValue(), '%m%d%y')
    print("Date: %s" % date)

    date_list.append(date)

print(date_list)

data_frame = pd.DataFrame(date_list)
data_frame['Marker'] = ['1'] * len(date_list)
data_frame.columns = ['Date', 'Marker']

# fig = px.histogram(data_frame)
# fig.show()
print(data_frame)
fig = px.scatter(data_frame, x="Date", y="Marker", range_x=['2015-01-01', '2017-12-31'])
fig.show()
