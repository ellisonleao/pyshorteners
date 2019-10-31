"""Short.cm shortner Implementation
"""

import re

from ..base import BaseShortener
from ..exceptions import (
    ShorteningErrorException,
    ExpandingErrorException,
    BadURLException,
)


class Shortener(BaseShortener):
    """Short.cm shortener Implementation

    Args:
        api_key: short.cm API key
        domain: which registered domain to create the link on

    Example:

        >>> import pyshorteners
        >>> s = pyshorteners.Shortener(api_key='YOUR_KEY')
        >>> s.shortcm.short('http://www.google.com')
        'http://short.cm/TEST'
        >>> s.shortcm.expand('https://short.cm/test')
        'http://www.google.com'
        >>> s.shortcm.expand('https://short.cm/test')
        10
"""

    api_url = "https://api.short.cm/links/"
    domain = ""
    api_key = ""

    def short(self, url):
        """Short implementation for Short.cm
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
        json = {"originalURL": url, "domain": self.domain}
        headers = {"authorization": self.api_key}
        response = self._post(self.api_url, json=json, headers=headers)
        if response.ok:
            data = response.json()
            if "shortURL" not in data:
                raise ShorteningErrorException(
                    f"API Returned wrong response: " f"{data}"
                )
            return data["shortURL"]
        raise ShorteningErrorException(response.content)

    def expand(self, url):
        """Expand implementation for Short.cm
        Args:
            url: the short URL you want to expand

        Returns:
            A string containing the expanded URL

        Raises:
            ExpandingErrorException: If the API Returns an error as response
        """
        expand_url = f"{self.api_url}expand"

        # split domain and path
        url_parser = re.compile("(https?://)([^/]*)/([^/?]*)")
        match = url_parser.match(url)
        if match is None:
            raise BadURLException(f"{url}")
        groups = url_parser.match(url).groups()

        if len(groups) != 3:
            raise BadURLException(f"{url}")

        params = {"domain": groups[1], "path": groups[2]}
        headers = {"authorization": self.api_key}
        response = self._get(expand_url, params=params, headers=headers)
        if response.ok:
            data = response.json()
            if "originalURL" not in data:
                raise ShorteningErrorException(
                    f"API Returned wrong response: " f"{data}"
                )
            return data["originalURL"]
        raise ExpandingErrorException(response.content)
