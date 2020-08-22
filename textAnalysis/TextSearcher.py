from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.search.highlight import QueryScorer
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.search.highlight import SimpleSpanFragmenter
from org.apache.lucene.search.highlight import TokenSources
from org.apache.lucene.search.spell import LuceneDictionary
from org.apache.lucene.util import BytesRefIterator


class TextSearcher:

    def __init__(self, fs_directory):
        directory = SimpleFSDirectory(Paths.get(fs_directory))
        self.index_reader = DirectoryReader.open(directory)
        self.searcher = IndexSearcher(DirectoryReader.open(directory))
        self.analyzer = StandardAnalyzer()
        self.query = None
        self.lucene_dictionary = LuceneDictionary(self.index_reader, 'contents')
        self.analyzer = StandardAnalyzer()
        self.formatter = SimpleHTMLFormatter()
        self.hits = None

    def search(self, searchtext):
        if searchtext is None:
            return 0

        self.query = QueryParser("contents", self.analyzer).parse(searchtext)
        score_docs = self.searcher.search(self.query, 50).scoreDocs
        print("%s total matching documents." % len(score_docs))
        return len(score_docs)

    def find_documents(self, search_text):
        self.query = QueryParser("contents", self.analyzer).parse(search_text)
        self.hits = self.searcher.search(self.query, 50)

        return self.hits

    def get_document(self, document_id):
        return self.searcher.doc(document_id)

    def get_current_query(self):
        return self.query

    def get_highlighted_hits(self):
        extracted_fragments = []

        scorer = QueryScorer(self.query)
        fragmenter = SimpleSpanFragmenter(scorer, 10)
        highlighter = Highlighter(self.formatter, scorer)
        highlighter.setTextFragmenter(fragmenter)

        for hit in self.hits.scoreDocs:
            document = self.searcher.doc(hit.doc)
            stream = TokenSources.getAnyTokenStream(self.index_reader, hit.doc, 'contents', self.analyzer)
            best_fragments = highlighter.getBestFragments(stream, document.get('contents'), 10)

            for fragment in best_fragments:
                print('fragment: ', fragment)

            extracted_fragments.append((hit.doc, best_fragments))

        return extracted_fragments
