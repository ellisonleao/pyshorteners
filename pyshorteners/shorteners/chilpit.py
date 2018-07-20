from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    Chilp.it shortener implementation
    No config params needed
    """
    api_url = 'http://chilp.it/api.php'

    def short(self, url):
        response = self._get(self.api_url, params={'url': url})
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException(response.content)
