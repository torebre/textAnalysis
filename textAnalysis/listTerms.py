import lucene

from java.nio.file import Paths
import textAnalysis.utilities as util
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search.spell import LuceneDictionary
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.util import BytesRef, BytesRefIterator


lucene.initVM(vmargs=['-Djava.awt.headless=true'])


paths_dict = util.getPaths()
# textSearcher = TextSearcher(paths_dict['fs_directory'])
fs_directory = FSDirectory.open(Paths.get(paths_dict['fs_directory']))
index_reader = DirectoryReader.open(fs_directory)
lucene_dictionary = LuceneDictionary(index_reader, 'contents')
iterator = lucene_dictionary.getEntryIterator();

for term in BytesRefIterator.cast_(iterator):
    print('term:', term.utf8ToString())
