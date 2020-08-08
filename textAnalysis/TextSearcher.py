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
        # run(searcher, analyzer)

    def search(self, searchtext):
        if searchtext is None:
            return 0

        query = QueryParser("contents", self.analyzer).parse(searchtext)
        scoreDocs = self.searcher.search(query, 50).scoreDocs
        print("%s total matching documents." % len(scoreDocs))
        return len(scoreDocs)

    def find_documents(self, search_text):
        query = QueryParser("contents", self.analyzer).parse(search_text)
        hits = self.searcher.search(query, 50)

        return hits

        # for hit in hits.scoreDocs:
        #     document_number = hit.doc
        #     document = self.searcher.doc(document_number)
        #     creation_date_field = document.getField("Creation-Date")
        #     doc_name = document.getField("doc_name")
        #
        #     print("Creation date: %s" % creation_date_field)
        #
        #     date = datetime.datetime.strptime(doc_name.stringValue(), self.DATE_FORMAT)
        #     print("Date: %s" % date)
        #
        #     for field in document.getFields():
        #         print("Field: %s. Value: %s" % (field.name(), field.stringValue()))

    def get_document(self, document_id):
        return self.searcher.doc(document_id)
