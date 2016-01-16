#!/usr/bin/env python
# encoding: utf-8
import json

from pyshorteners import Shortener, Shorteners
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

s = Shortener(Shorteners.READABILITY)
shorten = 'http://rdd.me/test'
expanded = 'http://www.test.com'


@responses.activate
def test_readability_short_method():
    # mock responses
    body = json.dumps({
        'meta': {'rdd_url': shorten}
    })
    responses.add(responses.POST, s.api_url, body=body)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded


@responses.activate
def test_readability_short_method_bad_response():
    # mock responses
    body = "{'mmmeta': {'rdd_url': shorten}}"
    responses.add(responses.POST, s.api_url, body=body)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_readability_short_method_bad_status_code():
    # mock responses
    body = "{'mmmeta': {'rdd_url': shorten}}"
    responses.add(responses.POST, s.api_url, body=body, status=400)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_readbility_expand_method():
    # mock responses
    body = json.dumps({
        'meta': {'full_url': expanded}
    })
    mock_url = '{0}{1}'.format(s.api_url, 'test')
    responses.add(responses.GET, mock_url, body=body)

    expanded_result = s.expand(shorten)

    assert expanded_result == expanded
    assert s.expanded == expanded


@responses.activate
def test_readbility_expand_method_bad_response():
    # mock responses
    body = "{'meta': {'full_url': }}"
    mock_url = '{0}{1}'.format(s.api_url, 'test')
    responses.add(responses.GET, mock_url, body=body)

    with pytest.raises(ExpandingErrorException):
        s.expand(shorten)


@responses.activate
def test_readbility_expand_method_bad_response_status():
    # mock responses
    body = "{'meta': {'full_url': }}"
    mock_url = '{0}{1}'.format(s.api_url, 'test')
    responses.add(responses.GET, mock_url, body=body, status=400)

    with pytest.raises(ExpandingErrorException):
        s.expand(shorten)
