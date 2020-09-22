import urllib
import json
from calibre_plugins.doi_meta.config import prefs
# see https://github.com/CrossRef/rest-api-doc#queries

class DoiQuery:
    API='https://api.crossref.org/works'
    def __init__(self, browser, log):
        self.browser = browser
        self.logger= log

    def check(self, cdata, identifiers = {}):
        data = json.loads(cdata)
        # check data['status']
        if data['status'] != 'ok':
            self.logger.info("query result '%s'"%data['status'])
            raise Exception( "Bad response status: %s"%data['status'])
        # message type should either be work or work-list
        # if data['message-type'] != 'work':
            # self.logger.warning("query result wrong type: '%s'"%data['message-type'])
            # raise Exception( "Bad response type: %s"%data['message-type'])
        result = data['message']
        return result

    def queryByDoi(self, doi):
        url = '%s/%s' % (DoiQuery.API, doi)
        self.logger.info("query url '%s'" % url)
        cdata = self.browser.open_novisit(url).read()
        return self.check(cdata)

    def byQuery(self, query):
        qs = urllib.urlencode(query)
        url = '%s?%s' % (DoiQuery.API, qs)
        self.logger.info("query url '%s'" % url)
        cdata = self.browser.open_novisit(url).read()
        return self.check(cdata)




