import lucene

from java.nio.file import Paths
import textAnalysis.utilities as util
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search.spell import LuceneDictionary
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.util import BytesRef, BytesRefIterator
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.search.highlight import Formatter
from org.apache.lucene.search.highlight import Fragmenter
from org.apache.lucene.search.highlight import Highlighter
from org.apache.lucene.search.highlight import QueryScorer
from org.apache.lucene.search.highlight import SimpleHTMLFormatter
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.highlight import SimpleSpanFragmenter
from org.apache.lucene.search.highlight import TokenSources

lucene.initVM(vmargs=['-Djava.awt.headless=true'])


paths_dict = util.getPaths()
# textSearcher = TextSearcher(paths_dict['fs_directory'])
fs_directory = FSDirectory.open(Paths.get(paths_dict['fs_directory']))
index_reader = DirectoryReader.open(fs_directory)
lucene_dictionary = LuceneDictionary(index_reader, 'contents')
iterator = lucene_dictionary.getEntryIterator()
analyzer = StandardAnalyzer()
searcher = IndexSearcher(index_reader)
formatter = SimpleHTMLFormatter()

counter = 0
for term in BytesRefIterator.cast_(iterator):
    term_as_string = term.utf8ToString()
    print('term:', term_as_string)
    query = QueryParser("contents", analyzer).parse(term_as_string)
    hits = searcher.search(query, 100000)
    scorer = QueryScorer(query)
    fragmenter = SimpleSpanFragmenter(scorer, 10)
    highlighter = Highlighter(formatter, scorer)
    highlighter.setTextFragmenter(fragmenter)

    for hit in hits.scoreDocs:
        document = searcher.doc(hit.doc)

        stream = TokenSources.getAnyTokenStream(index_reader, hit.doc, 'contents', analyzer)
        best_fragments = highlighter.getBestFragments(stream, document.get('contents'), 10)

        for fragment in best_fragments:
            print('fragment: ', fragment)

    counter += 1
    if counter > 2:
        break

# for document_number in range(index_reader.numDocs()):
#     document = index_reader.document(document_number)
#     for field in document.getFields():
#         print('field: ', field)
