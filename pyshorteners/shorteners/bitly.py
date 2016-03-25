# encoding: utf-8
"""
Bit.ly shortener Implementation
needs on app.config:
BITLY_TOKEN - Your bit.ly app access token
How to get an access token: http://dev.bitly.com/authentication.html
"""
from ..exceptions import ShorteningErrorException, ExpandingErrorException
from .base import BaseShortener


class Bitly(BaseShortener):
    api_url = 'https://api-ssl.bit.ly/'

    def __init__(self, **kwargs):
        if not kwargs.get('bitly_token', False):
            raise TypeError('bitly_token missing from kwargs')
        self.token = kwargs.get('bitly_token')
        super(Bitly, self).__init__(**kwargs)

    def short(self, url):
        shorten_url = '{0}{1}'.format(self.api_url, 'v3/shorten')
        params = dict(
            uri=url,
            access_token=self.token,
            format='txt'
        )
        response = self._get(shorten_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))

    def expand(self, url):
        expand_url = '{0}{1}'.format(self.api_url, 'v3/expand')
        params = dict(
            shortUrl=url,
            access_token=self.token,
            format='txt'
        )
        response = self._get(expand_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ExpandingErrorException('There was an error expanding'
                                      ' this url - {0}'.format(
                                          response.content))

    def total_clicks(self, url=None):
        url = url or self.shorten
        total_clicks = 0
        clicks_url = '{0}{1}'.format(self.api_url, 'v3/link/clicks')
        params = dict(
            link=url,
            access_token=self.token,
            format='txt'
        )
        response = self._get(clicks_url, params=params)
        if response.ok:
            total_clicks = int(response.text)
        return total_clicks
