'''
List of field names parsed
This list is just used to check responses, adding it will not change parsing!
Used-fields will always be parsed
Cond-fields will be parsed if corresponding setting is active.
Ignored fields are never used.
See https://github.com/Crossref/rest-api-doc/blob/master/api_format.md for available fields
'''
USED_FIELDS = frozen_set(
    ['author'
     ,'title'
     ,'publisher'
     ,'DOI'
     ,'issued'
     ,'container-title'
     ])

COND_FIELDS = frozen_set([
    'abstract' # offer to put it in comment
     ,'short-title' # maybe offer to use it instead of title
     ,'subtitle' # todo?
     ,'short-container-title'
     ,'issue' # volume OR issue will be put into series index (volume prefered)
     ,'volume'
])
IGNORED_FIELDS = frozen_set(
    ['original-title'
     ,'reference-count'
     ,'references-count'
     ,'is-referenced-by-count'
     ,'source'
     ,'prefix'
     ,'URL'
     ,'created'
     ,'deposited'
     ,'indexed'
     ,'posted'
     ,'accepted'
     ])
