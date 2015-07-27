# coding: utf-8
from __future__ import unicode_literals

from pyshorteners import Shortener
from pyshorteners.utils import is_valid_url
from pyshorteners.exceptions import UnknownShortenerException

import pytest
import responses

module = __import__('pyshorteners.shorteners')


def test_shorteners_type():
    shorteners = ['GoogleShortener', 'BitlyShortener', 'TinyurlShortener',
                  'AdflyShortener', 'IsgdShortener', 'SentalaShortener',
                  'OwlyShortener', 'AwsmShortener']
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


    with pytest.raises(ValueError):
        url = 'www.11.xom'
        s.expand(url)

def test_none_qrcode():
    shortener = Shortener('TinyurlShortener')
    assert shortener.qrcode() is None


@responses.activate
def test_qrcode():
    s = Shortener('TinyurlShortener')
    url = 'http://www.google.com'
    mock_url = '{}?url={}'.format(s.api_url, url)
    shorten = 'http://tinyurl.com/test'
    responses.add(responses.GET, mock_url, body=shorten,
                  match_querystring=True)
    s.short(url)
    # flake8: noqa
    assert s.qrcode() == 'http://chart.apis.google.com/chart?cht=qr&chl={0}&chs=120x120'.format(shorten)
