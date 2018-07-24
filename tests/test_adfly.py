from urllib.parse import urlencode

from pyshorteners import Shortener
from pyshorteners.exceptions import ShorteningErrorException, BadAPIResponseException

import responses
import pytest

s = Shortener(user_id='TEST', api_key='TEST_KEY')
shorten = 'http://ad.fly/test'
expanded = 'http://www.test.com'
adfly = s.adfly


@responses.activate
def test_adfly_short_method():
    # mock responses
    response = {
        'errors': [],
        'data': [{'short_url': shorten}],
    }
    mock_url = f'{adfly.api_url}v1/shorten'
    responses.add(responses.POST, mock_url, json=response)

    shorten_result = s.adfly.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_adfly_short_method_bad_response():
    # mock responses
    mock_url = f'{adfly.api_url}v1/shorten'
    responses.add(responses.POST, mock_url, status=400)

    with pytest.raises(BadAPIResponseException):
        adfly.short(expanded)


@responses.activate
def test_adfly_expand_method():
    # mock responses
    response = {
        'errors': [],
        'data': [{'url': expanded}],
    }
    mock_url = f'{adfly.api_url}v1/expand'
    responses.add(responses.POST, mock_url, json=response)

    expand_result = s.adfly.expand(shorten)

    assert expand_result == expanded


@responses.activate
def test_adfly_expand_method_bad_response():
    # mock responses
    mock_url = f'{adfly.api_url}v1/expand'
    responses.add(responses.POST, mock_url, status=400)

    with pytest.raises(BadAPIResponseException):
        adfly.expand(expanded)
