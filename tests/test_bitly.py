#!/usr/bin/env python
# encoding: utf-8
import json

from pyshorteners import Shortener
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

s = Shortener('BitlyShortener', bitly_api_key='TEST_KEY',
              bitly_token='TEST_TOKEN', bitly_login='TEST_LOGIN')
shorten = 'http://bit.ly/test'
expanded = 'http://www.test.com'


@responses.activate
def test_bitly_short_method():
    # mock responses
    body = json.dumps({
        'status_code': 200,
        'data': {'url': shorten}
    })
    url = '{0}{1}'.format(s.api_url, 'v3/shorten')
    responses.add(responses.POST, url, body=body)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded


@responses.activate
def test_bitly_short_method_bad_response():
    # mock responses
    body = json.dumps({
        'status_code': 200,
        'data': {'url': shorten}
    })
    url = '{0}{1}'.format(s.api_url, 'v3/shorten')
    responses.add(responses.POST, url, body=body, status=400)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_bitly_expand_method():
    # mock responses
    body = json.dumps({
        'status_code': 200,
        'data': {'expand': [{'long_url': expanded}]}
    })
    url = '{0}{1}'.format(s.api_url, 'v3/expand')
    responses.add(responses.GET, url, body=body)
    assert s.expand(shorten) == expanded


@responses.activate
def test_bitly_expand_method_bad_response():
    # mock responses
    body = json.dumps({
        'status_code': 400,
        'data': {'expand': [{'long_url': expanded}]}
    })
    url = '{0}{1}'.format(s.api_url, 'v3/expand')
    responses.add(responses.GET, url, body=body)

    with pytest.raises(ExpandingErrorException):
        s.expand(shorten)


@responses.activate
def test_bitly_expand_method_bad_status_code():
    # mock responses
    body = json.dumps({
        'status_code': 200,
        'data': {'expand': [{'long_url': expanded}]}
    })
    url = '{0}{1}'.format(s.api_url, 'v3/expand')
    responses.add(responses.GET, url, body=body, status=400)

    with pytest.raises(ExpandingErrorException):
        s.expand(shorten)


def test_bitly_bad_keys():
    s = Shortener('BitlyShortener')

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
