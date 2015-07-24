#!/usr/bin/env python
# encoding: utf-8
import json

from pyshorteners.shorteners import Shortener

import responses

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
def test_bitly_expand_method():
    # mock responses
    body = json.dumps({
        'status_code': 200,
        'data': {'expand': [{'long_url': expanded}]}
    })
    url = '{0}{1}'.format(s.api_url, 'v3/expand')
    responses.add(responses.GET, url, body=body)
    assert s.expand(shorten) == expanded
