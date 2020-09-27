import re
import json

QUERY_URL = 'https://doi.org/api/handles/%s'
DOI_START = re.compile('^10\.')

def is_short_doi(querydoi):
    if len(querydoi) > 12:
        return False
    if DOI_START.match(querydoi):
        return False
    return True

def return_full_doi(browser,doi):
    query = QUERY_URL % doi
    cdata = browser.open(query).read()
    res = json.loads(cdata)
    val = res['values']
    for v in val:
        if 'type' in v and v['type']=='HS_ALIAS':
            d = v['data']['value']
            return d
    raise Exception('No expanded DOI in query result.')
