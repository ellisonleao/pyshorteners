import json

from ..base import BaseShortener
from ..exceptions import BadAPIResponseException, ShorteningErrorException


class Shortener(BaseShortener):
    """ Yourls shortener implementation

    Args:
        api_url: URL of the yourls API endpoint (http://server/yourls-api.php)
        username: username
        password: password

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener(api_url='xxx', username='xxx',
        password='xxx')
        >>> s.yourls.short('http://www.google.com')
        'http://server/test'
        >>> s.yourls.expand('http://server/test')
        'http://www.google.com'
        >>> s.yourls.stats('http://server/test')
        '2'
    """

    def short(self, url, custom=None, title=None):
        """Short implementation for yourls
        Args:
            url: the URL you want to shorten
            custom: the desired shortened URL
            title: the title of this URL

        Returns:
            A string containing the shortened URL

        Raises:
            BadAPIResponseException: If the data is malformed or we got a bad
            status code on API response
            ShorteningErrorException: If the API Returns an error as response
        """

        payload = {
            'username': getattr(self, 'username', ''),
            'password': getattr(self, 'password', ''),
            'format': 'json',
            'action': 'shorturl',
            'url': url
        }

        if custom:
            payload['keyword'] = custom

        if title:
            payload['title'] = title

        # shorten
        response = self._post(self.api_url, data=payload)

        if response.ok:
            try:
                return json.loads(response.text)['shorturl']
            except (AttributeError, json.JSONDecodeError) as e:
                raise ShorteningErrorException(str(e))

        raise BadAPIResponseException(response.content)

    def expand(self, url):
        """Expand implementation for yourls
        Args:
            url: the URL you want to expand

        Returns:
            A string containing the expanded URL

        Raises:
            BadAPIResponseException: If the data is malformed or we got a bad
            status code on API response
            ShorteningErrorException: If the API Returns an error as response
        """
        payload = {
            'username': getattr(self, 'username', ''),
            'password': getattr(self, 'password', ''),
            'format': 'json',
            'action': 'expand',
            'shorturl': url
        }

        # expand
        response = self._post(self.api_url, data=payload)

        if response.ok:
            try:
                return json.loads(response.text)['longurl']
            except (KeyError, json.JSONDecodeError) as e:
                raise ShorteningErrorException(str(e))
        raise BadAPIResponseException(response.content)

    def total_clicks(self, url):
        """Total clicks implementation for yourls
        Args:
            url: the URL you want to get the total clicks count

        Returns:
            An int containing the total clicks count

        Raises:
            BadAPIResponseException: If the API Returns an error as response
        """

        payload = {
            'username': getattr(self, 'username', ''),
            'password': getattr(self, 'password', ''),
            'format': 'json',
            'action': 'url-stats',
            'shorturl': url
        }

        # total clicks
        response = self._post(self.api_url, data=payload)

        if response.ok:
            try:
                return int(json.loads(response.text)['click'])
            except (KeyError, json.JSONDecodeError, ValueError) as e:
                raise ShorteningErrorException(str(e))
        raise BadAPIResponseException(response.content)
