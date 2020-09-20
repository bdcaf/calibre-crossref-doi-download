from calibre.library import db
mydb = db('~/Archive/CalTest/').new_api

from calibre_plugins.doi_meta import DoiMeta

dm = DoiMeta('./plugin/')

# url = 'https://api.crossref.org/works/10.1002/bmc.835'
url = 'https://api.crossref.org/works/10.1109/tpami.2013.50'
# output = urlopen(url).read()
br = dm.browser
cdata = br.open_novisit(url).read()


from calibre import ipython
ipython(locals())

