"""
osdb.link shortener implementation
No config params needed
"""
import re

from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    api_url = 'http://osdb.link/'
    p = re.compile(r'(http:\/\/osdb.link\/[a-zA-Z0-9]+)')

    def _parse(self, response):
        """
        return parsed html
        """
        match = self.p.search(response)
        return match.group()

    def short(self, url):
        url = self.clean_url(url)
        response = self._post(self.api_url, data={'url': url})
        if response.ok:
            return self._parse(response.text)
        raise ShorteningErrorException(response.content)
