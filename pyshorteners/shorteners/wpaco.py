# encoding: utf-8
"""
WP-A.co shortener implementation
No config params needed
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class WPACO(BaseShortener):
    api_url = 'http://wp-a.co/api/'

    def short(self, url):
        params = {
            'url': url,
            'method': 'http',
            'customshort': self.kwargs.get('customshort', '')
        }

        response = self._get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))
