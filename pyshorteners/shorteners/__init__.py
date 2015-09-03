# encoding: utf-8
import logging

# flake8: noqa
from .base import BaseShortener
from .googl import GoogleShortener
from .bitly import BitlyShortener
from .tinyurl import TinyurlShortener
from .adfly import AdflyShortener
from .isgd import IsgdShortener
from .sentala import SentalaShortener
from .qrcx import QrCxShortener
from .owly import OwlyShortener
from .readability import ReadabilityShortener
from .awsm import AwsmShortener
from .osdb import OsdbShortener

from ..utils import is_valid_url
from ..exceptions import UnknownShortenerException

# Log Configs
logger = logging.getLogger('pyshorteners')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s -  %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


class Shortener(object):
    """
    Factory class for all Shorteners
    """

    def __init__(self, engine='BaseShortener', **kwargs):
        self.engine = engine
        self.kwargs = kwargs
        self.shorten = None
        self.expanded = None
        self.debug = kwargs.pop('debug', False)

        module = __import__('pyshorteners.shorteners')
        try:
            self._class = getattr(module.shorteners, self.engine)
        except AttributeError:
            raise UnknownShortenerException('Please enter a valid shortener.')

        for key, item in list(kwargs.items()):
            setattr(self, key, item)

    @property
    def api_url(self):
        return self._class.api_url

    def total_clicks(self, url=None):
        if self.debug:
            logger.info('total_clicks property called with url:'
                        ' {0}'.format(url))

        url = url or self.shorten
        if not url:
            raise TypeError('You need to pass an url or have an already '
                            'shortened one')

        if not is_valid_url(url):
            raise ValueError('Please enter a valid url')

        return self._class(**self.kwargs).total_clicks(url)

    def short(self, url):
        if self.debug:
            logger.info('Short method called with url: {0}'.format(url))

        if not is_valid_url(url):
            raise ValueError('Please enter a valid url')
        self.expanded = url

        if not self.kwargs.get('timeout'):
            self.kwargs['timeout'] = 0.5

        self.shorten = self._class(**self.kwargs).short(url)
        if self.debug:
            logger.info('Shorten url result: {0}'.format(self.shorten))
        return self.shorten

    def expand(self, url=None):
        if self.debug:
            logger.info('Expand method called with url: {0}'.format(url))

        if url and not is_valid_url(url):
            raise ValueError('Please enter a valid url')

        if url:
            if not self.kwargs.get('timeout'):
                self.kwargs['timeout'] = 0.5
            self.expanded = self._class(**self.kwargs).expand(url)
        if self.debug:
            logger.info('Expanded url result: {0}'.format(self.expanded))
        return self.expanded

    def qrcode(self, width=120, height=120):
        if not self.shorten:
            return None

        qrcode_url = ('http://chart.apis.google.com/chart?cht=qr&'
                      'chl={0}&chs={1}x{2}'.format(self.shorten, width,
                                                   height))
        return qrcode_url
