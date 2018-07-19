from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    WP-A.co shortener implementation
    No config params needed
    `customshort` param optional
    """
    api_url = 'http://wp-a.co/api/'

    def short(self, url):
        url = self.clean_url(url)
        params = {
            'url': url,
            'method': 'http',
            'customshort': getattr(self, 'customshort', '')
        }

        response = self._get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException(response.content)
