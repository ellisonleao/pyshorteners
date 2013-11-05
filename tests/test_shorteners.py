# coding: utf-8
import unittest

from pyshorteners import Shortener
from pyshorteners.utils import is_valid_url

class ShortenersTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://www.google.com'
        self.module = __import__('pyshorteners.shorteners')

    def test_shorteners_type(self):
        shorteners = ['GoogleShortener', 'BitlyShortener', 'TinyurlShortener',
                      'AdflyShortener']
        for shortener in shorteners:
            short = Shortener(shortener)
            self.assertEqual(type(short), short.__class__)

    def test_googl_short_function(self):
        engine = 'GoogleShortener'
        short = Shortener(engine)
        self.assertEqual(short.short('http://www.google.com'),
                         'http://goo.gl/fbsS')

    def test_googl_expand_function(self):
        engine = 'GoogleShortener'
        short = Shortener(engine)
        self.assertEqual(short.expand('http://goo.gl/fbsS'),
                         'http://www.google.com/')

    def test_tinyurl_short_function(self):
        engine = 'TinyurlShortener'
        short = Shortener(engine)
        self.assertEqual(short.short('http://www.google.com'),
                         'http://tinyurl.com/1c2')

    def test_tinyurl_expand_function(self):
        engine = 'TinyurlShortener'
        short = Shortener(engine)
        self.assertEqual(short.expand('http://tinyurl.com/ycus76'),
                         u'https://www.facebook.com')

    def test_adfly_short_function(self):
        engine = 'AdflyShortener'
        short = Shortener(engine)
        with self.assertRaises(ValueError):
            short.short('http://www.google.com')

    def test_adfly_expand_function(self):
        engine = 'AdflyShortener'
        short = Shortener(engine, key='abcd', uid='123')
        expand = short.expand('http://adf.ly/test')
        self.assertEqual(expand, 'http://adf.ly/test')

    def test_bitly_short_creation(self):
        engine = 'BitlyShortener'
        short = Shortener(engine)
        with self.assertRaises(ValueError):
            short.short('http://www.google.com')

    def test_wrong_shortener_engine(self):
        engine = 'UnknownShortener'
        with self.assertRaises(AttributeError):
            Shortener(engine)

    def test_is_valid_url(self):
        bad = 'ww.google.com'
        good = 'http://www.google.com'

        self.assertTrue(is_valid_url(good))
        self.assertFalse(is_valid_url(bad))

if __name__ == '__main__':
    unittest.main()
