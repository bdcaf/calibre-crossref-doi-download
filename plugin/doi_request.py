import urllib
from calibre_plugins.doi_meta.config import prefs

class DoiQuery:
    def __init__(self, browser, log):
        self.browser = browser
        self.logger= log

    def queryByDoi(self, doi):
        url = 'https://api.crossref.org/works/%s'%doi
        self.logger.info("query url '%s'" % url)
        cdata = self.browser.open_novisit(url).read()
        return cdata

    def byQuery(self, query):
        qs=urllib.urlencode(query)
        url = 'https://api.crossref.org/works?%s' % qs
        self.logger.info("query url '%s'" % url)
        cdata = self.browser.open_novisit(url).read()
        return cdata




