from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener()
shorten = "http://tinyurl.com/test"
expanded = "http://www.test.com"
tiny = s.tinyurl


@responses.activate
def test_tinyurl_short_method():
    # mock responses
    mock_url = f"{tiny.api_url}?url={expanded}"
    responses.add(responses.GET, mock_url, body=shorten, match_querystring=True)

    shorten_result = tiny.short(expanded)
    assert shorten_result == shorten


@responses.activate
def test_tinyurl_short_bad_response():
    # mock responses
    mock_url = f"{tiny.api_url}?url={expanded}"
    responses.add(
        responses.GET, mock_url, body=shorten, status=400, match_querystring=True
    )

    with pytest.raises(ShorteningErrorException):
        tiny.short(expanded)
