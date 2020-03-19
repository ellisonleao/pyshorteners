from urllib.parse import urlencode
import json

from pyshorteners import Shortener
from pyshorteners.exceptions import BadAPIResponseException

import responses
import pytest

s = Shortener(api_key="TEST_KEY")
url = "http://www.test.com"
shorted_url = "https://cutt.ly/TEST"
cuttly = s.cuttly


@responses.activate
def test_cuttly_short_method():
    # mock responses
    params = urlencode({"key": cuttly.api_key, "short": url})
    mock_url = f"{cuttly.api_url}?{params}"
    res = json.dumps({"url": {"status": 1, "shortLink": shorted_url}})
    responses.add(responses.GET, mock_url, status=200, body=res, match_querystring=True)

    shorten_result = cuttly.short(url)

    assert shorten_result == shorted_url


@responses.activate
def test_cuttly_short_method_bad_response():
    # mock responses
    mock_url = cuttly.api_url

    responses.add(responses.GET, mock_url, status=400)

    with pytest.raises(BadAPIResponseException):
        cuttly.short(url)
