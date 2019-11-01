#!/usr/bin/env python
# encoding: utf-8

import responses
import pytest

from pyshorteners import Shortener
from pyshorteners.exceptions import (
    ShorteningErrorException,
    ExpandingErrorException
)


token = "TEST_TOKEN"
domain = "short.cm"
path = "test"
expanded = "http://www.test.com"
shorten = f"http://{domain}/{path}"
s = Shortener(api_key=token, domain=domain)
shortcm = s.shortcm


@responses.activate
def test_shortcm_short_method():
    # mock responses
    json = {"path": path, "originalURL": expanded, "shortURL": shorten}

    responses.add(responses.POST, shortcm.api_url, json=json)

    shorten_result = shortcm.short(expanded)

    assert shorten_result == shorten


@responses.activate
def test_shortcm_short_method_bad_response():
    # mock responses
    json = {"error": "Test error", "success": False}
    responses.add(responses.POST, shortcm.api_url, json=json, status=400)

    with pytest.raises(ShorteningErrorException):
        shortcm.short(expanded)


@responses.activate
def test_shortcm_expand_method():
    # mock responses
    json = {"path": path, "shortURL": shorten, "originalURL": expanded}
    url = f"{shortcm.api_url}expand"
    responses.add(responses.GET, url, json=json)
    assert shortcm.expand(shorten) == expanded


@responses.activate
def test_shortcm_expand_method_bad_response():
    # mock responses
    json = {"error": "Test error"}
    url = f"{shortcm.api_url}expand"
    responses.add(responses.GET, url, json=json, status=400)

    with pytest.raises(ExpandingErrorException):
        shortcm.expand(shorten)
