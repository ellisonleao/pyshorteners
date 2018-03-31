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
login = 'TEST_LOGIN'
api_version = '2.0.3'
s = Shortener(
    Shorteners.TINYCC, tinycc_api_key=token, tinycc_login=login, timeout=3)
shorten = 'http://tiny.cc/test'
expanded = 'http://www.test.com'


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

    url = '{0}?{1}'.format(s.api_url, params)
    responses.add(responses.GET, url, json=body, match_querystring=True)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded


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
    url = '{0}?{1}'.format(s.api_url, params)
    responses.add(
        responses.GET, url, body=body, status=400, match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_tinycc_expand_method():
    # mock responses
    body = {"results": {"long_url": expanded}}
    params = urlencode(
        dict(
            shortUrl=shorten,
            apiKey=token,
            format='json',
            c='rest_api',
            version=api_version,
            login=login,
            m='expand',
        ))
    url = '{0}?{1}'.format(s.api_url, params)
    responses.add(responses.GET, url, json=body, match_querystring=True)
    assert s.expand(shorten) == expanded


@responses.activate
def test_tinycc_expand_method_bad_response():
    # mock responses
    body = expanded
    params = urlencode(
        dict(
            shortUrl=shorten,
            apiKey=token,
            format='json',
            c='rest_api',
            version=api_version,
            login=login,
            m='expand',
        ))
    url = '{0}?{1}'.format(s.api_url, params)
    responses.add(
        responses.GET, url, body=body, status=400, match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        s.expand(shorten)


def test_tinycc_bad_keys():
    s = Shortener(Shorteners.TINYCC)

    with pytest.raises(TypeError):
        s.short(expanded)

    with pytest.raises(TypeError):
        s.expand(shorten)


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
    url = '{0}?{1}'.format(s.api_url, params)
    responses.add(responses.GET, url, json=body, match_querystring=True)

    # shorten mock
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

    url = '{0}?{1}'.format(s.api_url, params)
    responses.add(responses.GET, url, json=body, match_querystring=True)

    s.short(expanded)
    assert s.total_clicks() == 20
    assert s.total_clicks(shorten) == 20


@responses.activate
def test_tinycc_total_clicks_bad_response():
    clicks_body = {"results": {"clicks": 0}}
    params = urlencode(
        dict(
            apiKey=token,
            format='json',
            c='rest_api',
            version=api_version,
            login=login,
            m='total_visits',
            shortUrl=shorten,
        ))
    url = '{0}?{1}'.format(s.api_url, params)
    responses.add(
        responses.GET,
        url,
        json=clicks_body,
        status=400,
        match_querystring=True)
    # shorten mock

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

    url = '{0}?{1}'.format(s.api_url, params)
    responses.add(responses.GET, url, json=body, match_querystring=True)

    s.short(expanded)
    assert s.total_clicks() == 0
    assert s.total_clicks(shorten) == 0
