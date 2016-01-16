#!/usr/bin/env python
# encoding: utf-8
import json
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from pyshorteners import Shortener, Shorteners
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

api_key = 'FAKE_KEY'
s = Shortener(Shorteners.GOOGLE, api_key=api_key)
short_url = 'http://goo.gl/rjf0oI'
expanded = 'http://www.test.com'


@responses.activate
def test_googl_short_method():
    # mock response
    body = json.dumps(dict(id=short_url))

    url = '{}?key={}'.format(s.api_url, api_key)
    responses.add(responses.POST, url, body=body, match_querystring=True)

    shorten = s.short(expanded)
    assert shorten == short_url


@responses.activate
def test_googl_short_method_bad_response():
    # mock response
    body = "{'badid': 'test'}"

    url = '{}?key={}'.format(s.api_url, api_key)
    responses.add(responses.POST, url, body=body, match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_googl_short_method_bad_status_code():
    # mock response
    body = "{'bad': 'test'}"

    url = '{}?key={}'.format(s.api_url, api_key)
    responses.add(responses.POST, url, body=body, match_querystring=True,
                  status=400)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_googl_expand_method():
    # mock response
    body = json.dumps(dict(longUrl=expanded))
    param = urlencode({
        'key': api_key,
        'shortUrl': short_url,
    })
    url = '{}?{}'.format(s.api_url, param)
    responses.add(responses.GET, url, body=body, match_querystring=True)

    expanded_result = s.expand(short_url)
    assert expanded_result == expanded


@responses.activate
def test_googl_expand_method_bad_response():
    # mock response
    body = "{'badkey': 'test'}"
    param = urlencode({
        'key': api_key,
        'shortUrl': short_url,
    })
    url = '{}?{}'.format(s.api_url, param)
    responses.add(responses.GET, url, body=body, match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        s.expand(short_url)


@responses.activate
def test_googl_expand_method_bad_status_code():
    # mock response
    body = "{'badkey': 'test'}"
    param = urlencode({
        'key': api_key,
        'shortUrl': short_url,
    })
    url = '{}?{}'.format(s.api_url, param)
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        s.expand(short_url)


def test_google_bad_params():
    s = Shortener(Shorteners.GOOGLE)

    with pytest.raises(TypeError):
        s.short(expanded)

    with pytest.raises(TypeError):
        s.expand(expanded)
