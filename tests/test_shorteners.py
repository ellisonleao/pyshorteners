# coding: utf-8
from __future__ import unicode_literals

import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from pyshorteners import Shortener
from pyshorteners.utils import is_valid_url
from pyshorteners.exceptions import (UnknownShortenerException,
                                     ExpandingErrorException)


class ShortenersTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://www.google.com'
        self.module = __import__('pyshorteners.shorteners')
        self.test_url = 'http://www.pilgrims.com'

    def test_shorteners_type(self):
        shorteners = ['GoogleShortener', 'BitlyShortener', 'TinyurlShortener',
                      'AdflyShortener', 'IsgdShortener', 'SentalaShortener']
        for shortener in shorteners:
            short = Shortener(shortener)
            self.assertEqual(type(short), short.__class__)

    def test_googl_shortener(self):
        engine = 'GoogleShortener'
        short = Shortener(engine)
        url = 'http://goo.gl/rjf0oI'
        shorten = short.short(self.test_url)
        self.assertEqual(shorten, url)

        self.assertEqual(short.expand(), self.test_url)
        self.assertEqual(short.expanded, self.test_url)

        self.assertEqual(short.shorten, url)
        self.assertEqual(short.qrcode(), 'http://chart.apis.google.com/'
                         'chart?cht=qr&chl={}&chs=120x120'.format(shorten))

        #test exceptions
        with self.assertRaises(ExpandingErrorException):
            short.expand('http://www.a.co')

    def test_tinyurl_shortener(self):
        engine = 'TinyurlShortener'
        short = Shortener(engine)
        url = 'http://tinyurl.com/nc9m936'
        shorten = short.short(self.test_url)
        self.assertEqual(shorten, url)

        self.assertEqual(short.expand(), self.test_url)
        self.assertEqual(short.expand(url), self.test_url)

        self.assertEqual(short.expanded, self.test_url)
        self.assertEqual(short.shorten, url)
        self.assertEqual(short.qrcode(), 'http://chart.apis.google.com/'
                         'chart?cht=qr&chl={}&chs=120x120'.format(shorten))

    def test_adfly_shortener(self):
        engine = 'AdflyShortener'
        short = Shortener(engine, key='abcd', uid='123')
        url = 'http://www.google.com/'

        short.short = MagicMock(return_value='http://adf.ly/test')
        short.short(url)
        short.short.assert_called_with(url)

        expand = short.expand('http://adf.ly/test')
        self.assertEqual(expand, 'http://adf.ly/test')

    def test_bitly_shortener(self):
        engine = 'BitlyShortener'
        short = Shortener(engine, bitly_api_key='abc', bitly_login='123x')
        url = 'http://www.google.com/'
        short_url = 'http://bit.ly/xxx'
        short.short = MagicMock(return_value='http://bit.ly/SsdA')
        short.short(url)
        short.short.assert_called_with(url)

        #expanding
        short.expand = MagicMock(return_value=url)
        short.expand(short_url)
        short.expand.assert_called_with(short_url)

    def test_isgd_shortener(self):
        engine = 'IsgdShortener'
        short = Shortener(engine)
        url = 'http://www.pilgrims.com'

        shorten = short.short(url)
        expand = short.expand(shorten)
        self.assertEqual(expand, url)
        self.assertEqual(short.qrcode(), 'http://chart.apis.google.com/'
                         'chart?cht=qr&chl={}&chs=120x120'.format(shorten))

    def test_sentala_shortener(self):
        engine = 'SentalaShortener'
        short = Shortener(engine)
        url = 'http://www.pilgrims.com'

        shorten = short.short(url)
        expand = short.expand(shorten)
        self.assertEqual(expand, url)
        self.assertEqual(short.qrcode(), 'http://chart.apis.google.com/'
                         'chart?cht=qr&chl={}&chs=120x120'.format(shorten))

    def test_wrong_shortener_engine(self):
        engine = 'UnknownShortener'
        with self.assertRaises(UnknownShortenerException):
            Shortener(engine)

    def test_is_valid_url(self):
        bad = 'www.google.com'
        good = 'http://www.google.com'

        self.assertTrue(is_valid_url(good))
        self.assertFalse(is_valid_url(bad))

        s = Shortener('TinyurlShortener')
        with self.assertRaises(ValueError):
            url = 'http://12'
            s.short(url)
