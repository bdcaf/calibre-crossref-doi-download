from calibre.library import db
from calibre.utils.logging import Log
import json

log = Log()
mydb = db('~/Archive/CalTest/').new_api

from calibre_plugins.doi_meta import DoiMeta
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.doi_meta.doi_reader import DoiReader

from calibre_plugins.doi_meta.crossref_fields import USED_FIELDS, IGNORED_FIELDS, COND_FIELDS
dm = DoiMeta('./plugin/')


reader = DoiReader(log)

if __name__ == "__main__":
    from calibre import ipython
    ipython(locals())

from calibre import random_user_agent
ua = random_user_agent(allow_ie=False)
url = 'https://api.crossref.org/works?sample=10'

br = dm.browser
visit = br.open_novisit(url)
cdata = visit.read()

parsed =  json.loads(cdata)
message = parsed['message']
results = message['items']
item = results[0]
