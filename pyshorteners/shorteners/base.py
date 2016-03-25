# encoding: utf-8

from abc import ABCMeta, abstractmethod

from ..exceptions import ExpandingErrorException


class BaseShortener(object):
    """
    Base class for all Shorteners
    """

    __metaclass__ = ABCMeta

    api_url = None

    def __init__(self, **kwargs):
        import requests
        self.kwargs = kwargs
        self.requests = requests

    def _get(self, url, params=None):
        response = self.requests.get(url, params=params,
                                     verify=self.kwargs.get('verify', True),
                                     timeout=self.kwargs['timeout'])
        return response

    def _post(self, url, data=None, params=None, headers=None):
        response = self.requests.post(url, data=data, params=params,
                                      headers=headers,
                                      verify=self.kwargs.get('verify', True),
                                      timeout=self.kwargs['timeout'])
        return response

    @abstractmethod
    def short(self, url):
        raise NotImplementedError

    def expand(self, url):
        response = self._get(url)
        if response.ok:
            return response.url
        raise ExpandingErrorException('There was an error expanding '
                                      'this url - {0}'.format(
                                          response.content))

    def total_clicks(self, url=None):
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, C):
        if cls is BaseShortener:
            if all(hasattr(C, name) for name in ('short', 'expand')):
                return True
        return NotImplemented


class Simple(BaseShortener):
    def short(self, url):
        return url
