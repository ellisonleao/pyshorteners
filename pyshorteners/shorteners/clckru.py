from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    Clck.ru shortener implementation

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener()
        >>> s.clckru.short('http://www.google.com')
        'http://clck.ru/TEST'
        >>> s.clckru.expand('http://clck.ru/TEST')
        'http://www.google.com'

    """

    api_url = "https://clck.ru/--"

    def short(self, url, clean_url=True):
        """Short implementation for Clck.ru

        Args:
            url: the URL you want to shorten

        Returns:
            A string containing the shortened URL

        Raises:
            ShorteningErrorException: If the API returns an error as response
        """

        url = self.clean_url(url, clean_url)
        response = self._get(self.api_url, params={"url": url})
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException(response.content)
