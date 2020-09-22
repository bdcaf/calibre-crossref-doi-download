'''
List of field names parsed
This list is just used to check responses, adding it will not change parsing!
Commented out fields need implementation.
Used-fields will always be parsed
Cond-fields will be parsed if corresponding setting is active.
Ignored fields don't make sense to store.
See https://github.com/Crossref/rest-api-doc/blob/master/api_format.md for available fields
'''
USED_FIELDS = frozenset(
    ['author'
     ,'title'
     ,'publisher'
     ,'DOI'
     ,'issued'
     ,'container-title'
     ,'ISBN'
     ,'language'
     ])

COND_FIELDS = frozenset([
    'abstract' # offer to put it in comment
    ,'short-title' # optional as alternative
    ,'subtitle' # todo?
    ,'short-container-title' # optional as alternative
    ,'issue' # volume OR issue will be put into series index (volume prefered)
    ,'volume' # to comments
    ,'page' # to comments
    ,'subject' # to tags
    ,'ISSN' # to comments
    ,'published-print' # to comment
    ,'published-online' # to comment
    # ,'funder' # todo
    # ,'assertion' # todo
    # ,'editor' # todo
    # ,'chair' # todo
    # ,'link' # to comments
    # ,'alternative-id' # todo
    # ,'reference' # todo
    # ,'relation' # todo
    # ,'clinical-trial-number' # todo
    # ,'review' # todo
    # ,'article-number' # todo
    # ,'references-count' # todo
    # ,'archive' # unclear
    # ,'license' # unclear
    # ,'group-title'
])

IGNORED_FIELDS = frozenset(
    ['original-title' # don't want
     ,'reference-count' # depreciated through references_-count
     ,'is-referenced-by-count' # depreciated through references_-count
     ,'source' # currently always crossref
     ,'prefix' # not needed
     ,'URL' # provided by calibre
     ,'created' # crossref specific
     ,'deposited' # crossref specific
     ,'indexed' # crossref specific
     ,'posted' # crossref specific
     ,'accepted' # crossref specific
     ,'update-policy' # crossref specific
     ])

def check_unknown(result):
    diff = result.keys() - USED_FIELDS
    return diff
