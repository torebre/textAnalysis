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
import numpy as np

import datetime

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

# counter = 0

# date_document_map = {}

    def populate_frame(self):
        iterator = self.lucene_dictionary.getEntryIterator()

        for term in BytesRefIterator.cast_(iterator):
            term_as_string = term.utf8ToString()
            print('term:', term_as_string)
            query = QueryParser("contents", self.analyzer).parse(term_as_string)
            collector = TopScoreDocCollector.create(10000, 10000)
            hits = self.searcher.search(query, collector)
            scorer = QueryScorer(query)

            for hit in hits.scoreDocs:
                document = self.searcher.doc(hit.doc)

                doc_name = document.getField("doc_name")
                date = datetime.datetime.strptime(doc_name.stringValue(), '%m%d%y')

                # if term_as_string in date_document_map:
                #     date_document_map[term_as_string].append()

                # date_document_map[term_as_string]

                stream = TokenSources.getAnyTokenStream(self.index_reader, hit.doc, 'contents', self.analyzer)
                # best_fragments = highlighter.getBestFragments(stream, document.get('contents'), 10)

                # for fragment in best_fragments:
                #     print('fragment: ', fragment)

    def get_terms(self):
        iterator = self.lucene_dictionary.getEntryIterator()

        map_iterator = map(lambda term: term.utf8ToString(), BytesRefIterator.cast_(iterator))

        return list(map_iterator)

        # for term in BytesRefIterator.cast_(iterator):
        #     term_as_string = term.utf8ToString()
        #     print('term:', term_as_string)
        #     query = QueryParser("contents", self.analyzer).parse(term_as_string)
        #     collector = TopScoreDocCollector.create(10000, 10000)
        #     hits = self.searcher.search(query, collector)
        #     scorer = QueryScorer(query)


temp = CreateOccurrenceData()
terms = temp.get_terms()
print("Terms: ", terms)

dates = pd.date_range('1/1/2015', '1/1/2020')

data_frame = pd.DataFrame(index=dates, columns=terms)

print("Data frame: ", data_frame)