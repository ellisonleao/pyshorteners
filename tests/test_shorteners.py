# coding: utf-8
from __future__ import unicode_literals

from pyshorteners.utils import is_valid_url
from pyshorteners.shorteners import Shortener
from pyshorteners.exceptions import UnknownShortenerException

import pytest


url = 'http://www.google.com'
module = __import__('pyshorteners.shorteners')
test_url = 'http://www.pilgrims.com'


def test_shorteners_type():
    shorteners = ['GoogleShortener', 'BitlyShortener', 'TinyurlShortener',
                  'AdflyShortener', 'IsgdShortener', 'SentalaShortener',
                  'OwlyShortener']
    for shortener in shorteners:
        short = Shortener(shortener)
        assert type(short) == short.__class__


def test_wrong_shortener_engine():
    engine = 'UnknownShortener'
    with pytest.raises(UnknownShortenerException):
        Shortener(engine)


def test_is_valid_url():
    bad = 'www.google.com'
    good = 'http://www.google.com'

    assert is_valid_url(good)
    assert not is_valid_url(bad)

    s = Shortener('TinyurlShortener')
    with pytest.raises(ValueError):
        url = 'http://12'
        s.short(url)


def test_none_qrcode():
    shortener = Shortener('TinyurlShortener')
    assert shortener.qrcode() is None
