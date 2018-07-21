from ..base import BaseShortener
from ..exceptions import ShorteningErrorException, ExpandingErrorException


class Shortener(BaseShortener):
    """
    da.gd url shortner api implementation
    Located at: https://da.gd/
    No config params needed
    """
    api_url = 'https://da.gd/'

    def short(self, url):
        url = self.clean_url(url)
        shorten_url = f'{self.api_url}shorten'
        response = self._get(shorten_url, params={'url': url})
        if not response.ok:
            raise ShorteningErrorException(response.content)
        return response.text.strip()

    def expand(self, url):
        url = self.clean_url(url)
        # da.gd's coshorten expects only the shorturl identifier
        # (i.e. the "stuff" in http://da.gd/stuff), not the full short URL.
        sanitized_url = url.split('da.gd/', 1)[-1]
        expand_url = f'{self.api_url}coshortern/{sanitized_url}'
        response = self._get(expand_url)
        if not response.ok:
            raise ExpandingErrorException(response.content)
        return response.text.strip()
