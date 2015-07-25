#!/usr/bin/env python
# encoding: utf-8
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


from pyshorteners.shorteners import Shortener

import responses

s = Shortener('SentalaShortener')
shorten = 'http://senta.la/test'
expanded = 'http://www.test.com'


@responses.activate
def test_sentala_short_method():
    # mock responses
    params = urlencode({
        'dever': 'encurtar',
        'format': 'simple',
        'url': expanded,
    })
    mock_url = '{}?{}'.format(s.api_url, params)
    responses.add(responses.GET, mock_url, body=shorten,
                  match_querystring=True)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded
