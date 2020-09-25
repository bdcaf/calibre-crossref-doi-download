#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import absolute_import, division, print_function, unicode_literals

__license__   = 'GPL v3'
__copyright__ = '2020, Clemens Ager'
__docformat__ = 'restructuredtext en'

import json
from calibre.ebooks.metadata.sources.base import Source
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.crossref_doi_download.doi_reader import DoiReader
from calibre_plugins.crossref_doi_download.doi_request import DoiQuery
from calibre_plugins.crossref_doi_download.config import prefs


class DoiMeta(Source):
    '''
    This class is a simple wrapper that provides information about the actual
    plugin class. The actual interface plugin class is called InterfacePlugin
    and is defined in the ui.py file, as specified in the actual_plugin field
    below.

    The reason for having two classes is that it allows the command line
    calibre utilities to run without needing to load the GUI libraries.
    '''
    name                = 'Crossref DOI Metadata Downloader'
    description         = 'Download DOI metadata from Crossref API.'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Clemens Ager'
    version             = (0, 0, 1)
    minimum_calibre_version = (0, 7, 53)

    capabilities = frozenset(['identify'])
    touched_fields = frozenset(['title'
                                ,'authors'
                                ,'identifier:doi'
                                ,'languages'
                                ,'series'
                                ,'pubdate'
                                ,'publisher'
                                ,'comments'
                                ,'tags'
                                ])
    supports_gzip_transfer_encoding=True

    def identify(self, log, result_queue, abort, title=None, authors=None,
                identifiers={}, timeout=30):
            '''
            Identify a book by its Title/Author/ISBN/etc.

            If identifiers(s) are specified and no match is found and this metadata
            source does not store all related identifiers (for example, all ISBNs
            of a book), this method should retry with just the title and author
            (assuming they were specified).

            Every Metadata object put into result_queue by this method must have a
            `source_relevance` attribute that is an integer indicating the order in
            which the results were returned by the metadata source for this query.
            This integer will be used by :meth:`compare_identify_results`. If the
            order is unimportant, set it to zero for every result.

            Make sure that any cover/ISBN mapping information is cached before the
            Metadata object is put into result_queue.

            :param log: A log object, use it to output debugging information/errors
            :param result_queue: A result Queue, results should be put into it.
                                Each result is a Metadata object
            :param abort: If abort.is_set() returns True, abort further processing
                          and return as soon as possible
            :param title: The title of the book, can be None
            :param authors: A list of authors of the book, can be None
            :param identifiers: A dictionary of other identifiers, most commonly
                                {'isbn':'1234...'}
            :param timeout: Timeout in seconds, no network request should hang for
                            longer than timeout.
            :return: None if no errors occurred, otherwise a unicode representation
                     of the error suitable for showing to the user

            '''
            log.info("start doi lookup")
            onlineQuery = DoiQuery(self.browser, log)
            reader = DoiReader(log)
            if 'doi' in identifiers:
                log("lookup by doi")
                doi = identifiers['doi']
                try:
                    message = onlineQuery.queryByDoi(doi)
                except Exception as e:
                    log.exception('Online query failed with reason: %s' % e)
                    return as_unicode(e)
                log.info("sucessfull retrieve")

                mi = reader.result2meta(message, identifiers)
                mi.source_relevance = 1
                result_queue.put(mi)

            if prefs['query_extra_by_name'] or not 'doi' in identifiers:
                # see https://github.com/CrossRef/rest-api-doc#queries
                log("lookup by query")
                query = {}
                # nres = prefs['query_max_res']
                # query['rows']=nres

                bibquery = []
                if title:
                    bibquery += list(self.get_title_tokens(title))
                if authors:
                    bibquery += list(self.get_author_tokens(authors))
                query['query.bibliographic']= " ".join(bibquery)
                # log.info("query: %s" % query)
                try:
                    message = onlineQuery.byQuery(query)
                    results = message['items']
                    fin = map(lambda x:reader.result2meta(x,identifiers),results)
                    map(lambda x: result_queue.put(x), fin)

                except Exception as e:
                    log.exception('Online query failed.')
                    return e


            return None

    def is_customizable(self):
        '''
        This method must return True to enable customization via
        Preferences->Plugins
        '''
        return True

    def config_widget(self):
        '''
        Implement this method and :meth:`save_settings` in your plugin to
        use a custom configuration dialog.

        This method, if implemented, must return a QWidget. The widget can have
        an optional method validate() that takes no arguments and is called
        immediately after the user clicks OK. Changes are applied if and only
        if the method returns True.

        If for some reason you cannot perform the configuration at this time,
        return a tuple of two strings (message, details), these will be
        displayed as a warning dialog to the user and the process will be
        aborted.

        The base class implementation of this method raises NotImplementedError
        so by default no user configuration is possible.
        '''
        # It is important to put this import statement here rather than at the
        # top of the module as importing the config class will also cause the
        # GUI libraries to be loaded, which we do not want when using calibre
        # from the command line
        from calibre_plugins.crossref_doi_download.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        '''
        Save the settings specified by the user with config_widget.

        :param config_widget: The widget returned by :meth:`config_widget`.
        '''
        config_widget.save_settings()
