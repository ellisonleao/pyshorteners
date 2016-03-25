# encoding: utf-8
"""
Is.gd shortener implementation
No config params needed
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class Isgd(BaseShortener):
    api_url = 'http://is.gd/create.php'

    def short(self, url):
        params = {
            'format': 'simple',
            'url': url,
        }
        response = self._get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))
