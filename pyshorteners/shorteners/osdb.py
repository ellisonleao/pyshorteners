import re

from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    Os.db shortener implementation

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener()
        >>> s.osdb.short('http://www.google.com')
        'https://osdb.link/TEST'
        >>> s.osdb.expand('http://osdb.link/TEST')
        'https://www.google.com'
    """

    api_url = "http://osdb.link/"
    p = re.compile(r"(http:\/\/osdb.link\/[a-zA-Z0-9]+)")

    def short(self, url):
        """Short implementation for Os.db

        Args:
            url: the URL you want to shorten

        Returns:
            A string containing the shortened URL

        Raises:
            ShorteningErrorException: If the API returns an error as response
        """
        url = self.clean_url(url)
        response = self._post(self.api_url, data={"url": url})
        if not response.ok:
            raise ShorteningErrorException(response.content)
        match = self.p.search(response.text)
        return match.group()
