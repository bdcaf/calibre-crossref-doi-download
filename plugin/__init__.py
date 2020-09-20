#!/usr/bin/env python2
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai
from __future__ import absolute_import, division, print_function, unicode_literals

__license__   = 'GPL v3'
__copyright__ = '2020, Clemens Ager'
__docformat__ = 'restructuredtext en'

from calibre.ebooks.metadata.sources.base import Source
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.doi_meta.doi_reader import DoiReader
import json

class DoiMeta(Source):
    '''
    This class is a simple wrapper that provides information about the actual
    plugin class. The actual interface plugin class is called InterfacePlugin
    and is defined in the ui.py file, as specified in the actual_plugin field
    below.

    The reason for having two classes is that it allows the command line
    calibre utilities to run without needing to load the GUI libraries.
    '''
    name                = 'DOI Metadata'
    description         = 'Download DOI metadata.'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Clemens Ager'
    version             = (0, 0, 0)
    minimum_calibre_version = (0, 7, 53)

    capabilities = frozenset(['identify'])
    touched_fields = frozenset(['title'
                                ,'authors'
                                ,'comments'
                                ,'identifier:doi'
                                ,'languages'
                                ,'series'
                                ,'pubdate'
                                ,'publisher'
                                ,'tags'
                                ])
    supports_gzip_transfer_encoding=True

    def get_book_url(self, identifiers):
        '''
        Return a 3-tuple or None. The 3-tuple is of the form:
        (identifier_type, identifier_value, URL).
        The URL is the URL for the book identified by identifiers at this
        source. identifier_type, identifier_value specify the identifier
        corresponding to the URL.
        This URL must be browseable to by a human using a browser. It is meant
        to provide a clickable link for the user to easily visit the books page
        at this source.
        If no URL is found, return None. This method must be quick, and
        consistent, so only implement it if it is possible to construct the URL
        from a known scheme given identifiers.
        '''
        if not identifiers.has_key('doi'):
            return None
        doi = identifiers['doi']
        return ('doi', doi, 'https://api.crossref.org/works/%s'%doi )
            # url = 'https://api.crossref.org/works/10.1002/bmc.835'

    def identify(self, log, result_queue, abort, title=None, authors=None,
                identifiers={}, timeout=30):
            '''
            Identify a book by its Title/Author/ISBN/etc.

            If identifiers(s) are specified and no match is found and this metadata
            source does not store all related identifiers (for example, all ISBNs
            of a book), this method should retry with just the title and author
            (assuming they were specified).

            If this metadata source also provides covers, the URL to the cover
            should be cached so that a subsequent call to the get covers API with
            the same ISBN/special identifier does not need to get the cover URL
            again. Use the caching API for this.

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
            log("start doi lookup")
            if not identifiers.has_key('doi'):
                log("has no doi entry")
                return None
            doi = identifiers['doi']
            log.info("query doi entry '%s'"%doi)
            url = 'https://api.crossref.org/works/%s'%doi
            log.info("query url '%s'" % url)
            # output = urlopen(url).read()
            try:
                br = self.browser
                cdata = br.open_novisit(url).read()
            except Exception as e:
                log.exception('Online query failed.')
                return as_unicode(e)


            reader = DoiReader(log)
            mi = reader.parseDoi(cdata, identifiers)

            result_queue.put(mi)
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
        from calibre_plugins.doi_meta.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        '''
        Save the settings specified by the user with config_widget.

        :param config_widget: The widget returned by :meth:`config_widget`.
        '''
        config_widget.save_settings()

        # Apply the changes
        # ac = self.actual_plugin_
        # if ac is not None:
            # ac.apply_settings()

