"""
osdb.link shortener implementation
No config params needed
"""
import re

from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class Osdb(BaseShortener):
    api_url = 'http://osdb.link/'
    p = re.compile(r'(http:\/\/osdb.link\/[a-zA-Z0-9]+)')

    def _parse(self, response):
        """
        return parsed html
        """
        match = self.p.search(response)
        return match.group()

    def short(self, url):
        response = self._post(self.api_url, data=dict(url=url))
        if response.ok:
            return self._parse(response.text)
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))
