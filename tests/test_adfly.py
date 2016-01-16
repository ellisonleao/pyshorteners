#!/usr/bin/env python
# encoding: utf-8
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from pyshorteners import Shortener, Shorteners
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener(Shorteners.ADFLY, uid='TEST', key='TEST_KEY')
shorten = 'http://ad.fly/test'
expanded = 'http://www.test.com'


@responses.activate
def test_adfly_short_method():
    # mock responses
    params = urlencode({
        'domain': 'adf.ly',
        'advert_type': 'int',  # int or banner
        'key': s.key,
        'uid': s.uid,
        'url': expanded,
    })
    mock_url = '{}?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=shorten,
                  match_querystring=True)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded


@responses.activate
def test_adfly_short_method_bad_response():
    # mock responses
    params = urlencode({
        'domain': 'adf.ly',
        'advert_type': 'int',  # int or banner
        'key': s.key,
        'uid': s.uid,
        'url': expanded,
    })
    mock_url = '{}?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=shorten, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


def test_adfly_bad_params():
    s = Shortener(Shorteners.ADFLY)

    with pytest.raises(TypeError):
        s.short(expanded)
