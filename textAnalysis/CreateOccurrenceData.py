import lucene

from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.search.highlight import QueryScorer
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.search.highlight import TokenSources
from org.apache.lucene.search.spell import LuceneDictionary
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.util import BytesRefIterator
from org.apache.lucene.search import TopScoreDocCollector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime
from typing import List

import textAnalysis.utilities as util


class CreateOccurrenceData:

    def __init__(self):
        lucene.initVM(vmargs=['-Djava.awt.headless=true'])

        paths_dict = util.getPaths()
        # textSearcher = TextSearcher(paths_dict['fs_directory'])
        fs_directory = FSDirectory.open(Paths.get(paths_dict['fs_directory']))
        index_reader = DirectoryReader.open(fs_directory)
        self.lucene_dictionary = LuceneDictionary(index_reader, 'contents')
        self.analyzer = StandardAnalyzer()
        self.searcher = IndexSearcher(index_reader)
        self.formatter = SimpleHTMLFormatter()

    def populate_frame(self, date_range, term_vector):
        data_frame = pd.DataFrame(data=0, index=date_range, columns=term_vector)
        iterator = self.lucene_dictionary.getEntryIterator()

        for term in BytesRefIterator.cast_(iterator):
            term_as_string = term.utf8ToString()
            # print('term:', term_as_string)
            query = QueryParser("contents", self.analyzer).parse(term_as_string)
            collector = TopScoreDocCollector.create(10000, 10000)
            hits = self.searcher.search(query, 1000)

            if hits is None:
                # print("No hit for term: ", term_as_string)
                continue

            print("Found hit: " + term_as_string)

            for hit in hits.scoreDocs:
                document = self.searcher.doc(hit.doc)

                doc_name = document.getField("doc_name")
                date = datetime.datetime.strptime(doc_name.stringValue(), '%m%d%y')

                current_value = data_frame.at[date, term_as_string]
                if np.isnan(current_value):
                    current_value = 0
                data_frame.at[date, term_as_string] = current_value + 1

        return data_frame

    def get_terms(self) -> List[str]:
        iterator = self.lucene_dictionary.getEntryIterator()

        map_iterator = map(lambda term: term.utf8ToString(), BytesRefIterator.cast_(iterator))

        return list(map_iterator)
