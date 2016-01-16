#!/usr/bin/env python
# encoding: utf-8
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from pyshorteners import Shortener, Shorteners
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

token = 'TEST_TOKEN'
s = Shortener(Shorteners.BITLY, bitly_token=token)
shorten = 'http://bit.ly/test'
expanded = 'http://www.test.com'


@responses.activate
def test_bitly_short_method():
    # mock responses
    body = shorten
    params = urlencode(dict(
        uri=expanded,
        access_token=token,
        format='txt'
    ))

    url = '{0}{1}?{2}'.format(s.api_url, 'v3/shorten', params)
    responses.add(responses.GET, url, body=body, match_querystring=True)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded


@responses.activate
def test_bitly_short_method_bad_response():
    # mock responses
    body = shorten
    params = urlencode(dict(
        uri=expanded,
        access_token=token,
        format='txt'
    ))
    url = '{0}{1}?{2}'.format(s.api_url, 'v3/shorten', params)
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_bitly_expand_method():
    # mock responses
    body = expanded
    params = urlencode(dict(
        shortUrl=shorten,
        access_token=token,
        format='txt'
    ))
    url = '{0}{1}?{2}'.format(s.api_url, 'v3/expand', params)
    responses.add(responses.GET, url, body=body, match_querystring=True)
    assert s.expand(shorten) == expanded


@responses.activate
def test_bitly_expand_method_bad_response():
    # mock responses
    body = expanded
    params = urlencode(dict(
        shortUrl=shorten,
        access_token=token,
        format='txt'
    ))
    url = '{0}{1}?{2}'.format(s.api_url, 'v3/expand', params)
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        s.expand(shorten)


def test_bitly_bad_keys():
    s = Shortener(Shorteners.BITLY)

    with pytest.raises(TypeError):
        s.short(expanded)

    with pytest.raises(TypeError):
        s.expand(shorten)


@responses.activate
def test_bitly_total_clicks():
    body = '20'
    params = urlencode(dict(
        link=shorten,
        access_token=token,
        format='txt'
    ))
    url = '{0}{1}?{2}'.format(s.api_url, 'v3/link/clicks', params)
    responses.add(responses.GET, url, body=body, match_querystring=True)

    # shorten mock
    body = shorten
    params = urlencode(dict(
        uri=expanded,
        access_token=token,
        format='txt'
    ))
    url = '{0}{1}?{2}'.format(s.api_url, 'v3/shorten', params)
    responses.add(responses.GET, url, body=body, match_querystring=True)

    s.short(expanded)
    assert s.total_clicks() == 20
    assert s.total_clicks(shorten) == 20


@responses.activate
def test_bitly_total_clicks_bad_response():
    body = '20'
    params = urlencode(dict(
        link=shorten,
        access_token=token,
        format='txt'
    ))
    url = '{0}{1}?{2}'.format(s.api_url, 'v3/link/clicks', params)
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)

    # shorten mock
    body = shorten
    params = urlencode(dict(
        uri=expanded,
        access_token=token,
        format='txt'
    ))
    url = '{0}{1}?{2}'.format(s.api_url, 'v3/shorten', params)
    responses.add(responses.GET, url, body=body, match_querystring=True)

    s.short(expanded)
    assert s.total_clicks() == 0
    assert s.total_clicks(shorten) == 0
