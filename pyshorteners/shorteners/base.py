import requests
import re

from ..exceptions import BadURLException, ExpandingErrorException

URL_RE = re.compile(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.]'
                    r'[a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)'
                    r'))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()'
                    r'\[\]{};:\'".,<>?«»“”‘’]))')


class BaseShortener:

    def __init__(self, **kwargs):
        for key, item in list(kwargs.items()):
            setattr(self, key, item)

    def _get(self, url, params=None, headers=None):
        url = self.clean_url(url)
        response = requests.get(url, params=params, verify=self.verify,
                                timeout=self.timeout, headers=headers)
        return response

    def _post(self, url, data=None, json=None, params=None, headers=None):
        url = self.clean_url(url)
        response = requests.post(url, data=data, json=json, params=params,
                                 headers=headers, timeout=self.timeout,
                                 verify=self.verify)
        return response

    def short(self, url):
        raise NotImplementedError

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        raise ExpandingErrorException

    @staticmethod
    def clean_url(url):
        if not url.startswith(('http://', 'https://')):
            url = f'http://{url}'

        if not URL_RE.match(url):
            raise BadURLException(f'{url} is not valid')

        return url
