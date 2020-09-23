import os, tempfile, time
from threading import Event

from calibre.ebooks.metadata.book.base import Metadata
from calibre.ebooks.metadata.sources.base import create_log
from calibre.utils.logging import Log
from calibre_plugins.crossref_doi_download import DoiMeta
from calibre_plugins.crossref_doi_download.doi_reader import DoiReader

def init_test(tdir_name):
    tdir = tempfile.gettempdir()
    lf = os.path.join(tdir, tdir_name.replace(' ', '')+'_identify_test.txt')
    log = create_log(open(lf, 'w'))
    abort = Event()
    return tdir, lf, log, abort



def test_identify_plugin(name, tests, modify_plugin=lambda plugin:None,  # {{{
        fail_missing_meta=True):
    '''
    :param name: Plugin name
    :param tests: List of 2-tuples. Each two tuple is of the form (args,
                  test_funcs). args is a dict of keyword arguments to pass to
                  the identify method. test_funcs are callables that accept a
                  Metadata object and return True iff the object passes the
                  test.
    '''
    plugin = None
    for x in all_metadata_plugins():
        if x.name == name and 'identify' in x.capabilities:
            plugin = x
            break
    modify_plugin(plugin)
    prints('Testing the identify function of', plugin.name)
    prints('Using extra headers:', plugin.browser.addheaders)

    tdir, lf, log, abort = init_test(plugin.name)
    prints('Log saved to', lf)

    times = []
    for kwargs, test_funcs in tests:
        log('')
        log('#'*80)
        log('### Running test with:', kwargs)
        log('#'*80)
        prints('Running test with:', kwargs)
        rq = Queue()
        args = (log, rq, abort)
        start_time = time.time()
        plugin.running_a_test = True
        try:
            err = plugin.identify(*args, **kwargs)
        finally:
            plugin.running_a_test = False
        total_time = time.time() - start_time
        times.append(total_time)
        if err is not None:
            prints('identify returned an error for args', args)
            prints(err)
            break

        results = []
        while True:
            try:
                results.append(rq.get_nowait())
            except Empty:
                break

        prints('Found', len(results), 'matches:', end=' ')
        prints('Smaller relevance means better match')

        results.sort(key=plugin.identify_results_keygen(
            title=kwargs.get('title', None), authors=kwargs.get('authors',
                None), identifiers=kwargs.get('identifiers', {})))

        for i, mi in enumerate(results):
            prints('*'*30, 'Relevance:', i, '*'*30)
            if mi.rating:
                mi.rating *= 2
            prints(mi)
            prints('\nCached cover URL    :',
                    plugin.get_cached_cover_url(mi.identifiers))
            prints('*'*75, '\n\n')

        possibles = []
        for mi in results:
            test_failed = False
            for tfunc in test_funcs:
                if not tfunc(mi):
                    test_failed = True
                    break
            if not test_failed:
                possibles.append(mi)

        if not possibles:
            prints('ERROR: No results that passed all tests were found')
            prints('Log saved to', lf)
            log.close()
            dump_log(lf)
            raise SystemExit(1)

        good = [x for x in possibles if plugin.test_fields(x) is
                None]
        if not good:
            prints('Failed to find', plugin.test_fields(possibles[0]))
            if fail_missing_meta:
                raise SystemExit(1)

        if results[0] is not possibles[0]:
            prints('Most relevant result failed the tests')
            raise SystemExit(1)

        if 'cover' in plugin.capabilities:
            rq = Queue()
            mi = results[0]
            plugin.download_cover(log, rq, abort, title=mi.title,
                    authors=mi.authors, identifiers=mi.identifiers)
            results = []
            while True:
                try:
                    results.append(rq.get_nowait())
                except Empty:
                    break
            if not results and fail_missing_meta:
                prints('Cover download failed')
                raise SystemExit(1)
            elif results:
                cdata = results[0]
                cover = os.path.join(tdir, plugin.name.replace(' ',
                    '')+'-%s-cover.jpg'%sanitize_file_name(mi.title.replace(' ',
                        '_')))
                with open(cover, 'wb') as f:
                    f.write(cdata[-1])

                prints('Cover downloaded to:', cover)

                if len(cdata[-1]) < 10240:
                    prints('Downloaded cover too small')
                    raise SystemExit(1)

    prints('Average time per query', sum(times)/len(times))

    if os.stat(lf).st_size > 10:
        prints('There were some errors/warnings, see log', lf)
