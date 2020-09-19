# get doi from url:
# e.g. curl https://api.crossref.org/works/10.1002/bmc.835 > test
# Link is under URL
import json
from calibre_plugins.acad_plug.config import prefs
from calibre import browser
class DoiReader:
    timeout = 30

    def retrieve(self):
            url = 'https://api.crossref.org/works/10.1002/bmc.835'
            # output = urlopen(url).read()
            br = browser()
            cdata = br.open_novisit(url, timeout=DoiReader.timeout).read()
            # urlbad = 'https://apu.crossref.urg/works/10.1002/bmc.835'
            # cdatabad = br.open_novisit(urlbad, timeout=30).read()
            # throws URLERROR
            # urlb2 = 'https://api.crossref.org/works/10.1002/bmi.836'
            # cdatabad = br.open_novisit(urlb2, timeout=30).read()
            # throws httperror_seek_wrapper
            data = json.loads(cdata)
            # check data['status']
            if data['status'] != 'ok':
                raise DoiException(data['status'])
            return data['message']


class DoiException(Exception):
    def __init__( self, status ):
        self.host = status
        Exception.__init__(self, 'Bad Doi result exception:  %s' % status)
