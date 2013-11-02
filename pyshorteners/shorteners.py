# coding: utf-8
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
            raise AttributeError(u'Please enter a valid shortener.')

        for key, item in kwargs.iteritems():
            setattr(self, key, item)

    def short(self, url):
        if isinstance(url, unicode):
            url = url.encode('utf-8')

        if not is_valid_url(url):
            raise ValueError(u'Please enter a valid url')

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
                return u''
            if 'id' in data:
                self.shorten = data['id']
                return data['id']
        return u''

    def expand(self, url):
        params = {'shortUrl': url}
        response = requests.get(self.api_url, params=params)
        if response.ok:
            try:
                data = response.json()
            except:
                return u''
            if 'longUrl' in data:
                return data['longUrl']
        return u''


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
            raise ValueError(u'bitly_login AND bitly_api_key missing from '
                             u'kwargs')
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
        return u''

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
                hash_key = data['results'].keys()[0]
                return data['results'][hash_key]['longUrl']
        return u''


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
        return u''

    def expand(self, url):
        response = requests.get(url)
        if response.ok:
            return response.url
        return u''


class AdflyShortener(object):
    """
    Adf.ly shortener implementation
    Needs api key and uid
    """
    api_url = 'http://api.adf.ly/api.php'

    def __init__(self, *args, **kwargs):
        if not all([kwargs.get('key'), kwargs.get('uid')]):
            raise ValueError(u'Please input the key and uid value')
        self.key = kwargs.get('key')
        self.uid = kwargs.get('uid')

    def short(self, url):
        data = {
            'domain': 'adf.ly',
            'advert_type': 'int',  # int or banner
            'key': self.key,
            'uid': self.uid,
        }
        response = requests.get(self.api_url, params=data)
        if response.ok:
            print response.json()

        return u''

    def expand(self, url):
        """
        No expand for now
        """
        return url
