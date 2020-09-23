'''
List of field names parsed
This list is just used to check responses, adding it will not change parsing!
Commented out fields need implementation.
Used-fields will always be parsed
Cond-fields will be parsed if corresponding setting is active.
Ignored fields don't make sense to store.
See https://github.com/Crossref/rest-api-doc/blob/master/api_format.md for available fields
'''

from itertools import chain
from calibre_plugins.crossref_doi_download.doi_reader import COMMENT_FIELDS

USED_FIELDS = frozenset(
    ['author'
     ,'title'
     ,'short-title' # optional as alternative
     ,'publisher'
     ,'issued'
     ,'container-title'
     ,'short-container-title' # optional as alternative
     ,'ISBN'
     ,'DOI'
     ,'language'
     ,'subject' # to tags
     ,'score' # used for metadata relevance
     ])

COND_FIELDS = frozenset(
    COMMENT_FIELDS.keys() + [
        'type' # placed in comment
        ,'abstract' # offer to put it in comment
        ,'subtitle' # todo
        ,'issue' # volume OR issue will be put into series index (volume prefered)
        ,'volume' # to comments
        ,'page' # to comments
        ,'ISSN' # to comments
        ,'published-print' # to comment
        ,'published-online' # to comment
        ,'link' # may contain link to full text, to comments
        ,'event' # not documented - for now dump
        ,'journal-issue' # not documented - for now dump
        ,'institution' # not documented - for now dump
        ,'publisher-location'
    ])
        # ,'reference' # todo
        # ,'relation' # todo
        # ,'clinical-trial-number' # todo
        # ,'review' # todo
        # ,'article-number' # todo
        # ,'references-count' # todo
        # ,'archive' # unclear
        # ,'license' # unclear
        # ,'group-title'

IGNORED_FIELDS = frozenset(
    ['original-title' # don't want
     ,'reference-count' # depreciated through references-count
     ,'references-count' # only makes sense when reference is stored
     ,'is-referenced-by-count' # depreciated through references_-count
     ,'source' # currently always crossref
     ,'prefix' # not needed
     ,'URL' # provided by calibre
     ,'member' # crossref specific
     ,'created' # crossref specific
     ,'deposited' # crossref specific
     ,'indexed' # crossref specific
     ,'posted' # crossref specific
     ,'content-domain' # crossref specific
     ,'accepted' # crossref specific
     ,'update-policy' # crossref specific
     ,'content-created' # crossref specific
     ,'content-updated' # crossref specific
     ,'assertion' # crossref specific
     ,'license' #  so far have only seen licenses for data-mining/text-only content
     ,'reference' # list of reverences made,
     ,'relation' # usually empty, could have been interesting
     ,'issn-type' # multiple ISSNs by type - not sure if storing them makes sense
     ,'isbn-type' # multiple ISBNs by type - not sure if storing them makes sense
     ,'alternative-id' # not enough info to make sense of
     ,'assertion' # peer review related, not sure how to use
     ,'review' # peer review related, not sure how to use
     ,'approved'
     ,'subtype'
     ])

def check_uninterpreted_fields(result):
    diff = set(result.keys()) - USED_FIELDS - COND_FIELDS - IGNORED_FIELDS
    return diff

def check_uninterpreted_list(results):
    dl = map(check_uninterpreted_fields, results)
    diff = set(chain(*dl))
    return diff

if __name__ == "__main__":
    print("hello:hello")
    print(COND_FIELDS)
pass
