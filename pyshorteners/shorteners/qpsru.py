from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    Qps.ru shortener implementation
    No config params needed
    """
    api_url = 'http://qps.ru/api'

    def short(self, url):
        url = self.clean_url(url)
        response = self._get(self.api_url, params={'url': url})
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException(response.content)
