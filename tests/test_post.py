from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener(api_key="TEST")
post = s.post
shorten = "http://po.st/test"
expanded = "http://www.test.com"
params = urlencode({"apiKey": "TEST", "longUrl": expanded, "format": "txt"})
mock_url = f"{post.api_url}?{params}"


@responses.activate
def test_post_short_method():
    # mock responses
    response = {"short_url": shorten}
    responses.add(responses.GET, mock_url, json=response, match_querystring=True)

    shorten_result = post.short(expanded)
    assert shorten_result == shorten


@responses.activate
def test_post_short_bad_response():
    # mock responses
    responses.add(
        responses.GET, mock_url, body=shorten, status=400, match_querystring=True
    )

    with pytest.raises(ShorteningErrorException):
        post.short(expanded)
