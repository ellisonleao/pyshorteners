# encoding: utf-8
"""
Senta.la shortener implementation
No config params needed
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class Sentala(BaseShortener):
    api_url = 'http://senta.la/api.php'

    def short(self, url):
        params = {
            'dever': 'encurtar',
            'format': 'simple',
            'url': url,
        }
        response = self._get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))
