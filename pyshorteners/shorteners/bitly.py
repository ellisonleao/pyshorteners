import logging

from .base import BaseShortener
from ..exceptions import (ShorteningErrorException, ExpandingErrorException,
                          BadAPIResponseException)

logger = logging.getLogger(__name__)


class Shortener(BaseShortener):
    """
    Bit.ly shortener Implementation
    needs on app.config:
    BITLY_TOKEN - Your bit.ly app access token
    How to get an access token: http://dev.bitly.com/authentication.html
    """
    api_url = 'https://api-ssl.bit.ly/'

    def short(self, url):
        self.clean_url(url)
        shorten_url = f'{self.api_url}v3/shorten'
        params = {
            'uri': url,
            'access_token': self.api_key,
            'format': 'txt',
        }
        response = self._get(shorten_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException(response.content)

    def expand(self, url):
        expand_url = f'{self.api_url}v3/expand'
        params = {
            'shortUrl': url,
            'access_toke': self.api_key,
            'format': 'txt',
        }
        response = self._get(expand_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ExpandingErrorException(response.content)

    def total_clicks(self, url):
        url = self.clean_url(url)
        clicks_url = f'{self.api_url}v3/link/clicks'
        params = {
            'link': url,
            'access_token': self.token,
            'format': 'txt'
        }
        response = self._get(clicks_url, params=params)
        if not response.ok:
            raise BadAPIResponseException(response.content)

        try:
            total_clicks = int(response.text)
        except (KeyError, ValueError) as e:
            logger.warning('Bad value from total_clicks response: %s', e)
            return 0

        return total_clicks
