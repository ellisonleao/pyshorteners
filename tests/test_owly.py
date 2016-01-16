#!/usr/bin/env python
# encoding: utf-8
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

import json

from pyshorteners import Shortener, Shorteners
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

s = Shortener(Shorteners.OWLY, api_key='TEST_KEY')
shorten = 'http://ow.ly/test'
expanded = 'http://www.test.com'


@responses.activate
def test_owly_short_method():
    # mock responses
    params = urlencode({
        'apiKey': 'TEST_KEY',
        'longUrl': expanded,
    })
    body = json.dumps({
        'results': {'shortUrl': shorten}
    })
    mock_url = '{}shorten?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=body,
                  match_querystring=True)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded


@responses.activate
def test_owly_short_method_bad_response():
    # mock responses
    params = urlencode({
        'apiKey': 'TEST_KEY',
        'longUrl': expanded,
    })
    body = "{'rerrsults': {'shortUrl': shorten}}"
    mock_url = '{}shorten?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=body,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_owly_short_method_bad_response_status():
    # mock responses
    params = urlencode({
        'apiKey': 'TEST_KEY',
        'longUrl': expanded,
    })
    body = "{'rerrsults': {'shortUrl': shorten}}"
    mock_url = '{}shorten?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_owly_expand_method():
    # mock responses
    params = urlencode({
        'apiKey': 'TEST_KEY',
        'shortUrl': shorten,
    })
    body = json.dumps({
        'results': {'longUrl': expanded}
    })
    mock_url = '{}expand?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=body,
                  match_querystring=True)

    expanded_result = s.expand(shorten)

    assert expanded_result == expanded
    assert s.expanded == expanded


@responses.activate
def test_owly_expand_method_bad_response():
    # mock responses
    params = urlencode({'apiKey': 'TEST_KEY', 'shortUrl': shorten})
    body = "{'results': {'longUrl': ''}}"
    mock_url = '{}expand?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=body,
                  match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        s.expand(shorten)


@responses.activate
def test_owly_expand_method_bad_status_code():
    # mock responses
    params = urlencode({'apiKey': 'TEST_KEY', 'shortUrl': shorten})
    body = "{'results': {'longUrl': ''}}"
    mock_url = '{}expand?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        s.expand(shorten)


def test_owly_bad_key():
    b = Shortener(Shorteners.OWLY)
    with pytest.raises(TypeError):
        b.short('http://www.test.com')

    with pytest.raises(TypeError):
        b.expand('http://www.test.com')
