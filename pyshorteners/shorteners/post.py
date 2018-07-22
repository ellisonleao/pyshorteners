from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    Po.st API
    apiKey needed
    """

    api_url = 'http://po.st/api/shorten'

    def short(self, url):
        url = self.clean_url(url)
        params = {'apiKey': self.api_key, 'longUrl': url, 'format': 'txt'}
        response = self._get(self.api_url, params=params)
        if not response.ok:
            raise ShorteningErrorException(response.content)

        return response.json()['short_url']
