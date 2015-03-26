# coding: utf-8
from __future__ import unicode_literals

import unittest
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from pyshorteners.shorteners import Shortener, show_current_apis
from pyshorteners.utils import is_valid_url
from pyshorteners.exceptions import (UnknownShortenerException,
                                     ShorteningErrorException,
                                     ExpandingErrorException)


class ShortenersTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://www.google.com'
        self.module = __import__('pyshorteners.shorteners')
        self.test_url = 'http://www.pilgrims.com'

    def test_shorteners_type(self):
        shorteners = ['GoogleShortener', 'BitlyShortener', 'TinyurlShortener',
                      'AdflyShortener', 'IsgdShortener', 'SentalaShortener',
                      'GenericExpander', 'OwlyShortener']
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

        # test exceptions
        with self.assertRaises(ExpandingErrorException):
            short.expand('http://www.a.co')

    def test_readability_shortener(self):
        engine = 'ReadabilityShortener'
        short = Shortener(engine)
        url = 'http://blog.arc90.com/2010/11/30/silence-is-golden/'
        short_url = 'http://rdd.me/tg8if9uj'
        readbility_url = 'http://readability.com/articles/tg8if9uj'
        shorten = short.short(url)
        self.assertEqual(shorten, short_url)

        expand = short.expand(shorten)
        self.assertEqual(expand, readbility_url)

        # Test wrong url_id
        short = Shortener(engine)
        with self.assertRaises(ExpandingErrorException):
            expand = short.expand('http://www.wqe.cc')

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

        # test with no key params
        with self.assertRaises(TypeError):
            short = Shortener(engine).short('http://www.google.com')

    def test_bitly_shortener(self):
        engine = 'BitlyShortener'
        short = Shortener(engine, bitly_api_key='abc', bitly_login='123x')
        url = 'http://www.google.com/'
        short_url = 'http://bit.ly/xxx'

        # test with no mock
        with self.assertRaises(ShorteningErrorException):
            short = short.short(url)

        # mocking the results
        short.expand = MagicMock(return_value=url)
        short.short = MagicMock(return_value='http://bit.ly/SsdA')

        short.short(url)
        short.short.assert_called_with(url)
        short.expand(short_url)
        short.expand.assert_called_with(short_url)

        # test with no key params
        with self.assertRaises(TypeError):
            short = Shortener(engine).short('http://www.google.com')

    def test_owly_shortener(self):
        engine = 'OwlyShortener'
        short = Shortener(engine, api_key='abc')
        url = 'http://www.google.com/'
        short_url = 'http://ow.ly/xxx'

        # test with no mock
        with self.assertRaises(ShorteningErrorException):
            short = short.short(url)

        # mocking
        short.short = MagicMock(return_value='http://ow.ly/SsdA')
        short.expand = MagicMock(return_value=url)

        short.short(url)
        short.short.assert_called_with(url)

        short.expand(short_url)
        short.expand.assert_called_with(short_url)

        # test with no key params
        with self.assertRaises(TypeError):
            short = Shortener(engine).short('http://www.google.com')

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

    def test_qrcx_shortener(self):
        engine = 'QrCxShortener'
        short = Shortener(engine)
        url = 'https://www.facebook.com/'

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

    def test_generic_expander(self):
        # testing new generic expander. Uses another shortener to test
        short = Shortener("TinyurlShortener")
        shorten = short.short(self.test_url)

        engine = "GenericExpander"
        expander = Shortener(engine)

        with self.assertRaises(NotImplementedError):
            expander.short('http://www.test.com')

        result_url = expander.expand(shorten)
        # A valid url result is enough for answer
        self.assertEqual(result_url, self.test_url)

    def test_show_current_apis(self):
        apis = ['Goo.gl', 'Bit.ly', 'Ad.fly', 'Is.gd', 'Senta.la',
                'Generic', 'QrCx', 'Ow.ly']
        self.assertEqual(show_current_apis(), apis)

    def test_none_qrcode(self):
        shortener = Shortener('TinyurlShortener')
        self.assertIsNone(shortener.qrcode())

