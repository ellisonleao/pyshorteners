# encoding: utf-8
"""
Adf.ly shortener implementation
Needs api key and uid
"""
from ..exceptions import ShorteningErrorException
from ..base import BaseShortener


class Shortener(BaseShortener):
    api_url = 'http://api.adf.ly/api.php'

    def short(self, url):
        url = self.clean_url(url)
        data = {
            'domain': getattr(self, 'domain', 'adf.ly'),
            'advert_type': getattr(self, 'type', 'int'),  # int or banner
            'key': self.key,
            'uid': self.uid,
            'url': url,
        }
        response = self._get(self.api_url, params=data)
        if response.ok:
            return response.text
        raise ShorteningErrorException(response.content)
