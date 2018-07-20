import json
from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

api_key = 'FAKE_KEY'
s = Shortener(api_key=api_key)
short_url = 'http://goo.gl/rjf0oI'
expanded = 'http://www.test.com'
googl = s.googl


@responses.activate
def test_googl_short_method():
    # mock response
    body = json.dumps(dict(id=short_url))

    url = f'{googl.api_url}?key={api_key}'
    responses.add(responses.POST, url, body=body, match_querystring=True)

    shorten = googl.short(expanded)
    assert shorten == short_url


@responses.activate
def test_googl_short_method_bad_status_code():
    # mock response
    body = '{"badid": "test"}'

    url = f'{googl.api_url}?key={api_key}'
    responses.add(responses.POST, url, body=body, match_querystring=True,
                  status=400)

    with pytest.raises(ShorteningErrorException):
        googl.short(expanded)


@responses.activate
def test_googl_expand_method():
    # mock response
    body = json.dumps(dict(longUrl=expanded))
    param = urlencode({
        'key': api_key,
        'shortUrl': short_url,
    })
    url = f'{googl.api_url}?{param}'
    responses.add(responses.GET, url, body=body, match_querystring=True)

    expanded_result = googl.expand(short_url)
    assert expanded_result == expanded


@responses.activate
def test_googl_expand_method_bad_response():
    # mock response
    body = '{"badkey": "test"}'
    param = urlencode({
        'key': api_key,
        'shortUrl': short_url,
    })
    url = f'{googl.api_url}?{param}'
    responses.add(responses.GET, url, body=body, match_querystring=True,
                  status=400)

    with pytest.raises(ExpandingErrorException):
        googl.expand(short_url)
