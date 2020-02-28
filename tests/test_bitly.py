#!/usr/bin/env python
from urllib.parse import urlparse
import json

from pyshorteners import Shortener
from pyshorteners.exceptions import (
    ShorteningErrorException,
    ExpandingErrorException,
    BadAPIResponseException,
)

import responses
import pytest

token = "TEST_TOKEN"
s = Shortener(api_key=token)
shorten = "http://bit.ly/test"
expanded = "http://www.test.com"
bitly = s.bitly


@responses.activate
def test_bitly_short_method():
    # mock responses
    body = json.dumps({"link": shorten})
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{bitly.api_url}/shorten"
    responses.add(
        responses.POST, url, headers=headers, body=body, match_querystring=True
    )

    shorten_result = bitly.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_bitly_short_method_bad_response():
    # mock responses
    body = json.dumps({"link": shorten})
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{bitly.api_url}/shorten"
    responses.add(
        responses.POST,
        url,
        headers=headers,
        body=body,
        status=400,
        match_querystring=True,
    )

    with pytest.raises(ShorteningErrorException):
        bitly.short(expanded)


@responses.activate
def test_bitly_expand_method():
    # mock responses
    body = json.dumps({"long_url": expanded})
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{bitly.api_url}/expand"
    responses.add(
        responses.POST, url, headers=headers, body=body, match_querystring=True
    )
    assert bitly.expand(shorten) == expanded


@responses.activate
def test_bitly_expand_method_bad_response():
    # mock responses
    body = json.dumps({"long_url": expanded})
    headers = {"Authorization": f"Bearer {token}"}

    url = f"{bitly.api_url}/expand"
    responses.add(
        responses.POST,
        url,
        headers=headers,
        body=body,
        status=400,
        match_querystring=True,
    )

    with pytest.raises(ExpandingErrorException):
        bitly.expand(shorten)


@responses.activate
def test_bitly_total_clicks():
    body = json.dumps({"link_clicks": [{"clicks": 20}]})
    headers = {"Authorization": f"Bearer {token}"}
    url = "".join(urlparse(shorten)[1:3])
    url = f"{bitly.api_url}/bitlinks/{url}/clicks"
    responses.add(
        responses.GET, url, headers=headers, body=body, match_querystring=True
    )

    assert bitly.total_clicks(shorten) == 20


@responses.activate
def test_bitly_total_clicks_bad_response():
    body = json.dumps({"link_clicks": [{"clicks": 20}]})
    headers = {"Authorization": f"Bearer {token}"}
    url = "".join(urlparse(shorten)[1:3])
    url = f"{bitly.api_url}/bitlinks/{url}/clicks"
    responses.add(
        responses.GET,
        url,
        headers=headers,
        body=body,
        status=400,
        match_querystring=True,
    )
    with pytest.raises(BadAPIResponseException):
        bitly.total_clicks(shorten)
