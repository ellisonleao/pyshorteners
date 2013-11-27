# coding: utf-8
from __future__ import unicode_literals

import json

import requests

from .utils import is_valid_url

__all__ = ['Shortener', ]


class Shortener(object):
    def __init__(self, engine, **kwargs):
        self.engine = engine
        self.kwargs = kwargs
        self.module = __import__('pyshorteners.shorteners')

        try:
            getattr(self.module.shorteners, self.engine)
        except AttributeError:
            raise AttributeError('Please enter a valid shortener.')

        for key, item in list(kwargs.items()):
            setattr(self, key, item)

    def short(self, url):
        if not is_valid_url(url):
            raise ValueError('Please enter a valid url')

        # Get the right short function based on self.engine
        _class = getattr(self.module.shorteners, self.engine)
        return _class(**self.kwargs).short(url)

    def expand(self, url):
        # Get the right short function based on self.engine
        _class = getattr(self.module.shorteners, self.engine)
        return _class(**self.kwargs).expand(url)


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
            except:
                return ''
            if 'id' in data:
                self.shorten = data['id']
                return data['id']
        return ''

    def expand(self, url):
        params = {'shortUrl': url}
        response = requests.get(self.api_url, params=params)
        if response.ok:
            try:
                data = response.json()
            except:
                return ''
            if 'longUrl' in data:
                return data['longUrl']
        return ''


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
        if not all([kwargs.get('bitly_login'), kwargs.get('bitly_api_key')]):
            raise ValueError('bitly_login AND bitly_api_key missing from '
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
                key = self.url
                return data['results'][key]['shortUrl']
        return ''

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
        return ''


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
        return ''

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        return ''


class AdflyShortener(object):
    """
    Adf.ly shortener implementation
    Needs api key and uid
    """
    api_url = 'http://api.adf.ly/api.php'

    def __init__(self, *args, **kwargs):
        if not all([kwargs.get('key'), kwargs.get('uid')]):
            raise ValueError('Please input the key and uid value')
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

        return ''

    def expand(self, url):
        """
        No expand for now
        """
        return url


class DottkShortener(object):
    """
    Dot.Tk shortener implementation
    No config params needed
    """
    api_url = "http://api.dot.tk/tweak/shorten"

    def short(self, url):
        params = {
            'long': url
        }
        response = requests.get(self.api_url, params=params)
        if response.ok:
            urls = response.text.strip().split('\n')
            if len(urls) > 0:
                return urls[0]
        return ''

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        return ''
