from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    Is.gd shortener implementation
    No config params needed
    """
    api_url = 'https://is.gd/create.php'

    def short(self, url):
        url = self.clean_url(url)
        params = {
            'format': 'simple',
            'url': url,
        }
        response = self._get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException(response.content)
