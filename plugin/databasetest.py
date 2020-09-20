# from calibre.library import db
# mydb = db('~/Archive/CalTest/').new_api
# db = self.gui.current_db.new_api

mydb.all_book_ids()
mydb.get_metadata(4)
mydb.has_id(10)

# all fields known.
mydb.fields


## get_metadata error
book_id=4
get_user_categories=False
from calibre.ebooks.metadata.book.base import Metadata
mi = mydb._get_metadata(book_id, get_user_categories=get_user_categories)
# still TypeError: 'bool' object is not callable
mi = Metadata(None, template_cache=mydb.formatter_template_cache)
author_ids = mydb._field_ids_for('authors', book_id)
adata = mydb._author_data(author_ids)
ids = mydb._field_for('identifiers', book_id)
mi.title       = mydb._field_for('title', book_id, default_value=_('Unknown'))
mi.comments    = mydb._field_for('comments', book_id)
mi.publisher   = mydb._field_for('publisher', book_id)
n = utcnow()
mi.timestamp   = mydb._field_for('timestamp', book_id, default_value=n)
mi.pubdate     = mydb._field_for('pubdate', book_id, default_value=n)
mi.uuid        = mydb._field_for('uuid', book_id,
                                 default_value='dummy')
mi.title_sort  = mydb._field_for('sort', book_id,
                                 default_value=_('Unknown'))
mi.last_modified = mydb._field_for('last_modified', book_id,
                                   default_value=n)
formats = mydb._field_for('formats', book_id)
