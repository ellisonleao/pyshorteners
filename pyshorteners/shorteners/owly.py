# encoding: utf-8
"""
Ow.ly url shortner api implementation
Located at: http://ow.ly/api-docs
Doesnt' need anything from the app
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException, ExpandingErrorException


class Owly(BaseShortener):
    api_url = 'http://ow.ly/api/1.1/url/'

    def __init__(self, **kwargs):
        if not kwargs.get('api_key', False):
            raise TypeError('api_key is missing from kwargs')
        self.api_key = kwargs.get('api_key')
        super(Owly, self).__init__(**kwargs)

    def short(self, url):
        shorten_url = '{0}{1}'.format(self.api_url, 'shorten')
        data = {'apiKey': self.api_key, 'longUrl': url}
        response = self._get(shorten_url, params=data)
        if response.ok:
            try:
                data = response.json()
            except ValueError:
                raise ShorteningErrorException('There was an error shortening'
                                               ' this url')
            return data['results']['shortUrl']
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))

    def expand(self, url):
        expand_url = '{0}{1}'.format(self.api_url, 'expand')
        data = {'apiKey': self.api_key, 'shortUrl': url}
        response = self._get(expand_url, params=data)
        if response.ok:
            try:
                data = response.json()
            except ValueError:
                raise ExpandingErrorException('There was an error shortening'
                                              ' this url')
            return data['results']['longUrl']
        raise ExpandingErrorException('There was an error shortening this '
                                      'url - {0}'.format(response.content))
