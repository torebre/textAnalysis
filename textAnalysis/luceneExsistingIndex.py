import lucene

from java.io import StringReader
from org.apache.lucene.analysis.standard import StandardAnalyzer, StandardTokenizer
# from org.apache.lucene.analysis.tokenattributes import CharTermAttribut
from java.nio.file import Paths
# from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher

# IndexReader reader = DirectoryReader.open(FSDirectory.open(indexDirectory));
#         IndexSearcher searcher = new IndexSearcher(reader);
#         Analyzer analyzer = new StandardAnalyzer();
#         String field = "contents";

# reader = DirectoryReader.open(FSDirectory.open("/media/student/"))

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# test = "This is how we do it."
# tokenizer = StandardTokenizer()

#base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
directory = SimpleFSDirectory(Paths.get("/media/project_data/index_test2"))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()
# run(searcher, analyzer)

query = QueryParser("contents", analyzer).parse("test")
scoreDocs = searcher.search(query, 50).scoreDocs
print("%s total matching documents." % len(scoreDocs))

for scoreDoc in scoreDocs:
    doc = searcher.doc(scoreDoc.doc)
    print('path:', doc.get("path"), 'name:', doc.get("name"))


del searcher
