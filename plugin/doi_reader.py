# get doi from url:
# e.g. curl https://api.crossref.org/works/10.1002/bmc.835 > test
# Link is under URL
import json
from calibre_plugins.doi_meta.config import prefs
from calibre.ebooks.metadata.book.base import Metadata
from calibre.utils.localization import canonicalize_lang
from calibre.utils.date import parse_date

class DoiReader:
    timeout = 30

    def __init__(self, logger):
        self.log = logger

    def parseDoi(self, cdata, identifiers = {}):
        data = json.loads(cdata)
        # check data['status']
        if data['status'] != 'ok':
            self.log.info("query result '%s'"%data['status'])
            return "Bad response status: %s"%data['status']
        if data['message-type'] != 'work':
            self.log.info("query result wrong type: '%s'"%data['message-type'])
            return "Bad response type: %s"%data['message-type']

        self.log.info("query result good for processing")
        result = data['message']

        if result.has_key('title'):
            title = ': '.join(result['title'])
        else:
            self.log.info("No title.")
            title = "Untitled"
        if result.has_key('author'):
            al = result['author']
            authors = [u"%s, %s"%(x['family'],x['given']) for x in al]
        else:
            self.log.info("No author.")
            authors = [_('Unknown')]

        if result.has_key('DOI'):
            identifiers['doi'] = result['DOI']

        self.log.info("found title %s."%title)
        self.log.info("found authors %s."%authors)

        mi = Metadata(title, authors)
        mi.identifiers = identifiers
        if result.has_key('language'):
            mi.language = canonicalize_lang( result['language'])
        if result.has_key('publisher'):
            mi.publisher = result['publisher']
        if result.has_key('subject'):
            mi.tags = result['subject']

        def datestr(dp):
            parse_date("-".join(map(str,dp['date-parts'][0])))
        if result.has_key('published-print'):
            mi.pubdate = datestr(result['published-print'])
        elif result.has_key('published-online'):
            mi.pubdate = datestr(result['published-online'])

        if result.has_key('container-title') and result.has_key('journal-issue'):
            journ = "/".join(result['container-title'])
            ji = result['journal-issue']
            if result.has_key('volume'):
                journ = "%s Vol. %s" % (journ, result['volume'])
            if ji.has_key('published-print'):
                jd ="-".join(map(str,ji['published-print']['date-parts'][0]))
                ser = "%s %s" % (journ, jd)
            else:
                ser = journ
            jiss = ji['issue']
            mi.series = ser
            mi.series_index= jiss

        extra_meta = self.mkComments(result)
        mi.comments = "\n".join(extra_meta)

        if result.has_key('score'):
            mi.source_relevance= result['score']
        else:
            mi.source_relevance= 0

        self.log.info("set comment to %s"%mi.comments)
        self.log.info("queuing")
        return(mi)

    def mkComments(self, result):
        extra_meta=["DOI-Download-Data:"]
        def quick_add(key, name=None, joiner=", "):
            if name is None:
                name = key
            if result.has_key(key):
                v = result[key]
                if isinstance(v, list):
                    strval = joiner.join(v)
                else:
                    strval = v
                extra_meta.append("%s: %s" % (key,strval))

        quick_add('type')
        quick_add('container-title', 'journal')
        quick_add('volume')
        quick_add('page')
        quick_add('issue')
        quick_add('ISSN')

        if result.has_key('link'):
            links = result['link']
            remove_mining = filter(lambda x: x['intended-application']!='text-mining', links)
            urlOnly = map(lambda x: x['URL'], remove_mining)
            extra_meta.append("URL: %s" % (" ".join(urlOnly)))
        return extra_meta


    # def retrieve(self):
        # url = 'https://api.crossref.org/works/10.1002/bmc.835'
        # # output = urlopen(url).read()
        # br = browser()
        # cdata = br.open_novisit(url, timeout=DoiReader.timeout).read()
        # # urlbad = 'https://apu.crossref.urg/works/10.1002/bmc.835'
        # # cdatabad = br.open_novisit(urlbad, timeout=30).read()
        # # throws URLERROR
        # # urlb2 = 'https://api.crossref.org/works/10.1002/bmi.836'
        # # cdatabad = br.open_novisit(urlb2, timeout=30).read()
        # # throws httperror_seek_wrapper
        # data = json.loads(cdata)
        # # check data['status']
        # if data['status'] != 'ok':
            # raise DoiException(data['status'])
        # return data['message']


class DoiException(Exception):
    def __init__( self, status ):
        self.host = status
        Exception.__init__(self, 'Bad Doi result exception:  %s' % status)
