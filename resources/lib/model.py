import sys
try:
    from urlparse import parse_qs
    from urllib import unquote_plus
except ImportError:
    from urllib.parse import parse_qs, unquote_plus
import xbmc
import xbmcaddon
import os
import xbmcvfs

def parse(argv):
    """Decode arguments
    """
    if (argv[2]):
        return Args(argv, parse_qs(argv[2][1:]))
    else:
        return Args(argv, {})


class Args(object):
    """Arguments class
    Hold all arguments passed to the script and also persistent user data and
    reference to the addon. It is intended to hold all data necessary for the
    script.
    """
    def __init__(self, argv, kwargs):
        """Initialize arguments object
        Hold also references to the addon which can't be kept at module level.
        """
        self.PY2        = sys.version_info[0] == 2 #: True for Python 2
        self._argv      = argv
        self._addonid   = self._argv[0][9:-1]
        self._addon     = xbmcaddon.Addon(id=self._addonid)
        self._addonname = self._addon.getAddonInfo("name")
        self._cj        = None
        self._crsftoken = ""
        self._cookie = ""
        self._baseUrl  = "https://www.anime-on-demand.de"

        for key, value in kwargs.items():
            if value:
                setattr(self, key, unquote_plus(value[0]))

    def set_crsftoken(self, x):
        self._crsftoken  = x
    
    def set_cookie(self, x):
        self._cookie = x  

class Stream(object):         
    def __init__(self, _bandwidth, avarge_bandwith ):
        """Initialize arguments object
        Hold also references to the addon which can't be kept at module level.
        """
        self.PY2        = sys.version_info[0] == 2 #: True for Python 2
        self._bandwidth = 0
        self.avarge_bandwith  = 0
