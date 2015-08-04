# encoding: utf-8
"""
Bit.ly shortener Implementation
needs on app.config:
BITLY_LOGIN - Your bit.ly login user
BITLY_API_KEY - Your bit.ly api key
BITLY_TOKEN - Your bit.ly app access token
"""
from ..exceptions import ShorteningErrorException, ExpandingErrorException
from .base import BaseShortener


class BitlyShortener(BaseShortener):
    api_url = 'https://api-ssl.bit.ly/'

    def __init__(self, **kwargs):
        if not all([kwargs.get('bitly_login', False),
                    kwargs.get('bitly_token', False),
                    kwargs.get('bitly_api_key', False)]):
            raise TypeError('bitly_login, bitly_api_key and bitly_token '
                            'missing from kwargs')
        self.login = kwargs.get('bitly_login')
        self.api_key = kwargs.get('bitly_api_key')
        self.token = kwargs.get('bitly_token')

    def short(self, url):
        shorten_url = '{}{}'.format(self.api_url, 'v3/shorten')
        params = dict(
            uri=url,
            x_apiKey=self.api_key,
            x_login=self.login,
            access_token=self.token,
        )
        response = self._post(shorten_url, data=params)
        if response.ok:
            data = response.json()
            if 'status_code' in data and data['status_code'] == 200:
                return data['data']['url']
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
