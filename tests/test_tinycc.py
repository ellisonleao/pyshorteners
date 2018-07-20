from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException,
                                     BadAPIResponseException)

import responses
import pytest

token = 'TEST_TOKEN'
login = 'TEST_LOGIN'
api_version = '2.0.3'
shorten = 'http://tiny.cc/test'
expanded = 'http://www.test.com'
s = Shortener(api_key=token, login=login)
tiny = s.tinycc


@responses.activate
def test_tinycc_short_method():
    # mock responses
    body = {"results": {"short_url": shorten}}
    params = urlencode(
        dict(
            longUrl=expanded,
            apiKey=token,
            format='json',
            c='rest_api',
            version=api_version,
            login=login,
            m='shorten',
        ))

    url = f'{tiny.api_url}?{params}'
    responses.add(responses.GET, url, json=body, match_querystring=True)

    shorten_result = tiny.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_tinycc_short_method_bad_response():
    # mock responses
    body = shorten
    params = urlencode(
        dict(
            longUrl=expanded,
            apiKey=token,
            format='json',
            c='rest_api',
            version=api_version,
            login=login,
            m='shorten',
        ))
    url = f'{tiny.api_url}?{params}'
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        tiny.short(expanded)


@responses.activate
def test_tinycc_expand_method():
    # mock responses
    body = {'results': {'longUrl': expanded}}
    params = urlencode(
        dict(
            longUrl=shorten,
            apiKey=token,
            format='json',
            c='rest_api',
            version=api_version,
            login=login,
            m='expand',
        ))
    url = f'{tiny.api_url}?{params}'
    responses.add(responses.GET, url, json=body, match_querystring=True)
    assert tiny.expand(shorten) == expanded


@responses.activate
def test_tinycc_expand_method_bad_response():
    # mock responses
    body = expanded
    params = urlencode(
        dict(
            longUrl=shorten,
            apiKey=token,
            format='json',
            c='rest_api',
            version=api_version,
            login=login,
            m='expand',
        ))
    url = f'{tiny.api_url}?{params}'
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        tiny.expand(shorten)


@responses.activate
def test_tinycc_total_clicks():
    body = {"results": {"clicks": 20}}
    params = urlencode(
        dict(
            shortUrl=shorten,
            apiKey=token,
            format='json',
            c='rest_api',
            version=api_version,
            login=login,
            m='total_visits',
        ))
    url = f'{tiny.api_url}?{params}'
    responses.add(responses.GET, url, json=body, match_querystring=True)
    assert tiny.total_clicks(shorten) == 20


@responses.activate
def test_tinycc_total_clicks_bad_response():
    clicks_body = {'results': 'a'}
    params = urlencode(
        dict(
            c='rest_api',
            version=api_version,
            format='json',
            apiKey=token,
            login=login,
            m='total_visits',
            shortUrl=shorten,
        ))
    url = f'{tiny.api_url}?{params}'
    responses.add(responses.GET, url, json=clicks_body, match_querystring=True)
    assert tiny.total_clicks(shorten) == 0
