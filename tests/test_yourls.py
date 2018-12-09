import os

import pytest
import responses

from pyshorteners import Shortener
from pyshorteners.exceptions import BadAPIResponseException

# Check and read from environment variables

expected_environment_variables = [
    "PYSHORTENERYOURLSTEST_USERNAME", "PYSHORTENERYOURLSTEST_PASSWORD",
    "PYSHORTENERYOURLSTEST_APIURL", "PYSHORTENERYOURLSTEST_SHORTEN",
    "PYSHORTENERYOURLSTEST_EXPANDED", "PYSHORTENERYOURLSTEST_TOTALCLICKS"
]

for expected_environment_variable in expected_environment_variables:
    assert expected_environment_variable in os.environ, \
        "Please set the environement variable %s to test `yourls`" % \
        expected_environment_variable

s = Shortener(
    username=os.environ['PYSHORTENERYOURLSTEST_USERNAME'],
    password=os.environ['PYSHORTENERYOURLSTEST_PASSWORD'],
    api_url=os.environ['PYSHORTENERYOURLSTEST_APIURL'],
)
shorten = os.environ['PYSHORTENERYOURLSTEST_SHORTEN']
expanded = os.environ['PYSHORTENERYOURLSTEST_EXPANDED']
total_clicks = int(os.environ['PYSHORTENERYOURLSTEST_TOTALCLICKS'])
yourls = s.yourls


@responses.activate
def test_yourls_short_method():
    # mock responses
    mock_url = f'{yourls.api_url}'
    response = {
        "shorturl": shorten,
    }
    responses.add(responses.POST, mock_url, json=response)
    shorten_result = yourls.short(expanded)
    assert shorten_result == shorten


@responses.activate
def test_yourls_short_method_bad_response():
    # mock responses
    mock_url = f'{yourls.api_url}'
    responses.add(responses.POST, mock_url, status=400)

    with pytest.raises(BadAPIResponseException):
        yourls.short(expanded)


@responses.activate
def test_yourls_expand_method():
    # mock responses
    mock_url = f'{yourls.api_url}'
    response = {
        'longurl': expanded,
    }
    responses.add(responses.POST, mock_url, json=response)
    expand_result = yourls.expand(shorten)
    assert expand_result == expanded


@responses.activate
def test_yourls_expand_method_bad_response():
    # mock responses
    mock_url = f'{yourls.api_url}'
    responses.add(responses.POST, mock_url, status=400)

    with pytest.raises(BadAPIResponseException):
        yourls.expand(expanded)


@responses.activate
def test_yourls_stats_method():
    # mock responses
    mock_url = f'{yourls.api_url}'
    response = {
        'click': total_clicks,
    }
    responses.add(responses.POST, mock_url, json=response)
    total_clicks_result = yourls.total_clicks(shorten)
    assert total_clicks_result == total_clicks


@responses.activate
def test_yourls_stats_method_bad_response():
    # mock responses
    mock_url = f'{yourls.api_url}'
    responses.add(responses.POST, mock_url, status=400)

    with pytest.raises(BadAPIResponseException):
        yourls.total_clicks(shorten)
