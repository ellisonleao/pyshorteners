# encoding: utf-8
"""
Qr.cx shortener implementation
No config params needed
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class QrCx(BaseShortener):
    api_url = 'http://qr.cx/api/'

    def short(self, url):
        params = {
            'longurl': url,
        }
        response = self._get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException('There was an error shortening this '
                                       'url')
