import re

from ..base import BaseShortener
from ..exceptions import ShorteningErrorException


class Shortener(BaseShortener):
    """
    Soo.gd shortener implementation
    No config params needed
    Optional Params
    `suffix` - String
    """
    api_url = 'http://soo.gd/processreq.php'
    p = re.compile(r'(http:\/\/soo.gd\/[a-zA-Z0-9]+)')

    def _parse(self, response):
        match = self.p.search(response)
        return match.group()

    @staticmethod
    def _generate_random_suffix():
        import string
        import random
        try:
            letters = string.letters
        except AttributeError:
            letters = string.ascii_letters

        return ''.join(random.choice(letters + string.digits)
                       for _ in range(4))

    def short(self, url):
        url = self.clean_url(url)
        params = {
            'txt_url': url,
            'txt_name': getattr(self, 'suffix', self._generate_random_suffix)
        }
        response = self._post(self.api_url, data=params)
        if response.ok:
            return self._parse(response.text)
        raise ShorteningErrorException(response.content)
