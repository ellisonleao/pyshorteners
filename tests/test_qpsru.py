from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener()
shorten = "http://qps.ru/test"
expanded = "http://www.test.com"
qp = s.qpsru


@responses.activate
def test_qpsru_short_method():
    # mock responses
    params = urlencode({"url": expanded})
    mock_url = f"{qp.api_url}?{params}"
    responses.add(responses.GET, mock_url, body=shorten, match_querystring=True)

    shorten_result = qp.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_qpsru_short_method_bad_response():
    # mock responses
    params = urlencode({"url": expanded})
    mock_url = f"{qp.api_url}?{params}"
    responses.add(
        responses.GET, mock_url, body=shorten, status=400, match_querystring=True
    )

    with pytest.raises(ShorteningErrorException):
        qp.short(expanded)
