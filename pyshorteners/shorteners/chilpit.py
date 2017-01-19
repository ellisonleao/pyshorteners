# encoding: utf-8
"""
Chilp.it shortener implementation
No config params needed
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class Chilpit(BaseShortener):
    api_url = 'http://chilp.it/api.php'

    def short(self, url):
        params = {
            'url': url,
        }
        response = self._get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))
