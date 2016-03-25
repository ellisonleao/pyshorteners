# encoding: utf-8
"""
Googl Shortener Implementation
Needs a API_KEY
"""
import json

from ..exceptions import ShorteningErrorException, ExpandingErrorException
from .base import BaseShortener


class Google(BaseShortener):
    api_url = 'https://www.googleapis.com/urlshortener/v1/url'

    def __init__(self, **kwargs):
        if not kwargs.get('api_key', False):
            raise TypeError('api_key missing from kwargs')
        self.api_key = kwargs.get('api_key')
        super(Google, self).__init__(**kwargs)

    def short(self, url):
        params = json.dumps({'longUrl': url})
        headers = {'content-type': 'application/json'}
        url = '{0}?key={1}'.format(self.api_url, self.api_key)
        response = self._post(url, data=params, headers=headers)
        if response.ok:
            try:
                data = response.json()
            except ValueError as e:
                raise ShorteningErrorException('There was an error shortening'
                                               ' this url - {0}'.format(e))
            if 'id' in data:
                return data['id']
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))

    def expand(self, url):
        params = {'shortUrl': url}
        url = '{0}?key={1}'.format(self.api_url, self.api_key)
        response = self._get(url, params=params)

        if response.ok:
            try:
                data = response.json()
            except ValueError:
                raise ExpandingErrorException('There was an error expanding'
                                              ' this url - {0}'.format(
                                                  response.content))
            if 'longUrl' in data:
                return data['longUrl']
        raise ExpandingErrorException('There was an error expanding '
                                      'this url - {0}'.format(
                                          response.content))
