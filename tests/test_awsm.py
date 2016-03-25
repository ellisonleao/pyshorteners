#!/usr/bin/env python
# encoding: utf-8
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from pyshorteners import Shortener, Shorteners
from pyshorteners.shorteners import Awsm
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

api_key = 'FAKE_KEY'
s = Shortener(Shorteners.AWSM, api_key=api_key, tool='abcde')
short_url = 'http://aw.sm/rjf0oI'
expanded = 'http://www.test.com'


@responses.activate
def test_awsm_short_method():
    # mock response
    params = urlencode({
        'url': expanded,
        'key': api_key,
        'channel': 'twitter',
        'tool': 'abcde',
        'v': 3
    })
    url = '{0}url.txt?{1}'.format(s.api_url, params)
    responses.add(responses.POST, url, body=short_url, match_querystring=True)

    shorten = s.short(expanded)
    assert shorten == short_url


@responses.activate
def test_awsm_short_method_bad_response():
    url = '{}url.txt'.format(s.api_url)
    responses.add(responses.POST, url, body=short_url, status=400)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_awsm_expand_method_bad_response():
    responses.add(responses.GET, short_url, body='', status=400,
                  match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        s.expand(short_url)


def test_generate_tool_staticmethod():
    tool = Awsm._generate_random_tool()
    assert len(tool) == 4


def test_bad_key():
    s = Shortener(Shorteners.AWSM)

    with pytest.raises(TypeError):
        s.short(expanded)
