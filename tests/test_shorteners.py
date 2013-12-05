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

    def test_shorteners_type(self):
        shorteners = ['GoogleShortener', 'BitlyShortener', 'TinyurlShortener',
                      'AdflyShortener', 'DottkShortener', 'IsgdShortener']
        for shortener in shorteners:
            short = Shortener(shortener)
            self.assertEqual(type(short), short.__class__)

    def test_googl_shortener(self):
        engine = 'GoogleShortener'
        short = Shortener(engine)
        self.assertEqual(short.short('http://www.google.com'),
                         'http://goo.gl/fbsS')

        self.assertEqual(short.expand('http://goo.gl/fbsS'),
                         'http://www.google.com/')

        #test exceptions
        with self.assertRaises(ExpandingErrorException):
            short.expand('http://www.a.co')

    def test_tinyurl_shortener(self):
        engine = 'TinyurlShortener'
        short = Shortener(engine)
        self.assertEqual(short.short('http://www.google.com'),
                         'http://tinyurl.com/1c2')

        self.assertEqual(short.expand('http://tinyurl.com/ycus76'),
                         'https://www.facebook.com')

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

    def test_dottk_shortener(self):
        engine = 'DottkShortener'
        short = Shortener(engine)
        url = 'http://www.google.com/'

        short.short = MagicMock(return_value='http://3vzpu.tk')
        short.short(url)
        short.short.assert_called_with(url)

        expand = short.expand('http://adf.ly/test')
        self.assertEqual(expand, 'http://adf.ly/test')

    def test_isgd_shortener(self):
        engine = 'IsgdShortener'
        short = Shortener(engine)
        url = 'http://www.example.com'

        short.short = MagicMock(return_value='http://is.gd/MOgh5q')
        short.short(url)
        short.short.assert_called_with(url)

        expand = short.expand('http://is.gd/MOgh5q')
        self.assertEqual(expand, url)

    def test_wrong_shortener_engine(self):
        engine = 'UnknownShortener'
        with self.assertRaises(UnknownShortenerException):
            Shortener(engine)

    def test_is_valid_url(self):
        bad = 'ww.google.com'
        good = 'http://www.google.com'

        self.assertTrue(is_valid_url(good))
        self.assertFalse(is_valid_url(bad))

        s = Shortener('TinyurlShortener')
        with self.assertRaises(ValueError):
            url = 'http://12'
            s.short(url)
