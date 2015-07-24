#!/usr/bin/env python
# encoding: utf-8
from pyshorteners.shorteners import Shortener

import responses

s = Shortener('TinyurlShortener')
shorten = 'http://tinyurl.com/test'
expanded = 'http://www.test.com'


@responses.activate
def test_tinyurl_short_method():
    # mock responses
    mock_url = '{}?url={}'.format(s.api_url, expanded)
    responses.add(responses.GET, mock_url, body=shorten,
                  match_querystring=True)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded
