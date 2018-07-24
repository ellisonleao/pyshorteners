import logging

from ..base import BaseShortener
from ..exceptions import (ShorteningErrorException, ExpandingErrorException,
                          BadAPIResponseException)

logger = logging.getLogger(__name__)


class Shortener(BaseShortener):
    """Bit.ly shortener Implementation

    Args:
        api_key: bit.ly API key

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener(api_key='YOUR_KEY')
        >>> s.bitly.short('http://www.google.com')
        'http://bit.ly/TEST'
        >>> s.bitly.expand('https://bit.ly/test')
        'http://www.google.com'
        >>> s.bitly.expand('https://bit.ly/test')
        10
    """
    api_url = 'https://api-ssl.bit.ly/'

    def short(self, url):
        """Short implementation for Bit.ly
        Args:
            url: the URL you want to shorten

        Returns:
            A string containing the shortened URL

        Raises:
            BadAPIResponseException: If the data is malformed or we got a bad
            status code on API response
            ShorteningErrorException: If the API Returns an error as response
        """

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
        """Expand implementation for Bit.ly
        Args:
            url: the URL you want to shorten

        Returns:
            A string containing the expanded URL

        Raises:
            ExpandingErrorException: If the API Returns an error as response
        """
        expand_url = f'{self.api_url}v3/expand'
        params = {
            'shortUrl': url,
            'access_token': self.api_key,
            'format': 'txt',
        }
        response = self._get(expand_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ExpandingErrorException(response.content)

    def total_clicks(self, url):
        """Total clicks implementation for Bit.ly
        Args:
            url: the URL you want to get the total clicks count

        Returns:
            An int containing the total clicks count

        Raises:
            BadAPIResponseException: If the API Returns an error as response
        """
        url = self.clean_url(url)
        clicks_url = f'{self.api_url}v3/link/clicks'
        params = {
            'link': url,
            'access_token': self.api_key,
            'format': 'txt'
        }
        response = self._get(clicks_url, params=params)
        if not response.ok:
            raise BadAPIResponseException(response.content)

        try:
            total_clicks = int(response.text)
        except (KeyError, TypeError) as e:
            logger.warning('Bad value from total_clicks response: %s', e)
            return 0

        return total_clicks
