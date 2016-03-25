"""
TinyURL.com shortener implementation
No config params needed
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class Tinyurl(BaseShortener):
    api_url = 'http://tinyurl.com/api-create.php'

    def short(self, url):
        response = self._get(self.api_url, params=dict(url=url))
        if response.ok:
            return response.text
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))
