# get doi from url:
# e.g. curl https://api.crossref.org/works/10.1002/bmc.835 > test
# Link is under URL
import json

from calibre.ebooks.metadata.book.base import Metadata
from calibre.utils.date import parse_date
from calibre.utils.localization import canonicalize_lang
from calibre_plugins.doi_meta.config import prefs

class DoiReader:
    used_fields= set(['author'
                     ,'title'
                     ,'issue'
                     ,'volume'
                      ])
    def __init__(self, logger):
        self.log = logger
        self.toComment = prefs['query_to_comment']

    def parseDoi(self, cdata, identifiers = {}):
        data = json.loads(cdata)
        # check data['status']
        if data['status'] != 'ok':
            self.log.info("query result '%s'"%data['status'])
            return "Bad response status: %s"%data['status']
        if data['message-type'] != 'work':
            self.log.warning("query result wrong type: '%s'"%data['message-type'])
            return "Bad response type: %s"%data['message-type']
        result = data['message']
        return self.result2meta(result, identifiers)

    def authorString(self, author):
        if author.has_key('family') and author.has_key('given'):
            return (u"%s, %s" % (author['family'],author['given']))
        elif author.has_key('name'):
            return author['name']
        else:
            self.log.warning("Weird author: %s" % author)
            return None
    def checkUsage(self, result):
        diff = list(set(result.keys()) - set(DoiReader.used_fields))
        if len(diff)>0:
            self.log("unused fields: %s" % diff)

    def result2meta(self, result, prev_identifiers={}):
        if result.has_key('title'):
            title = ': '.join(result['title'])
        else:
            title = _('Untitled')
        if result.has_key('author'):
            al = result['author']
            authors = [self.authorString(x) for x in al]
        else:
            authors = [_('Unknown')]

        if result.has_key('DOI'):
            prev_identifiers['doi'] = result['DOI']
        mi = Metadata(title, authors)
        mi.identifiers = prev_identifiers
        if result.has_key('language'):
            mi.language = canonicalize_lang( result['language'])
        if result.has_key('publisher'):
            mi.publisher = result['publisher']
        if result.has_key('subject'):
            mi.tags = result['subject']

        if result.has_key('published-print'):
            mi.pubdate = datestr(result['published-print'])
        elif result.has_key('published-online'):
            mi.pubdate = datestr(result['published-online'])

        if result.has_key('container-title'):
            mi.series = "/".join(result['container-title'])
        if result.has_key('volume'):
            mi.series_index= result['volume']
        elif result.has_key('issue'):
            mi.series_index= result['issue']

        if self.toComment:
            extra_meta = self.mkComments(result)
            mi.comments = "\n".join(extra_meta)

        if result.has_key('score'):
            mi.source_relevance= result['score']
        else:
            mi.source_relevance= 0
        # self.log.info("set comment to %s"%mi.comments)
        return mi

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
            url_only = map(lambda x: x['URL'], remove_mining)
            extra_meta.append("URL: %s" % (" ".join(url_only)))
        return extra_meta

        if  result.has_key('journal-issue'):
            ji = result['journal-issue']
            if ji.has_key('published-print'):
                jd ="-".join(map(str,ji['published-print']['date-parts'][0]))
                extra_meta.append("published: %s" % (jd))

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

def datestr(dp):
    return parse_date("-".join(map(str,dp['date-parts'][0])))

class DoiException(Exception):
    def __init__( self, status ):
        self.host = status
        Exception.__init__(self, 'Bad Doi result exception:  %s' % status)
