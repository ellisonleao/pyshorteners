# encoding: utf-8
"""
da.gd url shortner api implementation
Located at: https://da.gd/
No config params needed
"""
from .base import BaseShortener
from ..exceptions import ShorteningErrorException, ExpandingErrorException


class Dagd(BaseShortener):
    api_url = 'https://da.gd/'

    def short(self, url):
        shorten_url = '{0}{1}'.format(self.api_url, 'shorten')
        data = {'url': url}
        response = self._get(shorten_url, params=data)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))

    def expand(self, url):
        # da.gd's coshorten expects only the shorturl identifier
        # (i.e. the "stuff" in http://da.gd/stuff), not the full short URL.
        sanitized_url = url.split('da.gd/', 1)[-1]
        expand_url = '{0}{1}/{2}'.format(
            self.api_url,
            'coshorten',
            sanitized_url)
        response = self._get(expand_url)
        if response.ok:
            return response.text.strip()
        raise ExpandingErrorException('There was an error expanding this '
                                      'url - {0}'.format(response.content))
