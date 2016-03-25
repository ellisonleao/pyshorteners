# encoding: utf-8
"""
Adf.ly shortener implementation
Needs api key and uid
"""
from ..exceptions import ShorteningErrorException
from .base import BaseShortener


class Adfly(BaseShortener):
    api_url = 'http://api.adf.ly/api.php'

    def __init__(self, **kwargs):
        if not all([kwargs.get('key', False), kwargs.get('uid', False)]):
            raise TypeError('Please input the key and uid value')
        self.key = kwargs.get('key')
        self.uid = kwargs.get('uid')
        self.type = kwargs.get('type', 'int')
        super(Adfly, self).__init__(**kwargs)

    def short(self, url):
        data = {
            'domain': 'adf.ly',
            'advert_type': self.type,  # int or banner
            'key': self.key,
            'uid': self.uid,
            'url': url,
        }
        response = self._get(self.api_url, params=data)
        if response.ok:
            return response.text
        raise ShorteningErrorException('There was an error shortening this '
                                       'url - {0}'.format(response.content))
