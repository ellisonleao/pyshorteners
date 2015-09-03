# encoding: utf-8
from ..exceptions import ExpandingErrorException


class BaseShortener(object):
    """
    Base class for all Shorteners
    """
    api_url = None

    def __init__(self, **kwargs):
        import requests
        self.kwargs = kwargs
        self.requests = requests

    def _get(self, url, params=None):
        response = self.requests.get(url, params=params,
                                     timeout=self.kwargs['timeout'])
        return response

    def _post(self, url, data=None, params=None, headers=None):
        response = self.requests.post(url, data=data, params=params,
                                      headers=None,
                                      timeout=self.kwargs['timeout'])
        return response

    def short(self, url):
        return url

    def expand(self, url):
        response = self._get(url)
        if response.ok:
            return response.url
        raise ExpandingErrorException('There was an error expanding '
                                      'this url - {0}'.format(
                                          response.content))

    def total_clicks(self, url=None):
        raise NotImplementedError()
