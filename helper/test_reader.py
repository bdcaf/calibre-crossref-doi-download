
from calibre.ebooks.metadata.sources.test import (
    tests = [({
        'identifiers': {
            'doi': '10.1002/bmc.835'
        },
        'title': 'some',
        'authors': ['busz']
    }, [
        title_test('human exhaled air analytics: biomarkers of diseases', exact=True)
    ])
             # not most relevant result
             # , ({
             # 'identifiers': {},
             # 'title':'How to Interpret Hydrogen Breath Tests',
             # 'authors':['Ghoshal, Uday C']
             # },[
             # title_test('how to interpret hydrogen breath tests', exact=True)
             # ])
             ]
    test_identify_plugin(DoiMeta.name, tests[:])
