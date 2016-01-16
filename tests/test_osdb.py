#!/usr/bin/env python
# encoding: utf-8
from pyshorteners import Shortener, Shorteners
from pyshorteners.exceptions import ShorteningErrorException

import responses
import pytest

s = Shortener(Shorteners.OSDB)
shorten = 'http://osdb.link/test123'
expanded = 'http://www.test.com'

# flake8: noqa
body = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\r\n<html>\r\n  <head>\r\n    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\r\n    <title>URL shortener</title>\r\n    <link type="text/css" rel="stylesheet" href="/stylesheets/style.css" />\r\n    </head>\r\n    <body>\r\n\t  <div class="linearBg2">\r\n\t\t <div id="container">\r\n\t\t\t <h1>osdb<span class="dot">.</span>link</h1>\r\n\t\t\t <div class="form">\r\n\t\t\t   <!-- <?= $html ?> -->\r\n\t\t\t   <label id=surl>Your shortened URL is:<br/>{}</label>\r\n\t\t\t   <br /><br />\r\n\t\t\t   <span id="back"><a href="./">&#10006;</a></span>\r\n\t\t\t </div>\r\n\t\t\t <div class="info"><label>Click close button to shorten next URL</label></div>\t\r\n\t\t </div>\r\n\t  </div>\r\n    </body>\r\n</html>
    """.format(shorten)
mock_url = '{}'.format(s.api_url)


@responses.activate
def test_tinyurl_short_method():
    # mock responses
    responses.add(responses.POST, mock_url, body=body)

    shorten_result = s.short(expanded)

    assert shorten_result == shorten
    assert s.shorten == shorten_result
    assert s.expanded == expanded


@responses.activate
def test_tinyurl_short_bad_response():
    # mock responses
    responses.add(responses.POST, mock_url, body=body, status=400)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)
