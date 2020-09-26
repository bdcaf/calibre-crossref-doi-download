from polyglot.urllib import urlencode
import json
from calibre_plugins.crossref_doi_download.config import prefs
# see https://github.com/CrossRef/rest-api-doc#queries

class DoiQuery:
    API='https://api.crossref.org/works'
    def __init__(self, browser, log):
        self.browser = browser
        self.logger= log
        email = prefs['email4polite']
        add_req = {}
        if len(email) > 5:
            add_req['mailto']=email
        self.add_req = add_req



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
        cdata = self.submitWithQuery(url)
        return self.check(cdata)

    def byQuery(self, query):
        url = DoiQuery.API
        cdata = self.submitWithQuery(url, query)
        return self.check(cdata)

    def submitWithQuery(self, url, query={}):
        query.update(self.add_req)
        self.logger("query is:", query)
        if len(query) >0:
            qs = urlencode(query)
            fullurl = '%s?%s' % (url, qs)
            self.logger("Fullurl is:", fullurl)
        else:
            fullurl = url
        cdata = self.browser.open(fullurl).read()
        return cdata
