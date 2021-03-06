from calibre.library import db
from calibre.utils.logging import Log
import json
from itertools import chain

log = Log()
mydb = db('~/Archive/CalTest/').new_api

from calibre_plugins.crossref_doi_download import DoiMeta
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.crossref_doi_download.doi_reader import DoiReader

from crossref_fields import USED_FIELDS, IGNORED_FIELDS, COND_FIELDS, check_uninterpreted_fields, check_uninterpreted_list
# from calibre_plugins.crossref_doi_download.crossref_fields import USED_FIELDS, IGNORED_FIELDS, COND_FIELDS, check_uninterpreted_fields
dm = DoiMeta('./plugin/')
url1='https://api.crossref.org/works/10.1002/bmc.835?mailto=vikoya5988%40oniaj.com'

def get_prop_list(results, prop):
    for ind,res in enumerate(results):
        if prop in res:
            print(ind,res[prop])


reader = DoiReader(log)

br = dm.browser
br.set_debug_http(True)
# user_agent =
        # [('User-agent',
        # 'Mozilla/5.0 (X11;U;Linux 2.4.2.-2 i586; en-us;m18) Gecko/200010131 Netscape6/6.01'
        # )]
# user_agent = [('User-agent',
        # 'FollowingYourExample/0.1 (mailto:vikoya5988@oniaj.com) BasedOnExample/0.0'
        # )]
# br.addheaders=user_agent
# response = br.open("http://python.org/")
# br.addheaders.append( ['Accept-Encoding','gzip'] )
url = 'https://api.crossref.org/works?sample=100'
# url = 'https://api.crossref.org/works?sample=100&mailto=vikoya5988@oniaj.com'
def get_examples():
    visit = br.open(url)
    cdata = visit.read()
    parsed =  json.loads(cdata)
    message = parsed['message']
    return(message)

def check_res(res):
    print(check_uninterpreted_list(res))

if __name__ == "__main__":
    from calibre import ipython
    ipython(locals())


pass

# results = get_examples()['items']
# check_res(results)
# check_uninterpreted_list(results)
# get_prop_list(results, 'standards-body')
