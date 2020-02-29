from pyshorteners.base import BaseShortener
from pyshorteners.exceptions import BadURLException, ExpandingErrorException

import pytest


def test_base_init_params_become_properties():
    # pylint: disable=E1101
    shortener = BaseShortener(a=1, b=2)
    assert shortener.a == 1
    assert shortener.b == 2
    # check default params
    assert shortener.timeout == 2
    assert shortener.verify is True


def test_base_clean_url_method():
    # good
    url = "www.google.com"
    assert BaseShortener.clean_url(url) == f"http://{url}"

    # bad
    with pytest.raises(BadURLException):
        BaseShortener.clean_url("http://")


def test_base_expand_method():
    shortener = BaseShortener()
    url = "http://httpbin.org/get"
    assert shortener.expand(url) == url


def test_base_expand_method_bad_response():
    shortener = BaseShortener()
    with pytest.raises(ExpandingErrorException):
        shortener.expand("http://httpbin.org/status/400")


def test_base_get_request_bad_url():
    shortener = BaseShortener()
    url = "....."
    with pytest.raises(BadURLException):
        shortener._get(url)


def test_base_post_request():
    shortener = BaseShortener()
    url = "http://httpbin.org/status/200"
    assert shortener._post(url).status_code == 200


def test_base_post_request_bad_url():
    shortener = BaseShortener()
    url = "....."
    with pytest.raises(BadURLException):
        shortener._post(url)


def test_base_short_method_raises_notimplemented():
    shortener = BaseShortener()
    with pytest.raises(NotImplementedError):
        shortener.short("http://someurl")
