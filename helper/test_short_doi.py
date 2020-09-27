import json
from calibre.utils.logging import Log
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.crossref_doi_download import DoiMeta
from calibre_plugins.crossref_doi_download.doi_reader import DoiReader, get_title, get_author_list
from calibre_plugins.crossref_doi_download.doi_request import DoiQuery
from polyglot.urllib import urlencode
import calibre_plugins.crossref_doi_download.short_doi as sd
log = Log()
reader = DoiReader(log)
dm = DoiMeta('./plugin/')
br = dm.browser
onlineQuery = DoiQuery(br, log)

short_doi= '10/aabbe'
short_doi= '10.1002/9781118895047'

# cdata = br.open(doiquery).read()
# json.loads(cdata)
sd.is_short_doi(short_doi)
sd.return_full_doi(br,short_doi)
# https://doi.org/api/handles/10/aabbe

# doilink = 'https://dx.doi.org/10.1002/(SICI)1097-0258(19980815/30)17:15/16%3C1661::AID-SIM968%3E3.0.CO;2-2?noredirect'

# fullurl = 'https://api.crossref.org/works?%s' % dois
# fullurl = 'https://api.crossref.org/works?filter=doi:10/aabbe&mailto=vikoya5988%40oniaj.com'
# cdata = br.open(fullurl).read()

# data = json.loads(cdata)
# message = data['message']
# results = message['items']

# identifiers = {}
# # fin = map(lambda x:reader.result2meta(x,identifiers),results)

# for r in results:
    # reader.result2meta(r,identifiers)

# result = results[1]
# title = get_title(result)
# authors = get_author_list(result)
# mi = Metadata(title=title, authors=authors)

from calibre import ipython
ipython(locals())
