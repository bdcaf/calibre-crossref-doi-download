# get doi from url:
# e.g. curl https://api.crossref.org/works/10.1002/bmc.835 > test
# fields: https://github.com/Crossref/rest-api-doc/blob/master/api_format.md
# Link is under URL
import json

from calibre.ebooks.metadata.book.base import Metadata
from calibre.utils.date import parse_date
from calibre.utils.localization import canonicalize_lang
from calibre_plugins.crossref_doi_download.config import prefs

NAME_FIELDS=frozenset(['author','editor','funder'])
COMMENT_FIELDS = { 'type':None
                  ,'title':None
                  ,'short-title':None
                  ,'subtitle':None
                  ,'publisher':None
                  ,'publisher-location':None # undocumented, but seems simple string
                  ,'article-number':None # undocumented
                  ,'issued':None
                  ,'container-title':'journal'
                  ,'short-container-title':'short-journal'
                  ,'edition-number':None # not documented, but seems simple
                  ,'volume':None
                  ,'issue':None
                  ,'page':None
                  ,'DOI':None
                  ,'ISBN':None
                  ,'ISSN':None
                  ,'language':None
                  # following are just dumped
                  ,'published-print':None
                  ,'published-online':None
                  ,'funder':None
                  ,'editor':None
                  ,'event':None
                  ,'journal-issue':None # undocumented
                  ,'funder':None
                  ,'chair':None 
                  ,'alternative-id':None 
                  ,'institution':None # undocumented
                  ,'degree':None # undocumented
                  ,'archive':None # undocumented
                  ,'standards-body':None # undocumented
                  }

def get_title(result):
    if prefs['prefer_short_title'] and result.has_key('short-title'):
        title = ' '.join(result['short-title'])
    elif result.has_key('title'):
        title = ' '.join(result['title'])
    else:
        title = _('Untitled')
    return title

def _author2string(author):
    if author.has_key('family') and author.has_key('given'):
        return (u"%s, %s" % (author['family'],author['given']))
    elif author.has_key('family') and not author.has_key('given'):
        return author['family']
    elif author.has_key('name'):
        return author['name']
    else:
        raise Exception("Unimplementd author type: %s" % author)
def get_author_list(result):
    if result.has_key('author'):
        al = result['author']
        authors = [_author2string(x) for x in al]
    else:
        authors = [_('Unknown')]
    return authors

def update_identifiers(prev_identifiers, result):
    if result.has_key('DOI'):
        prev_identifiers['doi'] = result['DOI']
    if result.has_key('ISBN'):
        prev_identifiers['isbn'] = result['ISBN'][0]
    return prev_identifiers

def put_language(mi, result):
    if result.has_key('language'):
        mi.language = canonicalize_lang( result['language'])
def put_publisher(mi,result):
        if result.has_key('publisher'):
            mi.publisher = result['publisher']
def put_tags(mi,result):
        if prefs['add_tags'] and result.has_key('subject'):
            mi.tags = result['subject']
def put_journal(mi,result):
        if prefs['prefer_short_journal'] and result.has_key('short-container-title'):
            mi.series = "/".join(result['short-container-title'])
        elif result.has_key('container-title'):
            mi.series = "/".join(result['container-title'])
def put_series_index(mi, result):
        if result.has_key('volume'):
            mi.series_index= result['volume']
        elif result.has_key('issue'):
            mi.series_index= result['issue']
class DoiReader:
    '''
    Class to convert from the result structure to a Metadata object.
    '''
    def __init__(self, logger):
        self.log = logger

    # def parseDoi(self, cdata, identifiers = {}):
        # data = json.loads(cdata)
        # # check data['status']
        # if data['status'] != 'ok':
            # self.log.info("query result '%s'"%data['status'])
            # return "Bad response status: %s"%data['status']
        # if data['message-type'] != 'work':
            # self.log.warning("query result wrong type: '%s'"%data['message-type'])
            # return "Bad response type: %s"%data['message-type']
        # result = data['message']
        # return self.result2meta(result, identifiers)


    # def checkUsage(self, result):
        # diff = list(set(result.keys()) - set(DoiReader.used_fields))
        # if len(diff)>0:
            # self.log("unused fields: %s" % diff)

    def result2meta(self, result, prev_identifiers={}):
        title = get_title(result)
        authors = get_author_list(result)
        mi = Metadata(title, authors)

        mi.identifiers = update_identifiers(prev_identifiers, result)

        put_publisher(mi,result)
        put_language(mi,result)
        self.put_pubdate(mi,result)
        put_tags(mi,result)
        put_journal(mi, result)
        put_series_index(mi, result)

        comments = ""
        if prefs['abstract_to_comment'] and result.has_key('abstract'):
            comments = "\n\n".join([comments, result['abstract']])

        if prefs['query_to_comment']:
            extra_meta = self.mkComments(result)
            extra_plus = map(lambda x: "crossref:%s" % x, extra_meta)
            extra = "\n".join(extra_plus)
            comments = "\n\n".join([comments,extra])
        mi.comments = comments

        if result.has_key('score'):
            mi.source_relevance= 100 - result['score']
        else:
            mi.source_relevance=100
        # self.log.info("set comment to %s"%mi.comments)
        return mi

    def mkComments(self, result):
        extra_meta=[]
        def quick_add(key, name=None, joiner=", "):
            if name is None:
                name = key
            if result.has_key(key):
                v = result[key]
                if isinstance(v, list):
                    if (key in NAME_FIELDS):
                        strval = joiner.join(map(_author2string, v))
                    else:
                        strval = joiner.join(v)
                elif isinstance(v, dict):
                    if v.has_key('date-parts'):
                        strval = self.read_partial_date(v)
                    else:
                        self.log.warning("Unhandled dict:","%s: %s" % (key, v) )
                else:
                    strval = v
                extra_meta.append("%s: %s" % (key,strval))

        for a,targ in COMMENT_FIELDS.items():
            try:
                quick_add(a,targ)
            except Exception as e:
                self.log.warning("Encountered problem:",e )
                self.log.warning("Unhandled input:","%s: %s" % (a, result[a]) )


        if result.has_key('link'):
            links = result['link']
            remove_mining = filter(lambda x: x['intended-application']!='text-mining', links)
            url_only = map(lambda x: x['URL'], remove_mining)
            extra_meta.append("URL: %s" % (" ".join(url_only)))
        return extra_meta

        # if  result.has_key('journal-issue'):
            # ji = result['journal-issue']
            # if ji.has_key('published-print'):
                # jd ="-".join(map(str,ji['published-print']['date-parts'][0]))
                # extra_meta.append("published: %s" % (jd))

    def read_partial_date(self,dp):
        if dp.has_key('date-parts'):
            return "-".join(map(str,dp['date-parts'][0]))
        else:
            return None

    def datestr(self,dp):
        ds = self.read_partial_date(dp)
        if ds:
            try:
                return parse_date(ds)
            except Exception as e:
                self.log.warning("failed date input", dp)
                self.log.warning("failed date result", e)
                return None
        else:
            self.log.warning("unknown date format:", dp)
            return None

    def put_pubdate(self,mi,result):
            if result.has_key('issued'):
                mi.pubdate = self.datestr(result['issued'])

