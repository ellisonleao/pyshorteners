import json
from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

s = Shortener(api_key='TEST_KEY')
shorten = 'http://ow.ly/test'
expanded = 'http://www.test.com'
owly = s.owly


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
    mock_url = f'{owly.api_url}shorten?{params}'
    responses.add(responses.GET, mock_url, body=body,
                  match_querystring=True)

    shorten_result = owly.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_owly_short_method_bad_response():
    # mock responses
    params = urlencode({
        'apiKey': 'TEST_KEY',
        'longUrl': expanded,
    })
    body = "{'rerrsults': {'shortUrl': shorten}}"
    mock_url = f'{owly.api_url}shorten?{params}'
    responses.add(responses.GET, mock_url, body=body,
                  match_querystring=True)

    with pytest.raises(json.decoder.JSONDecodeError):
        owly.short(expanded)


@responses.activate
def test_owly_short_method_bad_response_status():
    # mock responses
    params = urlencode({
        'apiKey': 'TEST_KEY',
        'longUrl': expanded,
    })
    body = "{'rerrsults': {'shortUrl': shorten}}"
    mock_url = f'{owly.api_url}shorten?{params}'
    responses.add(responses.GET, mock_url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        owly.short(expanded)


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
    mock_url = f'{owly.api_url}expand?{params}'
    responses.add(responses.GET, mock_url, body=body,
                  match_querystring=True)

    expanded_result = owly.expand(shorten)

    assert expanded_result == expanded


@responses.activate
def test_owly_expand_method_bad_response():
    # mock responses
    params = urlencode({'apiKey': 'TEST_KEY', 'shortUrl': shorten})
    body = "{'results': {'longUrl': ''}}"
    mock_url = f'{owly.api_url}expand?{params}'
    responses.add(responses.GET, mock_url, body=body,
                  match_querystring=True)

    with pytest.raises(json.decoder.JSONDecodeError):
        owly.expand(shorten)


@responses.activate
def test_owly_expand_method_bad_status_code():
    # mock responses
    params = urlencode({'apiKey': 'TEST_KEY', 'shortUrl': shorten})
    body = "{'results': {'longUrl': ''}}"
    mock_url = f'{owly.api_url}expand?{params}'
    responses.add(responses.GET, mock_url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        owly.expand(shorten)
