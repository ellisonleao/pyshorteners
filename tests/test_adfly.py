from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener(uid='TEST', key='TEST_KEY')
shorten = 'http://ad.fly/test'
expanded = 'http://www.test.com'
adfly = s.adfly


@responses.activate
def test_adfly_short_method():
    # mock responses
    params = urlencode({
        'domain': 'adf.ly',
        'advert_type': 'int',  # int or banner
        'key': adfly.key,
        'uid': adfly.uid,
        'url': expanded,
    })
    mock_url = f'{adfly.api_url}?{params}'
    responses.add(responses.GET, mock_url, body=shorten,
                  match_querystring=True)

    shorten_result = s.adfly.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_adfly_short_method_bad_response():
    # mock responses
    params = urlencode({
        'domain': 'adf.ly',
        'advert_type': 'int',  # int or banner
        'key': adfly.key,
        'uid': adfly.uid,
        'url': expanded,
    })
    mock_url = f'{adfly.api_url}?{params}'
    responses.add(responses.GET, mock_url, body=shorten, status=400,
                  match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        adfly.short(expanded)
