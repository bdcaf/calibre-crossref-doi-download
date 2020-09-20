# https://manual.calibre-ebook.com/develop.html
# https://manual.calibre-ebook.com/creating_plugins.html
from calibre_plugins.doi_meta.doi_reader import DoiReader
dr = DoiReader()
dr.retrieve()

columns = {
    "is-referenced-by-count": "acad_is-referenced-by-count",
    "DOI": "acad_DOI",
    "type": "acad_type",
    "URL": "acad_URL",
    "ISSN": "acad_ISSN",
    "subtitle": "acad_subtitle",
    "member": "acad_member",
    "title": "acad_title",
    "content-domain": "acad_content-domain",
    "source": "acad_source",
    "publisher": "acad_publisher",
    "prefix": "acad_prefix",
    "author": "acad_author",
    "reference": "acad_reference",
    "published-print": "acad_published-print",
    "relation": "acad_relation",
    "issn-type": "acad_issn-type",
    "references-count": "acad_references-count",
    "container-title": "acad_container-title",
    "published-online": "acad_published-online",
    "license": "acad_license",
    "issue": "acad_issue",
    "volume": "acad_volume",
    "score": "acad_score",
    "original-title": "acad_original-title",
    "page": "acad_page",
    "subject": "acad_subject",
    "short-title": "acad_short-title",
    "reference-count": "acad_reference-count",
    "short-container-title": "acad_short-container-title",
    "created": "acad_created",
    "indexed": "acad_indexed",
    "journal-issue": "acad_journal-issue",
    "deposited": "acad_deposited",
    "language": "acad_language",
    "link": "acad_link",
    "issued": "acad_issued"
}
