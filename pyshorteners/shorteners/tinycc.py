from ..exceptions import ShorteningErrorException, ExpandingErrorException
from .base import BaseShortener


class Tinycc(BaseShortener):
    api_url = 'http://tiny.cc/'

    def __init__(self, **kwargs):
        if not kwargs.get('tinycc_api_key', False):
            raise TypeError('tinycc_api_key missing from kwargs')
        if not kwargs.get('tinycc_login', False):
            raise TypeError('tinycc login missing from kwargs')
        self.api_key = kwargs.get('tinycc_api_key')
        self.login = kwargs.get('tinycc_login')
        self.response_format = 'json'
        self.api_version = '2.0.3'
        self.params = {
            'c': 'rest_api',
            'version': self.api_version,
            'format': self.response_format,
            'login': self.login,
            'apiKey': self.api_key
        }
        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (X11; Ubuntu; Linux) Gecko/20100101 Firefox/59.0'
        }
        super(Tinycc, self).__init__(**kwargs)

    def short(self, url):
        params = self.params.copy()
        params.update({
            'm': 'shorten',
            'longUrl': url,
        })
        response = self._get(self.api_url, params=params, headers=self.headers)
        if response.ok:
            data = response.json()
            return data['results']['short_url']
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))

    def expand(self, url):
        params = self.params.copy()
        params.update({
            'm': 'expand',
            'shortUrl': url,
        })
        response = self._get(self.api_url, params=params, headers=self.headers)
        if response.ok:
            data = response.json()
            return data['results']['long_url']
        raise ExpandingErrorException('There was an error expanding'
                                      ' this url - {0}'.format(
                                          response.content))

    def total_clicks(self, url=None):
        params = self.params.copy()
        params.update({
            'm': 'total_visits',
            'shortUrl': url,
        })
        response = self._get(self.api_url, params=params, headers=self.headers)
        total_clicks = 0
        if response.ok:
            data = response.json()
            try:
                total_clicks = int(data['results']['clicks'])
            except KeyError:
                return total_clicks
        return total_clicks

    def qrcode(self, width=120, height=120, shorten=None):
        if shorten:
            return "{}/qr".format(shorten)
