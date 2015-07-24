# encoding: utf-8
from ..exceptions import ExpandingErrorException

import requests


class BaseShortener(object):
    """
    Base class for all Shorteners
    """
    api_url = None

    def short(self, url):
        return url

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        raise ExpandingErrorException('There was an error expanding '
                                      'this url - {0}'.format(
                                          response.content))
