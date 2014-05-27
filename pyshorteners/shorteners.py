# coding: utf-8
from __future__ import unicode_literals

import json

import requests

from .utils import is_valid_url
from .exceptions import (UnknownShortenerException, ShorteningErrorException,
                         ExpandingErrorException)

__all__ = ['Shortener', ]
module = __import__('pyshorteners.shorteners')


def show_current_apis():
    """
    Print on shell the current API's supported
    """
    return ['Goo.gl', 'Bit.ly', 'Ad.fly', 'Is.gd', 'Senta.la', 'Generic']


class Shortener(object):
    def __init__(self, engine, **kwargs):
        self.engine = engine
        self.kwargs = kwargs
        self.shorten = None
        self.expanded = None

        try:
            getattr(module.shorteners, self.engine)
        except AttributeError:
            raise UnknownShortenerException('Please enter a valid shortener.')

        for key, item in list(kwargs.items()):
            setattr(self, key, item)

    def short(self, url):
        if not is_valid_url(url):
            raise ValueError('Please enter a valid url')
        self.expanded = url

        # Get the right short function based on self.engine
        _class = getattr(module.shorteners, self.engine)
        self.shorten = _class(**self.kwargs).short(url)
        return self.shorten

    def expand(self, url=None):
        # Get the right short function based on self.engine
        _class = getattr(module.shorteners, self.engine)
        if url:
            self.expanded = _class(**self.kwargs).expand(url)
        return self.expanded

    def qrcode(self, width=120, height=120):
        if not self.shorten:
            return None

        qrcode_url = ('http://chart.apis.google.com/chart?cht=qr&'
                      'chl={}&chs={}x{}'.format(self.shorten, width,
                                                height))
        return qrcode_url


class GoogleShortener(object):
    """
    Based on:
    https://github.com/avelino/django-googl/blob/master/googl/short.py
    Googl Shortener Implementation
    Doesn't need anything from the app
    """
    api_url = "https://www.googleapis.com/urlshortener/v1/url"

    def short(self, url):
        params = json.dumps({'longUrl': url})
        headers = {'content-type': 'application/json'}
        response = requests.post(self.api_url, data=params,
                                 headers=headers)
        if response.ok:
            try:
                data = response.json()
            except ValueError:
                raise ShorteningErrorException("There was an error shortening"
                                               " this url")
            if 'id' in data:
                return data['id']
        raise ShorteningErrorException("There was an error shortening this "
                                       "url")

    def expand(self, url):
        params = {'shortUrl': url}
        response = requests.get(self.api_url, params=params)
        if response.ok:
            try:
                data = response.json()
            except ValueError:
                raise ExpandingErrorException("There was an error expanding"
                                              " this url")
            if 'longUrl' in data:
                return data['longUrl']
        raise ExpandingErrorException("There was an error expanding this url")


class BitlyShortener(object):
    """
    Bit.ly shortener Implementation
    needs on app.config:
    BITLY_LOGIN - Your bit.ly login user
    BITLY_API_KEY - Your bit.ly api key
    """
    shorten_url = 'http://api.bit.ly/shorten'
    expand_url = 'http://api.bit.ly/expand'

    def __init__(self, *args, **kwargs):
        if not all([kwargs.get('bitly_login', False),
                    kwargs.get('bitly_api_key', False)]):
            raise TypeError('bitly_login AND bitly_api_key missing from '
                            'kwargs')
        self.login = kwargs.get('bitly_login')
        self.api_key = kwargs.get('bitly_api_key')

    def short(self, url):
        params = dict(
            version="2.0.1",
            longUrl=url,
            login=self.login,
            apiKey=self.api_key,
        )
        response = requests.post(self.shorten_url, data=params)
        if response.ok:
            data = response.json()
            if 'statusCode' in data and data['statusCode'] == 'OK':
                return data['results'][self.url]['shortUrl']
        raise ShorteningErrorException("There was an error shortening this "
                                       "url")

    def expand(self, url):
        params = dict(
            version="2.0.1",
            shortUrl=url,
            login=self.login,
            apiKey=self.api_key,
        )
        response = requests.get(self.expand_url, params=params)
        if response.ok:
            data = response.json()
            if 'statusCode' in data and data['statusCode'] == 'OK':
                # get the hash key that contains the longUrl
                hash_key = list(data['results'].keys())[0]
                return data['results'][hash_key]['longUrl']
        raise ExpandingErrorException("There was an error expanding this url")


class TinyurlShortener(object):
    """
    TinyURL.com shortener implementation
    No config params needed
    """
    api_url = "http://tinyurl.com/api-create.php"

    def short(self, url):
        response = requests.get(self.api_url, params=dict(url=url))
        if response.ok:
            return response.text
        raise ShorteningErrorException("There was an error shortening this "
                                       "url")

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        raise ExpandingErrorException("There was an error expanding this url")


class AdflyShortener(object):
    """
    Adf.ly shortener implementation
    Needs api key and uid
    """
    api_url = 'http://api.adf.ly/api.php'

    def __init__(self, *args, **kwargs):
        if not all([kwargs.get('key', False), kwargs.get('uid', False)]):
            raise TypeError('Please input the key and uid value')
        self.key = kwargs.get('key')
        self.uid = kwargs.get('uid')
        self.type = kwargs.get('type', 'int')

    def short(self, url):
        data = {
            'domain': 'adf.ly',
            'advert_type': self.type,  # int or banner
            'key': self.key,
            'uid': self.uid,
            'url': url,
        }
        response = requests.get(self.api_url, params=data)
        if response.ok:
            return response.text
        raise ShorteningErrorException("There was an error shortening this "
                                       "url")

    def expand(self, url):
        """
        No expand for now
        """
        return url


class IsgdShortener(object):
    """
    Is.gd shortener implementation
    No config params needed
    """
    api_url = "http://is.gd/create.php"

    def short(self, url):
        params = {
            'format': 'simple',
            'url': url,
        }
        response = requests.get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException("There was an error shortening this "
                                       "url")

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        raise ExpandingErrorException("There was an error expanding this url")


class SentalaShortener(object):
    """
    Senta.la shortener implementation
    No config params needed
    """
    api_url = "http://senta.la/api.php"

    def short(self, url):
        params = {
            'dever': 'encurtar',
            'format': 'simple',
            'url': url,
        }
        response = requests.get(self.api_url, params=params)
        if response.ok:
            return response.text.strip()
        raise ShorteningErrorException("There was an error shortening this "
                                       "url")

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        raise ExpandingErrorException("There was an error expanding this url")

"""
Adding this generic expander, it doesn't shorten url's, just tries to retrieve
URL's using a get http method
"""


class GenericExpander(object):
    def short(self, url):
        raise NotImplementedError("This class doesn't support shortening")

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        raise ExpandingErrorException("There was an error expanding this url")
