from calibre.library import db
from calibre.utils.logging import Log
import json

log = Log()
mydb = db('~/Archive/CalTest/').new_api

from calibre_plugins.doi_meta import DoiMeta
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.doi_meta.doi_reader import DoiReader

dm = DoiMeta('./plugin/')

url = 'https://api.crossref.org/works?sample=10'
br = dm.browser
cdata = br.open_novisit(qurl).read()
parsed =  json.loads(cdata)
message = parsed['message']
results = message['items']

reader = DoiReader(log)

from calibre import ipython
ipython(locals())

