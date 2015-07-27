#!/usr/bin/env python
# encoding: utf-8

from pyshorteners import Shortener
from pyshorteners.exceptions import ExpandingErrorException

import responses
import pytest

s = Shortener()
short = 'http://www.t.com'
expanded = 'http://googl.com'


def test_base_short_method():
    shorten_result = s.short(expanded)
    assert shorten_result == expanded


@responses.activate
def test_expand_method_bad_response():
    responses.add(responses.GET, short, body='', status=400)
    s = Shortener()

    with pytest.raises(ExpandingErrorException):
        s.expand(short)
