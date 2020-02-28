from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener()
shorten = "http://chilp.it/test"
expanded = "http://www.test.com"
chil = s.chilpit


@responses.activate
def test_chilpit_short_method():
    # mock responses
    params = urlencode({"url": expanded})
    mock_url = f"{chil.api_url}?{params}"
    responses.add(responses.GET, mock_url, body=shorten, match_querystring=True)

    shorten_result = chil.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_chilpit_short_method_bad_response():
    # mock responses
    params = urlencode({"url": expanded})
    mock_url = f"{chil.api_url}?{params}"
    responses.add(
        responses.GET, mock_url, body=shorten, status=400, match_querystring=True
    )

    with pytest.raises(ShorteningErrorException):
        chil.short(expanded)
