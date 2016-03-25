# encoding: utf-8
"""
Readbility url shortner api implementation
Located at: https://readability.com/developers/api/shortener
Doesnt' need anything from the app
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException, ExpandingErrorException


class Readability(BaseShortener):
    api_url = 'http://www.readability.com/api/shortener/v1/urls/'

    def short(self, url):
        params = {'url': url}
        response = self._post(self.api_url, data=params)
        if response.ok:
            try:
                data = response.json()
            except ValueError:
                raise ShorteningErrorException('There was an error shortening'
                                               ' this url - {0}'.format(
                                                   response.content))
            return data['meta']['rdd_url']
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))

    def expand(self, url):
        url_id = url.split('/')[-1]
        api_url = '{0}{1}'.format(self.api_url, url_id)
        response = self._get(api_url)
        if response.ok:
            try:
                data = response.json()
            except ValueError as e:
                raise ExpandingErrorException('There was an error expanding'
                                              ' this url - {0}'.format(e))
            return data['meta']['full_url']
        raise ExpandingErrorException('There was an error expanding'
                                      ' this url - {0}'.format(
                                          response.content))
