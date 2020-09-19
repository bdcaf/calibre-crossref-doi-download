= Readme =

Plugin to help with academic content in calibre.

Based on the [calibre guides for plugins](https://manual.calibre-ebook.com/creating_plugins.html).

Following features are planned:
- Import/Export to bibtex file (similar what the [zotero metadata importer](https://www.mobileread.com/forums/showthread.php?p=3339191#poststop) plugin for Zotero does). The file needs to be compatible with [jabref](http://www.jabref.org).
- Query by doi - maybe also by arxiv, bioarxiv 
- Download from arxix, bioarxiv and (maybe) doi.

Some infrastructure helping with:
- assuring the database has correct shape, maybe migration
- helping with duplicates (merging in the zotero plugin throws errors)

## Ideas
I had a little look at how [zmi](https://www.mobileread.com/forums/showthread.php?p=3339191#poststop) achieves this and concluded it has little use to fork it.

## Libraries used
I want to use following libraries:
- [pybtex](https://bitbucket.org/pybtex-devs/pybtex/src/master/)
