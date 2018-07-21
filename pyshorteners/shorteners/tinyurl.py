from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    TinyURL.com shortener implementation
    No config params needed
    """
    api_url = 'http://tinyurl.com/api-create.php'

    def short(self, url):
        url = self.clean_url(url)
        response = self._get(self.api_url, params=dict(url=url))
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException(response.content)
