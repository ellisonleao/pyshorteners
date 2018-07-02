#!/usr/bin/env python
# encoding: utf-8
try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from pyshorteners import Shortener, Shorteners
from pyshorteners.shorteners import Soogd
from pyshorteners.exceptions import (ShorteningErrorException)

import responses
import pytest

s = Shortener(Shorteners.SOOGD, suffix='g4de')
short_url = 'http://soo.gd/g4de'
expanded = 'http://www.test.com'


@responses.activate
def test_soogd_short_method():
    # mock response
    body = '<input onclick="this.select();" name="link1" size="40" ' \
           'value="http://soo.gd/g4de" dir="ltr">'
    responses.add(responses.POST, s.api_url, body=body)

    shorten = s.short(expanded)
    assert shorten == short_url


@responses.activate
def test_soogd_short_method_bad_response():
    responses.add(responses.POST, s.api_url, body='bad_response', status=400)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


def test_generate_suffix_staticmethod():
    suffix = Soogd._generate_random_suffix()
    assert len(suffix) == 4
