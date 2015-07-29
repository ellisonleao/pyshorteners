# encoding: utf-8
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

from ..utils import is_valid_url
from ..exceptions import UnknownShortenerException


class Shortener(object):
    """
    Factory class for all Shorteners
    """

    def __init__(self, engine='BaseShortener', **kwargs):
        self.engine = engine
        self.kwargs = kwargs
        self.shorten = None
        self.expanded = None

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

    def short(self, url):
        if not is_valid_url(url):
            raise ValueError('Please enter a valid url')
        self.expanded = url

        self.shorten = self._class(**self.kwargs).short(url)
        return self.shorten

    def expand(self, url=None):
        if url and not is_valid_url(url):
            raise ValueError('Please enter a valid url')

        if url:
            self.expanded = self._class(**self.kwargs).expand(url)
        return self.expanded

    def qrcode(self, width=120, height=120):
        if not self.shorten:
            return None

        qrcode_url = ('http://chart.apis.google.com/chart?cht=qr&'
                      'chl={0}&chs={1}x{2}'.format(self.shorten, width,
                                                   height))
        return qrcode_url
