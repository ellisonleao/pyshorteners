from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException, BadAPIResponseException

import responses
import pytest

s = Shortener(api_key='TEST_KEY')
url = 'http://www.test.com'
shorted_url='https://cutt.ly/test'
cuttly = s.cuttly


@responses.activate
def test_cuttly_short_method():
    # mock responses
    payload = {
                'key': cuttly.api_key,
                'short': url,

            }
    mock_url = f'{cuttly.api_url}?key={payload.key}&short={payload.url}'
    responses.add(responses.get, mock_url)

    shorten_result = cuttly.short(url)

    assert shorten_result == shorted_url


@responses.activate
def test_cuttly_short_method_bad_response():
    # mock responses
    mock_url = cuttly.api_url

    responses.add(responses.GET, mock_url, status=400)

    with pytest.raises(BadAPIResponseException):
         cuttly.short(url)
