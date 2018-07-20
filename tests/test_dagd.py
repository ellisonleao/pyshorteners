from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener()
shorten = 'http://da.gd/test'
expanded = 'http://www.test.com'
dagd = s.dagd


@responses.activate
def test_dagd_short_method():
    # mock responses
    mock_url = f'{dagd.api_url}shorten?url={expanded}'
    responses.add(responses.GET, mock_url, body=shorten,
                  match_querystring=True)

    shorten_result = dagd.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_dagd_short_method_bad_response():
    # mock responses
    mock_url = f'{dagd.api_url}shorten?url={expanded}'
    responses.add(responses.GET, mock_url, body=shorten, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        dagd.short(expanded)
