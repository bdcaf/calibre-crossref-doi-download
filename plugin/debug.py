def pybtest():
    from pybtex.database import BibliographyData, Entry
    bib_data = BibliographyData({
        'article-minimal': Entry('article', [
            ('author', 'L[eslie] B. Lamport'),
            ('title', 'The Gnats and Gnus Document Preparation System'),
            ('journal', "G-Animal's Journal"),
            ('year', '1986'),
        ]),
    })
    print(bib_data.to_string('bibtex'))

from calibre import ipython
ipython(locals())

