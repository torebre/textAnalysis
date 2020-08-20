from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.store import SimpleFSDirectory
from java.nio.file import Paths
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser


class TextSearcher:

    def __init__(self, fs_directory):
        directory = SimpleFSDirectory(Paths.get(fs_directory))
        self.searcher = IndexSearcher(DirectoryReader.open(directory))
        self.analyzer = StandardAnalyzer()
        paths_dict = util.getPaths()
        fs_directory = FSDirectory.open(Paths.get(paths_dict['fs_directory']))
        index_reader = DirectoryReader.open(fs_directory)
        lucene_dictionary = LuceneDictionary(index_reader, 'contents')
        iterator = lucene_dictionary.getEntryIterator()
        analyzer = StandardAnalyzer()
        searcher = IndexSearcher(index_reader)
        formatter = SimpleHTMLFormatter()

    def search(self, searchtext):
        if searchtext is None:
            return 0

        self.query = QueryParser("contents", self.analyzer).parse(searchtext)
        score_docs = self.searcher.search(self.query, 50).scoreDocs
        print("%s total matching documents." % len(score_docs))
        return len(score_docs)

    def find_documents(self, search_text):
        self.query = QueryParser("contents", self.analyzer).parse(search_text)
        hits = self.searcher.search(self.query, 50)

        return hits

    def get_document(self, document_id):
        return self.searcher.doc(document_id)

    def get_current_query(self):
        return self.query