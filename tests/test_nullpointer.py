from pyshorteners import Shortener
from pyshorteners.exceptions import BadAPIResponseException

import responses
import pytest

s = Shortener(domain='https://0x0.st/')
shorten = "https://0x0.st/jU"
expanded = "https://www.google.com"
nullpointer = s.nullpointer


@responses.activate
def test_nullpointer_short_method():
    response = shorten
    mock_url = nullpointer.domain
    responses.add(responses.POST, mock_url, body=response)

    shorten_result = nullpointer.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_nullpointer_short_method_bad_response():
    mock_url = nullpointer.domain
    responses.add(responses.POST, mock_url, status=400)

    with pytest.raises(BadAPIResponseException):
        nullpointer.short(expanded)
        