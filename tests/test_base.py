#!/usr/bin/env python
# encoding: utf-8

from pyshorteners import Shortener
from pyshorteners.shorteners.base import BaseShortener, Simple
from pyshorteners.exceptions import ExpandingErrorException

import responses
import pytest

s = Shortener()
short = 'http://www.t.com'
expanded = 'http://googl.com'


def test_base_short_method():
    shorten_result = s.short(expanded)
    assert shorten_result == expanded


def test_base_total_clicks():
    s = Shortener()
    s.shorten = 'http://test.com'
    with pytest.raises(NotImplementedError):
        s.total_clicks()


@responses.activate
def test_expand_method_bad_response():
    responses.add(responses.GET, short, body='', status=400)
    s = Shortener()

    with pytest.raises(ExpandingErrorException):
        s.expand(short)


def test_timeout():
    import requests
    b = Simple(timeout=2)
    assert b.kwargs['timeout'] == 2

    # flake8: noqa
    # https://github.com/kennethreitz/requests/blob/master/test_requests.py#L46-L48
    with pytest.raises(requests.exceptions.Timeout):
        b.expand('http://10.255.255.1')

def test_base_verify_arg():
    s = Shortener(verify=False)
    assert s.kwargs['verify'] == False
