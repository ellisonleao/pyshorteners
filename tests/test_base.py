#!/usr/bin/env python
# encoding: utf-8

from pyshorteners.shorteners import Shortener

s = Shortener()
short = 'http://www.t.com'
expanded = 'http://googl.com'


def test_base_short_method():
    shorten_result = s.short(expanded)
    assert shorten_result == expanded
