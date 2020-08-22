import lucene

import textAnalysis.utilities as util
from textAnalysis.TextSearcher import TextSearcher

env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])

paths_dict = util.getPaths()
textSearcher = TextSearcher(paths_dict['fs_directory'])

hits = textSearcher.find_documents("Test")

highlighted_hits = textSearcher.get_highlighted_hits()

fragment_list = []
for highlighted_hit in highlighted_hits:
    for hit in highlighted_hit[1]:
        fragment_list.append(hit)

for fragment in fragment_list:
    print(fragment)

