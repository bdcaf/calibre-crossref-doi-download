from calibre.library import db
from calibre.utils.logging import Log
import json

log = Log()
mydb = db('~/Archive/CalTest/').new_api

from calibre_plugins.doi_meta import DoiMeta
from calibre_plugins.doi_meta.doi_reader import DoiReader

dm = DoiMeta('./plugin/')

# url = 'https://api.crossref.org/works/10.1002/bmc.835'
url = 'https://api.crossref.org/works/10.1109/tpami.2013.50'
# output = urlopen(url).read()
qurl='https://api.crossref.org/works?query.author=Bogus%C5%82aw+Buszewski&query.bibliographic=Human+exhaled+air+analytics%3A+biomarkers+of+diseases' 
br = dm.browser
cdata = br.open_novisit(qurl).read()
d2 =  json.loads(cdata)
message = d2['message']
results = message['items']

reader = DoiReader(log)

from calibre import ipython
ipython(locals())

