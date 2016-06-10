# coding: utf-8
from __future__ import unicode_literals

from pyshorteners import Shortener, Shorteners
from pyshorteners.utils import is_valid_url
from pyshorteners.exceptions import UnknownShortenerException
from pyshorteners.shorteners.base import BaseShortener

import pytest
import responses

module = __import__('pyshorteners.shorteners')


def test_shorteners_type():
    shorteners = [Shorteners.GOOGLE, Shorteners.BITLY,
                  Shorteners.TINYURL, Shorteners.ADFLY,
                  Shorteners.ISGD, Shorteners.SENTALA,
                  Shorteners.OWLY, Shorteners.AWSM,
                  Shorteners.DAGD]
    for shortener in shorteners:
        short = Shortener(shortener)
        assert issubclass(short._class, BaseShortener)
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

    s = Shortener(Shorteners.TINYURL)
    with pytest.raises(ValueError):
        url = 'http://12'
        s.short(url)


    with pytest.raises(ValueError):
        url = 'www.11.xom'
        s.expand(url)


def test_short_method_bad_url():
    s = Shortener()
    with pytest.raises(ValueError):
        s.short('test.com')


def test_expand_method_bad_url():
    s = Shortener()
    with pytest.raises(ValueError):
        s.expand('test.com')


def test_none_qrcode():
    shortener = Shortener(Shorteners.TINYURL)
    assert shortener.qrcode() is None


@responses.activate
def test_qrcode():
    s = Shortener(Shorteners.TINYURL)
    url = 'http://www.google.com'
    mock_url = '{}?url={}'.format(s.api_url, url)
    shorten = 'http://tinyurl.com/test'
    responses.add(responses.GET, mock_url, body=shorten,
                  match_querystring=True)
    s.short(url)
    # flake8: noqa
    assert s.qrcode() == 'http://chart.apis.google.com/chart?cht=qr&chl={0}&chs=120x120'.format(shorten)


def test_total_clicks_no_url_or_shorten():
    s = Shortener()

    with pytest.raises(TypeError):
        s.total_clicks()

def test_total_clicks_bad_url():
    s = Shortener()

    with pytest.raises(ValueError):
        s.total_clicks('test.com')

@responses.activate
def test_shortener_debug_enabled():
    url = 'http://www.test.com'
    small = 'http://small.com'
    responses.add(responses.GET, url, body=small)
    responses.add(responses.GET, small, body=url)

    s = Shortener(debug=True)
    s.short('http://www.test.com')
    s.expand('http://small.com')
    with pytest.raises(NotImplementedError):
        s.total_clicks('http://small.com')

def test_custom_shortener():
    class MyShortenerWithBlackJackAndHookers(BaseShortener):
        def short(self, url):
            return url

    s = Shortener(MyShortenerWithBlackJackAndHookers)
    url = 'http://www.test.com'
    assert s.short(url) == url
