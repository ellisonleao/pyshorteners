# encoding: utf-8
"""
Aw.sm Shortener Implementation
Needs a API_KEY
Optional Params
`tool` - String
`channel` - 'twitter' 'facebook'. 'twitter' default value
"""
from ..exceptions import ShorteningErrorException
from .base import BaseShortener


class Awsm(BaseShortener):
    api_url = 'http://api.awe.sm/'

    def __init__(self, **kwargs):
        if not kwargs.get('api_key', False):
            raise TypeError('api_key missing from kwargs')
        self.api_key = kwargs.get('api_key')
        self.tool = kwargs.get('tool', Awsm._generate_random_tool())
        self.channel = kwargs.get('channel', 'twitter')
        super(Awsm, self).__init__(**kwargs)

    @staticmethod
    def _generate_random_tool():
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
            'v': 3,
            'url': url,
            'key': self.api_key,
            'tool': self.tool,
            'channel': self.channel
        }
        url = '{0}url.txt'.format(self.api_url)
        response = self._post(url, params=params)
        if response.ok:
            return response.text
        raise ShorteningErrorException('There was an error shortening '
                                       'this url - {0}'.format(
                                           response.content))
