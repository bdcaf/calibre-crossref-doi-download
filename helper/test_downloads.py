import json
from calibre.utils.logging import Log
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.crossref_doi_download import DoiMeta
from calibre_plugins.crossref_doi_download.doi_reader import DoiReader, get_title, get_author_list
reader = DoiReader(Log())
dm = DoiMeta('./plugin/')
br = dm.browser

fullurl = 'https://api.crossref.org/works?query.bibliographic=Bayesian+data+analysis+Andrew+Gelman&mailto=vikoya5988%40oniaj.com'
cdata = br.open(fullurl).read()

data = json.loads(cdata)
message = data['message']
results = message['items']

identifiers = {}
# fin = map(lambda x:reader.result2meta(x,identifiers),results)

for r in results:
    reader.result2meta(r,identifiers)

result = results[1]
title = get_title(result)
authors = get_author_list(result)
mi = Metadata(title=title, authors=authors)

from calibre import ipython
ipython(locals())
