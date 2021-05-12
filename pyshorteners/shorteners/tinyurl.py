from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    TinyURL.com shortener implementation

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener()
        >>> s.tinyurl.short('http://www.google.com')
        'http://tinyurl.com/TEST'
        >>> s.tinyurl.expand('http://tinyurl.com/test')
        'http://www.google.com'
    """

    api_url = "http://tinyurl.com/api-create.php"

    def short(self, url, cleanUrl=True):
        """Short implementation for TinyURL.com

        Args:
            url: the URL you want to shorten
            cleanUrl: boolean to clean URL or not

        Returns:
            A string containing the shortened URL

        Raises:
            ShorteningErrorException: If the API returns an error as response
        """
        url = self.clean_url(url) if cleanUrl else url
        response = self._get(self.api_url, params=dict(url=url))
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException(response.content)
