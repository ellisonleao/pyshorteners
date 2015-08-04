# encoding: utf-8
from ..exceptions import ExpandingErrorException


class BaseShortener(object):
    """
    Base class for all Shorteners
    """
    api_url = None

    def _get(self, url, params=None):
        import requests
        response = requests.get(url, params=params)
        return response

    def _post(self, url, data=None, params=None, headers=None):
        import requests
        response = requests.post(url, data=data, params=params, headers=None)
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
