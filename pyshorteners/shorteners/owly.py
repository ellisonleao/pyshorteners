import json

from ..base import BaseShortener
from ..exceptions import (ShorteningErrorException, ExpandingErrorException,
                          BadAPIResponseException)


class Shortener(BaseShortener):
    """
    Ow.ly url shortner api implementation
    Located at: http://ow.ly/api-docs
    Doesnt' need anything from the app
    """
    api_url = 'http://ow.ly/api/1.1/url/'

    def short(self, url):
        url = self.clean_url(url)
        shorten_url = f'{self.api_url}shorten'
        params = {'apiKey': self.api_key, 'longUrl': url}
        response = self._get(shorten_url, params=params)
        if not response.ok:
            raise ShorteningErrorException(response.content)

        data = response.json()
        if 'results' not in data:
            raise ShorteningErrorException(f'API Returned wrong response: '
                                           f'{data}')

        return data['results']['shortUrl']

    def expand(self, url):
        url = self.clean_url(url)
        expand_url = f'{self.api_url}expand'
        data = {'apiKey': self.api_key, 'shortUrl': url}
        response = self._get(expand_url, params=data)
        if not response.ok:
            raise ExpandingErrorException(response.content)

        data = response.json()
        if 'results' not in data:
            raise ExpandingErrorException(f'API Returned wrong response: '
                                          f'{data}')

        return data['results']['longUrl']
