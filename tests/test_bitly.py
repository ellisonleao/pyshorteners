#!/usr/bin/env python
# encoding: utf-8
from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException,
                                     BadAPIResponseException)

import responses
import pytest

token = 'TEST_TOKEN'
s = Shortener(api_key=token)
shorten = 'http://bit.ly/test'
expanded = 'http://www.test.com'
bitly = s.bitly


@responses.activate
def test_bitly_short_method():
    # mock responses
    body = shorten
    params = urlencode(dict(
        uri=expanded,
        access_token=token,
        format='txt'
    ))

    url = f'{bitly.api_url}v3/shorten?{params}'
    responses.add(responses.GET, url, body=body, match_querystring=True)

    shorten_result = bitly.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_bitly_short_method_bad_response():
    # mock responses
    body = shorten
    params = urlencode(dict(
        uri=expanded,
        access_token=token,
        format='txt'
    ))
    url = f'{bitly.api_url}v3/shorten?{params}'
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        bitly.short(expanded)


@responses.activate
def test_bitly_expand_method():
    # mock responses
    body = expanded
    params = urlencode(dict(
        shortUrl=shorten,
        access_token=token,
        format='txt'
    ))
    url = f'{bitly.api_url}v3/expand?{params}'
    responses.add(responses.GET, url, body=body, match_querystring=True)
    assert bitly.expand(shorten) == expanded


@responses.activate
def test_bitly_expand_method_bad_response():
    # mock responses
    body = expanded
    params = urlencode(dict(
        shortUrl=shorten,
        access_token=token,
        format='txt'
    ))
    url = f'{bitly.api_url}v3/expand?{params}'
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        bitly.expand(shorten)


@responses.activate
def test_bitly_total_clicks():
    body = '20'
    params = urlencode(dict(
        link=shorten,
        access_token=token,
        format='txt'
    ))
    url = f'{bitly.api_url}v3/link/clicks?{params}'
    responses.add(responses.GET, url, body=body, match_querystring=True)

    assert bitly.total_clicks(shorten) == 20


@responses.activate
def test_bitly_total_clicks_bad_response():
    body = '20'
    params = urlencode(dict(
        link=shorten,
        access_token=token,
        format='txt'
    ))
    url = f'{bitly.api_url}v3/link/clicks?{params}'
    responses.add(responses.GET, url, body=body, status=400,
                  match_querystring=True)
    with pytest.raises(BadAPIResponseException):
        bitly.total_clicks(shorten)
