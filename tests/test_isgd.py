from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener()
shorten = "https://is.gd/test"
expanded = "http://www.test.com"
isgd = s.isgd


@responses.activate
def test_isgd_short_method():
    # mock responses
    params = urlencode({"format": "simple", "url": expanded})
    mock_url = f"{isgd.api_url}?{params}"
    responses.add(responses.GET, mock_url, body=shorten, match_querystring=True)

    shorten_result = isgd.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_isgd_short_method_bad_response():
    # mock responses
    params = urlencode({"format": "simple", "url": expanded})
    mock_url = f"{isgd.api_url}?{params}"
    responses.add(
        responses.GET, mock_url, body=shorten, status=400, match_querystring=True
    )

    with pytest.raises(ShorteningErrorException):
        isgd.short(expanded)
