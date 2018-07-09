# encoding: utf-8
"""
Soo.gd shortener implementation
No config params needed
Optional Params
`suffix` - String
"""
import re

from .base import BaseShortener
from ..exceptions import ShorteningErrorException


class Soogd(BaseShortener):
    api_url = 'http://soo.gd/processreq.php'
    p = re.compile(r'(http:\/\/soo.gd\/[a-zA-Z0-9]+)')

    def __init__(self, **kwargs):
        self.suffix = kwargs.get('suffix', Soogd._generate_random_suffix())
        super(Soogd, self).__init__(**kwargs)

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
        params = {
            'txt_url': url,
            'txt_name': self.suffix,
        }
        response = self._post(self.api_url, data=params)
        if response.ok:
            return self._parse(response.text)
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))
